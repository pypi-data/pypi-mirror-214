import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.dataset as ds
import pandas as pd
import os
import fsspec
from fsspec.parquet import open_parquet_file
import numpy as np
import datetime
import pyarrow.compute as pc

from parquet_datastore_utils.cleaner import delete_all_except_newest


def get_merged_schema(dataset, schema=None):
    if schema is None:
        schema = dataset.schema
    for p in dataset.get_fragments():
        schema = pa.unify_schemas([schema, p.scanner().dataset_schema])
    return schema


def _create_schema(types_dict):
    schema = []
    for key, val in types_dict.items():
        if val in (datetime.datetime, np.datetime64, pd.core.dtypes.dtypes.DatetimeTZDtype):
            schema.append((key,  pa.timestamp('ns')))
        else:
            schema.append((key, pa.from_numpy_dtype(val)))

    return pa.schema(schema)


def read(uri: str, columns: list = None, types_dict: dict = None, merge_schemas: bool = None, **kwargs):
    """
    Reads a parquet dataset and returns a pandas dataframe. Optionally performing a schema merge to allow for schema
    evolution. Note that schema merges can be expensive, specifying an explicit schema with the `schema` kwarg or
    `types_dict` is likely to improve performance in the case that the column(s) you want have been added after initial
    dataset creation.

    Parameters
    ----------
    uri: str
        The URI of the dataset, either a local filepath, or any fsspec compliant path specification.
    columns: list
        The columns to read from the dataset. Omit to read the whole dataset
    types_dict: dict
        A dictionary in the form {<field_name>: <type>} where type is a python or numpy type.
    merge_schemas: bool
        Can take values True, False or None (default). If True, an attempt will always be made to merge the schemas of
        all fragments in the dataset. If None, the returned DataFrame will not be guaranteed to contain all columns that
        only appear in some fragments, if a column specified by the `columns` argument isn't found, a schema merge will
        be performed implicitly. If False, a schema merge will never be performed, and a pyarrow.lib.ArrowInvalid error
        will be raised if a column is not found. Schema merges can be expensive, depending on the number of fragments and
        the seek performance of the filesystem and media (i.e. they will be slower on spinning hard drives than SSDs).
    kwargs:
        Will be passed to the PyArrow parquet engine. The `schema` argument will be overwritten if types_dict is passed.
         If merge_schemas is True, a Schema specified with `schema` will be merged with those read from fragments.

    Returns
    -------
    pandas.Dataframe
    """

    if types_dict is not None:
        kwargs['schema'] = pa.unify_schemas([ds.dataset(uri).schema, _create_schema(types_dict)])

    if merge_schemas is True:
        dataset = ds.dataset(uri)
        kwargs['schema'] = get_merged_schema(dataset, kwargs.get('schema'))

    try:
        return pd.read_parquet(uri, columns=columns, **kwargs)
    except pa.lib.ArrowInvalid:
        if merge_schemas is None or True:
            dataset = ds.dataset(uri)
            kwargs['schema'] = get_merged_schema(dataset, kwargs.get('schema'))
        else:
            raise

    return pd.read_parquet(uri, columns=columns, **kwargs)


def write(data: pd.DataFrame, uri: str, partition_cols: list = None, overwrite_period: bool = False):
    """
    Writes a pandas DataFrame to parquet. For timeseries data, existing data within the time range of the new data can
    optionally be overwritten.

    Parameters
    ----------
    data: pandas.DataFrame
        The data to be written
    uri:
        The destination to write the data to. Either a local file path or an fsspec style path like `file:///C:/data` or
        `s3://bucket/key`
    partition_cols: list
        Columns to partition on
    overwrite_period: bool
        Only applicable to timeseries data where there is existing data in the destination. If True, any chunks that
        overlap with the new data will be loaded, existing data in the interval covered by the new data will be removed,
        and the new data will be merged with any remaining data from those chunks. The result will then be written to
        `uri`. Only once the write is successful, all but the newest file in each partition directory will be removed,
        avoiding duplicate data in any given time period.
    """

    # Simple case, new dataset or relying on default behaviour
    if not fsspec.get_mapper(uri).fs.exists(uri) or not overwrite_period:
        data.to_parquet(uri, partition_cols=partition_cols)
        return

    current_ds = pq.ParquetDataset(uri)

    update_tables = []
    for fragment in current_ds.fragments:
        parts = ds._get_partition_keys(fragment.partition_expression)
        if all([(data[key]==value).any() for key, value in parts.items()]):
            update_tables.append(fragment.to_table())

    new_table = pa.table(data)

    if len(update_tables) > 0:
    # Data overlaps data in exsiting fragments
        ind = data.index.name
        filtered_table = pa.concat_tables(update_tables, promote=True).filter(
            (pc.field(ind) < data.index.min()), (pc.field(ind) > data.index.max()))

        filtered_table = filtered_table.set_column(filtered_table.column_names.index(ind), ind, filtered_table[ind].cast(new_table[ind].type))

        out = pa.concat_tables([filtered_table, new_table], promote=True)  # Promote=True to allow for mismatched schemas
    else:
        out = new_table

    pq.write_to_dataset(out, uri, partition_cols=partition_cols, use_legacy_dataset=False)

    dirs = set([os.path.dirname(fragment.path) for fragment in current_ds.fragments])

    for dir in dirs:
        delete_all_except_newest(dir)


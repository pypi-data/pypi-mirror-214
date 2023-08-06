import fsspec


def delete_all_except_newest(dir: str):
    f = fsspec.get_mapper(dir).fs
    if len(f.expand_path('{}/*'.format(dir))) <= 1:
        return

    newest_mtime = 0
    for leaf in f.expand_path('{}/*'.format(dir)):
        info = f.info(leaf)
        if info['mtime'] > newest_mtime:
            newest_mtime = info['mtime']
            newest_leaf = leaf

    deleted = []
    for leaf in f.expand_path('{}/*'.format(dir)):
        if leaf != newest_leaf:
            f.rm(leaf)
            deleted.append(leaf)

    return deleted

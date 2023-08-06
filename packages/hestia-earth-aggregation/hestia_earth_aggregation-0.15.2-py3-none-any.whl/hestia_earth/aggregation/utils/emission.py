from hestia_earth.utils.lookup import get_table_value, download_lookup, column_name


def is_in_system_boundary(term_id: str):
    lookup = download_lookup('emission.csv')
    value = get_table_value(lookup, 'termid', term_id, column_name('inHestiaDefaultSystemBoundary'))
    # handle numpy boolean
    return not (not value)

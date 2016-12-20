"""
Mango

A wrapper module that provides simple basic MongoDb operations.

date: 2016-12-19
license: MIT
"""


__version__ = "0.1.1"
IS_W2P_IMPORT = True
mgdb = None


import pymongo


try:
    from gluon.contrib.appconfig import AppConfig
except:
    IS_W2P_IMPORT = False


def init_db(uri=None):
    global mgdb
    """
    Initialize MongoDb Connection using PyMongo.
    """
    if IS_W2P_IMPORT:
        appconfig = AppConfig()
        uri = appconfig.get('db.uri')
    if uri:
        db_name = uri.split("/")[-1]
        client = pymongo.MongoClient(uri)
        mgdb = client[db_name]
        return mgdb
    else:
        return None


if IS_W2P_IMPORT:
    init_db()


def get_table(table_name):
    """
    Get the table object by table_name.
    """
    return mgdb[table_name]


def select(table_name,
        _filter=None,
        is_many=False,
        **kwargs):
    """
    MongoDb find wrapper function.
    """
    _table = mgdb[table_name]
    if not is_many:
        return _table.find_one(_filter, **kwargs)
    else:
        return _table.find(_filter, **kwargs)


def delete(table_name,
        _filter=None,
        is_many=False,
        **kwargs):
    """
    MongoDb delete wrapper function.
    """
    _table = mgdb[table_name]
    if not is_many:
        return _table.delete_one(
            _filter,
            **kwargs)
    else:
        return _table.delete_many(
            _filter,
            **kwargs)


def update(table_name,
        _filter=None,
        _value=None,
        is_many=False,
        _operation="$set",
        **kwargs):
    """
    MongoDb update wrapper function.
    """
    _table = mgdb[table_name]
    if _filter and _value:
        _update = {
            _operation: _value
        }
        if not is_many:
            return _table.update_one(
                _filter,
                _update,
                **kwargs)
        else:
            return _table.update_many(
                _filter,
                _update,
                **kwargs)
    else:
        return None


def insert(table_name,
        _value=None,
        is_many=False,
        **kwargs):
    """
    MongoDb insert wrapper function.
    """
    _table = mgdb[table_name]
    if not is_many:
        return _table.insert(_value, **kwargs)
    else:
        return _table.insert_many(_value, **kwargs)

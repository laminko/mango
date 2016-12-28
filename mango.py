"""
Mango

A wrapper module that provides simple basic MongoDb operations.

date: 2016-12-19
license: MIT
"""


__version__ = "0.1.4"
IS_W2P_IMPORT = True
mgdb = None


import pymongo
import collections
from bson.objectid import ObjectId


try:
    from gluon.contrib.appconfig import AppConfig
except:
    IS_W2P_IMPORT = False


def to_w2p_id(records, to_web2py_id=False):
    """
    Covert MongoDB ObjectID to Web2py compatible ID.
    """
    def converter(row):
        for k, v in row.items():
            if type(v) == ObjectId:
                stringified = str(v)
                if k == "_id":
                    row.pop(k)
                    k = "id"
                row[k] = long(stringified, 16)
        return row
    if not isinstance(records, collections.Iterable):
        raise ValueError("Records must be Iterable.")
    if to_web2py_id:
        if isinstance(records, dict):
            return converter(records)
        return map(converter, records)
    return records


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


def count(table_name,
        _filter=None,
        **kwargs):
    """
    MongoDb count wrapper function.
    """
    _table = get_table(table_name)
    return _table.count(_filter, **kwargs)


def select(table_name,
        _filter=None,
        is_many=False,
        to_web2py_id=False,
        **kwargs):
    """
    MongoDb find wrapper function.
    """
    _table = get_table(table_name)
    if not is_many:
        return to_w2p_id(_table.find_one(_filter, **kwargs), to_web2py_id)
    else:
        return to_w2p_id(_table.find(_filter, **kwargs), to_web2py_id)


def delete(table_name,
        _filter=None,
        is_many=False,
        **kwargs):
    """
    MongoDb delete wrapper function.
    """
    _table = get_table(table_name)
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
    _table = get_table(table_name)
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
    _table = get_table(table_name)
    if not is_many:
        return _table.insert(_value, **kwargs)
    else:
        return _table.insert_many(_value, **kwargs)

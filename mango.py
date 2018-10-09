"""Mango

A wrapper module that provides simple basic MongoDb operations.

date: 2016-12-19
license: MIT

changes:

2017-09-08
    - Changed pattern: modular to object oriented which make available to
      connect multiple databases
    - Version bumped: 0.2

2016-12-19
    - web2py DAL support
    - development started
    - stable release
    - Version bumped: 0.1.7
"""


import collections
import random
import pymongo
from bson.objectid import ObjectId


__version__ = "0.2"
IS_W2P_IMPORT = True


try:
    from gluon.contrib.appconfig import AppConfig
except:
    IS_W2P_IMPORT = False


def object_id(arg=None):
    """Convert input to a valid Mongodb ObjectId instance.
    object_id("<random>") -> ObjectId (not unique) instance

    REF: web2py's dal

    Args:
        arg ([type], optional): Defaults to None. [description]

    Raises:
        ValueError: Invalid ObjectID argument string
        ValueError: Invalid ObjectID. Requires an integer or base 16 value
        TypeError: object_id argument must be of type ObjectID or an objectid
                   representable integer.

    Returns:
        ObjectId: Mongodb ObjectId
    """
    if not arg:
        arg = 0
    if isinstance(arg, basestring):
        # we assume an integer as default input
        rawhex = len(arg.replace("0x", "").replace("L", "")) == 24
        if arg.isdigit() and (not rawhex):
            arg = int(arg)
        elif arg == "<random>":
            arg = int("0x%s" % "".join([
                random.choice("0123456789abcdef")
                for x in range(24)]), 0)
        elif arg.isalnum():
            if not arg.startswith("0x"):
                arg = "0x%s" % arg
            try:
                arg = int(arg, 0)
            except ValueError as e:
                raise ValueError(
                    "invalid objectid argument string: %s" % e)
        else:
            raise ValueError("Invalid objectid argument string. " +
                             "Requires an integer or base 16 value")
    elif isinstance(arg, ObjectId):
        return arg
    elif not isinstance(arg, (int, long)):
        raise TypeError(
            "object_id argument must be of type ObjectId or an objectid " +
            "representable integer (type %s)" % type(arg))
    hexvalue = hex(arg)[2:].rstrip('L').zfill(24)
    return ObjectId(hexvalue)


def w2p_id(arg=None, to_str=True):
    """Convert ObjectId to web2py ID.

    REF: web2py's dal

    Args:
        arg ([type], optional): Defaults to None. [description]
        to_str (bool, optional): Defaults to True. [description]

    Raises:
        TypeError: [description]

    Returns:
        [type]: [description]
    """
    if not isinstance(arg, ObjectId):
        raise TypeError('w2p_id argument must be ObjectId')
    converted = long(str(arg), 16)
    if to_str:
        return str(converted)
    return converted


def to_w2p_id(records, to_web2py_id=False, to_str=True):
    """Convert ObjectId of records to web2py compitible ID.

    Args:
        records ([type]): [description]
        to_web2py_id (bool, optional): Defaults to False. [description]
        to_str (bool, optional): Defaults to True. [description]

    Returns:
        [type]: [description]
    """
    mongodb_id_field = '_id'
    def converter(row):
        if mongodb_id_field in row:
            value = row.get(mongodb_id_field)
            row['id'] = w2p_id(value, to_str=to_str)
            row.pop(mongodb_id_field)
        return row
    if to_web2py_id:
        if isinstance(records, dict):
            return converter(records)
        elif isinstance(records, collections.Iterable):
            return map(converter, records)
    return records


def encoding_handler(value, encoding='utf8'):
    """To handle string encoding.

    Returns:
        [type]: [description]
    """
    if isinstance(value, str):
        return value.decode(encoding)
    elif isinstance(value, unicode):
        return value.encode(encoding)
    else:
        return value


class Mango(object):
    """PyMongo Wrapper: Mango
    """

    _uri = None
    _client = None
    _db = None
    _db_name = None
    _connected = False
    _last_exception = None

    def __init__(self, uri=None):
        """Initialize MongoDb Connection using PyMongo.

        Args:
            uri ([type], optional): Defaults to None. [description]
        """
        self._uri = uri
        if IS_W2P_IMPORT and not uri:
            appconfig = AppConfig()
            self._uri = appconfig.get('db.uri')
        if self._uri:
            self._client = pymongo.MongoClient(self._uri)
            self._db = self._client.get_default_database()
            self._db_name = self._db.name

    def connect(self):
        try:
            self._client.server_info()
            self._connected = True
        except pymongo.errors.ServerSelectionTimeoutError as sste:
            self._last_exception = sste
            self._connected = False
        return self._connected

    def disconnect(self):
        if self._connected:
            self._client.close()

    def get_table(self, table_name):
        """Get the table object by table_name.

        Args:
            table_name ([type]): [description]

        Returns:
            [type]: [description]
        """
        return self._db.get_collection(table_name)

    def count(self,
              table_name,
              cond=None,
              **kwargs):
        """MongoDb count wrapper function.

        Args:
            table_name ([type]): [description]
            cond ([type], optional): Defaults to None. [description]

        Returns:
            [type]: [description]
        """
        _table = self.get_table(table_name)
        return _table.count(cond, **kwargs)

    def select(self,
               table_name,
               cond=None,
               is_many=False,
               to_web2py_id=False,
               **kwargs):
        """MongoDb find wrapper function.

        Args:
            table_name ([type]): [description]
            cond ([type], optional): Defaults to None. [description]
            is_many (bool, optional): Defaults to False. [description]
            to_web2py_id (bool, optional): Defaults to False. [description]

        Returns:
            [type]: [description]
        """
        _table = self.get_table(table_name)
        if not is_many:
            return to_w2p_id(
                _table.find_one(cond, **kwargs),
                to_web2py_id)
        else:
            return to_w2p_id(
                _table.find(cond, **kwargs),
                to_web2py_id)

    def delete(self,
               table_name,
               cond=None,
               is_many=False,
               **kwargs):
        """MongoDb delete wrapper function.

        Args:
            table_name ([type]): [description]
            cond ([type], optional): Defaults to None. [description]
            is_many (bool, optional): Defaults to False. [description]

        Returns:
            [type]: [description]
        """
        _table = self.get_table(table_name)
        if not is_many:
            return _table.delete_one(
                cond,
                **kwargs)
        else:
            return _table.delete_many(
                cond,
                **kwargs)

    def update(self,
               table_name,
               cond=None,
               value=None,
               is_many=False,
               operator="$set",
               **kwargs):
        """MongoDb update wrapper function.

        Args:
            table_name ([type]): [description]
            cond ([type], optional): Defaults to None. [description]
            value ([type], optional): Defaults to None.
                If operator is provided in `value`, `operator` argument will
                be ignored.
            is_many (bool, optional): Defaults to False. [description]
            operator (str, optional): Defaults to "$set". [description]

        Returns:
            [type]: [description]
        """
        _table = self.get_table(table_name)
        _update = value
        _has_operators = any([k.startswith("$") for k in value.keys()])
        if cond and value:
            if not _has_operators:
                _update = {
                    operator: value
                }
            if not is_many:
                return _table.update_one(
                    cond,
                    _update,
                    **kwargs)
            else:
                return _table.update_many(
                    cond,
                    _update,
                    **kwargs)
        else:
            return None

    def insert(self,
               table_name,
               value=None,
               is_many=False,
               **kwargs):
        """MongoDb insert wrapper function.

        Args:
            table_name ([type]): [description]
            value ([type], optional): Defaults to None. [description]
            is_many (bool, optional): Defaults to False. [description]

        Returns:
            [type]: [description]
        """
        _table = self.get_table(table_name)
        if not is_many:
            return _table.insert_one(value, **kwargs)
        else:
            return _table.insert_many(value, **kwargs)

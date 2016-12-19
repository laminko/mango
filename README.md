## Mango

A Simple wrapper module for Mongo sit on top of PyMongo.


### Installation

To install `mango` lib: `pip install mango`.


### Usage


### Availabe functions

-[`init_db`](#init_db)
-[`get_table`](#get_table)
-[`select`](#select)
-[`insert`](#insert)
-[`update`](#update)
-[`delete`](#delete)


#### init_db

To initialize MongoDb Connection.

Parameter:

`uri`: MongoDb URI


#### get_table

Get the MongoDb Table object.

Parameter:

- `table_name`: Table name


#### select

Query record(s) from table.

Parameters:

- `table_name`: Table name
- `_filter`: MongoDb filter object
- `is_many`: Use `find` or `find_one`. Default is `False` which means `find_one` will be used.
- `**kwargs`: `KwArgs` which will be pass to pymongo function


#### insert

Insert record(s) to table.

Parameters:
- `table_name`: Table name
- `_value`: Value that will be inserted
- `is_many`: `insert_one` or `insert_many`. Default is `False` (means `insert_one`).
- `**kwargs`: `KwArgs` will be pass to pymongo function


#### update

Update record(s) to table.

Parameters:

- `table_name`: Table name
- `_filter`: MongoDb filter object
- `_value`: Value that will be updated
- `is_many`: `update_one` or `update_many`. Default is `False` (means `update_one`).
- `_operation`: MongoDb update operation. Default is `$set`.
- `**kwargs`: `KwArgs` will be pass to pymongo function.


#### delete

Delete record(s) to table.

Parameters:

- `table_name`: Table name
- `_filter`: MongoDb filter object
- `is_many`: `delete_one` or `delete_many`. Default is `False` (means `delete_one`).
- `**kwargs`: `KwArgs` will be pass to pymongo function.

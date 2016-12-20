Mango
=====

A Simple wrapper module for Mongo sit on top of PyMongo.

Installation
------------

To install ``mango`` lib: ``pip install python-mango``.

Usage
-----

To import module: ``import mango``.

Sample:

.. raw:: html


.. code:: python

    import mango

    uri = "mongodb://user:pwd@localhost:port/database"
    mango.init_db(uri)

    # To get database object
    db = mango.mgdb

    # To get table object
    mytable = mango.get_table('mytable')

    # Select rows
    rows = mango.select('mytable')
    rows = mango.select('mytable', { "qty": { "$gt": 4 } })

.. raw:: html


Availabe functions
------------------

-  `init_db`_
-  `get_table`_
-  `select`_
-  `insert`_
-  `update`_
-  `delete`_

init\_db
--------

To initialize MongoDb Connection.

Parameter:

``uri``: MongoDb URI

get\_table
----------

Get the MongoDb Table object.

Parameter:

-  ``table_name``: Table name

select
------

Query record(s) from table.

Parameters:

-  ``table_name``: Table name
-  ``_filter``: MongoDb filter object
-  ``is_many``: Use ``find`` or ``find_one``. Default is ``False`` which
   means ``find_one`` will be used.
-  ``**kwargs``: ``KwArgs`` which will be pass to pymongo function

insert
------

Insert record(s) to table.

Parameters: - ``table_name``: Table name - ``_value``: Value that will
be inserted - ``is_many``: ``insert_one`` or ``insert_many``. Default is
``False`` (means ``insert_one``). - ``**kwargs``: ``KwArgs`` will be
pass to pymongo function

update
------

Update record(s) to table.

Parameters:

-  ``table_name``: Table name
-  ``_filter``: MongoDb filter object
-  ``_value``: Value that will be updated
-  ``is_many``: ``update_one`` or ``update_many``. Default is ``False``
   (means ``update_one``).
-  ``_operation``: MongoDb update operation. Default is ``$set``.
-  ``**kwargs``: ``KwArgs`` will be pass to pymongo function.

delete
------

Delete record(s) to table.

Parameters:

-  ``table_name``: Table name
-  ``_filter``: MongoDb filter object
-  ``is_many``: ``delete_one`` or ``delete_many``. Default is ``False``
   (means ``delete_one``).
-  ``**kwargs``: ``KwArgs`` will be pass to pymongo function.

.. _``init_db``: #init_db
.. _``get_table``: #get_table
.. _``select``: #select
.. _``insert``: #insert
.. _``update``: #update
.. _``delete``: #delete

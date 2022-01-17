Welcome to lbry-rocksdb's documentation!
==========================================

Overview
--------
Python bindings to the C++ interface of http://rocksdb.org/ using cython::

    import rocksdb
    db = rocksdb.DB("test.db", rocksdb.Options(create_if_missing=True))
    db.put(b"a", b"b")
    print db.get(b"a")


Tested with python 3.7, 3.8, and 3.9 with RocksDB version 6.25.3

.. toctree::
    :maxdepth: 2

    Instructions how to install <installation>
    Tutorial <tutorial/index>
    API <api/index>
    Changelog <changelog>


Contributing
------------

Source can be found on `github <https://github.com/lbryio/lbry-rocksdb>`_.
Feel free to fork and send pull-requests or create issues on the
`github issue tracker <https://github.com/lbryio/lbry-rocksdb/issues>`_

RoadMap/TODO
------------

No plans so far. Please submit wishes to the github issues.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

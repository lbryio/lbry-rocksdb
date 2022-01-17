Installing
==========
.. highlight:: bash

From pypi
*********
.. code-block:: bash

    pip install lbry-rocksdb

From source (ubuntu)
********************
.. code-block:: bash

    sudo apt install build-essential binutils
    git clone https://github.com/lbryio/lbry-rocksdb.git
    cd lbry-rocksdb
    git submodule update --init --recursive
    git pull --recurse-submodules
    make clean && make
    pip install -e .
    python -m unittest discover . -v

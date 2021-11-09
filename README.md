## lbry-rocksdb

### Note
The `python-rocksdb` and `pyrocksdb` packages haven't been updated in a long time - this repo is a fork of python-rocksdb with many of the PRs to it merged, and with [bunch of updates and improvements](https://github.com/iFA88/python-rocksdb) from @iFA88 and @mosquito.


### Install from pip
    pip install lbry-rocksdb


### Install for development / from source
    sudo apt install build-essential binutils
    git clone https://github.com/lbryio/lbry-rocksdb.git
    cd lbry-rocksdb
    git submodule update --init --recursive
    git pull --recurse-submodules
    make clean && make
    pip install -e .
    python -m unittest discover . -v


### Quick Usage Guide
    >>> import rocksdb
    >>> db = rocksdb.DB("test.db", rocksdb.Options(create_if_missing=True))
    >>> db.put(b'a', b'data')
    >>> print db.get(b'a')
    b'data'

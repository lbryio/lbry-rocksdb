Database interactions
*********************

Database object
===============

.. py:class:: rocksdb.DB

    .. py:method:: __init__(db_name, Options opts, read_only=False)

        :param unicode db_name:  Name of the database to open
        :param opts: Options for this specific database
        :type opts: :py:class:`rocksdb.Options`
        :param bool read_only: If ``True`` the database is opened read-only.
                               All DB calls which modify data will raise an
                               Exception.


    .. py:method:: put(key, value, sync=False, disable_wal=False)

        Set the database entry for "key" to "value".

        :param bytes key: Name for this entry
        :param bytes value: Data for this entry
        :param bool sync: 
            If ``True``, the write will be flushed from the operating system
            buffer cache (by calling WritableFile::Sync()) before the write
            is considered complete.  If this flag is true, writes will be
            slower.

            If this flag is ``False``, and the machine crashes, some recent
            writes may be lost.  Note that if it is just the process that
            crashes (i.e., the machine does not reboot), no writes will be
            lost even if ``sync == False``.

            In other words, a DB write with ``sync == False`` has similar
            crash semantics as the "write()" system call.  A DB write
            with ``sync == True`` has similar crash semantics to a "write()"
            system call followed by "fdatasync()".

        :param bool disable_wal:
            If ``True``, writes will not first go to the write ahead log,
            and the write may got lost after a crash.

    .. py:method:: delete(key, sync=False, disable_wal=False)

        Remove the database entry for "key".

        :param bytes key: Name to delete
        :param sync: See :py:meth:`rocksdb.DB.put`
        :param disable_wal: See :py:meth:`rocksdb.DB.put`
        :raises rocksdb.errors.NotFound: If the key did not exists

    .. py:method:: merge(key, value, sync=False, disable_wal=False)

        Merge the database entry for "key" with "value".
        The semantics of this operation is determined by the user provided
        merge_operator when opening DB.

        See :py:meth:`rocksdb.DB.put` for the parameters

        :raises:
            :py:exc:`rocksdb.errors.NotSupported` if this is called and
            no :py:attr:`rocksdb.Options.merge_operator` was set at creation


    .. py:method:: write(batch, sync=False, disable_wal=False)

        Apply the specified updates to the database.

        :param rocksdb.WriteBatch batch: Batch to apply
        :param sync: See :py:meth:`rocksdb.DB.put`
        :param disable_wal: See :py:meth:`rocksdb.DB.put`

    .. py:method:: get(key, verify_checksums=False, fill_cache=True, snapshot=None, read_tier="all")

        :param bytes key: Name to get

        :param bool verify_checksums: 
            If ``True``, all data read from underlying storage will be
            verified against corresponding checksums.

        :param bool fill_cache:
                Should the "data block", "index block" or "filter block"
                read for this iteration be cached in memory?
                Callers may wish to set this field to ``False`` for bulk scans.
        
        :param snapshot:
            If not ``None``, read as of the supplied snapshot
            (which must belong to the DB that is being read and which must
            not have been released). Is it ``None`` a implicit snapshot of the
            state at the beginning of this read operation is used
        :type snapshot: :py:class:`rocksdb.Snapshot`

        :param string read_tier:
            Specify if this read request should process data that ALREADY
            resides on a particular cache. If the required data is not
            found at the specified cache,
            then :py:exc:`rocksdb.errors.Incomplete` is raised.

            | Use ``all`` if a fetch from disk is allowed.
            | Use ``cache`` if only data from cache is allowed.
 
        :returns: ``None`` if not found, else the value for this key

    .. py:method:: multi_get(keys, verify_checksums=False, fill_cache=True, snapshot=None, read_tier="all")

        :param keys: Keys to fetch
        :type keys: list of bytes

        For the other params see :py:meth:`rocksdb.DB.get`

        :returns:
            A ``dict`` where the value is either ``bytes`` or ``None`` if not found

        :raises: If the fetch for a single key fails
        
        .. note::
            keys will not be "de-duplicated".
            Duplicate keys will return duplicate values in order.

    .. py:method:: key_may_exist(key, fetch=False, verify_checksums=False, fill_cache=True, snapshot=None, read_tier="all")

        If the key definitely does not exist in the database, then this method
        returns ``False``, else ``True``. If the caller wants to obtain value
        when the key is found in memory, fetch should be set to ``True``.
        This check is potentially lighter-weight than invoking DB::get().
        One way to make this lighter weight is to avoid doing any IOs.

        :param bytes key: Key to check
        :param bool fetch: Obtain also the value if found

        For the other params see :py:meth:`rocksdb.DB.get`

        :returns: 
            * ``(True, None)`` if key is found but value not in memory
            * ``(True, None)`` if key is found and ``fetch=False``
            * ``(True, <data>)`` if key is found and value in memory and ``fetch=True``
            * ``(False, None)`` if key is not found

    .. py:method:: iterkeys(verify_checksums=False, fill_cache=True, snapshot=None, read_tier="all")

        Iterate over the keys

        For other params see :py:meth:`rocksdb.DB.get`

        :returns:
            A iterator object which is not valid yet.
            Call first one of the seek methods of the iterator to position it

        :rtype: :py:class:`rocksdb.BaseIterator`

    .. py:method:: itervalues(verify_checksums=False, fill_cache=True, snapshot=None, read_tier="all")

        Iterate over the values

        For other params see :py:meth:`rocksdb.DB.get`

        :returns:
            A iterator object which is not valid yet.
            Call first one of the seek methods of the iterator to position it

        :rtype: :py:class:`rocksdb.BaseIterator`

    .. py:method:: iteritems(verify_checksums=False, fill_cache=True, snapshot=None, read_tier="all")

        Iterate over the items

        For other params see :py:meth:`rocksdb.DB.get`

        :returns:
            A iterator object which is not valid yet.
            Call first one of the seek methods of the iterator to position it

        :rtype: :py:class:`rocksdb.BaseIterator`

    .. py:method:: iterator(start=None, column_family=None, iterate_lower_bound=None, iterate_upper_bound=None, reverse=False, include_key=True, include_value=True, fill_cache=True, prefix_same_as_start=False, auto_prefix_mode=False)

        :param start: prefix to seek to
        :type start: bytes

        :param column_family: column family handle
        :type column_family: :py:class:`rocksdb.ColumnFamilyHandle`

        :param iterate_lower_bound:
            defines the smallest key at which the backward iterator can return an entry.
            Once the bound is passed, Valid() will be false. `iterate_lower_bound` is
            inclusive ie the bound value is a valid entry.
            If prefix_extractor is not null, the Seek target and `iterate_lower_bound`
            need to have the same prefix. This is because ordering is not guaranteed
            outside of prefix domain.
        :type iterate_lower_bound: bytes

        :param iterate_upper_bound:
            defines the extent up to which the forward iterator
            can returns entries. Once the bound is reached, Valid() will be false.
            "iterate_upper_bound" is exclusive ie the bound value is
            not a valid entry. If prefix_extractor is not null:
                1. If auto_prefix_mode = true, iterate_upper_bound will be used
                   to infer whether prefix iterating (e.g. applying prefix bloom filter)
                   can be used within RocksDB. This is done by comparing
                   iterate_upper_bound with the seek key.
                2. If auto_prefix_mode = false, iterate_upper_bound only takes
                   effect if it shares the same prefix as the seek key. If
                   iterate_upper_bound is outside the prefix of the seek key, then keys
                   returned outside the prefix range will be undefined, just as if
                   iterate_upper_bound = null.
                   If iterate_upper_bound is not null, SeekToLast() will position the iterator
                   at the first key smaller than iterate_upper_bound.
        :type iterate_upper_bound: bytes

        :param reverse:          run the iteration in reverse - using `reversed` is also supported
        :type reverse: bool

        :param include_key:      the iterator should include the key in each iteration
        :type include_key: bool

        :param include_value:    the iterator should include the value in each iteration
        :type include_value: bool

        :param fill_cache:       Should the "data block"/"index block" read for this iteration be placed in
                                      block cache? Callers may wish to set this field to false for bulk scans.
                                      This would help not to the change eviction order of existing items in the
                                      block cache. Default: true
        :type fill_cache: bool

        :param bool prefix_same_as_start:
                                      Enforce that the iterator only iterates over the same prefix as the seek.
                                      This option is effective only for prefix seeks, i.e. prefix_extractor is
                                      non-null for the column family and total_order_seek is false.  Unlike
                                      iterate_upper_bound, prefix_same_as_start only works within a prefix
                                      but in both directions. Default: false
        :type prefix_same_as_start: bool

        :param bool auto_prefix_mode: When true, by default use total_order_seek = true, and RocksDB can
                                          selectively enable prefix seek mode if won't generate a different result
                                          from total_order_seek, based on seek key, and iterator upper bound.
                                          Not supported in ROCKSDB_LITE mode, in the way that even with value true
                                          prefix mode is not used. Default: false
        :type auto_prefix_mode: bool

        :returns:
            A iterator object which is valid and ready to begin using. It will be either a key, item or value
            iterator depending on the arguments provided.
        :rtype: :py:class:`rocksdb.BaseIterator`

    .. py:method:: snapshot()
    
        Return a handle to the current DB state.
        Iterators created with this handle will all observe a stable snapshot
        of the current DB state.
        
        :rtype: :py:class:`rocksdb.Snapshot`


    .. py:method:: get_property(prop)

        DB implementations can export properties about their state
        via this method. If "property" is a valid property understood by this
        DB implementation, a byte string with its value is returned.
        Otherwise ``None``
        
        Valid property names include:
        
        * ``b"rocksdb.num-files-at-level<N>"``: return the number of files at level <N>,
            where <N> is an ASCII representation of a level number (e.g. "0").

        * ``b"rocksdb.stats"``: returns a multi-line byte string that describes statistics
            about the internal operation of the DB.

        * ``b"rocksdb.sstables"``: returns a multi-line byte string that describes all
            of the sstables that make up the db contents.

        * ``b"rocksdb.num-immutable-mem-table"``: Number of immutable mem tables.

        * ``b"rocksdb.mem-table-flush-pending"``: Returns ``1`` if mem table flush is pending, otherwise ``0``.

        * ``b"rocksdb.compaction-pending"``:  Returns ``1`` if a compaction is pending, otherweise ``0``.

        * ``b"rocksdb.background-errors"``: Returns accumulated background errors encountered.

        * ``b"rocksdb.cur-size-active-mem-table"``: Returns current size of the active memtable.

    .. py:method:: get_live_files_metadata()

        Returns a list of all table files.

        It returns a list of dict's were each dict has the following keys.

        ``name``
            Name of the file

        ``level``
            Level at which this file resides

        ``size``
            File size in bytes

        ``smallestkey``
            Smallest user defined key in the file

        ``largestkey``
            Largest user defined key in the file

        ``smallest_seqno``
            smallest seqno in file

        ``largest_seqno``
            largest seqno in file

    .. py:method:: compact_range(begin=None, end=None, ** options)

        Compact the underlying storage for the key range [begin,end].
        The actual compaction interval might be superset of [begin, end].
        In particular, deleted and overwritten versions are discarded,
        and the data is rearranged to reduce the cost of operations
        needed to access the data.

        This operation should typically only be invoked by users who understand
        the underlying implementation.

        ``begin == None`` is treated as a key before all keys in the database.
        ``end == None`` is treated as a key after all keys in the database.
        Therefore the following call will compact the entire database: ``db.compact_range()``.

        Note that after the entire database is compacted, all data are pushed
        down to the last level containing any data. If the total data size
        after compaction is reduced, that level might not be appropriate for
        hosting all the files. In this case, client could set change_level
        to ``True``, to move the files back to the minimum level capable of holding
        the data set or a given level (specified by non-negative target_level).

        :param bytes begin: Key where to start compaction.
                            If ``None`` start at the beginning of the database.
        :param bytes end: Key where to end compaction.
                          If ``None`` end at the last key of the database.
        :param bool change_level:  If ``True``, compacted files will be moved to
                                   the minimum level capable of holding the data
                                   or given level (specified by non-negative target_level).
                                   If ``False`` you may end with a bigger level
                                   than configured. Default is ``False``.
        :param int target_level: If change_level is true and target_level have non-negative
                                 value, compacted files will be moved to target_level.
                                 Default is ``-1``.
        :param string bottommost_level_compaction:
            For level based compaction, we can configure if we want to
            skip/force bottommost level compaction. By default level based
            compaction will only compact the bottommost level if there is a
            compaction filter. It can be set to the following values.

            ``skip``
                Skip bottommost level compaction

            ``if_compaction_filter``
                Only compact bottommost level if there is a compaction filter.
                This is the default.

            ``force``
                Always compact bottommost level
        
    .. py:attribute:: options

        Returns the associated :py:class:`rocksdb.Options` instance.

        .. note::

            Changes to this object have no effect anymore.
            Consider this as read-only

Iterator
========

.. py:class:: rocksdb.BaseIterator

    Base class for all iterators in this module. After creation a iterator is
    invalid. Call one of the seek methods first before starting iteration

    .. py:method:: seek_to_first()

            Position at the first key in the source

    .. py:method:: seek_to_last()
    
            Position at the last key in the source

    .. py:method:: seek(key)
    
        :param bytes key: Position at the first key in the source that at or past
 
    Methods to support the python iterator protocol

    .. py:method:: __iter__()
    .. py:method:: __next__()
    .. py:method:: __reversed__()

Snapshot
========

.. py:class:: rocksdb.Snapshot

    Opaque handler for a single Snapshot.
    Snapshot is released if nobody holds a reference on it.
    Retrieved via :py:meth:`rocksdb.DB.snapshot`

WriteBatch
==========

.. py:class:: rocksdb.WriteBatch

     WriteBatch holds a collection of updates to apply atomically to a DB.

     The updates are applied in the order in which they are added
     to the WriteBatch.  For example, the value of "key" will be "v3"
     after the following batch is written::
     
        batch = rocksdb.WriteBatch()
        batch.put(b"key", b"v1")
        batch.delete(b"key")
        batch.put(b"key", b"v2")
        batch.put(b"key", b"v3")

    .. py:method:: __init__(data=None)

        Creates a WriteBatch.

        :param bytes data:
            A serialized version of a previous WriteBatch. As retrieved
            from a previous .data() call. If ``None`` a empty WriteBatch is
            generated

    .. py:method:: put(key, value)
    
        Store the mapping "key->value" in the database.

        :param bytes key: Name of the entry to store
        :param bytes value: Data of this entry

    .. py:method:: merge(key, value)
    
        Merge "value" with the existing value of "key" in the database.

        :param bytes key: Name of the entry to merge
        :param bytes value: Data to merge

    .. py:method:: delete(key)
 
        If the database contains a mapping for "key", erase it.  Else do nothing.

        :param bytes key: Key to erase

    .. py:method:: clear()

        Clear all updates buffered in this batch.

        .. note::
            Don't call this method if there is an outstanding iterator.
            Calling :py:meth:`rocksdb.WriteBatch.clear()` with outstanding
            iterator, leads to SEGFAULT.

    .. py:method:: data()

        Retrieve the serialized version of this batch.

        :rtype: ``bytes``

    .. py:method:: count()
    
        Returns the number of updates in the batch

        :rtype: int

    .. py:method:: __iter__()

        Returns an iterator over the current contents of the write batch.

        If you add new items to the batch, they are not visible for this
        iterator. Create a new one if you need to see them.

        .. note::
            Calling :py:meth:`rocksdb.WriteBatch.clear()` on the write batch
            invalidates the iterator.  Using a iterator where its corresponding
            write batch has been cleared, leads to SEGFAULT.

        :rtype: :py:class:`rocksdb.WriteBatchIterator`

WriteBatchIterator
==================

.. py:class:: rocksdb.WriteBatchIterator

    .. py:method:: __iter__()

        Returns self.

    .. py:method:: __next__()

        Returns the next item inside the corresponding write batch.
        The return value is a tuple of always size three.

        First item (Name of the operation):

            * ``"Put"``
            * ``"Merge"``
            * ``"Delete"``

        Second item (key):
            Key for this operation.

        Third item (value):
            The value for this operation. Empty for ``"Delete"``.

Repair DB
=========

.. py:function:: repair_db(db_name, opts)

    :param unicode db_name: Name of the database to open
    :param opts: Options for this specific database
    :type opts: :py:class:`rocksdb.Options`

    If a DB cannot be opened, you may attempt to call this method to
    resurrect as much of the contents of the database as possible.
    Some data may be lost, so be careful when calling this function
    on a database that contains important information.


Errors
======

.. py:exception:: rocksdb.errors.NotFound
.. py:exception:: rocksdb.errors.Corruption
.. py:exception:: rocksdb.errors.NotSupported
.. py:exception:: rocksdb.errors.InvalidArgument
.. py:exception:: rocksdb.errors.RocksIOError
.. py:exception:: rocksdb.errors.MergeInProgress
.. py:exception:: rocksdb.errors.Incomplete



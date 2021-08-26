all: src/rocksdb/librocksdb.a

JOBS=8

src/rocksdb/librocksdb.a:
	make \
		-e EXTRA_CXXFLAGS="-fPIC" \
		-e EXTRA_CFLAGS="-fPIC" \
		-C src/rocksdb \
		-j $(JOBS) \
			libsnappy.a \
			liblz4.a \
			libbz2.a \
			libzstd.a \
			libz.a

	(cd src/rocksdb && mkdir -p build && cd build && cmake \
		-DWITH_SNAPPY=1 \
		-DWITH_LZ4=1 \
		-DWITH_ZLIB=1 \
		-DWITH_ZSTD=1 \
		-DWITH_GFLAGS=0 \
		-DROCKSDB_BUILD_SHARED=0 \
		-DWITH_TOOLS=0 \
		-DWITH_BENCHMARK_TOOLS=0 \
		-DWITH_CORE_TOOLS=0 \
		-DWITH_JEMALLOC=0 \
		-DCMAKE_BUILD_TYPE=Release \
		-DSnappy_INCLUDE_DIRS=../snappy-1.1.8/ \
		-DSnappy_LIBRARIES=../snappy-1.1.8/build \
		-Dlz4_INCLUDE_DIRS=../lz4-1.9.3/lib \
		-Dlz4_LIBRARIES=../lz4-1.9.3/lib \
		-Dzstd_INCLUDE_DIRS=../zstd-1.4.9/lib \
		-Dzstd_LIBRARIES=../zstd-1.4.9/lib \
		-DZLIB_INCLUDE_DIR=../zlib-1.2.11 \
		-DZLIB_LIBRARY=./zlib-1.2.11 \
		-DCMAKE_CXX_FLAGS="-fPIC -I../snappy-1.1.8/build -I../zstd-1.4.9/lib/dictBuilder" \
		.. && make -j $(JOBS))

	cp src/rocksdb/build/librocksdb.a src/rocksdb/librocksdb.a

clean:
	rm -rf src/rocksdb/build
	make -C src/rocksdb clean

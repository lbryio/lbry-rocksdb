import sys
import platform
import os
from setuptools import setup
from setuptools import find_packages
from setuptools import Extension

try:
    from Cython.Build import cythonize
except ImportError:
    def cythonize(extensions):
        return extensions

    SOURCES = ['rocksdb/_rocksdb.cpp']
else:
    SOURCES = ['rocksdb/_rocksdb.pyx']

with open(os.path.join(os.path.dirname(__file__), 'rocksdb', '__init__.py'), 'r') as init_file:
    version_line = [l for l in init_file.readlines() if l.startswith('__version__ = "')][0]
    version = version_line.split('__version__ = "')[1][:-2]

EXTRA_COMPILE_ARGS = [
    '-std=c++11',
    '-fPIC',
    '-Os',
    '-Wall',
    '-Wextra',
    '-Wconversion',
    '-fno-strict-aliasing',
    '-fno-rtti',
]

LIBRARIES = ['rocksdb', 'snappy', 'bz2', 'z', 'lz4']
EXTRA_OBJECTS = []
EXTRA_LINK_ARGS = []
INCLUDE_DIRS = []


if platform.system() == 'Darwin':
    EXTRA_COMPILE_ARGS += ['-mmacosx-version-min=10.7', '-stdlib=libc++']
    EXTRA_LINK_ARGS += ['-Wl,-s']

if platform.system() == 'Linux':
    EXTRA_LINK_ARGS += ['-Wl,--strip-all']


STATIC_LIBRARIES = [os.path.join("src", "rocksdb", item) for item in [
    "librocksdb.a",
    "libbz2.a",
    "liblz4.a",
    "libsnappy.a",
    "libz.a",
    "libzstd.a",
]]

if all(map(os.path.exists, STATIC_LIBRARIES)):
    LIBRARIES = []
    EXTRA_OBJECTS = STATIC_LIBRARIES
    INCLUDE_DIRS = [
        os.path.join("src", "rocksdb", "bzip2-1.0.8"),
        os.path.join("src", "rocksdb", "zstd-1.4.9", "lib"),
        os.path.join("src", "rocksdb", "zlib-1.2.11"),
        os.path.join("src", "rocksdb", "snappy-1.1.8"),
        os.path.join("src", "rocksdb", "snappy-1.1.8", "build"),
        os.path.join("src", "rocksdb", "lz4-1.9.3", "lib"),
        os.path.join("src", "rocksdb", "include"),
    ]
    print("✔️ all static libraries exist in expected locations")
else:
    print('✘ missing static library files')
    sys.exit(1)

setup(
    name="lbry-rocksdb",
    version=version,
    keywords=['rocksdb', 'lbry-rocksdb', 'python-rocksdb', 'leveldb', 'embedded', 'database'],
    description="Python bindings for RocksDB",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    author='Jack Robison',
    author_email="jackrobison@lbry.com",
    url="https://github.com/lbryio/lbry-rocksdb",
    license='BSD License',
    python_requires=">=3.7.0",
    package_dir={'rocksdb': 'rocksdb'},
    packages=find_packages(exclude=('tests',)),
    ext_modules=cythonize([Extension(
        'rocksdb._rocksdb',
        SOURCES,
        extra_compile_args=EXTRA_COMPILE_ARGS,
        language='c++',
        libraries=LIBRARIES,
        include_dirs=INCLUDE_DIRS,
        extra_objects=EXTRA_OBJECTS,
        extra_link_args=EXTRA_LINK_ARGS,
    )]),
    extras_require={
        "doc": ['sphinx_rtd_theme', 'sphinx']
    },
    include_package_data=False,
    zip_safe=False,
)

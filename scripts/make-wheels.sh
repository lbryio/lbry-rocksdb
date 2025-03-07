set -ex

cd lbry-rocksdb
mkdir -p dist

function build_wheel() {
  /opt/python/$1/bin/pip install cython wheel
	/opt/python/$1/bin/pip wheel . -f . -w dist
}

build_wheel cp37-cp37m
build_wheel cp38-cp38
build_wheel cp39-cp39
build_wheel cp310-cp310
build_wheel pp37-pypy37_pp73

cd dist
for f in ./*linux_*;
do if [ -f $f ]; then auditwheel repair $f -w . ; rm $f; fi;
done
cd -

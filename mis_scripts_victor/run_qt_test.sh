#!/bin/sh

set -ex

export LD_LIBRARY_PATH="${PREFIX}/${HOST}/sysroot/usr/lib64:${PREFIX}/${HOST}/sysroot/usr/lib:${LD_LIBRARY_PATH}"

test -f ${PREFIX}/bin/qt6.conf

cmake -Stest -Bbuild -GNinja
cmake --build build --target all
ctest --test-dir build --output-on-failure

set -exou

pushd pyqt_webengine

SIP_ARGS="
  --qmake-setting QMAKE_CC=${CC_FOR_BUILD}
  --qmake-setting QMAKE_CXX=${CXX_FOR_BUILD}
  --qmake-setting QMAKE_LINK=${CXX_FOR_BUILD}
"

if [[ $(uname) == "Linux" ]]; then
    USED_BUILD_PREFIX=${BUILD_PREFIX:-${PREFIX}}
    echo USED_BUILD_PREFIX=${BUILD_PREFIX}

    export PKG_CONFIG_EXECUTABLE=$(basename $(which pkg-config))

    # Still need these for the initial tests sip does to see which bindings will be made.
    ln -s ${GXX} g++ || true
    ln -s ${GCC} gcc || true
    ln -s ${USED_BUILD_PREFIX}/bin/${HOST}-gcc-ar gcc-ar || true
    export LD=${GXX}
    export CC=${GCC}
    export CXX=${GXX}
    chmod +x g++ gcc gcc-ar
    export PATH=${PWD}:${PATH}

    SIP_ARGS="${SIP_ARGS}
      --qmake-setting QMAKE_AR_CMD=${USED_BUILD_PREFIX}/bin/${HOST}-gcc-ar
      --qmake-setting QMAKE_INCDIR_OPENGL=${PREFIX}/include
      --qmake-setting QMAKE_LIBDIR_OPENGL=${PREFIX}/lib
    "
elif [[ $(uname) == "Darwin" ]]; then
    SIP_ARGS="${SIP_ARGS}
      --qmake-setting QMAKE_MACOSX_DEPLOYMENT_TARGET=${c_stdlib_version}
      --qmake-setting QMAKE_MAC_SDK=macosx${OSX_SDK_VER}
    "
fi

sip-build ${SIP_ARGS} \
  --jobs=${CPU_COUNT} \
  --qmake=${PREFIX}/bin/qmake6 \
  --verbose \
  --no-make

pushd build
make -j$CPU_COUNT
make install

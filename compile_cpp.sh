#!/usr/bin/env bash
set -e

PYTHON="$(which python)"

echo "Using python: $PYTHON"

$PYTHON -m pybind11 --includes

EXT_SUFFIX="$($PYTHON - <<'EOF'
import sysconfig
print(sysconfig.get_config_var("EXT_SUFFIX"))
EOF
)"

echo "Using EXT_SUFFIX: $EXT_SUFFIX"

clang++ -O3 -std=c++20 -shared -fPIC \
  $($PYTHON -m pybind11 --includes) \
  -I nbody_engine/include \
  nbody_engine/src/*.cpp \
  -undefined dynamic_lookup \
  -o "nbody_core${EXT_SUFFIX}"

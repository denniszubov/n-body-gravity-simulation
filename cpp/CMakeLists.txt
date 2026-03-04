pybind11_add_module(_nbody_core
    src/gravity.cpp
    src/leapfrog.cpp
    src/simulator.cpp
    src/bindings.cpp
)

target_include_directories(_nbody_core PUBLIC include)
target_compile_options(_nbody_core PRIVATE -O3)

install(TARGETS _nbody_core DESTINATION nbody)

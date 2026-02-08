#include <pybind11/pybind11.h>

namespace py = pybind11;

int add(int i, int j) {
    return i + j;
}

PYBIND11_MODULE(nbody_engine, m) {
    m.doc() = "example addition module";
    m.def("add", &add, "Simple addition");
}

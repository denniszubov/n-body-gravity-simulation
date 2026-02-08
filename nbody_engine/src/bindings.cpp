#include <pybind11/pybind11.h>

namespace py = pybind11;

int add(int i, int j) {
    return i + j;
}

PYBIND11_MODULE(nbody_core, m) {
    m.doc() = "N-body gravity simulation core";
    m.def("add", &add, "Simple addition");
}

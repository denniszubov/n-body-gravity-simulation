#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

#include <nbody_engine/api.hpp>

namespace py = pybind11;

static void step(
    py::array_t<double, py::array::c_style | py::array::forcecast> position,
    py::array_t<double, py::array::c_style | py::array::forcecast> velocity,
    py::array_t<double, py::array::c_style | py::array::forcecast> mass,
    double dt,
    double G,
    double eps,
    int substeps = 1
) {
    auto p = position.request();
    auto v = velocity.request();
    auto m = mass.request();

    if (p.ndim != 2 || p.shape[1] != 2) {
        throw std::invalid_argument("position must have shape (N, 2)");
    }
    if (v.ndim != 2 || v.shape[1] != 2) {
        throw std::invalid_argument("velocity must have shape (N, 2)");
    }

    const std::size_t n = static_cast<std::size_t>(p.shape[0]);

    if (static_cast<std::size_t>(v.shape[0]) != n) {
        throw std::invalid_argument("velocity must have same N as position");
    }
    if (m.ndim != 1 || static_cast<std::size_t>(m.shape[0]) != n) {
        throw std::invalid_argument("mass must have shape (N,)");
    }

    auto* pos_ptr = static_cast<double*>(p.ptr);
    auto* vel_ptr = static_cast<double*>(v.ptr);
    auto* mass_ptr = static_cast<const double*>(m.ptr);

    nbody_engine::step_from_arrays(pos_ptr, vel_ptr, mass_ptr, n, dt, G, eps, substeps);
}

PYBIND11_MODULE(nbody_core, mod) {
    mod.doc() = "N-body gravity simulation engine";
    mod.def(
        "step",
        &step,
        py::arg("position"),
        py::arg("velocity"),
        py::arg("mass"),
        py::arg("dt"),
        py::arg("G"),
        py::arg("eps"),
        py::arg("substeps") = 1
    );
}

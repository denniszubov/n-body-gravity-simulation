#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

#include <nbody/simulator.hpp>
#include <nbody/vec2.hpp>

#include <cstddef>
#include <memory>
#include <stdexcept>
#include <vector>

namespace py = pybind11;
using namespace nbody;

// Verify Vec2 layout is compatible with (N, 2) float64 NumPy arrays.
static_assert(sizeof(Vec2) == 2 * sizeof(double),
              "Vec2 must be tightly packed (no padding)");
static_assert(offsetof(Vec2, y) == sizeof(double),
              "Vec2.y must immediately follow Vec2.x");

// Create a (N, 2) NumPy view into a vector<Vec2> without copying.
// The base parameter prevents the Simulator from being garbage-collected
// while the view is alive.
static py::array_t<double> vec2_view(const std::vector<Vec2>& vec,
                                     py::object base) {
    auto n = static_cast<py::ssize_t>(vec.size());
    return py::array_t<double>(
        {n, py::ssize_t(2)},
        {py::ssize_t(sizeof(Vec2)), py::ssize_t(sizeof(double))},
        reinterpret_cast<const double*>(vec.data()),
        std::move(base));
}

// Create a (N,) NumPy view into a vector<double> without copying.
static py::array_t<double> real_view(const std::vector<real>& vec,
                                     py::object base) {
    auto n = static_cast<py::ssize_t>(vec.size());
    return py::array_t<double>(
        {n},
        {py::ssize_t(sizeof(double))},
        vec.data(),
        std::move(base));
}

PYBIND11_MODULE(_nbody_core, mod) {
    mod.doc() = "N-body gravity simulation engine (C++ core)";

    py::class_<Config>(mod, "Config")
        .def(py::init<>())
        .def(py::init<real, real>(),
             py::arg("G") = 1.0, py::arg("eps") = 0.01)
        .def_readwrite("G", &Config::G)
        .def_readwrite("eps", &Config::eps);

    py::class_<Simulator>(mod, "Simulator")
        .def(py::init([](const Config& config,
                         py::array_t<double, py::array::c_style | py::array::forcecast> positions,
                         py::array_t<double, py::array::c_style | py::array::forcecast> velocities,
                         py::array_t<double, py::array::c_style | py::array::forcecast> masses) {
                 auto p = positions.request();
                 auto v = velocities.request();
                 auto m = masses.request();

                 if (p.ndim != 2 || p.shape[1] != 2)
                     throw std::invalid_argument("positions must have shape (N, 2)");
                 if (v.ndim != 2 || v.shape[1] != 2)
                     throw std::invalid_argument("velocities must have shape (N, 2)");
                 if (m.ndim != 1)
                     throw std::invalid_argument("masses must have shape (N,)");

                 auto n = static_cast<std::size_t>(p.shape[0]);
                 if (static_cast<std::size_t>(v.shape[0]) != n ||
                     static_cast<std::size_t>(m.shape[0]) != n)
                     throw std::invalid_argument("all arrays must have the same N");

                 auto* pp = static_cast<const double*>(p.ptr);
                 auto* vp = static_cast<const double*>(v.ptr);
                 auto* mp = static_cast<const double*>(m.ptr);

                 std::vector<Vec2> pos(n), vel(n);
                 std::vector<real> mass(n);
                 for (std::size_t i = 0; i < n; ++i) {
                     pos[i] = {pp[2 * i], pp[2 * i + 1]};
                     vel[i] = {vp[2 * i], vp[2 * i + 1]};
                     mass[i] = mp[i];
                 }

                 return std::make_unique<Simulator>(
                     config, std::move(pos), std::move(vel), std::move(mass));
             }),
             py::arg("config"),
             py::arg("positions"),
             py::arg("velocities"),
             py::arg("masses"))

        .def("step", &Simulator::step,
             py::arg("dt"), py::arg("n_steps") = 1)

        .def("positions", [](py::object self) {
            return vec2_view(self.cast<Simulator&>().positions(), self);
        })
        .def("velocities", [](py::object self) {
            return vec2_view(self.cast<Simulator&>().velocities(), self);
        })
        .def("masses", [](py::object self) {
            return real_view(self.cast<Simulator&>().masses(), self);
        })

        .def_property_readonly("n", &Simulator::size)
        .def("kinetic_energy", &Simulator::kinetic_energy)
        .def("potential_energy", &Simulator::potential_energy)
        .def("total_energy", &Simulator::total_energy)
        .def("last_step_time_sec", &Simulator::last_step_time_sec)
        .def("total_steps", &Simulator::total_steps);
}

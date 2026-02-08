#pragma once

#include <cstddef>

namespace nbody_engine {

// Python-friendly engine API: step the system in-place.
// position: (N, 2) float64 contiguous
// velocity: (N, 2) float64 contiguous
// mass:     (N,)   float64 contiguous
void step_from_arrays(
    double *position,
    double *velocity,
    const double* mass,
    std::size_t n,
    double dt,
    double G,
    double eps,
    int substeps
);

}
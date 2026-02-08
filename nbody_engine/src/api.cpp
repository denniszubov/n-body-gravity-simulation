#include <nbody_engine/state.hpp>
#include <nbody_engine/gravity.hpp>
#include <nbody_engine/leapfrog.hpp>
#include <nbody_engine/api.hpp>

#include <stdexcept>

namespace nbody_engine {

void step_from_arrays(
    double* position,
    double* velocity,
    const double* mass,
    std::size_t n,
    double dt,
    double G,
    double eps,
    int substeps
) {
    if (position == nullptr || velocity == nullptr || mass == nullptr) {
        throw std::invalid_argument("Null pointer passed to step_from_arrays");
    }
    if (n <= 0) return;
    if (dt <= 0.0) throw std::invalid_argument("dt must be > 0");
    if (eps <= 0.0) throw std::invalid_argument("eps must be > 0");
    if (substeps < 1) throw std::invalid_argument("substeps must be >= 1");

    State state(n);

    // Copy inputs into State
    for (std::size_t i = 0; i < n; ++i) {
        state.position[i].x = position[2 * i + 0];
        state.position[i].y = position[2 * i + 1];

        state.velocity[i].x = velocity[2 * i + 0];
        state.velocity[i].y = velocity[2 * i + 1];

        state.mass[i] = mass[i];
    }

    // Initialize acceleration once for leapfrog
    compute_acceleration(state, static_cast<real>(G), static_cast<real>(eps));

    for (int k = 0; k < substeps; ++k) {
        leapfrog_step(state, static_cast<real>(dt), static_cast<real>(G), static_cast<real>(eps));
    }

    // Copy back to arrays (in-place update for Python)
    for (std::size_t i = 0; i < n; ++i) {
        position[2 * i + 0] = state.position[i].x;
        position[2 * i + 1] = state.position[i].y;

        velocity[2 * i + 0] = state.velocity[i].x;
        velocity[2 * i + 1] = state.velocity[i].y;
    }
}

}

#include <nbody/state.hpp>
#include <nbody/gravity.hpp>
#include <nbody/leapfrog.hpp>

#include <cstddef>

namespace nbody {

void leapfrog_step(State& state, real dt, real G, real eps) {
    // Kick-drift-kick leapfrog integrator.
    // Assumes acceleration has been computed for current positions.

    for (std::size_t i = 0; i < state.size(); ++i) {
        // Half kick
        state.velocity[i].x += state.acceleration[i].x * 0.5 * dt;
        state.velocity[i].y += state.acceleration[i].y * 0.5 * dt;

        // Drift
        state.position[i].x += state.velocity[i].x * dt;
        state.position[i].y += state.velocity[i].y * dt;
    }

    // Recompute acceleration at new positions
    compute_acceleration(state, G, eps);

    for (std::size_t i = 0; i < state.size(); ++i) {
        // Final half kick
        state.velocity[i].x += state.acceleration[i].x * 0.5 * dt;
        state.velocity[i].y += state.acceleration[i].y * 0.5 * dt;
    }
}

}  // namespace nbody

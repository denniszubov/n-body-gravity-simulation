#include <nbody_engine/state.hpp>
#include <nbody_engine/gravity.hpp>
#include <nbody_engine/leapfrog.hpp>
#include <cstddef>


namespace nbody_engine {

void leapfrog_step(State& state, real dt, real G, real eps) {
    // using kick-drift-kick for stability.
    // assumes acceleration has been calculated for current state.

    for (std::size_t i = 0; i < state.size(); ++i) {
        // kick
        state.velocity[i].x = state.velocity[i].x + (state.acceleration[i].x * 0.5 * dt);
        state.velocity[i].y = state.velocity[i].y + (state.acceleration[i].y * 0.5 * dt);

        // drift
        state.position[i].x = state.position[i].x + (state.velocity[i].x * dt);
        state.position[i].y = state.position[i].y + (state.velocity[i].y * dt);
    }

    // recompute acceleration
    compute_acceleration(state, G, eps);

    for (std::size_t i = 0; i < state.size(); ++i) {
        // kick
        state.velocity[i].x = state.velocity[i].x + (state.acceleration[i].x * 0.5 * dt);
        state.velocity[i].y = state.velocity[i].y + (state.acceleration[i].y * 0.5 * dt);
    }
}

}

#include <nbody_engine/state.hpp>
#include <nbody_engine/gravity.hpp>
#include <cstddef>


namespace nbody_engine {

void leapfrog_step(State& state, nbody_engine::real dt, nbody_engine::real G, nbody_engine::real eps) {
    // using kick-drift-kick for stability.
    // assumes acceleration has been calculated for current state.

    for (std::size_t i; i < state.size(); ++i) {
        // kick
        state.velocity[i].x = state.velocity[i].x + (state.acceleration[i].x * 0.5 * dt);
        state.velocity[i].y = state.velocity[i].y + (state.acceleration[i].y * 0.5 * dt);

        // drift
        state.position[i].x = state.position[i].x + (state.velocity[i].x * dt);
        state.position[i].y = state.position[i].y + (state.velocity[i].y * dt);

        // recompute acceleration
        nbody_engine::compute_acceleration(state, G, eps);

        // kick
        state.velocity[i].x = state.velocity[i].x + (state.acceleration[i].x + 0.5 * dt);
        state.velocity[i].y = state.velocity[i].y + (state.acceleration[i].y + 0.5 * dt);
    }
}

}

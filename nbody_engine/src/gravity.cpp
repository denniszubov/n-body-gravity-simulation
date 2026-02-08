#include <nbody_engine/state.hpp>
#include <nbody_engine/gravity.hpp>
#include <cmath>
#include <cstddef>

namespace nbody_engine {

void compute_acceleration(nbody_engine::State& state, real G, real eps) {
    for (std::size_t i = 0; i < state.size(); ++i) {
        real F_x_total = 0.0;
        real F_y_total = 0.0;

        const Vec2& current_position = state.position[i];
        const real current_mass = state.mass[i];

        for (std::size_t j = 0; j < state.size(); ++j) {
            if (i == j) continue;
            const Vec2& other_position = state.position[j];
            const real other_mass = state.mass[j];

            // compute dx, dy, r
            real dx = other_position.x - current_position.x;
            real dy = other_position.y - current_position.y;
            real r = std::sqrt(dx*dx + dy*dy + eps*eps);

            // compute force
            real Fg = G * current_mass * other_mass / (r*r); 
            
            // compute unit vector to apply force to x and y component
            real uhat_x = dx / r;
            real uhat_y = dy / r;

            // compute x and y force components
            real Fg_x = uhat_x * Fg;
            real Fg_y = uhat_y * Fg;

            // add to force total
            F_x_total += Fg_x;
            F_y_total += Fg_y;
        }
        state.acceleration[i].x = F_x_total / current_mass;
        state.acceleration[i].y = F_y_total / current_mass;
    }
}

}

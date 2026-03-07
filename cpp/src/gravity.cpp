#include <nbody/state.hpp>
#include <nbody/gravity.hpp>

#include <cmath>
#include <cstddef>

namespace nbody {

void compute_acceleration(State& state, real G, real eps) {
    for (std::size_t i = 0; i < state.size(); ++i) {
        real F_x_total = 0.0;
        real F_y_total = 0.0;

        const Vec2& current_position = state.position[i];
        const real current_mass = state.mass[i];

        for (std::size_t j = 0; j < state.size(); ++j) {
            if (i == j) continue;
            const Vec2& other_position = state.position[j];
            const real other_mass = state.mass[j];

            real dx = other_position.x - current_position.x;
            real dy = other_position.y - current_position.y;
            real r = std::sqrt(dx * dx + dy * dy + eps * eps);

            real Fg = G * current_mass * other_mass / (r * r);

            real uhat_x = dx / r;
            real uhat_y = dy / r;

            real Fg_x = uhat_x * Fg;
            real Fg_y = uhat_y * Fg;

            F_x_total += Fg_x;
            F_y_total += Fg_y;
        }
        state.acceleration[i].x = F_x_total / current_mass;
        state.acceleration[i].y = F_y_total / current_mass;
    }
}

}  // namespace nbody

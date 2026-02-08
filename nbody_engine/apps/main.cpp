#include <nbody_engine/state.hpp>
#include <nbody_engine/gravity.hpp>
#include <nbody_engine/leapfrog.hpp>
#include <iostream>

using namespace nbody_engine;

int main() {
    State s(2);
    real G = 9.8;
    real eps = 0.01;
    real dt = 0.1;

    s.position[0] = Vec2{5.0, 0.0};
    s.position[1] = Vec2{-5.0, 0.0};

    s.velocity[0] = Vec2{0.0, -5.0};
    s.velocity[1] = Vec2{0.0, 5.0};

    s.mass[0] = 1.0;
    s.mass[1] = 1.0;

    compute_acceleration(s, G, eps);
    std::cout << "a0 = (" << s.acceleration[0].x << ", " << s.acceleration[0].y << ")\n";
    std::cout << "a1 = (" << s.acceleration[1].x << ", " << s.acceleration[1].y << ")\n\n";

    for (std::size_t i = 0; i < 50; ++i) {
        leapfrog_step(s, dt, G, eps);
        std::cout << "a0 = (" << s.acceleration[0].x << ", " << s.acceleration[0].y << ")\n";
        std::cout << "a1 = (" << s.acceleration[1].x << ", " << s.acceleration[1].y << ")\n";
        std::cout << "p0 = (" << s.position[0].x << ", " << s.position[0].y << ")\n";
        std::cout << "p0 = (" << s.position[1].x << ", " << s.position[1].y << ")\n\n";
    }
    
    return 0;
}

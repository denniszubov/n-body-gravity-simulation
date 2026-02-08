#include <nbody_engine/state.hpp>
#include <nbody_engine/gravity.hpp>
#include <iostream>

using namespace nbody_engine;

int main() {
    State s(2);

    s.position[0] = Vec2{0.0, 0.0};
    s.position[1] = Vec2{0.0, 1.0};

    s.mass[0] = 1.0;
    s.mass[1] = 1.0;

    compute_acceleration(s, 1.0, 0.01);

    std::cout << "a0 = (" << s.acceleration[0].x << ", " << s.acceleration[0].y << ")\n";
    std::cout << "a1 = (" << s.acceleration[1].x << ", " << s.acceleration[1].y << ")\n";

    return 0;
}
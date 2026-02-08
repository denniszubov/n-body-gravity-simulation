#pragma once

#include <cstddef>
#include <vector>

namespace nbody_engine {

using real = double;

struct Vec2 {
    real x = 0.0;
    real y = 0.0;
};

struct State {
    std::vector<Vec2> position;
    std::vector<Vec2> velocity;
    std::vector<Vec2> acceleration;
    std::vector<real> mass;

    State() = default;

    explicit State(std::size_t n)
        : position(n), velocity(n), acceleration(n), mass(n) {}
        
    std::size_t size() const {
        return position.size();
    }

    void resize(std::size_t n) {
        position.resize(n);
        velocity.resize(n);
        acceleration.resize(n);
        mass.resize(n);
    }
}



}
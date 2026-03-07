#pragma once

#include <nbody/state.hpp>

#include <cstddef>
#include <vector>

namespace nbody {

struct Config {
    real G   = 1.0;
    real eps = 0.01;
};

class Simulator {
public:
    Simulator(Config config,
              std::vector<Vec2> positions,
              std::vector<Vec2> velocities,
              std::vector<real> masses);

    void step(real dt, int n_steps = 1);

    const std::vector<Vec2>& positions() const;
    const std::vector<Vec2>& velocities() const;
    const std::vector<real>& masses() const;

    std::size_t size() const;

    real kinetic_energy() const;
    real potential_energy() const;
    real total_energy() const;

    double last_step_time_sec() const;
    long long total_steps() const;

private:
    Config config_;
    State state_;
    bool acceleration_initialized_ = false;

    double last_step_time_sec_ = 0.0;
    long long total_steps_ = 0;
};

}  // namespace nbody

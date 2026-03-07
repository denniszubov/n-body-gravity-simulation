#include <nbody/simulator.hpp>
#include <nbody/gravity.hpp>
#include <nbody/leapfrog.hpp>

#include <chrono>
#include <cmath>
#include <stdexcept>

namespace nbody {

Simulator::Simulator(Config config,
                     std::vector<Vec2> positions,
                     std::vector<Vec2> velocities,
                     std::vector<real> masses)
    : config_(config)
{
    std::size_t n = positions.size();
    if (velocities.size() != n || masses.size() != n) {
        throw std::invalid_argument(
            "positions, velocities, and masses must have the same length");
    }
    state_.position     = std::move(positions);
    state_.velocity     = std::move(velocities);
    state_.mass         = std::move(masses);
    state_.acceleration.resize(n);
}

void Simulator::step(real dt, int n_steps) {
    if (dt <= 0.0) throw std::invalid_argument("dt must be > 0");
    if (n_steps < 1) throw std::invalid_argument("n_steps must be >= 1");

    auto t0 = std::chrono::high_resolution_clock::now();

    if (!acceleration_initialized_) {
        compute_acceleration(state_, config_.G, config_.eps);
        acceleration_initialized_ = true;
    }

    for (int k = 0; k < n_steps; ++k) {
        leapfrog_step(state_, dt, config_.G, config_.eps);
    }
    total_steps_ += n_steps;

    auto t1 = std::chrono::high_resolution_clock::now();
    last_step_time_sec_ = std::chrono::duration<double>(t1 - t0).count();
}

const std::vector<Vec2>& Simulator::positions() const { return state_.position; }
const std::vector<Vec2>& Simulator::velocities() const { return state_.velocity; }
const std::vector<real>& Simulator::masses() const { return state_.mass; }
std::size_t Simulator::size() const { return state_.size(); }

real Simulator::kinetic_energy() const {
    real ke = 0.0;
    for (std::size_t i = 0; i < state_.size(); ++i) {
        real vx = state_.velocity[i].x;
        real vy = state_.velocity[i].y;
        ke += 0.5 * state_.mass[i] * (vx * vx + vy * vy);
    }
    return ke;
}

real Simulator::potential_energy() const {
    real pe = 0.0;
    for (std::size_t i = 0; i < state_.size(); ++i) {
        for (std::size_t j = i + 1; j < state_.size(); ++j) {
            real dx = state_.position[j].x - state_.position[i].x;
            real dy = state_.position[j].y - state_.position[i].y;
            real r  = std::sqrt(dx * dx + dy * dy + config_.eps * config_.eps);
            pe -= config_.G * state_.mass[i] * state_.mass[j] / r;
        }
    }
    return pe;
}

real Simulator::total_energy() const {
    return kinetic_energy() + potential_energy();
}

double Simulator::last_step_time_sec() const { return last_step_time_sec_; }
long long Simulator::total_steps() const { return total_steps_; }

}  // namespace nbody

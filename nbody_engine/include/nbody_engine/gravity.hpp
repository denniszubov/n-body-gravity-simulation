#pragma once

#include <nbody_engine/state.hpp>

namespace nbody_engine {

void compute_acceleration(nbody_engine::State& state, double G, double eps);

}

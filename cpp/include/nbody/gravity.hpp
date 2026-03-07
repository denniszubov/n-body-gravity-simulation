#pragma once

#include <nbody/state.hpp>

namespace nbody {

void compute_acceleration(State& state, real G, real eps);

}  // namespace nbody

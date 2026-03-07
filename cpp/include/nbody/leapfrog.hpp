#pragma once

#include <nbody/state.hpp>

namespace nbody {

void leapfrog_step(State& state, real dt, real G, real eps);

}  // namespace nbody

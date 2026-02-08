#pragma once

#include <nbody_engine/state.hpp>

namespace nbody_engine {

void compute_acceleration(nbody_engine::State& state, real G, real eps);

}

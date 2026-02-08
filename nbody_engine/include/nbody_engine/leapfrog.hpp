#pragma once

#include <nbody_engine/state.hpp>


namespace nbody_engine {

void leapfrog_step(State& state, real dt, real G, real eps);

}

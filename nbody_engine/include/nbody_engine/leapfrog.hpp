#pragma once

#include <nbody_engine/state.hpp>


namespace nbody_engine {

void leapfrog_step(State& state, nbody_engine::real dt, nbody_engine::real G, nbody_engine::real eps);

}

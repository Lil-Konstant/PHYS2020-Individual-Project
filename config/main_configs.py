TEST_CONFIG = {
    # Simulation settings
    "dt": 0.01,
    "steps": 5000,
    "box_size": 10.0,
    "N": 2000,

    # Properties of the fluid environment
    "fluid_velocity_mean": [0,0],
    "fluid_velocity_std": [1,1],
    "fluid_particle_radius": 0.05,
    "fluid_particle_mass": 1.0,

    # Properties of the brownian particle
    "brownian_initial_position": [0, 0],
    "brownian_initial_velocity": [0, 0],
    "brownian_particle_radius": 1.0,
    "brownian_particle_mass": 50.0
}
TEST_CONFIG = {
    # Simulation settings
    "dt": 0.01,
    "steps": 5000,
    "box_size": 10.0,
    "N": 200,

    # Properties of the fluid environment
    "fluid_is_ideal_gas": True,
    "fluid_velocity_mean": [0,0],
    "fluid_velocity_std": [10,10],
    "fluid_particle_radius": 0.05,
    "fluid_particle_mass": 1.0,

    # Properties of the brownian particle
    "brownian_is_ideal_gas": True,
    "brownian_initial_position": [0, 0],
    "brownian_initial_velocity": [0, 0],
    "brownian_particle_radius": 1.0,
    "brownian_particle_mass": 30.0,

    # Debug and display settings
    "draw_boundary": True,
    "draw_maxwells_demon": True,
    "draw_brownian_trail": True,
}
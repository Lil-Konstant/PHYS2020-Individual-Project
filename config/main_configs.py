TEST_CONFIG = {
    # Simulation Settings
    "dt": 0.01,
    "steps": 1000,
    "box_size": 10.0,
    "N": 200,
    "render_every": 10,
    "live_render": False,
    "plot_msd": True,
    "num_runs": 100,

    # Properties of the fluid environment
    "fluid_velocity_std": [1,1],
    "fluid_particle_radius": 0.05,
    "fluid_particle_mass": 1.0,

    # Properties of the brownian particle
    "brownian_is_ideal_gas": True,
    "brownian_initial_velocity": [0, 0],
    "brownian_particle_radius": 1.0,
    "brownian_particle_mass": 20.0,

    "use_LJ_potential": False,
    "use_LJ_for_brownian_to_fluid": False,
    "LJ_epsilon": 10,

    # Debug and display settings
    "draw_boundary": True,
    "draw_maxwells_demon": True,
    "draw_brownian_trail": True,
}
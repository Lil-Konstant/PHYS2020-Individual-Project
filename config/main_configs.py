TEST_CONFIG = {
    # Simulation Settings
    "dt": 0.01, # 0.01, 0.0005
    "steps": 1000, # 1000, 150000
    "box_size": 10.0,
    "N": 1000,
    "live_render": False,
    "num_runs": 1,
    "plot_msd": True,
    "save_plot": True,

    # Properties of the fluid environment
    "fluid_velocity_std": [1,1],
    "fluid_particle_radius": 0.05,
    "fluid_particle_mass": 1.0,

    # Properties of the brownian particle
    "brownian_is_ideal_gas": True,
    "brownian_initial_velocity": [0, 0],
    "brownian_particle_radius": 0.5,
    "brownian_particle_mass": 100.0,

    # LJ Potential parameters
    "use_LJ_potential": False,
    "use_LJ_for_brownian_to_fluid": False,
    "LJ_epsilon": 10,

    # Render Settings
    "render_every": 10,
    "draw_boundary": True,
    "draw_brownian_trail": True,
    # "draw_maxwells_demon": True,
}
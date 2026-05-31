TEST_CONFIG = {
    # Simulation Settings
    "dt": 0.0005, # 0.01, 0.0005
    "steps": 6000, # 1000, 150000
    "box_size": 10.0,
    "N": 1000,
    "live_render": False,
    "num_runs": 100,
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

DEBUG_CONFIG = {
    # Simulation Settings
    "dt": 0.01,
    "steps": 1000,
    "box_size": 10.0,
    "N": 1000,
    "live_render": False,
    "num_runs": 100,
    "plot_msd": True,
    "save_plot": True,

    # Properties of the fluid environment
    "fluid_velocity_std": [3,3],
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

    # Render Settings - for when Live render is true
    "render_every": 10,
    "draw_boundary": True,
    "draw_brownian_trail": True,
}

IDEAL_CONFIG = {
    # Simulation Settings
    "dt": 0.01,
    "steps": 1000,
    "box_size": 10.0,
    "N": 1000,
    "live_render": False,
    "num_runs": 100,
    "plot_msd": True,
    "save_plot": True,

    # Properties of the fluid environment
    "fluid_velocity_std": [3,3],
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
    "LJ_epsilon": 0,

    # Render Settings - for when Live render is true
    "render_every": 10,
    "draw_boundary": True,
    "draw_brownian_trail": True,
}

FUll_LJ_CONFIG_1 = {
    # Simulation Settings
    "dt": 0.0005,
    "steps": 20000, #20000
    "box_size": 10.0,
    "N": 1000,
    "live_render": False,
    "num_runs": 100,
    "plot_msd": True,
    "save_plot": True,

    # Properties of the fluid environment
    "fluid_velocity_std": [3,3],
    "fluid_particle_radius": 0.05,
    "fluid_particle_mass": 1.0,

    # Properties of the brownian particle
    "brownian_is_ideal_gas": True,
    "brownian_initial_velocity": [0, 0],
    "brownian_particle_radius": 0.5,
    "brownian_particle_mass": 100.0,

    # LJ Potential parameters
    "use_LJ_potential": True,
    "use_LJ_for_brownian_to_fluid": True,
    "LJ_epsilon": 9*4, # 1/4 kT/e

    # Render Settings - for when Live render is true
    "render_every": 10,
    "draw_boundary": True,
    "draw_brownian_trail": True,
}
FUll_LJ_CONFIG_2 = {
    # Simulation Settings
    "dt": 0.0005,
    "steps": 20000, #20000
    "box_size": 10.0,
    "N": 1000,
    "live_render": False,
    "num_runs": 100,
    "plot_msd": True,
    "save_plot": True,

    # Properties of the fluid environment
    "fluid_velocity_std": [3,3],
    "fluid_particle_radius": 0.05,
    "fluid_particle_mass": 1.0,

    # Properties of the brownian particle
    "brownian_is_ideal_gas": True,
    "brownian_initial_velocity": [0, 0],
    "brownian_particle_radius": 0.5,
    "brownian_particle_mass": 100.0,

    # LJ Potential parameters
    "use_LJ_potential": True,
    "use_LJ_for_brownian_to_fluid": True,
    "LJ_epsilon": 9*2, # 1/2 kT/e

    # Render Settings - for when Live render is true
    "render_every": 10,
    "draw_boundary": True,
    "draw_brownian_trail": True,
}
FUll_LJ_CONFIG_3 = {
    # Simulation Settings
    "dt": 0.0005,
    "steps": 20000, #20000
    "box_size": 10.0,
    "N": 1000,
    "live_render": False,
    "num_runs": 100,
    "plot_msd": True,
    "save_plot": True,

    # Properties of the fluid environment
    "fluid_velocity_std": [3,3],
    "fluid_particle_radius": 0.05,
    "fluid_particle_mass": 1.0,

    # Properties of the brownian particle
    "brownian_is_ideal_gas": True,
    "brownian_initial_velocity": [0, 0],
    "brownian_particle_radius": 0.5,
    "brownian_particle_mass": 100.0,

    # LJ Potential parameters
    "use_LJ_potential": True,
    "use_LJ_for_brownian_to_fluid": True,
    "LJ_epsilon": 9, # 1 kT/e

    # Render Settings - for when Live render is true
    "render_every": 10,
    "draw_boundary": True,
    "draw_brownian_trail": True,
}
FUll_LJ_CONFIG_4 = {
    # Simulation Settings
    "dt": 0.0005,
    "steps": 20000, #20000
    "box_size": 10.0,
    "N": 1000,
    "live_render": False,
    "num_runs": 100,
    "plot_msd": True,
    "save_plot": True,

    # Properties of the fluid environment
    "fluid_velocity_std": [3,3],
    "fluid_particle_radius": 0.05,
    "fluid_particle_mass": 1.0,

    # Properties of the brownian particle
    "brownian_is_ideal_gas": True,
    "brownian_initial_velocity": [0, 0],
    "brownian_particle_radius": 0.5,
    "brownian_particle_mass": 100.0,

    # LJ Potential parameters
    "use_LJ_potential": True,
    "use_LJ_for_brownian_to_fluid": True,
    "LJ_epsilon": 9/2, # 2 kT/e

    # Render Settings - for when Live render is true
    "render_every": 10,
    "draw_boundary": True,
    "draw_brownian_trail": True,
}
FUll_LJ_CONFIG_5 = {
    # Simulation Settings
    "dt": 0.0005,
    "steps": 20000, #20000
    "box_size": 10.0,
    "N": 1000,
    "live_render": False,
    "num_runs": 100,
    "plot_msd": True,
    "save_plot": True,

    # Properties of the fluid environment
    "fluid_velocity_std": [3,3],
    "fluid_particle_radius": 0.05,
    "fluid_particle_mass": 1.0,

    # Properties of the brownian particle
    "brownian_is_ideal_gas": True,
    "brownian_initial_velocity": [0, 0],
    "brownian_particle_radius": 0.5,
    "brownian_particle_mass": 100.0,

    # LJ Potential parameters
    "use_LJ_potential": True,
    "use_LJ_for_brownian_to_fluid": True,
    "LJ_epsilon": 9/4, # 4 kT/e

    # Render Settings - for when Live render is true
    "render_every": 10,
    "draw_boundary": True,
    "draw_brownian_trail": True,
}
FUll_LJ_CONFIG_6 = {
    # Simulation Settings
    "dt": 0.0005,
    "steps": 20000, #20000
    "box_size": 10.0,
    "N": 1000,
    "live_render": False,
    "num_runs": 100,
    "plot_msd": True,
    "save_plot": True,

    # Properties of the fluid environment
    "fluid_velocity_std": [3,3],
    "fluid_particle_radius": 0.05,
    "fluid_particle_mass": 1.0,

    # Properties of the brownian particle
    "brownian_is_ideal_gas": True,
    "brownian_initial_velocity": [0, 0],
    "brownian_particle_radius": 0.5,
    "brownian_particle_mass": 100.0,

    # LJ Potential parameters
    "use_LJ_potential": True,
    "use_LJ_for_brownian_to_fluid": True,
    "LJ_epsilon": 9/8, # 8 kT/e

    # Render Settings - for when Live render is true
    "render_every": 10,
    "draw_boundary": True,
    "draw_brownian_trail": True,
}
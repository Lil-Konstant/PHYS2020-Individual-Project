from sim.engine import timeStep, initialise_fluid, initialise_brownian_particle
from analysis.metrics import computeFluidMetrics
from render.dashboard import Dashboard
from config.main_configs import TEST_CONFIG as CONFIG # Change import dict for different setups

def run():
    # Use imported config dict to initialise N particles in a box
    brownianState = initialise_brownian_particle(CONFIG)
    fluidState = initialise_fluid(CONFIG)
    dashboard = Dashboard(CONFIG)

    # Iterate by the config number of steps
    for step in range(CONFIG["steps"]):
        # Update engine state
        timeStep(fluidState, brownianState, CONFIG)

        if step % CONFIG["render_every"] == 0:
            # Update live display with new metrics and state
            dashboard.update(fluidState, brownianState, computeFluidMetrics(fluidState, CONFIG["LJ_epsilon"]))

    dashboard.finalise()

if __name__ == "__main__":
    run()
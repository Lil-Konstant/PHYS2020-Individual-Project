from sim.engine import timeStep
from sim.engine import initialise_particles
from analysis.metrics import compute_metrics
from render.dashboard import Dashboard
from config.main_configs import TEST_CONFIG as config # Change import dict for different setups

render_every = 1

def run():
    # Use imported config dict to initialise N particles in a box
    state = initialise_particles(config)
    dashboard = Dashboard(config)

    # Iterate by the config number of steps
    for t in range(config["steps"]):
        timeStep(state, config) # Update engine state
        # print(state.positions[0])

        if t % render_every == 0:
            dashboard.update(state, compute_metrics(state)) # Update live display with new metrics and state

    dashboard.finalise()

if __name__ == "__main__":
    run()
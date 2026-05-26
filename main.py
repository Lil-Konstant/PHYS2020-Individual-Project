from tqdm import tqdm
from sim.engine import timeStep, initialise_fluid, initialise_brownian_particle
from analysis.metrics import computeFluidMetrics
from render.dashboard import Dashboard
from config.main_configs import TEST_CONFIG as CONFIG # Change import dict for different setups

def run_single_simulation(config, dashboard=None, liveRender=False):
    brownianState = initialise_brownian_particle(config)
    fluidState = initialise_fluid(config)

    brownianPositions = []

    for step in range(config["steps"]):
        timeStep(fluidState, brownianState, config)
        brownianPositions.append(brownianState.position.copy())

        if liveRender and step % config["render_every"] == 0:
            dashboard.update(
                fluidState,
                brownianState,
                computeFluidMetrics(fluidState, config["LJ_epsilon"])
            )

    return brownianPositions


def run():
    liveRender = CONFIG.get("live_render", True)
    plotMSD = CONFIG.get("plot_msd", True)
    numRuns = CONFIG.get("num_runs", 1)

    dashboard = Dashboard(CONFIG)

    # If live render, then conduct only one simulation live with the dashboard
    if liveRender:
        brownianPositions = run_single_simulation(CONFIG, dashboard=dashboard,liveRender=True)

        if plotMSD:
            dashboard.plotMSD([brownianPositions], CONFIG["dt"])

        dashboard.finalise()
        return None

    # Otherwise don't live render, conduct the config specified number of runs and store the brownian position data for all of them
    else:
        allBrownianPositions = []

        for _ in tqdm(range(numRuns), desc="Running simulations"):
            brownianPositions = run_single_simulation(CONFIG, dashboard=None, liveRender=False)
            allBrownianPositions.append(brownianPositions)

        if plotMSD:
            dashboard.plotMSD(allBrownianPositions, CONFIG["dt"])
            dashboard.finalise()

        return allBrownianPositions

if __name__ == "__main__":
    run()
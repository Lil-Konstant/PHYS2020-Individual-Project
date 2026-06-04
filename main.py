from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor
from sim.engine import runSingleSimulationSquaredDisplacement, timeStep, initialiseFluid, initialiseBrownianParticle
from analysis.metrics import computeFluidMetrics
from render.dashboard import Dashboard
from config.main_configs import FUll_LJ_CONFIG_8 as CONFIG # Change import dict for different setups

def run():
    liveRender = CONFIG.get("live_render", True)
    plotMSD = CONFIG.get("plot_msd", True)

    # If live render is true, only simulate 1 experiment run and configure the dashboard for live viewing
    if liveRender:
        # Init
        brownianState = initialiseBrownianParticle(CONFIG)
        fluidState = initialiseFluid(CONFIG)
        dashboard = Dashboard(CONFIG)
        brownianPositions = []

        # For each time step, update by dt, update the list of brownian positions, and update live view
        for step in range(CONFIG["steps"]):
            timeStep(fluidState, brownianState, CONFIG)
            brownianPositions.append(brownianState.position.copy())

            # Render once every render_every number of time steps, allowing dt and live frame to decouple a little
            if step % CONFIG["render_every"] == 0:
                dashboard.update(fluidState, brownianState, computeFluidMetrics(fluidState, CONFIG["LJ_epsilon"]))

        # Once the sim is finished, plot the MSD history if true
        if plotMSD:
            dashboard.plotMSD([brownianPositions], CONFIG["dt"])
            dashboard.finalise()

        return [brownianPositions]

    # Otherwise don't live render, conduct the config specified number of runs in parallel, cache them for average MSD results
    numRuns = CONFIG.get("num_runs", 10)
    seeds = list(range(numRuns)) # Create an integer list of seeds for seeding rng's
    maxWorkers = 26

    # Instantiate the process pool executor, map the run function over a list of identical configs, different seeds
    with ProcessPoolExecutor(max_workers=maxWorkers) as executor:
        results = list(tqdm( # tqdm for progress loading bar
                executor.map(runSingleSimulationSquaredDisplacement,[CONFIG] * numRuns, seeds),
                total=numRuns,
                desc="Running simulations"))

    # Once the sim is finished, plot the MSD history if true
    if plotMSD:
        dashboard = Dashboard(CONFIG)
        dashboard.plotMSD(results, CONFIG["dt"], True, CONFIG)
        dashboard.finalise()

    return results

if __name__ == "__main__":
    run()
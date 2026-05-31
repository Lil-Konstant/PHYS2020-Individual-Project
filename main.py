import os
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor
from sim.engine import runSingleSimulationSquaredDisplacement, timeStep, initialiseFluid, initialiseBrownianParticle
from analysis.metrics import computeFluidMetrics
from render.dashboard import Dashboard
from config.main_configs import FUll_LJ_CONFIG_1 as CONFIG # Change import dict for different setups

def run():
    liveRender = CONFIG.get("live_render", True)
    plotMSD = CONFIG.get("plot_msd", True)

    if liveRender:
        brownianState = initialiseBrownianParticle(CONFIG)
        fluidState = initialiseFluid(CONFIG)
        dashboard = Dashboard(CONFIG)
        brownianPositions = []

        for step in range(CONFIG["steps"]):
            timeStep(fluidState, brownianState, CONFIG)
            brownianPositions.append(brownianState.position.copy())

            if step % CONFIG["render_every"] == 0:
                dashboard.update(fluidState, brownianState, computeFluidMetrics(fluidState, CONFIG["LJ_epsilon"]))

        if plotMSD:
            dashboard.plotMSD([brownianPositions], CONFIG["dt"])
            dashboard.finalise()

        return [brownianPositions]

    # Otherwise don't live render, conduct the config specified number of runs in parallel, cache them for average MSD results
    numRuns = CONFIG.get("num_runs", 10)
    seeds = list(range(numRuns))
    maxWorkers = os.cpu_count()

    with ProcessPoolExecutor(max_workers=maxWorkers) as executor:
        results = list(tqdm(
                executor.map(runSingleSimulationSquaredDisplacement,[CONFIG] * numRuns, seeds),
                total=numRuns,
                desc="Running simulations"))

    if plotMSD:
        dashboard = Dashboard(CONFIG)
        dashboard.plotMSD(results, CONFIG["dt"], True, CONFIG)
        dashboard.finalise()

    return results

if __name__ == "__main__":
    run()
from render.simulation_view import SimulationView
from analysis.metrics import estimateConfiguredTemperatures

RUNGROUP_TITLES = ["Ideal Fluid & Ideal Brownian", "LJ Fluid & Ideal Brownian", "LJ Fluid & LJ Brownian"]
SAVE_FILENAMES = ["Ideal", "Partial-LJ", "Full-LJ"]

# Manages live view and analytic view
class Dashboard:
    def __init__(self, config):
        self.view = SimulationView(config)

        rungroupTitle = ""
        saveFilename = ""
        if config["use_LJ_potential"] and config["use_LJ_for_brownian_to_fluid"]:
            rungroupTitle = RUNGROUP_TITLES[2]
            saveFilename = SAVE_FILENAMES[2]
        elif config["use_LJ_potential"]:
            rungroupTitle = RUNGROUP_TITLES[1]
            saveFilename = SAVE_FILENAMES[1]
        else:
            rungroupTitle = RUNGROUP_TITLES[0]
            saveFilename = SAVE_FILENAMES[0]

        self.rungroupTitle = rungroupTitle
        self.saveFilename = saveFilename
        self.shouldSave = config["save_plot"]

    def update(self, fluidState, brownianState, metrics):
        self.view.updateParticles(fluidState.positions, fluidState.radius)
        self.view.updateBrownian(brownianState.position, brownianState.radius)
        self.view.updateTemperatureBox(metrics["reduced_temperature"], metrics["reduced_LJ_temperature"])

    def plotMSD(self, brownianPositions, dt, isSquaredDisplacements=False, config=None):
        if config is not None and config["use_LJ_potential"]:
            temps = estimateConfiguredTemperatures(config)
            self.view.updateMSDTemperatureBox(*temps)
        self.view.plotMSD(brownianPositions, dt, isSquaredDisplacements, self.rungroupTitle, self.saveFilename, self.shouldSave)

    def finalise(self):
        self.view.finalise()
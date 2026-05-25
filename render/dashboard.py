import matplotlib.pyplot as plt
from render.simulation_view import SimulationView

# Manages live view and analytic view
class Dashboard:
    def __init__(self, config):
        self.view = SimulationView(config)

    def update(self, fluidState, brownianState, metrics):
        self.view.updateParticles(fluidState.positions, fluidState.radius)
        self.view.updateBrownian(brownianState.position, brownianState.radius)
        self.view.updateTemperatureBox(metrics["reduced_temperature"], metrics["reduced_LJ_temperature"])

    def finalise(self):
        plt.ioff()
        plt.show()
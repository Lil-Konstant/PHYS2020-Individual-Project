import matplotlib.pyplot as plt
from render.simulation_view import SimulationView

# Manages live view and analytic view
class Dashboard:
    def __init__(self, config):
        self.view = SimulationView(config)

        # plt.ion()
        # self.fig_hist, self.ax_hist = plt.subplots()
        # self.hist_initialized = False
        # self.bars = None

    def update(self, state, metrics):
        self.view.update_particles(state.positions)

        # self.ax_hist.clear()
        # self.ax_hist.hist(metrics["speeds"], bins=30, density=True)
        # self.ax_hist.set_title("Speed Distribution")
        # self.fig_hist.canvas.draw_idle()
        # self.fig_hist.canvas.flush_events()
        # plt.pause(0.001)

    def finalise(self):
        plt.ioff()
        plt.show()
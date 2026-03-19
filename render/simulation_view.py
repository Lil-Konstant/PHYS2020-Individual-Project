import pyqtgraph as pg
from pyqtgraph.Qt import QtCore

class SimulationView:
    def __init__(self, config):
        self.app = pg.mkQApp("Thermal Simulation")

        # Window and plot area
        self.win = pg.GraphicsLayoutWidget(show=True, title="Thermal Simulation")
        self.win.resize(800, 800)

        # Initialise plot props
        self.plot = self.win.addPlot()
        self.plot.setXRange(0, config["box_size"])
        self.plot.setYRange(0, config["box_size"])
        self.plot.setAspectLocked(True)
        self.plot.showGrid(x=True, y=True, alpha=0.2)

        # Use scatter for particle display
        self.scatter = pg.ScatterPlotItem(size=8, pen=None, brush="w")
        self.plot.addItem(self.scatter)

        # Add boundary for box size
        rect = QtCore.QRectF(0, 0, config["box_size"], config["box_size"])
        pen = pg.mkPen(color='r', width=2)
        self.border = pg.QtWidgets.QGraphicsRectItem(rect)
        self.border.setPen(pen)
        self.plot.addItem(self.border)

    def update_particles(self, positions):
        self.scatter.setData(
            x=positions[:, 0],
            y=positions[:, 1]
        )
        self.app.processEvents()

    def close(self):
        self.win.close()
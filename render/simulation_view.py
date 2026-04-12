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

        # Use scatter for fluid and brownian display
        self.fluidScatter = pg.ScatterPlotItem(size=8, pen=None, brush="w")
        self.plot.addItem(self.fluidScatter)
        self.brownianScatter = pg.ScatterPlotItem(size=12, pen=None, brush='r')
        self.plot.addItem(self.brownianScatter)

        # Add boundary for box size
        rect = QtCore.QRectF(0, 0, config["box_size"], config["box_size"])
        pen = pg.mkPen(color='r', width=2)
        self.border = pg.QtWidgets.QGraphicsRectItem(rect)
        self.border.setPen(pen)
        self.plot.addItem(self.border)

    def updateParticles(self, positions, radii):
        scale = self.plot.viewRange()[0][1] / self.plot.width()
        sizes = 2 * radii / scale

        self.fluidScatter.setData(
            x=positions[:, 0],
            y=positions[:, 1],
            size=sizes,
        )
        self.app.processEvents()

    def updateBrownian(self, position, radius):
        scale = self.plot.viewRange()[0][1] / self.plot.width()
        size = 2 * radius / scale

        self.brownianScatter.setData(
            x=[position[0]],
            y=[position[1]],
            size=size,
        )
        self.app.processEvents()

    def close(self):
        self.win.close()
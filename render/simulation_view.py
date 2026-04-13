import pyqtgraph as pg
import numpy as np
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
        self.fluidScatter = pg.ScatterPlotItem(size=config["fluid_particle_radius"]*2, pen=None,
                                               brush=pg.mkBrush(245, 66, 66, 240), pxMode=False)
        self.plot.addItem(self.fluidScatter)
        self.brownianScatter = pg.ScatterPlotItem(size=config["brownian_particle_radius"]*2, pen=None,
                                                  brush=pg.mkBrush(222, 185, 0, 255), pxMode=False)
        self.plot.addItem(self.brownianScatter)

        # Trail line
        self.trailItem = pg.PlotDataItem(pen=pg.mkPen(0, 255, 0, 255, width=2))
        self.plot.addItem(self.trailItem)
        self.trailHistory = []
        self.maxTrailPoints = 200
        self.drawBrownianTrail = config["draw_brownian_trail"]

        # Add boundary for box size
        rect = QtCore.QRectF(0, 0, config["box_size"], config["box_size"])
        pen = pg.mkPen(color='r', width=2)
        self.border = pg.QtWidgets.QGraphicsRectItem(rect)
        self.border.setPen(pen)
        self.plot.addItem(self.border)

    def updateParticles(self, positions, radii):
        self.fluidScatter.setData(
            x=positions[:, 0],
            y=positions[:, 1],
        )
        self.app.processEvents()

    def updateBrownian(self, position, radius):
        self.brownianScatter.setData(
            x=[position[0]],
            y=[position[1]],
        )

        # Update trail if debug is true
        if self.drawBrownianTrail:
            self.trailHistory.append([float(position[0]), float(position[1])])
            if len(self.trailHistory) > self.maxTrailPoints:
                self.trailHistory.pop(0)

            trail = np.array(self.trailHistory, dtype=float)
            self.trailItem.setData(trail[:, 0], trail[:, 1])

        self.app.processEvents()

    def close(self):
        self.win.close()
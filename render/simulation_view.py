import pyqtgraph as pg
import numpy as np
from pyqtgraph.Qt import QtCore

class SimulationView:
    def __init__(self, config):
        self.app = pg.mkQApp("Thermal Simulation")

        if config.get("live_render", True):
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

            # Temperature display box
            self.temperatureBox = pg.TextItem(anchor=(0, 0), html="")
            self.temperatureBox.setPos(0, -0.25)
            self.plot.addItem(self.temperatureBox)

        # MSD plot window
        self.msdWindow = pg.GraphicsLayoutWidget(show=False, title="Brownian MSD")
        self.msdWindow.resize(700, 500)
        self.msdPlot = self.msdWindow.addPlot(
            title="Brownian Particle Squared Displacement"
        )
        self.msdCurve = self.msdPlot.plot(
            pen=pg.mkPen(width=2)
        )
        self.msdPlot.setLabel("bottom", "Time")
        self.msdPlot.setLabel("left", "Squared displacement")
        self.msdPlot.showGrid(x=True, y=True, alpha=0.3)

    def updateTemperatureBox(self, reducedTemperature, reducedLJTemperature):
        self.temperatureBox.setHtml(f"""
            <div style="
                background-color: rgba(0, 0, 0, 180);
                color: white;
                border: 1px solid white;
                padding: 6px;
                font-size: 12pt;
            ">
                <div>Reduced Temperature: {reducedTemperature:.3f} kT</div>
                <div>Reduced LJ Temperature: {reducedLJTemperature:.3f} kT/epsilon</div>
            </div>
        """)

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

    def plotMSD(self, allBrownianPositions, dt, isSquaredDisplacements=False):
        self.msdWindow.show()
        self.msdWindow.raise_()
        self.msdWindow.activateWindow()
        self.msdPlot.clear()

        allSquaredDisplacements = []

        for runIdx, brownianPositions in enumerate(allBrownianPositions):
            positions = np.array(brownianPositions)
            if len(positions) == 0: continue

            # Convert these brownian positions to squared displacement if not already
            if not isSquaredDisplacements:
                initialPosition = positions[0]
                displacements = positions - initialPosition
                squaredDisplacements = np.sum(displacements ** 2, axis=1)
            else:
                squaredDisplacements = positions

            allSquaredDisplacements.append(squaredDisplacements)
            times = np.arange(len(squaredDisplacements)) * dt
            self.msdPlot.plot(times, squaredDisplacements, pen=pg.mkPen((180, 180, 180, 80), width=1)
            )

        if len(allSquaredDisplacements) == 0: return

        # Average over runs
        allSquaredDisplacements = np.array(allSquaredDisplacements)
        meanSquaredDisplacement = np.mean(allSquaredDisplacements, axis=0)
        times = np.arange(len(meanSquaredDisplacement)) * dt

        # Plot averaged MSD curve
        self.msdPlot.plot(times, meanSquaredDisplacement, pen=pg.mkPen((255, 80, 80), width=4), name="Average MSD")

        # Fit diffusion coefficient from later-time linear region
        # Avoid very early transient region
        fitStartFraction = 0.2
        fitEndFraction = 0.8
        startIdx = int(fitStartFraction * len(times))
        endIdx = int(fitEndFraction * len(times))
        fitTimes = times[startIdx:endIdx]
        fitMSD = meanSquaredDisplacement[startIdx:endIdx]
        slope, intercept = np.polyfit(fitTimes, fitMSD, 1)

        # MSD = 4Dt
        D = slope / 4

        # Plot fitted line
        fittedMSD = slope * times + intercept

        self.msdPlot.plot(times, fittedMSD, pen=pg.mkPen((80, 180, 255), width=2, style=QtCore.Qt.PenStyle.DashLine), name=f"Fit: D = {D:.4f}")
        self.msdPlot.setTitle(f"Brownian MSD over {len(allSquaredDisplacements)} runs | D = {D:.4f}")
        self.msdPlot.setLabel("bottom", "Time")
        self.msdPlot.setLabel("left", "Mean squared displacement")
        self.msdPlot.showGrid(x=True, y=True, alpha=0.3)

        print(f"Estimated diffusion coefficient D = {D:.6f}")
        print(f"Fit slope = {slope:.6f}")
        print(f"Fit intercept = {intercept:.6f}")

        self.app.processEvents()

    def finalise(self):
        self.app.exec()

    def close(self):
        self.win.close()
        self.msdWindow.close()
import os
import pyqtgraph as pg
import numpy as np
from pyqtgraph.Qt import QtCore
import pyqtgraph.exporters as exporters

SAVE_DIR = "outputs"

class SimulationView:
    def __init__(self, config):
        self.app = pg.mkQApp("Thermal Simulation")

        # If live render is true, create a plot and screen for particle display during runtime
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
            self.fluidScatter = pg.ScatterPlotItem(size=config["fluid_particle_radius"]*2, pen=None, brush=pg.mkBrush(245, 66, 66, 240), pxMode=False)
            self.plot.addItem(self.fluidScatter)
            self.brownianScatter = pg.ScatterPlotItem(size=config["brownian_particle_radius"]*2, pen=None, brush=pg.mkBrush(222, 185, 0, 255), pxMode=False)
            self.plot.addItem(self.brownianScatter)

            # Trail line for brownian particle movement
            self.trailItem = pg.PlotDataItem(pen=pg.mkPen(0, 255, 0, 255, width=2))
            self.plot.addItem(self.trailItem)
            self.trailHistory = []
            self.maxTrailPoints = 200
            self.drawBrownianTrail = config["draw_brownian_trail"]

            # Add visible boundary for box extents
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
        self.msdWindow.resize(800, 600)
        self.msdPlot = self.msdWindow.addPlot(title="Brownian Particle Mean Squared Displacement")
        self.msdCurve = self.msdPlot.plot(pen=pg.mkPen(width=2))
        self.msdPlot.setLabel("bottom", "Time")
        self.msdPlot.setLabel("left", "Mean Squared displacement")
        self.msdPlot.showGrid(x=True, y=True, alpha=0.3)
        self.msdTemperatureBox = pg.TextItem(anchor=(0, 0), html="")
        self.msdPlot.addItem(self.msdTemperatureBox)
        self.msdLegend = self.msdPlot.addLegend()
        self.msdLegend.setLabelTextSize("14pt")

    def updateTemperatureBox(self, reducedTemperature, reducedLJTemperature):
        """
        Adds temperature box to live display window
        """
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

    def updateMSDTemperatureBox(self, reducedTemperature, reducedLJTemperature):
        """
        Adds temperature box to MSD plot
        """
        self.msdTemperatureBox.setHtml(f"""
            <div style="
                background-color: rgba(0, 0, 0, 180);
                color: white;
                border: 1px solid white;
                padding: 6px;
                font-size: 12pt;
            ">
                <div>Reduced Temperature: {reducedTemperature:.1f} kT</div>
                <div>Reduced LJ Temperature: {reducedLJTemperature:.1f} kT/epsilon</div>
            </div>
        """)

    def updateParticles(self, positions):
        """
        Update the fluid scatter plot
        """
        self.fluidScatter.setData(x=positions[:, 0], y=positions[:, 1],)
        self.app.processEvents()

    def updateBrownian(self, position):
        """
        Update the brownian scatter plot, draw trail if set to.
        """
        self.brownianScatter.setData(x=[position[0]], y=[position[1]],)

        # Update trail if debug is true
        if self.drawBrownianTrail:
            self.trailHistory.append([float(position[0]), float(position[1])])
            if len(self.trailHistory) > self.maxTrailPoints:
                self.trailHistory.pop(0)

            trail = np.array(self.trailHistory, dtype=float)
            self.trailItem.setData(trail[:, 0], trail[:, 1])

        self.app.processEvents()

    def plotMSD(self, allBrownianPositions, dt, isSquaredDisplacements=False, runGroupTitle="", saveFilename="", shouldSave=False):
        """
        Given a list of lists brownian positions either as squared displacements or just positions, plot each list using
        dt as the range of time values. If not already in squared distance form, puts it into this form. Then calculates
        the mean squared distance of all of these lists and plots it in red. Also fits a diffusion coefficient given
        a fixed time window of linearity and plots this as a blue dotted line. Saves to output directory if shouldSave.
        """
        self.msdWindow.show()
        self.msdWindow.raise_()
        self.msdWindow.activateWindow()
        self.msdPlot.clear()
        self.msdPlot.addItem(self.msdTemperatureBox)

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
            self.msdPlot.plot(times, squaredDisplacements, pen=pg.mkPen((180, 180, 180, 80), width=1, name=None))

        if len(allSquaredDisplacements) == 0: return

        # Average over runs
        allSquaredDisplacements = np.array(allSquaredDisplacements)
        meanSquaredDisplacement = np.mean(allSquaredDisplacements, axis=0)
        times = np.arange(len(meanSquaredDisplacement)) * dt

        # Plot averaged MSD curve
        self.msdPlot.plot(times, meanSquaredDisplacement, pen=pg.mkPen((255, 80, 80), width=4), name="Average MSD")

        # Fit diffusion coefficient from later-time linear region
        fitStartTime = 2.0
        fitEndTime = 5.0
        fitMask = (times >= fitStartTime) & (times <= fitEndTime)
        fitTimes = times[fitMask]
        fitMSD = meanSquaredDisplacement[fitMask]
        slope, intercept = np.polyfit(fitTimes, fitMSD, 1)
        D = slope / 4

        # Plot Linear MSD
        fittedMSD = slope * fitTimes + intercept
        self.msdPlot.plot(fitTimes,fittedMSD,pen=pg.mkPen((80, 180, 255),width=2,style=QtCore.Qt.PenStyle.DashLine),name=f"Fit: D = {D:.4f}")
        self.msdPlot.setTitle(f"Brownian MSD over {len(allSquaredDisplacements)} runs | {runGroupTitle}")
        self.msdPlot.setLabel("bottom", "Time")
        self.msdPlot.setLabel("left", "Mean squared displacement")
        self.msdPlot.showGrid(x=True, y=True, alpha=0.3)

        # Fix the plot fitting to window size
        xMin = times[0]
        xMax = times[-1]
        yMin = 0
        yMax = max(np.max(meanSquaredDisplacement), np.max(allSquaredDisplacements))
        self.msdPlot.setXRange(xMin, xMax, padding=0)
        self.msdPlot.setYRange(yMin, yMax * 1.05, padding=0)
        self.msdPlot.getViewBox().setDefaultPadding(0.0)

        # Reposition the temperature box within the limits
        xPos = xMin + 0.5 * (xMax - xMin)
        yPos = yMax * 1.1 - 0.12 * (yMax * 1.05 - yMin)
        self.msdTemperatureBox.setPos(xPos, yPos)

        if shouldSave:
            os.makedirs(SAVE_DIR, exist_ok=True)
            exporter = pg.exporters.ImageExporter(self.msdPlot)
            exporter.parameters()["width"] = 1200
            exporter.export(SAVE_DIR + "/" + saveFilename + "_msd_plot.png")

        self.app.processEvents()

    def finalise(self):
        self.app.exec()

    def close(self):
        self.win.close()
        self.msdWindow.close()
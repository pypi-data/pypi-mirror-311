from __future__ import annotations

import logging

from silx.gui import qt

from tomwer.core.process.reconstruction.axis import mode as axis_mode
from tomwer.core.process.reconstruction.axis.anglemode import CorAngleMode
from tomwer.core.process.reconstruction.axis.params import (
    DEFAULT_CMP_N_SUBSAMPLING_Y,
    DEFAULT_CMP_OVERSAMPLING,
    DEFAULT_CMP_TAKE_LOG,
    DEFAULT_CMP_THETA,
)
from tomwer.gui.utils.scrollarea import QComboBoxIgnoreWheel
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.gui.utils.qt_utils import block_signals
from tomwer.synctools.axis import QAxisRP
from .CalculationWidget import CalculationWidget
from .ManualFramesSelection import ManualFramesSelection

_logger = logging.getLogger(__name__)


class InputWidget(qt.QWidget):
    """
    Widget used to define the radios or the sinogram to be used for computing the cor
    Used as a tab of the AxisSettingsTabWidget
    """

    sigChanged = qt.Signal()
    """Signal emitted when input changed"""

    _sigUrlChanged = qt.Signal()
    """Signal emit when url to be used changed"""

    def __init__(self, parent=None, axis_params=None):
        assert isinstance(axis_params, QAxisRP)
        self._blockUpdateAxisParams = False
        super().__init__(parent)
        self.setLayout(qt.QVBoxLayout())

        # radio input
        self._radioGB = qt.QGroupBox(self)
        self._radioGB.setTitle("radios")
        self._radioGB.setLayout(qt.QVBoxLayout())
        self._radioGB.setCheckable(True)
        self.layout().addWidget(self._radioGB)
        ## angle mode
        self._angleModeWidget = _AngleSelectionWidget(
            parent=self, axis_params=axis_params
        )
        self._radioGB.layout().addWidget(self._angleModeWidget)
        self._axis_params = axis_params

        # sinogram input
        self._sinogramGB = qt.QGroupBox(self)
        self._sinogramGB.setLayout(qt.QVBoxLayout())
        self._standardSinogramOpts = qt.QGroupBox(self)
        self._sinogramGB.layout().addWidget(self._standardSinogramOpts)
        self._standardSinogramOpts.setLayout(qt.QFormLayout())
        self._standardSinogramOpts.layout().setContentsMargins(0, 0, 0, 0)
        self._standardSinogramOpts.setTitle("standard options")

        self._sinogramGB.setTitle("sinogram")
        self._sinogramGB.setCheckable(True)
        self.layout().addWidget(self._sinogramGB)
        ##  sinogram line
        self._sinogramLineSB = _SliceSelector(self)
        self._standardSinogramOpts.layout().addRow("line", self._sinogramLineSB)
        ##  sinogram subsampling
        self._sinogramSubsampling = qt.QSpinBox(self)
        self._sinogramSubsampling.setRange(1, 1000)
        self._sinogramSubsampling.setValue(10)
        self._standardSinogramOpts.layout().addRow(
            "subsampling", self._sinogramSubsampling
        )

        self._spacer = qt.QWidget(self)
        self._spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self.layout().addWidget(self._spacer)

        ## options for the composite mode
        self._compositeOpts = qt.QGroupBox(self)
        self._compositeOpts.setTitle("composite options")
        self._sinogramGB.layout().addWidget(self._compositeOpts)
        self._compositeOpts.setLayout(qt.QFormLayout())
        self._compositeOpts.layout().setContentsMargins(0, 0, 0, 0)
        self._thetaSB = qt.QSpinBox(self)
        self._thetaSB.setRange(0, 360)
        self._thetaSB.setValue(DEFAULT_CMP_THETA)
        self._thetaSB.setToolTip("a radio will be picked each theta degres")
        self._thetaLabel = qt.QLabel("angle interval (in degree)", self)
        self._thetaLabel.setToolTip(
            "algorithm will take one projection each 'angle interval'. Also know as 'theta'"
        )
        self._compositeOpts.layout().addRow(self._thetaLabel, self._thetaSB)

        self._oversamplingSB = qt.QSpinBox(self)
        self._oversamplingSB.setValue(DEFAULT_CMP_OVERSAMPLING)
        self._oversamplingSB.setToolTip("sinogram oversampling")
        self._compositeOpts.layout().addRow("oversampling", self._oversamplingSB)

        self._nearwidthSB = qt.QSpinBox(self)
        self._nearwidthSB.setRange(-40000, 40000)
        self._nearwidthSB.setValue(0)
        self._nearwidthSB.setToolTip("position to be used with near option")
        self._nearwidthLabel = qt.QLabel("near width", self)
        self._nearwidthLabel.setToolTip("position to be used with near option")
        self._compositeOpts.layout().addRow(self._nearwidthLabel, self._nearwidthSB)

        self._subsamplingYSB = qt.QSpinBox(self)
        self._subsamplingYSB.setValue(DEFAULT_CMP_N_SUBSAMPLING_Y)
        self._subsamplingYSB.setToolTip("sinogram number of subsampling along y")
        self._compositeOpts.layout().addRow("n_subsampling_y", self._subsamplingYSB)

        self._takeLogCB = qt.QCheckBox(self)
        self._takeLogCB.setToolTip("Take logarithm")
        self._takeLogCB.setChecked(DEFAULT_CMP_TAKE_LOG)
        self._takeTheLogLabel = qt.QLabel("linearisation (-log(I/I0))")
        self._takeTheLogLabel.setToolTip(
            "take (-log(I/I0)) as input. Also know as 'take_log' option"
        )
        self._compositeOpts.layout().addRow(self._takeTheLogLabel, self._takeLogCB)

        # set up
        self._sinogramGB.setChecked(False)

        # connect signal / slot
        self._sinogramGB.toggled.connect(self._sinogramChecked)
        self._radioGB.toggled.connect(self._radiosChecked)
        self._sinogramSubsampling.valueChanged.connect(self._changed)
        self._sinogramLineSB.sigChanged.connect(self._changed)
        self._thetaSB.valueChanged.connect(self._changed)
        self._oversamplingSB.valueChanged.connect(self._changed)
        self._subsamplingYSB.valueChanged.connect(self._changed)
        self._nearwidthSB.valueChanged.connect(self._changed)
        self._takeLogCB.toggled.connect(self._changed)
        self._angleModeWidget.sigChanged.connect(self._sigUrlChanged)

    def setScan(self, scan: TomwerScanBase):
        if scan is not None:
            self._angleModeWidget.setScan(scan)
            self._angleModeWidget.setScanRange(scan.scan_range)

    def setAxisParams(self, axis_params):
        with block_signals(axis_params):
            with block_signals(self._axis_params):
                self._blockUpdateAxisParams = True

                if axis_params is not None:
                    assert isinstance(axis_params, QAxisRP)
                    with block_signals(self._sinogramGB):
                        self._sinogramChecked(axis_params.use_sinogram, on_load=True)
                    self._sinogramLineSB.setSlice(axis_params.sinogram_line)
                    self._sinogramSubsampling.setValue(axis_params.sinogram_subsampling)
                    self.setCompositeOptions(axis_params.composite_options)
                self._angleModeWidget.setAxisParams(axis_params)
                self._axis_params = axis_params

        self._blockUpdateAxisParams = False

    def getSinogramLine(self) -> str | int:
        return self._sinogramLineSB.getSlice()

    def getSinogramSubsampling(self) -> int:
        return self._sinogramSubsampling.value()

    def _sinogramChecked(self, checked, on_load=False):
        with block_signals(self._radioGB):
            with block_signals(self._sinogramGB):
                if checked:
                    self._radioGB.setChecked(False)
                    self._sinogramGB.setChecked(True)
                elif self._radioGB.isEnabled():
                    self._radioGB.setChecked(not checked)
                elif on_load:
                    self._sinogramGB.setChecked(checked)
                else:
                    # ignore it if radio disabled
                    self._sinogramGB.setChecked(True)
        self._changed()

    def _radiosChecked(self, checked, on_load=False):
        with block_signals(self._radioGB):
            with block_signals(self._sinogramGB):
                if checked:
                    self._sinogramGB.setChecked(False)
                    self._radioGB.setChecked(True)
                elif self._sinogramGB.isEnabled():
                    self._sinogramGB.setChecked(not checked)
                elif on_load:
                    self._radioGB.setChecked(checked)
                else:
                    # ignore it if sinogram disabled
                    self._radioGB.setChecked(True)
        self._changed()

    def _changed(self, *args, **kwargs):
        self._updateAxisParams()
        self.sigChanged.emit()

    def _updateAxisParams(self):
        if not self._blockUpdateAxisParams:
            self._axis_params.use_sinogram = self._sinogramGB.isChecked()
            self._axis_params.sinogram_line = self.getSinogramLine()
            self._axis_params.sinogram_subsampling = self.getSinogramSubsampling()
            self._axis_params.composite_options = self.getCompositeOptions()

    def setValidInputs(self, modes: list | tuple):
        """
        Define possible inputs.

        :raises: ValueError if modes are invalid
        """
        modes = set(modes)
        for mode in modes:
            try:
                axis_mode._InputType.from_value(mode)
            except Exception:
                raise ValueError(
                    f"mode {mode} should be an instance of {axis_mode._InputType}"
                )
        if len(modes) == 2:
            self._sinogramGB.setEnabled(True)
            self._radioGB.setEnabled(True)
        elif len(modes) > 2:
            raise ValueError(f"invalid input {modes}")
        elif len(modes) < 0:
            raise ValueError("modes is empty")
        else:
            mode = axis_mode._InputType.from_value(modes.pop())
            if mode in (axis_mode._InputType.SINOGRAM, axis_mode._InputType.COMPOSITE):
                self._sinogramGB.setEnabled(True)
                self._radioGB.setEnabled(False)
                self._sinogramGB.setChecked(True)
                self._compositeOpts.setEnabled(mode is axis_mode._InputType.COMPOSITE)
                self._standardSinogramOpts.setEnabled(
                    mode is not axis_mode._InputType.COMPOSITE
                )
            elif mode is axis_mode._InputType.RADIOS_X2:
                self._radioGB.setEnabled(True)
                self._sinogramGB.setEnabled(False)
                self._radioGB.setChecked(True)
            else:
                raise ValueError(f"Nothing implemented for {mode.value}")

    def getCompositeOptions(self) -> dict:
        return {
            "theta": self.getTheta(),
            "oversampling": self.getOversampling(),
            "n_subsampling_y": self.getSubsamplingY(),
            "take_log": self.getTakeLog(),
            "near_pos": self.getNearpos(),
            "near_width": self.getNearwidth(),
        }

    def setCompositeOptions(self, opts: dict) -> None:
        if not isinstance(opts, dict):
            raise TypeError("opts should be an instance of dict")
        for key in opts.keys():
            if key not in (
                "theta",
                "oversampling",
                "n_subsampling_y",
                "take_log",
                "near_pos",
                "near_width",
            ):
                raise KeyError(f"{key} is not recogized")
            theta = opts.get("theta", None)
            if theta is not None:
                self.setTheta(theta=theta)
            oversampling = opts.get("oversampling", None)
            if oversampling is not None:
                self.setOversampling(oversampling)
            n_subsampling_y = opts.get("n_subsampling_y", None)
            if n_subsampling_y is not None:
                self.setSubsamplingY(n_subsampling_y)

            near_width = opts.get("near_width", None)
            if near_width is not None:
                self.setNearwidth(near_width)

            take_log = opts.get("take_log", None)
            if take_log is not None:
                self.setTakeLog(take_log)

    def getTheta(self) -> int:
        return self._thetaSB.value()

    def setTheta(self, theta: int) -> None:
        self._thetaSB.setValue(theta)

    def getOversampling(self) -> int:
        return self._oversamplingSB.value()

    def setOversampling(self, oversampling: int) -> None:
        self._oversamplingSB.setValue(oversampling)

    def getNearpos(self) -> int:
        cal_widget = self.parentWidget().widget(0)
        assert isinstance(cal_widget, CalculationWidget)
        return cal_widget.getEstimatedCor()

    def setNearpos(self, value) -> int:
        cal_widget = self.parentWidget().widget(0)
        assert isinstance(cal_widget, CalculationWidget)
        cal_widget.setNearPosition(value)

    def getNearwidth(self) -> int:
        return self._nearwidthSB.value()

    def setNearwidth(self, value) -> int:
        return self._nearwidthSB.setValue(value)

    def getSubsamplingY(self) -> int:
        return self._subsamplingYSB.value()

    def setSubsamplingY(self, subsampling: int) -> None:
        self._subsamplingYSB.setValue(subsampling)

    def getTakeLog(self) -> bool:
        return self._takeLogCB.isChecked()

    def setTakeLog(self, log: bool) -> None:
        self._takeLogCB.setChecked(log)


class _AngleSelectionWidget(qt.QWidget):
    """Group box to select the angle to used for cor calculation
    (0-180, 90-270 or manual)"""

    sigChanged = qt.Signal()
    """signal emitted when the selected angle changed"""

    def __init__(self, parent=None, axis_params=None):
        assert isinstance(axis_params, QAxisRP)
        qt.QWidget.__init__(
            self,
            parent=parent,
        )
        self.setLayout(qt.QVBoxLayout())
        self._groupBoxMode = qt.QGroupBox(
            self, title="Angles to use for axis calculation"
        )
        self._groupBoxMode.setLayout(qt.QHBoxLayout())
        self.layout().addWidget(self._groupBoxMode)

        self._corButtonsGps = qt.QButtonGroup(parent=self)
        self._corButtonsGps.setExclusive(True)
        self._qrbCOR_0_180 = qt.QRadioButton("0-180", parent=self)
        self._groupBoxMode.layout().addWidget(self._qrbCOR_0_180)
        self._qrbCOR_90_270 = qt.QRadioButton("90-270", parent=self)
        self._qrbCOR_90_270.setToolTip(
            "pick radio closest to angles 90° and "
            "270°. If disable mean that the scan "
            "range is 180°"
        )
        self._groupBoxMode.layout().addWidget(self._qrbCOR_90_270)
        self._qrbCOR_manual = qt.QRadioButton("other", parent=self)
        self._qrbCOR_manual.setVisible(True)
        self._groupBoxMode.layout().addWidget(self._qrbCOR_manual)
        # add all button to the button group
        for b in (self._qrbCOR_0_180, self._qrbCOR_90_270, self._qrbCOR_manual):
            self._corButtonsGps.addButton(b)

        self.setAxisParams(axis_params)

        self._manualFrameSelection = ManualFramesSelection(self)
        self.layout().addWidget(self._manualFrameSelection)
        self._manualFrameSelection.setVisible(False)

        # connect signal / Slot
        self._corButtonsGps.buttonClicked.connect(self._angleModeChanged)
        self._manualFrameSelection.sigChanged.connect(self._changed)

    def setScan(self, scan: TomwerScanBase):
        if scan is not None:
            self.setScanRange(scan.scan_range)
        self._manualFrameSelection.setScan(scan=scan)

    def setScanRange(self, scanRange):
        if scanRange == 180:
            self._qrbCOR_90_270.setEnabled(False)
            # force using 0-180 if was using 90-270
            if self._qrbCOR_90_270.isChecked():
                self._qrbCOR_0_180.setChecked(True)
                self._axis_params.angle_mode = CorAngleMode.use_0_180
        else:
            self._qrbCOR_90_270.setEnabled(True)

    def setAngleMode(self, mode):
        """

        :param mode: mode to use (can be manual , 90-270 or 0-180)
        """
        assert isinstance(mode, CorAngleMode)
        if mode == CorAngleMode.use_0_180:
            self._qrbCOR_0_180.setChecked(True)
        elif mode == CorAngleMode.use_90_270:
            self._qrbCOR_90_270.setChecked(True)
        else:
            self._qrbCOR_manual.setChecked(True)

    def getAngleMode(self) -> CorAngleMode:
        """

        :return: the angle to use for the axis calculation
        """
        if self._qrbCOR_90_270.isChecked():
            return CorAngleMode.use_90_270
        elif self._qrbCOR_0_180.isChecked():
            return CorAngleMode.use_0_180
        else:
            return CorAngleMode.manual_selection

    def setAxisParams(self, axis_params):
        with block_signals(self):
            self._axis_params = axis_params
            # set up
            self.setAngleMode(axis_params.angle_mode)

    def _angleModeChanged(self, *args, **kwargs):
        self._axis_params.angle_mode = self.getAngleMode()
        if self.getAngleMode() is CorAngleMode.manual_selection:
            self._axis_params.angle_mode_extra = (
                self._manualFrameSelection.getFramesUrl()
            )
        else:
            self._axis_params.angle_mode_extra = None
        self._manualFrameSelection.setVisible(
            self.getAngleMode() is CorAngleMode.manual_selection
        )
        self._changed()

    def _changed(self):
        self.sigChanged.emit()


class _SliceSelector(qt.QWidget):
    sigChanged = qt.Signal()
    """signal emit when the selected slice change"""

    def __init__(self, parent):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QHBoxLayout())
        self.setContentsMargins(0, 0, 0, 0)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self._modeCB = QComboBoxIgnoreWheel(self)
        self._modeCB.addItem("middle")
        self._modeCB.addItem("other")
        self.layout().addWidget(self._modeCB)
        self._otherSB = qt.QSpinBox(self)
        self._otherSB.setRange(0, 10000)
        self.layout().addWidget(self._otherSB)

        # connect signal / slot
        self._otherSB.valueChanged.connect(self._valueChanged)
        self._modeCB.currentIndexChanged.connect(self._modeChanged)
        # set up
        self._modeChanged()

    def getSlice(self) -> int | str:
        "return a specific slice index or 'middle'"
        if self.getMode() == "middle":
            return "middle"
        else:
            return self._otherSB.value()

    def setSlice(self, slice_):
        if slice_ is None:
            return
        if slice_ == "middle":
            idx = self._modeCB.findText("middle")
            self._modeCB.setCurrentIndex(idx)
        else:
            idx = self._modeCB.findText("other")
            self._modeCB.setCurrentIndex(idx)
            self._otherSB.setValue(slice_)
        self.sigChanged.emit()

    def getMode(self):
        return self._modeCB.currentText()

    def _valueChanged(self):
        self.sigChanged.emit()

    def _modeChanged(self, *args, **kwargs):
        self._otherSB.setVisible(self.getMode() == "other")
        self._valueChanged()

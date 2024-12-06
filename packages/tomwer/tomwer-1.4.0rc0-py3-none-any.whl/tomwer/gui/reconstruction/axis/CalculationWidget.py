from __future__ import annotations

import logging

from silx.gui import qt

from tomwer.core.process.reconstruction.axis import mode as axis_mode
from tomwer.gui.utils.buttons import PadlockButton
from tomwer.gui.utils.qt_utils import block_signals
from tomwer.synctools.axis import QAxisRP
from tomwer.gui.utils.scrollarea import QComboBoxIgnoreWheel

_logger = logging.getLogger(__name__)


class CalculationWidget(qt.QWidget):
    """
    Main widget to select the algorithm to use for COR calculation
    Used as a tab of the AxisSettingsTabWidget
    """

    sigModeChanged = qt.Signal(str)
    """signal emitted when the algorithm for computing COR changed"""

    sigLockModeChanged = qt.Signal(bool)
    """signal emitted when the mode has been lock or unlock"""

    def __init__(self, parent, axis_params):
        assert isinstance(axis_params, QAxisRP)
        qt.QWidget.__init__(self, parent)
        self._axis_params = None
        self.setLayout(qt.QVBoxLayout())

        self._modeWidget = qt.QWidget(parent=self)
        self._modeWidget.setLayout(qt.QHBoxLayout())
        self.layout().addWidget(self._modeWidget)

        self.__rotAxisSelLabel = qt.QLabel("algorithm to compute cor")
        self._modeWidget.layout().addWidget(self.__rotAxisSelLabel)
        self._qcbPosition = QComboBoxIgnoreWheel(self)

        algorithm_groups = (
            # radio group
            (
                axis_mode.AxisMode.centered,
                axis_mode.AxisMode.global_,
                axis_mode.AxisMode.growing_window_radios,
                axis_mode.AxisMode.sliding_window_radios,
                axis_mode.AxisMode.octave_accurate_radios,
            ),
            # sino group
            (
                axis_mode.AxisMode.growing_window_sinogram,
                axis_mode.AxisMode.sino_coarse_to_fine,
                axis_mode.AxisMode.sliding_window_sinogram,
                axis_mode.AxisMode.sino_fourier_angles,
            ),
            # composite corase to fine
            (
                axis_mode.AxisMode.composite_coarse_to_fine,
                axis_mode.AxisMode.near,
            ),
            # read
            (axis_mode.AxisMode.read,),
            # manual
            (axis_mode.AxisMode.manual,),
        )
        current_pos = 0
        for i_grp, algorithm_group in enumerate(algorithm_groups):
            if i_grp != 0:
                self._qcbPosition.insertSeparator(current_pos)
                current_pos += 1
            for cor_algorithm in algorithm_group:
                self._qcbPosition.addItem(cor_algorithm.value)
                idx = self._qcbPosition.findText(cor_algorithm.value)
                self._qcbPosition.setItemData(
                    idx,
                    axis_mode.AXIS_MODE_METADATAS[cor_algorithm].tooltip,
                    qt.Qt.ToolTipRole,
                )
                current_pos += 1

        self._modeWidget.layout().addWidget(self._qcbPosition)

        # method lock button
        self._lockMethodPB = PadlockButton(parent=self._modeWidget)
        self._lockMethodPB.setToolTip(
            "Lock the method to compute the cor. \n"
            "This will automatically call the "
            "defined algorithm each time a scan is received."
        )
        self._modeWidget.layout().addWidget(self._lockMethodPB)

        self._optsWidget = qt.QWidget(self)
        self._optsWidget.setLayout(qt.QVBoxLayout())
        self.layout().addWidget(self._optsWidget)

        # padding option
        self._padding_widget = qt.QGroupBox("padding mode")
        self._padding_widget.setCheckable(True)
        self._optsWidget.layout().addWidget(self._padding_widget)
        self._padding_widget.setLayout(qt.QHBoxLayout())

        self._qbPaddingMode = QComboBoxIgnoreWheel(self._padding_widget)
        for _mode in (
            "constant",
            "edge",
            "linear_ramp",
            "maximum",
            "mean",
            "median",
            "minimum",
            "reflect",
            "symmetric",
            "wrap",
        ):
            self._qbPaddingMode.addItem(_mode)
        def_index = self._qbPaddingMode.findText("edge")
        self._qbPaddingMode.setCurrentIndex(def_index)
        self._padding_widget.layout().addWidget(self._qbPaddingMode)

        # side option
        self._sideWidget = qt.QWidget(self)
        self._sideWidget.setLayout(qt.QHBoxLayout())
        self._optsWidget.layout().addWidget(self._sideWidget)
        self._sideWidget.layout().addWidget(qt.QLabel("side:", self))
        self._sideCB = QComboBoxIgnoreWheel(self._optsWidget)
        self._sideWidget.layout().addWidget(self._sideCB)
        self._sideCB.setToolTip(
            "Define a side for the sliding and growing" "window algorithms"
        )

        # near mode options
        self._nearOptsWidget = qt.QWidget(parent=self)
        self._nearOptsWidget.setLayout(qt.QVBoxLayout())
        self._optsWidget.layout().addWidget(self._nearOptsWidget)

        #    near value lock button
        self._nearValueCB = qt.QCheckBox(
            "Update automatically if `x_rotation_axis_pixel_position` found"
        )
        self._nearValueCB.setToolTip(
            "If the acquisition contains an "
            "estimation of the COR value then "
            "will set it automatically as estimated "
            "value."
        )
        self._nearOptsWidget.layout().addWidget(self._nearValueCB)

        #    LineEdit position value
        self._qleValueW = qt.QWidget(self._nearOptsWidget)
        self._qleValueW.setLayout(qt.QFormLayout())
        self._nearOptsWidget.layout().addWidget(self._qleValueW)

        self._qleNearPosQLE = qt.QLineEdit("0", self._nearOptsWidget)
        validator = qt.QDoubleValidator(self._qleNearPosQLE)
        self._qleNearPosQLE.setValidator(validator)
        self._qleValueW.layout().addRow(
            "estimated value (in relative):", self._qleNearPosQLE
        )

        # cor_options
        self._corOptsWidget = qt.QWidget(self)
        self._corOptsWidget.setLayout(qt.QHBoxLayout())
        self._corOpts = qt.QLineEdit(self)
        self._corOpts.setToolTip(
            "Options for methods finding automatically the rotation axis position. 'side', 'near_pos' and 'near_width' are already provided by dedicated interface. The parameters are separated by commas and passed as 'name=value'. Mind the semicolon separator (;)."
        )
        self._corOpts.setPlaceholderText("low_pass=1; high_pass=20")
        self._corOptsWidget.layout().addWidget(qt.QLabel("cor advanced options"))
        self._corOptsWidget.layout().addWidget(self._corOpts)
        self._optsWidget.layout().addWidget(self._corOptsWidget)

        # connect signal / slot
        self._qcbPosition.currentIndexChanged.connect(self._modeChanged)
        self._qleNearPosQLE.editingFinished.connect(self._nearValueChanged)
        self._sideCB.currentTextChanged.connect(self._sideChanged)
        self._lockMethodPB.sigLockChanged.connect(self.lockMode)
        self._qbPaddingMode.currentIndexChanged.connect(self._paddingModeChanged)
        self._padding_widget.toggled.connect(self._paddingModeChanged)
        self._corOpts.editingFinished.connect(self._corOptsChanged)

        # set up interface
        self._sideWidget.setVisible(False)
        self.setAxisParams(axis_params)
        self._nearValueCB.setChecked(True)
        self._nearOptsWidget.setHidden(True)

    def getMethodLockPB(self) -> qt.QPushButton:
        return self._lockMethodPB

    def setEstimatedCorValue(self, value):
        if value is not None:
            self._qleNearPosQLE.setText(str(value))
            # note: keep self._axis_params up to date.
            if self._axis_params:
                self._axis_params.estimated_cor = value

    def getEstimatedCor(self):
        try:
            return float(self._qleNearPosQLE.text())
        except ValueError:
            return 0

    def updateAutomaticallyEstimatedCor(self):
        return self._nearValueCB.isChecked()

    def setUpdateAutomaticallyEstimatedCor(self, checked):
        self._nearValueCB.setChecked(checked)

    def setSide(self, side):
        if side is not None:
            idx = self._sideCB.findText(side)
            if idx >= 0:
                self._sideCB.setCurrentIndex(idx)

    def getSide(self):
        return self._sideCB.currentText()

    def _modeChanged(self, *args, **kwargs):
        mode = self.getMode()
        with block_signals(self._qcbPosition):
            with block_signals(self._axis_params):
                self._corOptsWidget.setVisible(
                    mode
                    not in (
                        axis_mode.AxisMode.manual,
                        axis_mode.AxisMode.read,
                    )
                )

                self._padding_widget.setVisible(
                    axis_mode.AXIS_MODE_METADATAS[mode].allows_padding
                )
                if axis_mode.AXIS_MODE_METADATAS[mode].is_lockable:
                    self._lockMethodPB.setVisible(True)
                else:
                    self._lockMethodPB.setVisible(False)
                    self.lockMode(False)

                sides_visible = len(axis_mode.AXIS_MODE_METADATAS[mode].valid_sides) > 0
                self._sideWidget.setVisible(sides_visible)
                if sides_visible is True:
                    self._updateSideVisible(mode)
                self._nearOptsWidget.setVisible(self.getSide() == "near")
                self._axis_params.mode = mode.value
            self._axis_params.changed()
            self.sigModeChanged.emit(mode.value)

    def _updateSideVisible(self, mode: axis_mode.AxisMode):
        mode = axis_mode.AxisMode.from_value(mode)
        if len(axis_mode.AXIS_MODE_METADATAS[mode].valid_sides) == 0:
            return
        else:
            current_value = self._axis_params.side
            with block_signals(self._sideCB):
                self._sideCB.clear()
                values = axis_mode.AXIS_MODE_METADATAS[mode].valid_sides
                for value in values:
                    self._sideCB.addItem(value)
                idx = self._sideCB.findText(current_value)
                if idx == -1:
                    # if side doesn't exists, propose right as default when possible
                    idx = self._sideCB.findText("right")
                if idx >= 0:
                    self._sideCB.setCurrentIndex(idx)
            self._axis_params.side = self.getSide()

    def isModeLock(self):
        return self._lockMethodPB.isLocked()

    def setModeLock(self, mode=None):
        """set a specific mode and lock it.

        :param mode: mode to lock. If None then keep the current mode
        """
        if mode is not None:
            mode = axis_mode.AxisMode.from_value(mode)
        if mode is None and axis_mode.AXIS_MODE_METADATAS[self.getMode()].is_lockable():
            raise ValueError(
                "Unable to lock the current mode is not an automatic algorithm"
            )
        elif (
            mode != self.getMode() and axis_mode.AXIS_MODE_METADATAS[mode].is_lockable()
        ):
            raise ValueError("Unable to lock %s this is not a lockable mode")

        if mode is not None:
            self.setMode(mode)
        if not self._lockMethodPB.isLocked():
            with block_signals(self._lockMethodPB):
                self._lockMethodPB.setLock(True)
        self.lockMode(True)

    def lockMode(self, lock):
        with block_signals(self._lockMethodPB):
            self._lockMethodPB.setLock(lock)
            self._qcbPosition.setEnabled(not lock)

        self.sigLockModeChanged.emit(lock)

    def getMode(self):
        """Return algorithm to use for axis calculation"""
        return axis_mode.AxisMode.from_value(self._qcbPosition.currentText())

    def setMode(self, mode):
        with block_signals(self._qcbPosition):
            index = self._qcbPosition.findText(mode.value)
            if index >= 0:
                self._qcbPosition.setCurrentIndex(index)
            else:
                raise ValueError("Unable to find mode", mode)
            self._lockMethodPB.setVisible(mode not in (axis_mode.AxisMode.manual,))

    def _nearValueChanged(self, *args, **kwargs):
        self._axis_params.estimated_cor = self.getEstimatedCor()

    def _paddingModeChanged(self, *args, **kwargs):
        self._axis_params.padding_mode = self.getPaddingMode()

    def _corOptsChanged(self, *args, **kwargs):
        self._axis_params.extra_cor_options = self.getCorOptions()

    def _sideChanged(self, *args, **kwargs):
        side = self.getSide()
        if side not in ("", None):
            self._axis_params.side = side
        self._nearOptsWidget.setVisible(side == "near")

    def getCorOptions(self):
        return self._corOpts.text()

    def setCorOptions(self, opts: str | None):
        with block_signals(self._axis_params):
            self._corOpts.clear()
            if opts:
                self._corOpts.setText(opts)
                self._corOptsChanged()

    def getPaddingMode(self):
        if self._padding_widget.isChecked():
            return self._qbPaddingMode.currentText()
        else:
            return None

    def setPaddingMode(self, mode):
        index = self._qbPaddingMode.findText(mode)
        if index >= 0:
            self._qbPaddingMode.setCurrentIndex(index)
        self._paddingModeChanged()

    def setAxisParams(self, axis):
        with block_signals(self):
            if self._axis_params is not None:
                self._axis_params.sigChanged.disconnect(self._axis_params_changed)
            self._axis_params = axis
            if self._axis_params.mode in (axis_mode.AxisMode.manual,):
                # those mode cannot be handled by the auto calculation dialog
                self._axis_params.mode = axis_mode.AxisMode.growing_window_radios
            self._axis_params.sigChanged.connect(self._axis_params_changed)
            self._axis_params_changed()
            self._sideChanged()

    def _axis_params_changed(self, *args, **kwargs):
        self.setMode(self._axis_params.mode)
        self.setEstimatedCorValue(self._axis_params.estimated_cor)
        self.setSide(self._axis_params.side)
        sides_visible = (
            len(axis_mode.AXIS_MODE_METADATAS[self._axis_params.mode].valid_sides) > 0
        )
        self._sideWidget.setVisible(sides_visible)
        self._updateSideVisible(mode=self._axis_params.mode)
        self.setPaddingMode(self._axis_params.padding_mode)
        self.setCorOptions(self._axis_params.extra_cor_options)

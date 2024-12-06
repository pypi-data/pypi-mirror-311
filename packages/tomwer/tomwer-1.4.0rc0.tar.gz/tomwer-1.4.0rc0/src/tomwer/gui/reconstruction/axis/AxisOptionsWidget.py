from __future__ import annotations

from silx.gui import qt

from tomwer.synctools.axis import QAxisRP
from tomwer.core.process.reconstruction.axis.params import AxisCalculationInput
from tomwer.gui.utils.qt_utils import block_signals


class AxisOptionsWidget(qt.QWidget):
    """
    GUI to define (advanced) option of the AxisTask

    Used as a tab of the AxisSettingsTabWidget
    """

    def __init__(self, parent, axis_params):
        qt.QWidget.__init__(self, parent=parent)
        assert isinstance(axis_params, QAxisRP)
        self._axis_params = axis_params
        self.setLayout(qt.QVBoxLayout())

        # define common options
        self._commonOpts = qt.QWidget(parent=self)
        self._commonOpts.setLayout(qt.QFormLayout())

        self._qcbDataMode = qt.QComboBox(parent=self)
        for data_mode in AxisCalculationInput:
            # paganin is not managed for sinogram
            self._qcbDataMode.addItem(data_mode.name(), data_mode)
        self._qcbDataMode.hide()

        # add scale option
        self._scaleOpt = qt.QCheckBox(parent=self)
        self._commonOpts.layout().addRow("scale the two images", self._scaleOpt)
        self.layout().addWidget(self._commonOpts)

        # add near options
        self._nearOpts = _AxisNearOptsWidget(parent=self, axis_params=self._axis_params)
        self.layout().addWidget(self._nearOpts)

        # set up
        self.setCalculationInputType(self._axis_params.calculation_input_type)

        # connect signal / slot
        self._scaleOpt.toggled.connect(self._updateScaleOpt)
        self._qcbDataMode.currentIndexChanged.connect(self._updateInputType)
        self._axis_params.sigChanged.connect(self._updateMode)

    def _updateMode(self):
        with block_signals(self):
            index = self._qcbDataMode.findText(
                self._axis_params.calculation_input_type.name()
            )
            if index >= 0:
                self._qcbDataMode.setCurrentIndex(index)

    def _updateScaleOpt(self, *arg, **kwargs):
        self._axis_params.scale_img2_to_img1 = self.isImageScaled()

    def isImageScaled(self):
        return self._scaleOpt.isChecked()

    def _updateInputType(self, *arg, **kwargs):
        self._axis_params.calculation_input_type = self.getCalculationInputType()

    def getCalculationInputType(self, *arg, **kwargs):
        return AxisCalculationInput.from_value(self._qcbDataMode.currentText())

    def setCalculationInputType(self, calculation_type):
        calculation_type = AxisCalculationInput.from_value(calculation_type)
        index_dm = self._qcbDataMode.findText(calculation_type.name())
        self._qcbDataMode.setCurrentIndex(index_dm)

    def setAxisParams(self, axis):
        self._nearOpts.setAxisParams(axis=axis)
        self._axis_params = axis
        with block_signals(self):
            self._scaleOpt.setChecked(axis.scale_img2_to_img1)
            index = self._qcbDataMode.findText(axis.calculation_input_type.name())
            self._qcbDataMode.setCurrentIndex(index)


class _AxisNearOptsWidget(qt.QWidget):
    """GUI dedicated to the near options"""

    def __init__(self, parent, axis_params):
        qt.QWidget.__init__(self, parent=parent)
        assert isinstance(axis_params, QAxisRP)
        self._axis_params = axis_params

        self.setLayout(qt.QFormLayout())

        self._stdMaxOpt = qt.QCheckBox(parent=self)
        self.layout().addRow("look at max standard deviation", self._stdMaxOpt)

        self._nearWX = qt.QSpinBox(parent=self)
        self._nearWX.setMinimum(1)
        self._nearWX.setValue(5)
        self.layout().addRow("window size", self._nearWX)

        self._fineStepX = qt.QDoubleSpinBox(parent=self)
        self._fineStepX.setMinimum(0.05)
        self._fineStepX.setSingleStep(0.05)
        self._fineStepX.setMaximum(1.0)
        self.layout().addRow("fine step x", self._fineStepX)

        # connect signal / Slot
        self._stdMaxOpt.toggled.connect(self._lookForStxMaxChanged)
        self._nearWX.valueChanged.connect(self._windowSizeChanged)
        self._fineStepX.valueChanged.connect(self._fineStepXChanged)

    def _lookForStxMaxChanged(self, *args, **kwargs):
        self._axis_params.look_at_stdmax = self.isLookAtStdMax()

    def isLookAtStdMax(self) -> bool:
        """

        :return: is the option for looking at max standard deviation is
                 activated
        """
        return self._stdMaxOpt.isChecked()

    def _windowSizeChanged(self, *args, **kwargs):
        self._axis_params.near_wx = self.getWindowSize()

    def getWindowSize(self) -> int:
        """

        :return: window size for near search
        """
        return self._nearWX.value()

    def _fineStepXChanged(self, *args, **kwargs):
        self._axis_params.fine_step_x = self.getFineStepX()

    def getFineStepX(self) -> float:
        """

        :return: fine step x for near calculation
        """
        return self._fineStepX.value()

    def setAxisParams(self, axis: QAxisRP):
        """

        :param axis: axis to edit
        """
        with block_signals(self):
            self._axis_params = axis
            self._stdMaxOpt.setChecked(axis.look_at_stdmax)
            self._nearWX.setValue(axis.near_wx)
            self._fineStepX.setValue(axis.fine_step_x)

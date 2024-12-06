import pytest

from tomwer.gui.reconstruction.axis.AxisSettingsWidget import AxisSettingsTabWidget
from tomwer.synctools.axis import QAxisRP
from tomwer.tests.utils import skip_gui_test
from tomwer.tests.conftest import qtapp  # noqa F401


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
def test_get_nabu_cor_opts(qtapp):  # noqa F811
    axis_params = QAxisRP()
    widget = AxisSettingsTabWidget(recons_params=axis_params)
    assert axis_params.get_nabu_cor_options_as_str() == "side='right'"
    widget._calculationWidget._corOpts.setText("low_pass=2")
    widget._calculationWidget._corOpts.editingFinished.emit()
    assert axis_params.get_nabu_cor_options_as_str() == "side='right' ; low_pass=2"
    widget._calculationWidget._corOpts.setText("low_pass=2 ; high_pass=10")
    widget._calculationWidget._corOpts.editingFinished.emit()
    assert axis_params.get_nabu_cor_options_as_str() == (
        "side='right' ; low_pass=2 ; high_pass=10"
    )
    widget._calculationWidget._sideCB.setCurrentText("left")
    widget._calculationWidget._corOpts.editingFinished.emit()
    assert (
        axis_params.get_nabu_cor_options_as_str()
        == "side='left' ; low_pass=2 ; high_pass=10"
    )

# coding: utf-8
from __future__ import annotations

import os
import shutil
import tempfile
import unittest

import h5py
from tomoscan.io import get_swmr_mode
import numpy
from silx.io.utils import h5py_read_dataset

from tomwer.core.process.reconstruction.axis.mode import AxisMode
from tomwer.core.process.reconstruction.axis.params import AxisRP
from tomwer.core.process.task import Task
from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.utils.scanutils import MockEDF, MockNXtomo

from ..reconstruction.axis.axis import AxisTask


class TestAxisIO(unittest.TestCase):
    """Test inputs and outputs types of the handler functions"""

    @staticmethod
    def _random_calc(scan):
        return numpy.random.random()

    def setUp(self):
        self.scan_folder = tempfile.mkdtemp()

        self.scan = MockEDF.mockScan(
            scanID=self.scan_folder, nRadio=10, nRecons=1, nPagRecons=4, dim=10
        )
        self.recons_params = AxisRP()

        # set the axis url to be used
        projections = self.scan.projections
        urls = list(projections.values())
        self.scan.axis_params = AxisRP()
        self.scan.axis_params.axis_url_1 = urls[0]
        self.scan.axis_params.axis_url_2 = urls[1]

    def tearDown(self):
        shutil.rmtree(self.scan_folder)

    def testInputOutput(self):
        """Test that io using TomoBase instance work"""
        for input_type in (dict, TomwerScanBase):
            for serialize_output_data in (True, False):
                with self.subTest(
                    serialize_output_data=serialize_output_data,
                    input_type=input_type,
                ):
                    input_obj = self.scan
                    if input_obj is dict:
                        input_obj = input_obj.to_dict()
                    axis_process = AxisTask(
                        inputs={
                            "axis_params": self.recons_params,
                            "data": input_obj,
                            "serialize_output_data": serialize_output_data,
                        }
                    )

                    # patch the axis process
                    axis_process._CALCULATIONS_METHODS[AxisMode.centered] = (
                        TestAxisIO._random_calc
                    )

                    axis_process.run()
                    out = axis_process.outputs.data
                    if serialize_output_data:
                        self.assertTrue(isinstance(out, dict))
                    else:
                        self.assertTrue(isinstance(out, TomwerScanBase))


class TestAxis(unittest.TestCase):
    """Test the axis process"""

    def setUp(self):
        self.recons_params = AxisRP()
        self.recons_params.mode = "centered"

    def test_process_saved_edf(self):
        """Test that if process is called, the tomwer.h5 file is created
        and is correctly saving information regarding the center of position
        """
        self.tempdir = tempfile.mkdtemp()
        mock = MockEDF(scan_path=self.tempdir, n_radio=10, n_ini_radio=10)
        scan = EDFTomoScan(mock.scan_path)
        self.recons_params.mode = "centered"
        axis_process = AxisTask(
            inputs={
                "data": scan,
                "axis_params": self.recons_params,
                "serialize_output_data": False,
            }
        )

        axis_process.run()
        self.assertTrue(os.path.exists(scan.process_file))

        with h5py.File(scan.process_file, "r", swmr=get_swmr_mode()) as h5f:
            self.assertTrue("entry" in h5f)
            self.assertTrue("tomwer_process_0" in h5f["entry"])
            group_axis = h5f["entry"]["tomwer_process_0"]
            self.assertTrue("configuration" in group_axis)
            self.assertTrue("program" in group_axis)
            self.assertTrue("results" in group_axis)
            self.assertTrue("center_of_rotation" in group_axis["results"])
            axis_value = h5py_read_dataset(group_axis["results"]["center_of_rotation"])

        processes = Task.get_processes_frm_type(
            process_file=scan.process_file, process_type=AxisTask, entry="entry"
        )
        self.assertEqual(len(processes), 1)
        self.assertEqual(processes[0].results["center_of_rotation"], axis_value)

    def test_process_saved_hdf5(self):
        """Test that if process is called, the tomwer.h5 file is created
        and is correctly saving information regarding the center of position
        """
        self.tempdir = tempfile.mkdtemp()
        dim = 10
        mock = MockNXtomo(
            scan_path=self.tempdir, n_proj=10, n_ini_proj=10, scan_range=180, dim=dim
        )
        mock.add_alignment_radio(index=10, angle=90)
        mock.add_alignment_radio(index=10, angle=0)
        scan = mock.scan
        self.recons_params.mode = "centered"

        # check data url take
        axis_process = AxisTask(
            inputs={
                "data": scan,
                "axis_params": self.recons_params,
                "serialize_output_data": False,
            }
        )
        axis_process.run()
        # make sure center of position has been computed
        self.assertTrue(os.path.exists(scan.process_file))

        with h5py.File(scan.process_file, "r", swmr=get_swmr_mode()) as h5f:
            self.assertTrue("entry" in h5f)
            self.assertTrue("tomwer_process_0" in h5f["entry"])
            group_axis = h5f["entry"]["tomwer_process_0"]
            self.assertTrue("configuration" in group_axis)
            self.assertTrue("program" in group_axis)
            self.assertTrue("results" in group_axis)
            self.assertTrue("center_of_rotation" in group_axis["results"])
            axis_value = h5py_read_dataset(group_axis["results"]["center_of_rotation"])
        self.assertTrue(-dim / 2 <= axis_value <= dim / 2)
        processes = Task.get_processes_frm_type(
            process_file=scan.process_file, process_type=AxisTask
        )
        self.assertEqual(len(processes), 1)
        self.assertEqual(processes[0].results["center_of_rotation"], axis_value)


class TestAxisRP(unittest.TestCase):
    """Test the class used for AxisProcess configuration"""

    def setUp(self):
        self.axis_rp = AxisRP()
        self.tmp_folder = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp_folder)


class TestSinogramAlgorithm(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp_folder = tempfile.mkdtemp()
        dim = 512
        self.scan = MockNXtomo(
            scan_path=self.tmp_folder,
            n_proj=10,
            n_ini_proj=10,
            create_ini_dark=True,
            create_final_flat=True,
            scan_range=360,
            dim=dim,
        ).scan

    def tearDown(self):
        shutil.rmtree(self.tmp_folder)

    def test_growing_window_sinogram(self):
        recons_params = AxisRP()
        axis_process = AxisTask(
            inputs={"axis_params": recons_params, "data": self.scan}
        )
        recons_params.mode = AxisMode.growing_window_sinogram
        recons_params.use_sinogram = True
        recons_params.sinogram_subsampling = 1
        axis_process.run()

    def test_sliding_window(self):
        recons_params = AxisRP()
        axis_process = AxisTask(
            inputs={
                "axis_params": recons_params,
                "data": self.scan,
                "serialize_output_data": False,
            }
        )
        recons_params.mode = AxisMode.sliding_window_sinogram
        recons_params.side = "left"
        recons_params.sinogram_subsampling = 1
        recons_params.use_sinogram = True
        axis_process.run()

    def test_sino_coarse_to_fine(self):
        recons_params = AxisRP()
        axis_process = AxisTask(
            inputs={
                "axis_params": recons_params,
                "data": self.scan,
                "serialize_output_data": False,
            }
        )
        recons_params.mode = AxisMode.sino_coarse_to_fine
        recons_params.sinogram_subsampling = 1
        recons_params.sinogram_line = 2
        axis_process.run()

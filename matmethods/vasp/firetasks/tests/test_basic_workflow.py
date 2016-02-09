import os

from monty.os.path import which

from fireworks import LaunchPad, FWorker
from fireworks.core.rocket_launcher import launch_rocket, rapidfire
from fireworks.utilities.fw_serializers import load_object
from matmethods.vasp.examples.basic_vasp_workflows import get_basic_workflow
from matmethods.vasp.firetasks.tests.vasp_fake import RunVaspFake
from matmethods.vasp.firetasks.write_inputs import WriteVaspFromIOSet, WriteVaspFromPMGObjects, ModifyIncar
from pymatgen import IStructure, Lattice
from pymatgen.io.vasp import Incar, Poscar, Potcar, Kpoints
from pymatgen.io.vasp.sets import MPVaspInputSet

import unittest

__author__ = 'Anubhav Jain <ajain@lbl.gov>'

module_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
VASP_CMD = "vasp"

class FakeWorkflowTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.lp = LaunchPad(name="fireworks_matmethods_test")

        coords = [[0, 0, 0], [0.75, 0.5, 0.75]]
        lattice = Lattice([[3.8401979337, 0.00, 0.00],
                                [1.9200989668, 3.3257101909, 0.00],
                                [0.00, -2.2171384943, 3.1355090603]])
        cls.struct_si = IStructure(lattice, ["Si"] * 2, coords)

        cls.module_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        cls.scratch_dir = os.path.join(cls.module_dir, "scratch")
        cls.reference_dir = os.path.join(cls.module_dir, "reference_files")

    @classmethod
    def tearDownClass(cls):
        cls.lp.reset("", require_password=False)

    def setUp(self):
        os.chdir(self.scratch_dir)

    def tearDown(self):
        pass

    def test_relax_workflow(self):
        # add the workflow
        vis = MPVaspInputSet()
        structure = self.struct_si
        my_wf = get_basic_workflow(structure, vis, VASP_CMD, fake_dir=os.path.join(self.reference_dir, "Si_structure_optimization"))
        self.lp.add_wf(my_wf)

        # run the workflow
        rapidfire(self.lp)

        # confirm results
        # TODO: add some confirmation stuff
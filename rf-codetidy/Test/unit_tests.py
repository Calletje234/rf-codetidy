import unittest
import os
import shutil

from Add_spacing.get_section_order import GetOrder
from Add_spacing.init_Spacing import StartSpacing

from robot.parsing import get_model


class AddDocSectionTestCase(unittest.TestCase):
    def setUp(self):
        src = "C:\\Users\\BEEKC02\\rf-codetidy\\Test\\Robot_file\\Zelfmelder.robot"
        self.check_file = os.path.isfile(src)
        self.assertTrue(self.check_file)

    def tearDown(self):
        src = "C:\\Users\\BEEKC02\\rf-codetidy\\Test\\Robot_file\\Zelfmelder - Backup.robot"
        dst = "C:\\Users\\BEEKC02\\rf-codetidy\\Test\\Robot_file\\Zelfmelder.robot"
        os.remove(dst)
        shutil.copyfile(src, dst)


class AddSpacingTestCase(unittest.TestCase):
    def setUp(self):
        src = "C:\\Users\\BEEKC02\\rf-codetidy\\Test\\Robot_file\\Zelfmelder.robot"
        self.check_file = os.path.isfile(src)
        self.assertTrue(self.check_file)
        self.model = get_model(src)

    def test_model(self):
        self.initiator = StartSpacing(self.model)

    def tearDown(self):
        src = "C:\\Users\\BEEKC02\\rf-codetidy\\Test\\Robot_file\\Zelfmelder - Backup.robot"
        dst = "C:\\Users\\BEEKC02\\rf-codetidy\\Test\\Robot_file\\Zelfmelder.robot"
        os.remove(dst)
        shutil.copyfile(src, dst)

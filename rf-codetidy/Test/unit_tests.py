import unittest
import os
import shutil
import filecmp
import subprocess
import time

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


class RunCommandLine(unittest.TestCase):
    def setUp(self):
        self.src = "C:\\Users\\BEEKC02\\rf-codetidy\\Test\\Robot_file\\Zelfmelder - Backup.robot"
        self.dst = "C:\\Users\\BEEKC02\\rf-codetidy\\Test\\Robot_file\\Zelfmelder.robot"
        self.alt_file = "C:\\Users\\BEEKC02\\rf-codetidy\\Test\\Robot_file\\Zelfmelder - unaltered.robot"
        self.msg = "Opening a command line"

    def test_file_run(self):
        print(self.msg)
        subprocess.call("C:\\Users\\BEEKC02\\rf-codetidy\\Test\\Robot_file\\commands.bat")
        time.sleep(10)

    def test_model(self):
        self.assertTrue(filecmp.cmp(self.src, self.alt_file, shallow=False))

    def tearDown(self):
        os.remove(self.dst)
        shutil.copyfile(self.src, self.dst)


class AddSpacingTestCase(unittest.TestCase):
    def setUp(self):
        self.src = "C:\\Users\\BEEKC02\\rf-codetidy\\Test\\Robot_file\\Zelfmelder - Backup.robot"
        self.dst = "C:\\Users\\BEEKC02\\rf-codetidy\\Test\\Robot_file\\Zelfmelder.robot"
        self.alt_file = "C:\\Users\\BEEKC02\\rf-codetidy\\Test\\Robot_file\\Zelfmelder - unaltered.robot"
        self.check_file = os.path.isfile(self.src)
        self.assertTrue(self.check_file)
        self.model = get_model(self.src)
        self.sorter = GetOrder()

    def test_model(self):
        self.initiator = StartSpacing(self.src)
        self.sorter.visit(self.model)
        self.assertFalse(filecmp.cmp(self.src, self.alt_file))

    def tearDown(self):
        os.remove(self.dst)
        shutil.copyfile(self.src, self.dst)
        shutil.copyfile(self.src, self.alt_file)

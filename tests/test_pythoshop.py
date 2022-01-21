import sys, os
from time import sleep
sys.path.insert(0, './src')

import unittest
from pythoshop import Pythoshop

class TestPythoshop(unittest.TestCase):

    def setUp(self):
        self.psd_path = os.path.abspath("./tests/resources/pythoshop-example-template.psd")
        self.result_path = os.path.abspath("./tests/resources/temporary_result")
        self.result_name = "pythoshop-example.jpg"
        self.result_full_path = os.path.join(self.result_path, self.result_name)

        if not os.path.exists(self.result_path):
            os.mkdir(self.result_path)

        sleep(1)
        self.pythoshop = Pythoshop()

    def tearDown(self):
        self.pythoshop.closePhotoshop()

        if os.path.exists(self.result_full_path):
            os.remove(self.result_full_path)

        if os.path.exists(self.result_path):
            os.rmdir(self.result_path)

    def test_openPSD(self):
        opened = self.pythoshop.openPSDFile(self.psd_path)

        if opened:
            self.pythoshop.closePSDFile()

        self.assertTrue(opened)

    def test_updateTitleLayer(self):
        updatedTitle = False

        opened = self.pythoshop.openPSDFile(self.psd_path)

        if opened:
            updatedTitle = self.pythoshop.updateTitleLayer("example_title", "Testing")
            self.pythoshop.closePSDFile()

        self.assertTrue(updatedTitle)

    def test_exportJPEG(self):
        exported = False

        opened = self.pythoshop.openPSDFile(self.psd_path)

        if opened:
            updatedTitle = self.pythoshop.updateTitleLayer("example_title", "Testing")

            if updatedTitle:
                exported = self.pythoshop.exportJPEG(self.result_name, self.result_path)

            self.pythoshop.closePSDFile()

        self.assertTrue(exported)

if __name__ == '__main__':
    unittest.main()

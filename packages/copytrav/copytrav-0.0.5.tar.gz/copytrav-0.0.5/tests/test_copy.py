"""Testing the copy functions. Good example usage."""
import os
import shutil
import tempfile
import unittest
from copytrav import copy

class TestCanCopy(unittest.TestCase):
    """Test can copy."""
    def setUp(self):
        self.tdir = tempfile.mkdtemp()
    def test_copy_even_more_data(self):
        """Tests copying data/two/even_more_data"""
        copy("copytrav.data", "two/even_more_data", self.tdir)
        self.assertTrue(os.path.exists(os.path.join(self.tdir, "even_more_data")))
        self.assertTrue(os.path.exists(os.path.join(self.tdir, "even_more_data", "data3.rst")))
        self.assertTrue(os.path.exists(os.path.join(self.tdir, "even_more_data", "data3.txt")))
    def test_copy_just_module(self):
        """Tests copying just the module."""
        copy("copytrav.data", dst=self.tdir)
        one = os.path.join(self.tdir, "data", "one")
        two = os.path.join(self.tdir, "data", "two")
        emd = os.path.join(two, "even_more_data")
        self.assertTrue(os.path.exists(os.path.join(one, "data1.rst")))
        self.assertTrue(os.path.exists(os.path.join(one, "data1.txt")))
        self.assertTrue(os.path.exists(os.path.join(two, "data2.txt")))
        self.assertTrue(os.path.exists(os.path.join(two, "data2.rst")))
        self.assertTrue(os.path.exists(os.path.join(emd, "data3.txt")))
        self.assertTrue(os.path.exists(os.path.join(emd, "data3.rst")))
    def test_copy_one(self):
        """Tests copying just data/one"""
        copy("copytrav.data", "one", self.tdir)
        one = os.path.join(self.tdir, "one")
        self.assertTrue(os.path.exists(os.path.join(one, "data1.rst")))
        self.assertTrue(os.path.exists(os.path.join(one, "data1.txt")))
    def test_copy_notop(self):
        """Tests the notop ability."""
        copy("copytrav.data", "one", self.tdir, True)
        self.assertTrue(os.path.exists(os.path.join(self.tdir, "data1.rst")))
        self.assertTrue(os.path.exists(os.path.join(self.tdir, "data1.txt")))
    def test_copy_two(self):
        """Tests copying just data/two"""
        copy("copytrav.data", "two", self.tdir)
        two = os.path.join(self.tdir, "two")
        emd = os.path.join(two, "even_more_data")
        self.assertTrue(os.path.exists(os.path.join(two, "data2.txt")))
        self.assertTrue(os.path.exists(os.path.join(two, "data2.rst")))
        self.assertTrue(os.path.exists(os.path.join(emd, "data3.txt")))
        self.assertTrue(os.path.exists(os.path.join(emd, "data3.rst")))
    def test_copy_single_file(self):
        """Tests copying a single file."""
        copy("copytrav.data", "two/even_more_data/data3.rst", self.tdir)
        self.assertTrue(os.path.exists(os.path.join(self.tdir, "data3.rst")))
    def test_copy_without_dst(self):
        """Tests copying a single file without supplying a dst."""
        self.tdir = copy("copytrav.data", "two/even_more_data/data3.rst")
        self.assertTrue(os.path.exists(os.path.join(self.tdir, "data3.rst")))
    def tearDown(self):
        shutil.rmtree(self.tdir)

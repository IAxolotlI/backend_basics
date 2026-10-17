import unittest
from processing import preprocessing


class TestPreprocessing(unittest.TestCase):
    def test_warm_clothes(self):
        self.assertTrue(preprocessing.warm_clothes(-1))
        self.assertFalse(preprocessing.warm_clothes(1))

    def test_expensive(self):
        self.assertTrue(preprocessing.expensive(101))
        self.assertFalse(preprocessing.expensive(100))

    def test_normalize(self):
        self.assertEqual(preprocessing.strip_description("  "), "unknown")
        self.assertEqual(preprocessing.strip_description(None), "unknown")
        self.assertEqual(preprocessing.strip_description("rain"), "rain")


if __name__ == "__main__":
    unittest.main()
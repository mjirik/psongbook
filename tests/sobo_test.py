import unittest
import sobo
import sobo.psongbook
import os.path as op


class MyTestCase(unittest.TestCase):
    def test_generate_example(self):
        sobo.psongbook.generate_example()

        self.assertTrue(op.exists("saxana.txt"))

    def test_something(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()

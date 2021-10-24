import unittest

from prime import is_prime


class Tests(unittest.TestCase):
    def test_1(self):
        self.assertFalse(is_prime(1))

    def test_2(self):
        self.assertTrue(is_prime(2))

    def test_4(self):
        self.assertFalse(is_prime(25))

    def test_8(self):
        self.assertFalse(is_prime(8))


if __name__ == '__main__':
    unittest.main()

import unittest
from spacecases_common import get_best_condition_idx


class TestGetBestConditionIdx(unittest.TestCase):
    def test_float_too_low(self):
        with self.assertRaises(ValueError):
            get_best_condition_idx(-100)

    def test_float_too_high(self):
        with self.assertRaises(ValueError):
            get_best_condition_idx(1.5)

    def test_normal_float(self):
        for input, expected in [
            (0.05, 0),
            (0.10, 1),
            (0.18, 2),
            (0.39, 3),
            (0.69, 4),
        ]:
            self.assertEqual(get_best_condition_idx(input), expected)

    def test_border_float(self):
        for input, expected in [
            (0.0, 0),
            (0.07, 1),
            (0.15, 2),
            (0.38, 3),
            (0.45, 4),
            (1.0, 4),
        ]:
            self.assertEqual(get_best_condition_idx(input), expected)


if __name__ == "__main__":
    unittest.main()

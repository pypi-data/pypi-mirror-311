import unittest
from spacecases_common import get_all_conditions_for_float_range, Condition


class TestGetAllConditionsForFloatRange(unittest.TestCase):
    def test_invalid_range(self):
        with self.assertRaises(ValueError):
            get_all_conditions_for_float_range(0.5, 0.4)
        with self.assertRaises(ValueError):
            get_all_conditions_for_float_range(0.0, 0.0)

    def test_full_range(self):
        self.assertEqual(
            get_all_conditions_for_float_range(0.0, 1.0),
            [
                Condition.FACTORY_NEW,
                Condition.MINIMAL_WEAR,
                Condition.FIELD_TESTED,
                Condition.WELL_WORN,
                Condition.BATTLE_SCARRED,
            ],
        )

    def test_single_condition_ranges(self):
        for min_float, max_float, expected in [
            (0.01, 0.06, Condition.FACTORY_NEW),
            (0.00, 0.06, Condition.FACTORY_NEW),
            (0.05, 0.07, Condition.FACTORY_NEW),
            (0.00, 0.07, Condition.FACTORY_NEW),
            (0.08, 0.14, Condition.MINIMAL_WEAR),
            (0.07, 0.08, Condition.MINIMAL_WEAR),
            (0.08, 0.15, Condition.MINIMAL_WEAR),
            (0.07, 0.15, Condition.MINIMAL_WEAR),
            (0.16, 0.27, Condition.FIELD_TESTED),
            (0.15, 0.16, Condition.FIELD_TESTED),
            (0.16, 0.38, Condition.FIELD_TESTED),
            (0.15, 0.38, Condition.FIELD_TESTED),
            (0.15, 0.18, Condition.FIELD_TESTED),
            (0.39, 0.44, Condition.WELL_WORN),
            (0.38, 0.39, Condition.WELL_WORN),
            (0.39, 0.45, Condition.WELL_WORN),
            (0.38, 0.45, Condition.WELL_WORN),
            (0.46, 0.85, Condition.BATTLE_SCARRED),
            (0.45, 0.46, Condition.BATTLE_SCARRED),
            (0.46, 1.00, Condition.BATTLE_SCARRED),
            (0.45, 1.00, Condition.BATTLE_SCARRED),
        ]:
            self.assertEqual(
                get_all_conditions_for_float_range(min_float, max_float), [expected]
            )

    def test_multiple_condition_ranges(self):
        for min_float, max_float, expected in [
            (0.05, 0.10, [Condition.FACTORY_NEW, Condition.MINIMAL_WEAR]),
            (0.12, 0.18, [Condition.MINIMAL_WEAR, Condition.FIELD_TESTED]),
            (0.35, 0.42, [Condition.FIELD_TESTED, Condition.WELL_WORN]),
            (0.40, 0.50, [Condition.WELL_WORN, Condition.BATTLE_SCARRED]),
        ]:
            self.assertEqual(
                get_all_conditions_for_float_range(min_float, max_float), expected
            )


if __name__ == "__main__":
    unittest.main()

import math
import unittest

from model import MODEL, PREDICTOR_IDS, predict, validate_plausibility


class ModelSpecificationTests(unittest.TestCase):
    def test_locked_specification(self):
        self.assertEqual(MODEL["intercept"], -3.26185495025)
        self.assertEqual(
            PREDICTOR_IDS,
            ("age", "crp", "lymphocyte", "neutrophil", "nihss", "end", "cerebral_edema"),
        )

    def test_worked_examples(self):
        examples = [
            (
                {"age": 70, "crp": 10, "lymphocyte": 1.5, "neutrophil": 7.5, "nihss": 15, "end": 0, "cerebral_edema": 0},
                -0.0948823706830001,
                0.47629718703395163,
            ),
            (
                {"age": 80, "crp": 50, "lymphocyte": 0.8, "neutrophil": 12, "nihss": 22, "end": 1, "cerebral_edema": 1},
                3.2742311243513997,
                0.9635341289049191,
            ),
            (
                {"age": 55, "crp": 3, "lymphocyte": 2.2, "neutrophil": 5, "nihss": 8, "end": 0, "cerebral_edema": 0},
                -1.0506541780704,
                0.25909950046024804,
            ),
        ]
        for values, expected_lp, expected_probability in examples:
            lp, probability = predict(values)
            self.assertTrue(math.isclose(lp, expected_lp, abs_tol=1e-12))
            self.assertTrue(math.isclose(probability, expected_probability, abs_tol=1e-12))

    def test_binary_coding_is_enforced(self):
        values = {"age": 70, "crp": 10, "lymphocyte": 1.5, "neutrophil": 7.5, "nihss": 15, "end": 2, "cerebral_edema": 0}
        with self.assertRaises(ValueError):
            predict(values)

    def test_missing_value_is_reported(self):
        values = {"age": None, "crp": 10, "lymphocyte": 1.5, "neutrophil": 7.5, "nihss": 15, "end": 0, "cerebral_edema": 0}
        self.assertIn("Age is required.", validate_plausibility(values))


if __name__ == "__main__":
    unittest.main()

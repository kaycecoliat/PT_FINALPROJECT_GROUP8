import unittest

from tests import cases


class TestValidation(unittest.TestCase):
    def test_invalid_inputs_are_rejected_with_a_clear_message(self):
        for case in cases.VALIDATION_CASES:
            with self.subTest(case["id"], title=case["title"]):
                self.assertEqual(cases.run_validation_case(case), case["expected_error"])

    def test_valid_input_is_accepted(self):
        results = cases.backend.run_all(50, cases.DEFAULT_QUEUE, 0, 199, "Left")
        self.assertEqual(set(results), {"FCFS", "SSTF", "SCAN"})


if __name__ == "__main__":
    unittest.main()

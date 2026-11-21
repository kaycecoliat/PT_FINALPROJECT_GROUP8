import unittest

from tests import cases


class TestSCAN(unittest.TestCase):
    def test_sequence_and_total(self):
        for case in cases.cases_for("SCAN"):
            with self.subTest(case["id"], title=case["title"]):
                result = cases.run_algorithm_case(case)
                self.assertEqual(result["sequence"], case["expected_sequence"])
                self.assertEqual(result["total"], case["expected_total"])

    def test_boundary_stop_is_marked(self):
        result = cases.backend.scan(53, cases.TEXTBOOK_QUEUE, 0, 199, "Left")
        boundaries = [s for s in result["steps"] if s["type"] == "Boundary"]
        self.assertEqual(len(boundaries), 1)
        self.assertEqual(boundaries[0]["to"], 0)

    def test_direction_changes_the_result(self):
        left = cases.backend.scan(53, cases.TEXTBOOK_QUEUE, 0, 199, "Left")["total"]
        right = cases.backend.scan(53, cases.TEXTBOOK_QUEUE, 0, 199, "Right")["total"]
        self.assertNotEqual(left, right)


if __name__ == "__main__":
    unittest.main()

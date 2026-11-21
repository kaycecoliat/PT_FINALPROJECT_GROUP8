import unittest

from tests import cases


class TestFCFS(unittest.TestCase):
    def test_sequence_and_total(self):
        for case in cases.cases_for("FCFS"):
            with self.subTest(case["id"], title=case["title"]):
                result = cases.run_algorithm_case(case)
                self.assertEqual(result["sequence"], case["expected_sequence"])
                self.assertEqual(result["total"], case["expected_total"])

    def test_requests_are_served_in_arrival_order(self):
        result = cases.backend.fcfs(53, cases.TEXTBOOK_QUEUE)
        self.assertEqual(result["sequence"][1:], cases.TEXTBOOK_QUEUE)

    def test_step_distances_add_up_to_total(self):
        result = cases.backend.fcfs(53, cases.TEXTBOOK_QUEUE)
        self.assertEqual(sum(s["movement"] for s in result["steps"]), result["total"])


if __name__ == "__main__":
    unittest.main()

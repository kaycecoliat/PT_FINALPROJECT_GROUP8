import unittest

from tests import cases


class TestSSTF(unittest.TestCase):
    def test_sequence_and_total(self):
        for case in cases.cases_for("SSTF"):
            with self.subTest(case["id"], title=case["title"]):
                result = cases.run_algorithm_case(case)
                self.assertEqual(result["sequence"], case["expected_sequence"])
                self.assertEqual(result["total"], case["expected_total"])

    def test_never_more_movement_than_fcfs_on_textbook_example(self):
        sstf = cases.backend.sstf(53, cases.TEXTBOOK_QUEUE)["total"]
        fcfs = cases.backend.fcfs(53, cases.TEXTBOOK_QUEUE)["total"]
        self.assertLess(sstf, fcfs)

    def test_every_request_is_served_exactly_once(self):
        result = cases.backend.sstf(53, cases.TEXTBOOK_QUEUE)
        self.assertEqual(sorted(result["sequence"][1:]), sorted(cases.TEXTBOOK_QUEUE))


if __name__ == "__main__":
    unittest.main()

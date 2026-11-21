"""Test case data shared by the unit tests and the report generator.

Every EXPECTED value was worked out by hand (see docs/TEST_REPORT.md),
independently of the program's output.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

import backend  # noqa: E402

TEXTBOOK_QUEUE = [98, 183, 37, 122, 14, 124, 65, 67]
DEFAULT_QUEUE = [82, 170, 43, 140, 24, 16, 190]


def _case(cid, title, algorithm, head, queue, low, high, direction, sequence, total):
    return {
        "id": cid, "title": title, "algorithm": algorithm, "head": head,
        "queue": queue, "min": low, "max": high, "direction": direction,
        "expected_sequence": sequence, "expected_total": total,
    }


ALGORITHM_CASES = [
    _case("TC-01", "FCFS, textbook example", "FCFS", 53, TEXTBOOK_QUEUE, 0, 199, "Left",
          [53, 98, 183, 37, 122, 14, 124, 65, 67], 640),
    _case("TC-02", "SSTF, textbook example", "SSTF", 53, TEXTBOOK_QUEUE, 0, 199, "Left",
          [53, 65, 67, 37, 14, 98, 122, 124, 183], 236),
    _case("TC-03", "SCAN moving left, textbook example", "SCAN", 53, TEXTBOOK_QUEUE, 0, 199, "Left",
          [53, 37, 14, 0, 65, 67, 98, 122, 124, 183], 236),
    _case("TC-04", "SCAN moving right, textbook example", "SCAN", 53, TEXTBOOK_QUEUE, 0, 199, "Right",
          [53, 65, 67, 98, 122, 124, 183, 199, 37, 14], 331),
    _case("TC-05", "FCFS, default queue (head 50)", "FCFS", 50, DEFAULT_QUEUE, 0, 199, "Left",
          [50, 82, 170, 43, 140, 24, 16, 190], 642),
    _case("TC-06", "SSTF, default queue (head 50)", "SSTF", 50, DEFAULT_QUEUE, 0, 199, "Left",
          [50, 43, 24, 16, 82, 140, 170, 190], 208),
    _case("TC-07", "SCAN moving left, default queue", "SCAN", 50, DEFAULT_QUEUE, 0, 199, "Left",
          [50, 43, 24, 16, 0, 82, 140, 170, 190], 240),
    _case("TC-08", "SCAN moving right, default queue", "SCAN", 50, DEFAULT_QUEUE, 0, 199, "Right",
          [50, 82, 140, 170, 190, 199, 43, 24, 16], 332),
    _case("TC-09", "Edge: SCAN left with head already at cylinder 0", "SCAN", 0, [10, 20], 0, 199, "Left",
          [0, 10, 20], 20),
    _case("TC-10", "Edge: every request equals the head position (FCFS)", "FCFS", 100, [100, 100], 0, 199, "Left",
          [100, 100, 100], 0),
    _case("TC-11", "Edge: SCAN right, all requests ahead (no reversal)", "SCAN", 10, [20, 50], 0, 199, "Right",
          [10, 20, 50], 40),
    _case("TC-12", "Edge: SSTF tie goes to the earlier request", "SSTF", 50, [40, 60], 0, 199, "Left",
          [50, 40, 60], 30),
]


def cases_for(algorithm):
    return [c for c in ALGORITHM_CASES if c["algorithm"] == algorithm]


def run_algorithm_case(case):
    results = backend.run_all(case["head"], case["queue"], case["min"], case["max"], case["direction"])
    return results[case["algorithm"]]


VALIDATION_CASES = [
    {"id": "TC-13", "title": "Minimum equal to maximum", "head": 5, "queue": [1],
     "min": 10, "max": 10, "direction": "Left",
     "expected_error": "Minimum cylinder must be less than maximum."},
    {"id": "TC-14", "title": "Head position outside the disk", "head": 300, "queue": [98, 183],
     "min": 0, "max": 199, "direction": "Left",
     "expected_error": "Initial head position is outside disk range."},
    {"id": "TC-15", "title": "A request outside the disk", "head": 50, "queue": [20, 250],
     "min": 0, "max": 199, "direction": "Left",
     "expected_error": "Request 250 is outside the disk range."},
    {"id": "TC-16", "title": "Empty request queue", "head": 50, "queue": [],
     "min": 0, "max": 199, "direction": "Left",
     "expected_error": "Please enter at least one disk request."},
    {"id": "TC-17", "title": "Invalid SCAN direction", "head": 50, "queue": [20],
     "min": 0, "max": 199, "direction": "Up",
     "expected_error": "Invalid SCAN direction."},
]


def run_validation_case(case):
    try:
        backend.run_all(case["head"], case["queue"], case["min"], case["max"], case["direction"])
    except ValueError as error:
        return str(error)
    return "no error raised"

# Track Attack - Test Report

| | |
|---|---|
| **Date** | November 18, 2026 |
| **Python** | 3.12.3 |
| **Command** | `python -m unittest discover -s tests -v` |
| **Scope** | `src/backend.py` (algorithms, input validation, accounts) |
| **Result** | **41 tests run, 41 passed, 0 failed** |

## 1. Summary by area

| Test file | Area | Tests | Passed |
|-----------|------|------:|-------:|
| `tests/test_algorithms.py` | FCFS | 4 | 4 |
| `tests/test_algorithms.py` | SSTF | 4 | 4 |
| `tests/test_algorithms.py` | SCAN | 6 | 6 |
| `tests/test_algorithms.py` | `run_all` (all three together) | 3 | 3 |
| `tests/test_validation_accounts.py` | Parsing (`parse_int`, `parse_requests`) | 5 | 5 |
| `tests/test_validation_accounts.py` | Validation (`validate_input`, `parse_inputs`) | 8 | 8 |
| `tests/test_validation_accounts.py` | Accounts (create account, log in) | 11 | 11 |
| | **Total** | **41** | **41** |

## 2. Results checked against the class slides

Head at 53, queue `98, 183, 37, 122, 14, 124, 65, 67`, disk 0-199:

| Algorithm | Expected (slides) | Program result | Match |
|-----------|------------------:|---------------:|:-----:|
| FCFS | 640 | 640 | Yes |
| SSTF | 236 | 236 | Yes |
| SCAN (left) | 236 | 236 | Yes |
| SCAN (right) | not in slides | 331 (53 → 183 → 199 → 37 → 14) | Checked by hand |

## 3. What is tested

**Algorithms**
- FCFS serves in arrival order; average = total / number of requests
- SSTF picks the nearest request; a tie goes to the request that arrived first
- SCAN goes to the disk edge before reversing, in both directions
- SCAN skips the edge trip when no request is behind the head, and does not stop twice at the edge
- Every request is served exactly once

**Input**
- Numbers with spaces are accepted; text and decimals are rejected
- Queue can be separated by commas, spaces or semicolons
- Errors for: minimum not less than maximum, head or request outside the disk, empty queue, wrong direction

**Accounts**
- Create an account, then log in (username is not case sensitive)
- Wrong password and unknown user are rejected
- Password is not saved as plain text
- Errors for: duplicate username, duplicate email, short password, passwords that do not match, bad email, bad username

## 4. Not covered by automated tests

The windows and graphs (`src/frontend.py`) are **not** covered by these tests. They
are tested by hand with the checklist in [MANUAL_TESTS.md](MANUAL_TESTS.md).
Record the manual results there before submission.

## 5. How to re-run

```bash
python -m unittest discover -s tests -v
```

Update this report (date, counts) whenever tests are added or changed.

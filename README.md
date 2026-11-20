# Track Attack

An interactive **disk scheduling simulator** written in Python (tkinter). Enter the head's starting
position and a queue of cylinder requests, then see how **FCFS**, **SSTF** and **SCAN** serve them:
the service sequence, a step-by-step computation table, and a bar chart comparing total head movement.

## Requirements

- Python 3.8 or newer
- tkinter (included with Python on Windows and macOS; on Ubuntu/Debian run `sudo apt install python3-tk`)

No other packages are needed.

## Run

```bash
git clone <your-repository-url>
cd track-attack
python src/frontend.py
```

On Windows you can also use `py src/frontend.py`.

## Run the tests

```bash
python -m unittest discover -s tests -t . -v
python -m tests.generate_test_report      # rewrites docs/TEST_REPORT.md
```

## Repository layout

```
track-attack/
├── src/
│   ├── backend.py               # input validation + FCFS, SSTF, SCAN algorithms
│   └── frontend.py              # tkinter user interface
├── tests/
│   ├── cases.py                 # test cases with hand-calculated expected results
│   ├── test_fcfs.py
│   ├── test_sstf.py
│   ├── test_scan.py
│   ├── test_validation.py
│   └── generate_test_report.py  # writes docs/TEST_REPORT.md
└── docs/
    ├── USER_GUIDE.md            # how to run, inputs, reading the output
    ├── TEST_REPORT.md           # automated tests: expected vs actual
    ├── MANUAL_TESTS.md          # GUI test cases with screenshots
    ├── GITHUB_GUIDE.md          # team workflow and commit plan
    └── screenshots/
```

## Documentation

- [User guide](docs/USER_GUIDE.md)
- [Test report](docs/TEST_REPORT.md) and [manual GUI tests](docs/MANUAL_TESTS.md)
- [GitHub workflow and commit plan](docs/GITHUB_GUIDE.md)

## Team

| Role | Name | GitHub username | Responsibility |
|---|---|---|---|
| Leader | | | Repository, README, merging pull requests, final release |
| Backend 1 | | | `src/backend.py`, shared test cases, FCFS and SSTF tests |
| Backend 2 | | | SCAN and validation tests, test report generator |
| Frontend 1 | | | `src/frontend.py` |
| Frontend 2 | | | User guide, manual GUI tests, screenshots |

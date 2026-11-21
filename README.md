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
cd PT_FINALPROJECT_GROUP8
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
PT_FINALPROJECT_GROUP8/
├── README.md
├── .gitignore               
├── requirements.txt            
├── Mago/
│   ├── assets/               
│       ├── login_bg.jpg             # backgroud image
│       ├── title_font.otf           # title font
├──src/ 
    ├── backend.py                   # input validation + FCFS, SSFT, SCAN
    ├── frontend.py                  # tkinter user interface
├── tests/
│   ├── __init__.py          
│   ├── cases.py                     # test cases with expected results
│   ├── test_fcfs.py
│   ├── test_sstf.py
│   ├── test_scan.py
│   ├── test_validation.py
│   ├── generate_test_report.py      # write docs/TEST_REPORT.md
├── docs/
    ├── USER_GUIDE.md                # how to run, inputs, reading the output
    ├── TEST_REPORT.md               # automated tests; expected vs actual
    ├── MANUAL_TEST.md               # GUI test cases 
```

## Documentation

- [USER_GUIDE.md](docs/USER_GUIDE.md)
- [TEST_REPORT.md](docs/TEST_REPORT.md) and [MANUAL_TESTS.md](docs/MANUAL_TESTS.md)

## Team

| Role | Name | GitHub username |
|---|---|---|
| Project Manager / Fullstack Developer | Kayce Coliat | kayce-coliat |
| Backend 1 | Kenneth Aclan | knnthaclan-cloud |
| Backend 2 | Princess Nicole Mago | magoprincessnicole |
| Frontend 1 | James Bryan De Guzman | jamesbryandeguzman5-spec |
| Frontend 2 | Anne Jeline Dimaano | dimaanoannejeline |

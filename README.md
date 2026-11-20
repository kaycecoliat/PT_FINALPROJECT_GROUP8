# Track Attack

An interactive Disk Scheduling Simulator developed using Python and Tkinter. Enter the disk head's starting position and a queue of cylinder requests, then see how First Come First Serve (FCFS), Shortest Seek Time First (SSTF), and SCAN process them.

The system displays the service sequence, a step-by-step computation table, and a bar chart comparing the total head movement of each disk scheduling algorithm and also the Algorithm information.

## Features

- **FCFS (First Come First Serve):** Processes requests in the order they arrive.
- **SSTF (Shortest Seek Time First):** Selects the closest pending cylinder request.
- **SCAN (Elevator Algorithm):** Moves the disk head in one direction before reversing at the disk boundary.
- **Service Sequence:** Displays the order of processed cylinder requests.
- **Computation Table:** Shows step-by-step head movement calculations.
- **Bar Chart Comparison:** Visually compares the total head movement of all three algorithms.
- **Input Validation:** Checks user inputs before performing the simulation.

## Requirements

-**Python 3.8 or newer:**
-**Tkinter** (included with Python on Windows and macOS; on Ubuntu/Debian run "sudo apt install python3-tk")

No other packages are needed.

## Run

Clone the repository:

git clone <your-repository-url>

Open the project folder:

cd track-attack

Run the application:

python src/frontend.py

On Windows, you can also use:

py src/frontend.py

## Run the Tests

Execute the automated tests:

python -m unittest discover -s tests -t . -v

Generate the test report:

python -m tests.generate_test_report

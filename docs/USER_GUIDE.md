# Track Attack - User Guide

## 1. Start the program

```bash
python src/frontend.py
```

## 2. Create an account or log in

1. On the first screen choose **Create Account** (first time) or **Log In**.
2. For a new account fill in:
   - **Username**: 3-20 characters (letters, numbers, `_`, `.`, `-`)
   - **Email**: a valid email address
   - **Password**: at least 8 characters
   - **Confirm Password**: the same password again
3. Tick **Show password** to see what you typed.
4. Press **CREATE ACCOUNT** or **LOG IN** (pressing Enter also works).

Error messages appear in red inside the form. Accounts are saved on your own
computer in `src/users.json`.

## 3. The simulator

### Input Configuration (left side)

| Field | Meaning | Example |
|-------|---------|---------|
| Initial Head Position | Where the disk head starts | `53` |
| Request Queue | Cylinders to visit, in arrival order, separated by commas | `98,183,37,122,14,124,65,67` |
| Minimum Cylinder | Lowest cylinder of the disk | `0` |
| Maximum Cylinder | Highest cylinder of the disk | `199` |
| SCAN Direction | Which way SCAN starts moving (**Left** or **Right**) | `Left` |
| Select Algorithm | **FCFS**, **SSTF** or **SCAN** | `FCFS` |

### Buttons

- **GENERATE RANDOM QUEUE**: fills the queue with 8 random cylinders.
- **RUN SIMULATION**: runs the selected algorithm (Enter key also works).
- **COMPARE ALL**: runs all three and shows the one with the least head movement.
- **RESET**: puts the default values back.
- **Log Out** (top right): returns to the login screen.

### Results (right side)

The three cards show the **total head movement**, the **average seek per request**
and the **number of steps**. The *Service Sequence* line lists the order the cylinders
were visited.

| Tab | What it shows |
|-----|---------------|
| **Seek Path** | A bar graph: one bar per stop, in service order. Bar height = cylinder number. Under each bar: the step number and `+N`, how far the head moved. White bar = start, orange bar = disk edge (SCAN). |
| **Step-by-Step** | A table of every move (from → to) and its distance. |
| **Comparison** | Bars comparing the total head movement of FCFS, SSTF and SCAN. The lowest gets a star. |
| **Algorithm Info** | Definition, how it works, advantages and disadvantages of the selected algorithm. |

## 4. The algorithms in one minute

- **FCFS**: serves requests in the order they arrived. Simple and fair, but the head
  can travel far.
- **SSTF**: always serves the request closest to the head. Usually less movement than
  FCFS, but far requests may starve.
- **SCAN** (elevator): moves one way to the disk edge, then reverses. Predictable
  waiting times, but it may travel to the edge even if nothing is there.

Example: head at 53 and queue `98,183,37,122,14,124,65,67` gives
**FCFS = 640**, **SSTF = 236**, **SCAN (left) = 236**, **SCAN (right) = 331** cylinders.

## 5. Troubleshooting

| Problem | Fix |
|---------|-----|
| `No module named tkinter` | Windows/Mac: reinstall Python from python.org. Linux: `sudo apt install python3-tk` |
| Plain background / plain title font | Run `pip install pillow` and keep the `assets` folder next to `frontend.py` |
| "Invalid Input" message | Check that all fields are whole numbers and every request is between the minimum and maximum cylinder |
| Forgot the password | Close the program and delete `src/users.json`, then create a new account |

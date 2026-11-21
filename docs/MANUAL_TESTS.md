# Track Attack - Manual Test Checklist

Use this list to test the windows by hand (the automated tests only cover
`backend.py`). Run `python src/frontend.py`, do the steps, and write **Pass** or
**Fail** in the *Result* column. Write what went wrong in *Notes* when a test fails.

Tester: ______________________   Date: ______________   Python: ______________

Default values: head `53`, queue `98,183,37,122,14,124,65,67`, range `0`-`199`.

## A. Account screen

| ID | Steps | Expected result | Result | Notes |
|----|-------|-----------------|--------|-------|
| A1 | Start the program | Pink/black login screen with the "Track Attack" title and the Create Account form | | |
| A2 | Create an account with valid details | "Account created" message, then the simulator opens | | |
| A3 | Create an account with a password of 5 characters | Red message: password must be at least 8 characters | | |
| A4 | Create an account with different Password / Confirm | Red message: passwords do not match | | |
| A5 | Create an account with email `abc` | Red message: please enter a valid email | | |
| A6 | Create the same username again | Red message: username already taken | | |
| A7 | Click **Log In** tab, enter the correct details, press Enter | Simulator opens, subtitle shows "Signed in as <username>" | | |
| A8 | Log in with a wrong password | Red message: incorrect username or password | | |
| A9 | Tick **Show password** | Password text becomes visible; untick hides it again | | |
| A10 | Resize the login window | Background fills the window; form stays centered | | |

## B. Simulator

| ID | Steps | Expected result | Result | Notes |
|----|-------|-----------------|--------|-------|
| B1 | Open the simulator | Default values filled in; Seek Path says to run a simulation | | |
| B2 | Select **FCFS**, press RUN SIMULATION | Total **640** cyl, 8 steps | | |
| B3 | Select **SSTF**, press RUN SIMULATION | Total **236** cyl; sequence 53 → 65 → 67 → 37 → 14 → 98 → 122 → 124 → 183 | | |
| B4 | Select **SCAN**, direction **Left**, RUN | Total **236** cyl; an orange bar at cylinder 0 | | |
| B5 | Select **SCAN**, direction **Right**, RUN | Total **331** cyl; an orange bar at cylinder 199 | | |
| B6 | Press **COMPARE ALL** | Comparison tab opens; SSTF and SCAN show the star (lowest); dropdown changes to SSTF | | |
| B7 | Press **GENERATE RANDOM QUEUE**, then RUN | 8 new random numbers; results update | | |
| B8 | Enter a request of `500` and RUN | "Invalid Input" message (outside the disk range) | | |
| B9 | Enter `abc` as the head position and RUN | "Invalid Input" message (must be a whole number) | | |
| B10 | Leave the queue empty and RUN | "Invalid Input" message (enter at least one request) | | |
| B11 | Press **RESET** | All fields back to the defaults, results cleared | | |
| B12 | Press the Enter key instead of the button | Same as RUN SIMULATION | | |

## C. Tabs and display

| ID | Steps | Expected result | Result | Notes |
|----|-------|-----------------|--------|-------|
| C1 | Run any algorithm, open **Seek Path** | Bar graph: white start bar, bar heights match cylinder numbers, numbers on top, step and `+N` below | | |
| C2 | Open **Step-by-Step** | One row per move with "from ➜ to" and the distance; distances add up to the total | | |
| C3 | Open **Comparison** after RUN | Three bars with totals; the lowest has a star | | |
| C4 | Open **Algorithm Info**, change the dropdown FCFS → SSTF → SCAN | Text changes each time (definition, how it works, advantages, disadvantages) | | |
| C5 | Select SCAN, open Algorithm Info | An "Important" note about reaching the boundary is shown | | |
| C6 | Enter 40 random requests and RUN SCAN | Seek Path stays readable (small labels may be hidden) | | |
| C7 | Resize / maximize the window | Graphs redraw to fit | | |

## D. Look and extra

| ID | Steps | Expected result | Result | Notes |
|----|-------|-----------------|--------|-------|
| D1 | Look at all buttons | Pink and oblong (rounded ends); they lighten when the mouse is over them | | |
| D2 | Look at the "Track Attack" title on both screens | Calligraphy font with a soft pink glow | | |
| D3 | Click **Log Out** | Returns to the login screen | | |
| D4 | Uninstall Pillow (or run on a PC without it) and start | Program still opens; pink-to-black gradient background and a script/italic title | | |

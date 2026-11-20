"""Track Attack - backend.

Everything that has NO window/graphics in it:
  * accounts (create account, log in)
  * input parsing and validation
  * the disk scheduling algorithms (FCFS, SSTF, SCAN)
  * the text shown in the "Algorithm Info" tab

frontend.py imports this file. The tests in /tests test this file directly.
"""

import hashlib
import hmac
import json
import os
import re
import urllib.error
import urllib.request


# ===================== SETTINGS =====================

# OPTIONAL: URL of a server that receives new accounts (POST, JSON).
# Leave empty ("") to keep accounts local only.
SIGNUP_API_URL = ""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, "users.json")     # created automatically


# ===================== ACCOUNTS =====================

def _load_users():
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, dict) else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=2)


def _hash_password(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000)


def _send_to_server(username, email, password):
    """Send the new account to the website's server (only if SIGNUP_API_URL is set)."""
    payload = json.dumps({
        "username": username,
        "email": email,
        "password": password,
    }).encode("utf-8")

    request = urllib.request.Request(
        SIGNUP_API_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=10):
            pass
    except urllib.error.HTTPError as error:
        raise ValueError(
            f"The website rejected the sign-up (error {error.code})."
        ) from None
    except (urllib.error.URLError, OSError):
        raise ValueError(
            "Could not reach the website. Check your internet connection."
        ) from None


def create_account(username, email, password, confirm):
    """Validate the form, store the account, return the username."""
    username = username.strip()
    email = email.strip().lower()

    if not re.fullmatch(r"[A-Za-z0-9_.-]{3,20}", username):
        raise ValueError(
            "Username must be 3-20 characters: letters, numbers, _ . or -"
        )

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        raise ValueError("Please enter a valid email address.")

    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters.")

    if password != confirm:
        raise ValueError("Passwords do not match.")

    users = _load_users()

    if username.lower() in users:
        raise ValueError("That username is already taken.")

    if any(user["email"] == email for user in users.values()):
        raise ValueError("An account with that email already exists.")

    if SIGNUP_API_URL:
        _send_to_server(username, email, password)

    salt = os.urandom(16)
    users[username.lower()] = {
        "username": username,
        "email": email,
        "salt": salt.hex(),
        "hash": _hash_password(password, salt).hex(),
    }
    _save_users(users)

    return username


def log_in(username, password):
    """Check the credentials and return the username."""
    user = _load_users().get(username.strip().lower())

    if user is None:
        raise ValueError("Incorrect username or password.")

    expected = bytes.fromhex(user["hash"])
    actual = _hash_password(password, bytes.fromhex(user["salt"]))

    if not hmac.compare_digest(expected, actual):
        raise ValueError("Incorrect username or password.")

    return user["username"]


# ===================== ALGORITHM INFO =====================

ALGORITHM_NAMES = ["FCFS", "SSTF", "SCAN"]

ALGORITHM_INFO = {
    "FCFS": {
        "title": "FCFS - First Come, First Served",
        "definition": (
            "FCFS is the simplest disk scheduling algorithm. It services the "
            "disk requests one by one in the exact order they arrive in the queue."
        ),
        "how": [
            "Accepts the initial head position.",
            "Reads the request queue.",
            "Processes requests one by one in their original order.",
            "Calculates the head movement for every request.",
            "Adds all movements to get the total head movement.",
        ],
        "important": None,
        "pros": [
            "Easy to understand and implement.",
            "Processes requests in arrival order.",
            "Fair to incoming requests.",
        ],
        "cons": [
            "Can result in longer head movement.",
            "Does not prioritize nearby requests.",
        ],
        "example": (
            "Queue = 98, 183, 37, 122, 14, 124, 65, 67 with the head at 53 "
            "gives a total head movement of 640 cylinders."
        ),
    },
    "SSTF": {
        "title": "SSTF - Shortest Seek Time First",
        "definition": (
            "SSTF is a disk scheduling algorithm that selects the request "
            "closest to the current head position."
        ),
        "how": [
            "Accepts the initial head position.",
            "Reads all pending disk requests.",
            "Finds the request with the shortest distance from the current head.",
            "Processes the nearest request first.",
            "Repeats until all requests are completed.",
            "Calculates the total head movement.",
        ],
        "important": None,
        "pros": [
            "Usually reduces total head movement compared with FCFS.",
            "Prioritizes nearby requests.",
            "Can improve seek performance.",
        ],
        "cons": [
            "Far-away requests may experience starvation.",
            "Requests are not necessarily processed in arrival order.",
        ],
        "example": (
            "Queue = 98, 183, 37, 122, 14, 124, 65, 67 with the head at 53 "
            "gives a total head movement of 236 cylinders."
        ),
    },
    "SCAN": {
        "title": "SCAN - Elevator Algorithm",
        "definition": (
            "SCAN, also known as the Elevator Algorithm, moves the disk head in "
            "one direction, servicing requests along the way until it reaches "
            "the disk boundary. It then reverses direction and services the "
            "remaining requests."
        ),
        "how": [
            "Accepts the initial head position.",
            "Reads the request queue.",
            "Accepts the initial direction (LEFT or RIGHT).",
            "Moves the head in the selected direction.",
            "Services requests along the way.",
            "Reaches the disk boundary before reversing direction.",
            "Services the remaining requests.",
            "Calculates the total head movement.",
        ],
        "important": (
            "Unlike SSTF, SCAN follows a specific direction and must reach the "
            "disk boundary before reversing."
        ),
        "pros": [
            "Provides more predictable waiting times.",
            "Reduces excessive back-and-forth movement.",
            "Handles multiple requests efficiently.",
        ],
        "cons": [
            "May travel to the disk boundary even when there are no requests there.",
            "Requests just behind the moving head may wait longer.",
        ],
        "example": (
            "Queue = 98, 183, 37, 122, 14, 124, 65, 67 with the head at 53 "
            "moving LEFT goes 53 \u2192 0, then 0 \u2192 183, for a total of "
            "236 cylinders."
        ),
    },
}


# ===================== BACKEND =====================

def parse_int(text, label):
    text = text.strip()
    try:
        return int(text)
    except ValueError:
        raise ValueError(f"{label} must be a whole number (got '{text}').") from None


def parse_requests(text):
    cleaned = text.replace(";", ",").replace(" ", ",")
    parts = [p for p in cleaned.split(",") if p]
    return [parse_int(p, "Each request") for p in parts]


def validate_input(head, requests, minimum, maximum, direction):
    if minimum >= maximum:
        raise ValueError("Minimum cylinder must be less than maximum.")

    if not minimum <= head <= maximum:
        raise ValueError("Initial head position is outside the disk range.")

    if not requests:
        raise ValueError("Please enter at least one disk request.")

    for request in requests:
        if not minimum <= request <= maximum:
            raise ValueError(f"Request {request} is outside the disk range.")

    if direction not in ("Left", "Right"):
        raise ValueError("Invalid SCAN direction.")


def parse_inputs(head_text, queue_text, min_text, max_text, direction):
    head = parse_int(head_text, "Initial head position")
    minimum = parse_int(min_text, "Minimum cylinder")
    maximum = parse_int(max_text, "Maximum cylinder")
    requests = parse_requests(queue_text)
    validate_input(head, requests, minimum, maximum, direction)
    return head, requests, minimum, maximum, direction


def create_result(name, head, stops, types, request_count):
    steps = []
    total = 0
    current = head

    for destination, movement_type in zip(stops, types):
        distance = abs(destination - current)
        total += distance
        steps.append({
            "from": current,
            "to": destination,
            "type": movement_type,
            "movement": distance,
        })
        current = destination

    return {
        "algorithm": name,
        "sequence": [head] + stops,
        "steps": steps,
        "total": total,
        "average": total / request_count if request_count else 0,
        "requests": request_count,
    }


def fcfs(head, requests):
    stops = list(requests)
    types = ["Request"] * len(stops)
    return create_result("FCFS", head, stops, types, len(requests))


def sstf(head, requests):
    remaining = list(enumerate(requests))
    stops, types = [], []
    current = head

    while remaining:
        selected = min(remaining, key=lambda item: (abs(item[1] - current), item[0]))
        stops.append(selected[1])
        types.append("Request")
        current = selected[1]
        remaining.remove(selected)

    return create_result("SSTF", head, stops, types, len(requests))


def scan(head, requests, minimum, maximum, direction):
    going_right = direction == "Right"

    if going_right:
        ahead = sorted(r for r in requests if r >= head)
        behind = sorted(r for r in requests if r < head)
        far = maximum
    else:
        ahead = sorted((r for r in requests if r <= head), reverse=True)
        behind = sorted(r for r in requests if r > head)
        far = minimum

    stops = list(ahead)
    types = ["Request"] * len(ahead)

    if behind:
        last = stops[-1] if stops else head

        # go to the disk edge, then reverse
        if last != far:
            stops.append(far)
            types.append("Boundary")

        order = sorted(behind, reverse=going_right)
        stops.extend(order)
        types.extend(["Request"] * len(order))

    return create_result("SCAN", head, stops, types, len(requests))


def run_all(head, requests, minimum, maximum, direction):
    validate_input(head, requests, minimum, maximum, direction)

    return {
        "FCFS": fcfs(head, requests),
        "SSTF": sstf(head, requests),
        "SCAN": scan(head, requests, minimum, maximum, direction),
    }

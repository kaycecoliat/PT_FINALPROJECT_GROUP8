"""Track Attack - frontend (the windows and graphics).

Setup:  pip install pillow      (only needed to show the background picture)
Run:    python src/frontend.py

Keep the "assets" folder next to this file. All the logic (algorithms,
accounts, validation) lives in backend.py.
"""

import os
import random
import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont

from backend import (
    ALGORITHM_INFO,
    ALGORITHM_NAMES,
    create_account,
    log_in,
    parse_inputs,
    run_all,
)

try:
    from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageFilter   # pip install pillow
except ImportError:                  # login screen falls back to a plain color
    Image = ImageTk = None


# ===================== SETTINGS =====================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Login screen pictures
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
BG_IMAGE = os.path.join(ASSETS_DIR, "login_bg.jpg")    # pink tech background
TEAM_IMAGE = os.path.join(ASSETS_DIR, "team.png")      # team photo (transparent)
SHOW_TEAM_PHOTO = False    # set to True to show the team photo on the login screen

# Calligraphy font for the "Track Attack" title (needs Pillow).
# Currently TeX Gyre Chorus (a chancery calligraphy font). To use another one
# (e.g. Great Vibes, Allura), put its .ttf/.otf in assets and change this name.
TITLE_FONT_FILE = os.path.join(ASSETS_DIR, "title_font.otf")
TITLE_TEXT = "Track Attack"
TITLE_GLOW = "#E6179B"      # soft glow behind the title

# Used only if Pillow / the font file is missing: the first one installed is used.
CALLIGRAPHY_FONTS = [
    "Ink Free", "Segoe Script", "Brush Script MT", "Lucida Handwriting",
    "Freestyle Script", "Kunstler Script", "Monotype Corsiva",   # Windows
    "Savoye LET", "Snell Roundhand", "Bradley Hand", "Apple Chancery",  # Mac
    "URW Chancery L", "Z003", "Purisa",                          # Linux
]


# ===================== TITLE FONT =====================

def render_title(text, size, color):
    """Draw the title with the calligraphy font file + a soft glow. Returns an image, or None."""
    if Image is None or not os.path.exists(TITLE_FONT_FILE):
        return None
    try:
        font = ImageFont.truetype(TITLE_FONT_FILE, size)
        left, top, right, bottom = font.getbbox(text)
    except OSError:
        return None

    pad = 14
    canvas_size = (right - left + pad * 2, bottom - top + pad * 2)
    position = (pad - left, pad - top)

    glow = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    ImageDraw.Draw(glow).text(position, text, font=font, fill=TITLE_GLOW)
    glow = glow.filter(ImageFilter.GaussianBlur(5))
    glow = Image.alpha_composite(glow, glow)        # make the glow stronger

    letters = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    ImageDraw.Draw(letters).text(position, text, font=font, fill=color)
    return Image.alpha_composite(glow, letters)


def title_image(text, size, color):
    picture = render_title(text, size, color)
    return ImageTk.PhotoImage(picture) if picture is not None else None


def title_font(size):
    """Return a calligraphy font for the title (italic serif if none is installed)."""
    installed = set(tkfont.families())
    for name in CALLIGRAPHY_FONTS:
        if name in installed:
            return (name, size, "bold")
    return ("Times New Roman", size, "bold italic")


# ===================== OBLONG BUTTON =====================

def _lighten(color, amount=0.18):
    color = color.lstrip("#")
    r, g, b = (int(color[i:i + 2], 16) for i in (0, 2, 4))
    r, g, b = (int(c + (255 - c) * amount) for c in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"


class PillButton(tk.Canvas):
    """Oblong (pill-shaped) button with a hover effect.

    Works like a normal button: PillButton(parent, "Text", command, "#E6179B").
    .config(text=..., bg=..., fg=...) changes it later.
    """

    def __init__(self, parent, text, command, color, fg="white",
                 font=("Arial", 10, "bold"), width=250, height=40):
        super().__init__(
            parent, width=width, height=height, bg=parent.cget("bg"),
            highlightthickness=0, bd=0, cursor="hand2",
        )
        self._text = text
        self._command = command
        self._color = color
        self._fg = fg
        self._font = font
        self._hover = False

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonRelease-1>", self._on_release)
        self._draw()

    def _draw(self):
        self.delete("all")
        w = int(float(self.cget("width")))
        h = int(float(self.cget("height")))
        color = _lighten(self._color) if self._hover else self._color

        # two round ends + a rectangle in the middle = oblong shape
        self.create_oval(0, 0, h, h, fill=color, outline=color)
        self.create_oval(w - h, 0, w, h, fill=color, outline=color)
        self.create_rectangle(h / 2, 0, w - h / 2, h, fill=color, outline=color)
        self.create_text(w / 2, h / 2, text=self._text, fill=self._fg, font=self._font)

    def configure(self, cnf=None, **kw):
        for key, attr in (("text", "_text"), ("bg", "_color"), ("fg", "_fg"),
                          ("font", "_font"), ("command", "_command")):
            if key in kw:
                setattr(self, attr, kw.pop(key))
        kw.pop("activebackground", None)
        kw.pop("activeforeground", None)
        if cnf or kw:
            super().configure(cnf, **kw)
        self._draw()

    config = configure

    def _on_enter(self, event):
        self._hover = True
        self._draw()

    def _on_leave(self, event):
        self._hover = False
        self._draw()

    def _on_release(self, event):
        inside = 0 <= event.x <= int(float(self.cget("width"))) and \
                 0 <= event.y <= int(float(self.cget("height")))
        if inside and self._command:
            self._command()


# ===================== ACCOUNT SCREEN =====================

class AuthScreen(tk.Frame):
    """First screen: create an account (or log in), then continue.

    Pink-and-black background (picture, or a gradient if Pillow is missing).
    The team photo can be switched on with SHOW_TEAM_PHOTO.
    """

    CARD_TOP = 132   # y position of the form card

    def __init__(self, root, on_success):
        # pink and black theme
        self.bg = "#05020A"
        self.panel = "#14061C"
        self.field = "#2D1038"
        self.blue = "#E6179B"      # accent color (hot pink)
        self.white = "#FFFFFF"
        self.muted = "#E3B8D6"

        super().__init__(root, bg=self.bg)
        self.root = root
        self.on_success = on_success
        self.mode = "signup"
        self.entries = {}

        self.bg_src = self.load_image(BG_IMAGE)
        self.team_src = self.load_image(TEAM_IMAGE) if SHOW_TEAM_PHOTO else None
        self.bg_photo = None
        self.team_photo = None
        self.last_size = None
        self.resize_job = None
        self.card_height = 470

        root.title("Track Attack - Create Account")
        root.geometry("1100x800")
        root.minsize(900, 720)
        root.configure(bg=self.bg)
        self.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self, bg=self.bg, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # layers (bottom to top): background, team photo, texts, form card
        self.bg_item = self.canvas.create_image(0, 0, anchor="nw")
        self.team_item = self.canvas.create_image(0, 0, anchor="s")
        self.title_photo = title_image(TITLE_TEXT, 76, self.white)
        if self.title_photo is not None:
            self.title_item = self.canvas.create_image(0, 0, image=self.title_photo)
        else:
            self.title_item = self.canvas.create_text(
                0, 0, text=TITLE_TEXT, font=title_font(36), fill=self.white,
            )
        self.subtitle_item = self.canvas.create_text(
            0, 0, text="Interactive Disk Scheduling Simulator",
            font=("Arial", 11), fill=self.muted,
        )

        if Image is None:
            self.canvas.create_text(
                10, 10, anchor="nw", fill=self.muted, font=("Arial", 9),
                text="Tip: run  pip install pillow  to show the background picture.",
            )

        self.card = tk.Frame(
            self.canvas, bg=self.panel, padx=25, pady=15,
            highlightbackground=self.blue, highlightthickness=1,
        )
        self.card_item = self.canvas.create_window(0, 0, window=self.card, anchor="n")

        tabs = tk.Frame(self.card, bg=self.panel)
        tabs.pack(pady=(0, 6))

        self.signup_tab = PillButton(
            tabs, "Create Account", lambda: self.set_mode("signup"),
            self.field, width=160, height=36,
        )
        self.signup_tab.pack(side="left", padx=3)

        self.login_tab = PillButton(
            tabs, "Log In", lambda: self.set_mode("login"),
            self.field, width=160, height=36,
        )
        self.login_tab.pack(side="left", padx=3)

        self.form = tk.Frame(self.card, bg=self.panel)
        self.form.pack(fill="x")

        self.error = tk.Label(
            self.card, text="", bg=self.panel, fg="#FF6B6B",
            font=("Arial", 10), wraplength=340, justify="center", height=2,
        )
        self.error.pack(pady=(6, 0))

        self.submit_button = PillButton(
            self.card, "", self.submit, self.blue,
            font=("Arial", 11, "bold"), width=330, height=44,
        )
        self.submit_button.pack(pady=(4, 0))

        self.set_mode("signup")

        # measure the (tallest) sign-up card so the photo never covers it
        self.update_idletasks()
        self.card_height = self.card.winfo_reqheight()

        self.canvas.bind("<Configure>", self.schedule_layout)
        root.bind("<Return>", lambda e: self.submit())

    # ---------- background + photo ----------

    @staticmethod
    def load_image(path):
        if Image is None:
            return None
        try:
            return Image.open(path).convert("RGBA")
        except (OSError, ValueError):
            return None

    def schedule_layout(self, event=None):
        # wait a moment while the window is being resized
        if self.resize_job:
            self.after_cancel(self.resize_job)
        self.resize_job = self.after(60, self.layout)

    def layout(self):
        self.resize_job = None
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width < 50 or height < 50:
            return

        center = width / 2
        self.canvas.coords(self.title_item, center, 52)
        self.canvas.coords(self.subtitle_item, center, 106)
        self.canvas.coords(self.card_item, center, self.CARD_TOP)

        if (width, height) == self.last_size:
            return
        self.last_size = (width, height)

        # no picture available: pink-and-black gradient drawn with plain tkinter
        if self.bg_src is None:
            self.draw_gradient(width, height)

        # background: fill the whole window (cropped from the center)
        if self.bg_src is not None:
            scale = max(width / self.bg_src.width, height / self.bg_src.height)
            new_w = int(self.bg_src.width * scale) + 1
            new_h = int(self.bg_src.height * scale) + 1
            image = self.bg_src.resize((new_w, new_h), Image.BILINEAR)
            left = (new_w - width) // 2
            top = (new_h - height) // 2
            image = image.crop((left, top, left + width, top + height))
            self.bg_photo = ImageTk.PhotoImage(image)
            self.canvas.itemconfig(self.bg_item, image=self.bg_photo)

        # team photo: attached to the bottom, sized to the free space under the card
        if self.team_src is not None:
            free = height - (self.CARD_TOP + self.card_height) - 4
            target_h = max(150, min(340, free))
            target_w = self.team_src.width * target_h / self.team_src.height
            if target_w > width:
                target_w = width
                target_h = target_w * self.team_src.height / self.team_src.width
            image = self.team_src.resize((int(target_w), int(target_h)), Image.LANCZOS)
            self.team_photo = ImageTk.PhotoImage(image)
            self.canvas.itemconfig(self.team_item, image=self.team_photo)
            self.canvas.coords(self.team_item, center, height)

    def draw_gradient(self, width, height):
        self.canvas.delete("gradient")
        steps = 60
        top, bottom = (0, 0, 0), (200, 20, 130)
        for i in range(steps):
            t = (i / (steps - 1)) ** 1.6
            color = "#%02x%02x%02x" % tuple(
                int(a + (b - a) * t) for a, b in zip(top, bottom)
            )
            self.canvas.create_rectangle(
                0, height * i / steps, width, height * (i + 1) / steps + 1,
                fill=color, outline="", tags="gradient",
            )
        self.canvas.tag_lower("gradient")

    def destroy(self):
        if self.resize_job:
            self.after_cancel(self.resize_job)
            self.resize_job = None
        super().destroy()

    # ---------- form ----------

    def set_mode(self, mode):
        self.mode = mode
        self.error.config(text="")

        active, idle = self.blue, self.field
        for button, name in ((self.signup_tab, "signup"), (self.login_tab, "login")):
            color = active if mode == name else idle
            button.config(
                bg=color, fg="white",
                activebackground=color, activeforeground="white",
            )

        for child in self.form.winfo_children():
            child.destroy()
        self.entries = {}

        self.add_field("username", "Username")
        if mode == "signup":
            self.add_field("email", "Email")
        self.add_field("password", "Password", secret=True)
        if mode == "signup":
            self.add_field("confirm", "Confirm Password", secret=True)

        self.show_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            self.form, text="Show password", variable=self.show_var,
            command=self.toggle_password, bg=self.panel, fg=self.white,
            selectcolor=self.field, activebackground=self.panel,
            activeforeground=self.white,
        ).pack(anchor="w", pady=(8, 0))

        if mode == "signup":
            self.root.title("Track Attack - Create Account")
            self.submit_button.config(text="CREATE ACCOUNT")
        else:
            self.root.title("Track Attack - Log In")
            self.submit_button.config(text="LOG IN")

        self.entries["username"].focus_set()

    def add_field(self, key, label, secret=False):
        tk.Label(
            self.form, text=label, bg=self.panel, fg=self.white,
            font=("Arial", 10),
        ).pack(anchor="w", pady=(8, 3))

        entry = tk.Entry(
            self.form, width=32, font=("Arial", 11), bg=self.field,
            fg=self.white, insertbackground="white", relief="flat",
            show="\u2022" if secret else "",
        )
        entry.pack(anchor="w", pady=3, ipady=5)
        self.entries[key] = entry

    def toggle_password(self):
        show = "" if self.show_var.get() else "\u2022"
        for key in ("password", "confirm"):
            if key in self.entries:
                self.entries[key].config(show=show)

    def submit(self):
        try:
            if self.mode == "signup":
                username = create_account(
                    self.entries["username"].get(),
                    self.entries["email"].get(),
                    self.entries["password"].get(),
                    self.entries["confirm"].get(),
                )
            else:
                username = log_in(
                    self.entries["username"].get(),
                    self.entries["password"].get(),
                )
        except ValueError as error:
            self.error.config(text=str(error))
            return

        if self.mode == "signup":
            messagebox.showinfo(
                "Account created",
                f"Welcome, {username}! Your account has been created.",
            )

        self.root.unbind("<Return>")
        self.destroy()
        self.on_success(username)


# ===================== SIMULATOR =====================

class TrackAttackApp:

    # Default values match the sample slides (head 53, 8 requests).
    DEFAULTS = {
        "head": "53",
        "queue": "98,183,37,122,14,124,65,67",
        "min": "0",
        "max": "199",
    }

    def __init__(self, root, username=None, on_logout=None):
        self.root = root
        self.username = username
        self.on_logout = on_logout
        self.root.title("Track Attack - Disk Scheduling Simulator")
        self.root.geometry("1250x800")
        self.root.minsize(1050, 700)

        # pink and black theme
        self.bg = "#05020A"
        self.panel = "#14061C"
        self.field = "#2D1038"
        self.blue = "#E6179B"          # main accent (hot pink)
        self.purple = "#B66DFF"
        self.green = "#FF6FC8"         # light pink (total card)
        self.orange = "#FFB020"        # disk-edge marker
        self.pink_light = "#FF8AD0"    # headings
        self.white = "#FFFFFF"
        self.muted = "#E3B8D6"

        # line / bar color of each algorithm
        self.colors = {
            "FCFS": "#FF3CAC",
            "SSTF": "#B66DFF",
            "SCAN": "#2DE2E6",
        }

        self.root.configure(bg=self.bg)

        self.current = None
        self.all_results = None
        self.disk_range = (0, 199)

        self.setup_style()
        self.create_interface()
        self.root.bind("<Return>", lambda e: self.run_selected())

    # ---------- styling ----------

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=self.panel,
            foreground="white",
            fieldbackground=self.panel,
            rowheight=28,
            borderwidth=0,
            font=("Arial", 10),
        )
        style.configure(
            "Treeview.Heading",
            background=self.field,
            foreground="white",
            font=("Arial", 10, "bold"),
            borderwidth=0,
        )
        style.map("Treeview", background=[("selected", "#8A1560")])

        style.configure("TNotebook", background=self.bg, borderwidth=0)
        style.configure(
            "TNotebook.Tab",
            background=self.field,
            foreground="white",
            padding=(16, 7),
            font=("Arial", 10, "bold"),
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", self.blue)],
            foreground=[("selected", "white")],
        )

        style.configure(
            "TCombobox",
            fieldbackground=self.field,
            background=self.field,
            foreground="white",
            arrowcolor="white",
            selectbackground=self.field,
            selectforeground="white",
        )
        style.map("TCombobox", fieldbackground=[("readonly", self.field)])
        self.root.option_add("*TCombobox*Listbox.background", self.field)
        self.root.option_add("*TCombobox*Listbox.foreground", "white")

    # ---------- layout ----------

    def create_interface(self):
        self.status = tk.Label(
            self.root,
            text="Ready to simulate. Press Enter or click RUN SIMULATION.",
            bg=self.field,
            fg=self.white,
            anchor="w",
            padx=15,
            pady=4,
        )
        self.status.pack(fill="x", side="bottom")

        self.title_photo = title_image(TITLE_TEXT, 52, self.white)
        if self.title_photo is not None:
            tk.Label(
                self.root, image=self.title_photo, bg=self.bg,
            ).pack(pady=(8, 0))
        else:
            tk.Label(
                self.root,
                text=TITLE_TEXT,
                font=title_font(34),
                bg=self.bg,
                fg=self.white,
            ).pack(pady=(14, 0))

        subtitle = "Interactive Disk Scheduling Simulator"
        if self.username:
            subtitle += f"   \u2022   Signed in as {self.username}"

        tk.Label(
            self.root,
            text=subtitle,
            font=("Arial", 11),
            bg=self.bg,
            fg=self.muted,
        ).pack(pady=(0, 10))

        # top-corner button
        if self.on_logout:
            PillButton(
                self.root, "Log Out", self.on_logout, "#9C1F70",
                font=("Arial", 9, "bold"), width=90, height=30,
            ).place(relx=1.0, x=-20, y=16, anchor="ne")

        main = tk.Frame(self.root, bg=self.bg)
        main.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        self.create_input_panel(main)
        self.create_result_panel(main)

    def create_input_panel(self, main):
        panel = tk.LabelFrame(
            main,
            text=" Input Configuration ",
            font=("Arial", 12, "bold"),
            bg=self.panel,
            fg=self.white,
            padx=15,
            pady=10,
        )
        panel.pack(side="left", fill="y", padx=(0, 15))

        self.head_entry = self.add_input(panel, "Initial Head Position:", self.DEFAULTS["head"])
        self.queue_entry = self.add_input(panel, "Request Queue (comma separated):", self.DEFAULTS["queue"])
        self.minimum_entry = self.add_input(panel, "Minimum Cylinder:", self.DEFAULTS["min"])
        self.maximum_entry = self.add_input(panel, "Maximum Cylinder:", self.DEFAULTS["max"])

        self.make_button(panel, "GENERATE RANDOM QUEUE", self.random_queue, "#B3157F", pady=6)

        tk.Label(
            panel, text="SCAN Direction:",
            bg=self.panel, fg=self.white, font=("Arial", 10, "bold"),
        ).pack(anchor="w", pady=(12, 4))

        self.direction = tk.StringVar(value="Left")
        row = tk.Frame(panel, bg=self.panel)
        row.pack(anchor="w")
        for text in ("Left", "Right"):
            tk.Radiobutton(
                row, text=text, variable=self.direction, value=text,
                bg=self.panel, fg=self.white, selectcolor=self.field,
                activebackground=self.panel, activeforeground=self.white,
            ).pack(side="left", padx=(0, 12))

        tk.Label(
            panel, text="Select Algorithm:",
            bg=self.panel, fg=self.white, font=("Arial", 10, "bold"),
        ).pack(anchor="w", pady=(14, 4))

        self.algorithm = tk.StringVar(value="FCFS")
        self.algorithm_box = ttk.Combobox(
            panel,
            textvariable=self.algorithm,
            values=ALGORITHM_NAMES,
            state="readonly",
            width=27,
        )
        self.algorithm_box.pack(anchor="w", pady=4)
        # update the Algorithm Info tab whenever a different algorithm is picked
        self.algorithm_box.bind(
            "<<ComboboxSelected>>", lambda e: self.show_info(self.algorithm.get())
        )

        self.make_button(panel, "RUN SIMULATION", self.run_selected, self.blue)
        self.make_button(panel, "COMPARE ALL", self.compare_all, "#FF3CAC")
        self.make_button(panel, "RESET", self.reset, "#9C1F70")

    def create_result_panel(self, main):
        panel = tk.Frame(main, bg=self.bg)
        panel.pack(side="left", fill="both", expand=True)

        self.result_title = tk.Label(
            panel, text="Simulation Results",
            font=("Arial", 17, "bold"), bg=self.bg, fg=self.white,
        )
        self.result_title.pack(anchor="w", pady=(0, 6))

        cards = tk.Frame(panel, bg=self.bg)
        cards.pack(fill="x")
        self.total_value = self.make_card(cards, "TOTAL HEAD MOVEMENT", self.green)
        self.average_value = self.make_card(cards, "AVG. SEEK PER REQUEST", self.blue)
        self.steps_value = self.make_card(cards, "STEPS", self.orange)

        self.sequence_label = tk.Label(
            panel, text="Service Sequence: --",
            font=("Arial", 10), bg=self.panel, fg=self.white,
            padx=10, pady=10, wraplength=700, justify="left", anchor="w",
        )
        self.sequence_label.pack(fill="x", pady=8)
        panel.bind(
            "<Configure>",
            lambda e: self.sequence_label.config(wraplength=max(200, e.width - 30)),
        )

        notebook = ttk.Notebook(panel)
        notebook.pack(fill="both", expand=True)
        self.notebook = notebook

        path_tab = tk.Frame(notebook, bg=self.panel)
        steps_tab = tk.Frame(notebook, bg=self.panel)
        chart_tab = tk.Frame(notebook, bg=self.panel)
        info_tab = tk.Frame(notebook, bg=self.panel)
        notebook.add(path_tab, text="Seek Path")
        notebook.add(steps_tab, text="Step-by-Step")
        notebook.add(chart_tab, text="Comparison")
        notebook.add(info_tab, text="Algorithm Info")

        self.path_canvas = tk.Canvas(path_tab, bg=self.panel, highlightthickness=0)
        self.path_canvas.pack(fill="both", expand=True)
        self.path_canvas.bind("<Configure>", lambda e: self.draw_path())

        columns = ("step", "movement", "distance")
        self.table = ttk.Treeview(steps_tab, columns=columns, show="headings")
        headings = {
            "step": ("Step", 80),
            "movement": ("Head Movement", 240),
            "distance": ("Distance", 120),
        }
        for key, (text, width) in headings.items():
            self.table.heading(key, text=text)
            self.table.column(key, width=width, anchor="center")

        scroll = ttk.Scrollbar(steps_tab, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self.table.pack(fill="both", expand=True)

        self.chart = tk.Canvas(chart_tab, bg=self.panel, highlightthickness=0)
        self.chart.pack(fill="both", expand=True)
        self.chart.bind("<Configure>", lambda e: self.draw_chart())

        # ---- Algorithm Info tab ----
        info_scroll = ttk.Scrollbar(info_tab, orient="vertical")
        info_scroll.pack(side="right", fill="y")

        self.info_text = tk.Text(
            info_tab, wrap="word", bg=self.panel, fg=self.white,
            relief="flat", padx=18, pady=14, font=("Arial", 11),
            spacing1=2, spacing3=2, cursor="arrow",
            yscrollcommand=info_scroll.set, highlightthickness=0,
        )
        info_scroll.config(command=self.info_text.yview)
        self.info_text.pack(fill="both", expand=True)

        self.info_text.tag_configure("heading", font=("Arial", 12, "bold"),
                                     foreground=self.pink_light, spacing1=10)
        self.info_text.tag_configure("body", font=("Arial", 11),
                                     foreground=self.white)
        self.info_text.tag_configure("bullet", font=("Arial", 11),
                                     foreground=self.white,
                                     lmargin1=14, lmargin2=30)
        self.info_text.tag_configure("important", font=("Arial", 11, "bold"),
                                     foreground="#FFC2E8")
        self.info_text.tag_configure("example", font=("Arial", 10, "italic"),
                                     foreground=self.muted)

        self.draw_path()
        self.draw_chart()
        self.show_info(self.algorithm.get())

    # ---------- widgets ----------

    def add_input(self, parent, label, default):
        tk.Label(
            parent, text=label, bg=self.panel, fg=self.white, font=("Arial", 10)
        ).pack(anchor="w", pady=(8, 3))

        entry = tk.Entry(
            parent, width=30, font=("Arial", 11),
            bg=self.field, fg=self.white, insertbackground="white", relief="flat",
        )
        entry.insert(0, default)
        entry.pack(anchor="w", pady=3, ipady=5)
        return entry

    def make_button(self, parent, text, command, color, pady=10):
        PillButton(
            parent, text, command, color,
            font=("Arial", 10, "bold"), width=250, height=26 + pady * 2,
        ).pack(anchor="w", pady=6)

    def make_card(self, parent, title, color):
        card = tk.Frame(parent, bg=self.panel, padx=12, pady=8)
        card.pack(side="left", fill="x", expand=True, padx=(0, 8))
        tk.Label(card, text=title, bg=self.panel, fg=self.muted,
                 font=("Arial", 8, "bold")).pack(anchor="w")
        value = tk.Label(card, text="--", bg=self.panel, fg=color,
                         font=("Arial", 18, "bold"))
        value.pack(anchor="w")
        return value

    # ---------- algorithm info ----------

    def show_info(self, name):
        """Fill the Algorithm Info tab with the details of the given algorithm."""
        info = ALGORITHM_INFO.get(name)
        if info is None:
            return

        text = self.info_text
        text.config(state="normal")
        text.delete("1.0", "end")

        # title uses the algorithm's own color
        text.tag_configure(
            "title", font=("Arial", 16, "bold"),
            foreground=self.colors.get(name, self.blue),
        )
        text.insert("end", info["title"] + "\n", "title")

        text.insert("end", "Definition:\n", "heading")
        text.insert("end", info["definition"] + "\n", "body")

        text.insert("end", "How it works:\n", "heading")
        for number, line in enumerate(info["how"], 1):
            text.insert("end", f"{number}.  {line}\n", "bullet")

        if info.get("important"):
            text.insert("end", "Important:\n", "heading")
            text.insert("end", info["important"] + "\n", "important")

        text.insert("end", "Advantages:\n", "heading")
        for line in info["pros"]:
            text.insert("end", f"\u2022  {line}\n", "bullet")

        text.insert("end", "Disadvantages:\n", "heading")
        for line in info["cons"]:
            text.insert("end", f"\u2022  {line}\n", "bullet")

        if info.get("example"):
            text.insert("end", "\nSample: " + info["example"] + "\n", "example")

        text.config(state="disabled")
        text.yview_moveto(0)

    # ---------- inputs ----------

    def get_inputs(self):
        try:
            data = parse_inputs(
                self.head_entry.get(),
                self.queue_entry.get(),
                self.minimum_entry.get(),
                self.maximum_entry.get(),
                self.direction.get(),
            )
        except ValueError as error:
            messagebox.showerror("Invalid Input", str(error))
            self.status.config(text="Invalid input - please check the fields.")
            return None

        self.disk_range = (data[2], data[3])
        return data

    def random_queue(self):
        try:
            low = int(self.minimum_entry.get())
            high = int(self.maximum_entry.get())
            if low >= high:
                raise ValueError
        except ValueError:
            low, high = 0, 199

        queue = [random.randint(low, high) for _ in range(8)]
        self.queue_entry.delete(0, tk.END)
        self.queue_entry.insert(0, ",".join(map(str, queue)))
        self.status.config(text="Random request queue generated.")

    # ---------- results ----------

    def show_result(self, result):
        self.current = result

        self.result_title.config(text=f"Simulation Results - {result['algorithm']}")
        self.total_value.config(text=f"{result['total']} cyl")
        self.average_value.config(text=f"{result['average']:.2f} cyl")
        self.steps_value.config(text=str(len(result["steps"])))

        self.sequence_label.config(
            text="Service Sequence: " + " \u2192 ".join(map(str, result["sequence"]))
        )

        for item in self.table.get_children():
            self.table.delete(item)

        for number, step in enumerate(result["steps"], 1):
            self.table.insert(
                "", "end",
                values=(
                    number,
                    f"{step['from']} \u279c {step['to']}",
                    step["movement"],
                ),
            )

        self.show_info(result["algorithm"])
        self.draw_path()
        self.status.config(text=f"{result['algorithm']} simulation completed.")

    def draw_path(self):
        """Seek path as a bar graph: one bar per stop, in service order.

        Bar height = cylinder number. The number under each bar is the step,
        and the small "+N" is how far the head moved to reach that bar.
        """
        c = self.path_canvas
        c.delete("all")
        width = max(c.winfo_width(), 400)
        height = max(c.winfo_height(), 250)

        if not self.current:
            c.create_text(
                width / 2, height / 2, fill=self.muted, font=("Arial", 12),
                text="Run a simulation to see the head's seek path.",
            )
            return

        sequence = self.current["sequence"]
        steps = self.current["steps"]
        low, high = self.disk_range
        left, right, top, bottom = 55, 20, 40, 55
        plot_w = width - left - right
        plot_h = height - top - bottom

        line_color = self.colors.get(self.current["algorithm"], self.blue)

        c.create_text(left, 14, anchor="w", fill=self.muted, font=("Arial", 9),
                      text="Bar height = cylinder number   |   left to right = service order")

        # y-axis grid lines and cylinder labels
        for i in range(5):
            value = low + (high - low) * i / 4
            y = top + plot_h - plot_h * i / 4
            c.create_line(left, y, width - right, y, fill="#3A1A32")
            c.create_text(left - 8, y, text=str(round(value)), anchor="e",
                          fill=self.muted, font=("Arial", 9))

        c.create_line(left, top, left, top + plot_h, fill="#7A3A66")
        c.create_line(left, top + plot_h, width - right, top + plot_h, fill="#7A3A66")

        count = len(sequence)
        slot = plot_w / count
        bar_w = max(4, min(60, slot * 0.6))
        roomy = slot >= 24          # hide small labels when the bars are crowded

        for i, cylinder in enumerate(sequence):
            if i == 0:
                fill = self.white
            elif steps[i - 1]["type"] == "Boundary":
                fill = self.orange
            else:
                fill = line_color

            center = left + slot * i + slot / 2
            bar_h = max(2, (cylinder - low) / (high - low) * plot_h)
            y_top = top + plot_h - bar_h

            c.create_rectangle(center - bar_w / 2, y_top, center + bar_w / 2,
                               top + plot_h, fill=fill, outline="")

            if roomy:
                c.create_text(center, y_top - 8, text=str(cylinder),
                              fill=self.white, font=("Arial", 9, "bold"))
                c.create_text(center, top + plot_h + 14,
                              text="Start" if i == 0 else str(i),
                              fill=self.white, font=("Arial", 9))
                if i > 0:
                    c.create_text(center, top + plot_h + 30,
                                  text=f"+{steps[i - 1]['movement']}",
                                  fill=self.muted, font=("Arial", 8))

        c.create_text(width - right, height - 8, anchor="e", fill=self.muted,
                      font=("Arial", 8),
                      text="white = start   orange = disk edge")

    def draw_chart(self):
        c = self.chart
        c.delete("all")
        width = max(c.winfo_width(), 400)
        height = max(c.winfo_height(), 200)

        if not self.all_results:
            c.create_text(
                width / 2, height / 2, fill=self.muted, font=("Arial", 12),
                text="Run a simulation or click COMPARE ALL to compare algorithms.",
            )
            return

        names = list(self.all_results)
        totals = [self.all_results[n]["total"] for n in names]
        best = min(totals)
        biggest = max(totals) or 1

        label_w, right_pad, top, bottom = 80, 190, 20, 20
        row_h = (height - top - bottom) / len(names)
        bar_h = min(34, row_h * 0.6)
        max_bar = max(50, width - label_w - right_pad)

        for i, name in enumerate(names):
            result = self.all_results[name]
            y = top + i * row_h + row_h / 2
            length = result["total"] / biggest * max_bar

            c.create_text(label_w - 12, y, text=name, anchor="e",
                          fill=self.white, font=("Arial", 11, "bold"))
            c.create_rectangle(label_w, y - bar_h / 2, label_w + max(length, 2), y + bar_h / 2,
                               fill=self.colors.get(name, self.blue), outline="")

            text = f"{result['total']} cyl  (avg {result['average']:.1f})"
            if result["total"] == best:
                text += "  \u2605 lowest"
            c.create_text(label_w + length + 10, y, text=text, anchor="w",
                          fill=self.white, font=("Arial", 10, "bold"))

    # ---------- actions ----------

    def run_selected(self):
        data = self.get_inputs()
        if data is None:
            return

        try:
            self.all_results = run_all(*data)
            self.show_result(self.all_results[self.algorithm.get()])
            self.draw_chart()
            self.notebook.select(0)
        except Exception as error:
            messagebox.showerror("Simulation Error", str(error))

    def compare_all(self):
        data = self.get_inputs()
        if data is None:
            return

        try:
            self.all_results = run_all(*data)
            best = min(self.all_results.values(), key=lambda item: item["total"])

            self.algorithm.set(best["algorithm"])
            self.show_result(best)
            self.draw_chart()
            self.notebook.select(2)
            self.status.config(
                text=f"Comparison complete - lowest movement: "
                     f"{best['algorithm']} ({best['total']} cylinders)."
            )
        except Exception as error:
            messagebox.showerror("Comparison Error", str(error))

    def reset(self):
        for entry, key in (
            (self.head_entry, "head"),
            (self.queue_entry, "queue"),
            (self.minimum_entry, "min"),
            (self.maximum_entry, "max"),
        ):
            entry.delete(0, tk.END)
            entry.insert(0, self.DEFAULTS[key])

        self.direction.set("Left")
        self.algorithm.set("FCFS")

        self.current = None
        self.all_results = None
        self.disk_range = (0, 199)

        for item in self.table.get_children():
            self.table.delete(item)

        self.result_title.config(text="Simulation Results")
        self.total_value.config(text="--")
        self.average_value.config(text="--")
        self.steps_value.config(text="--")
        self.sequence_label.config(text="Service Sequence: --")

        self.show_info("FCFS")
        self.draw_path()
        self.draw_chart()
        self.status.config(text="Inputs have been reset.")


# ===================== START =====================

def show_auth(root):
    for widget in root.winfo_children():
        widget.destroy()
    AuthScreen(root, on_success=lambda name: show_app(root, name))


def show_app(root, username):
    TrackAttackApp(root, username, on_logout=lambda: show_auth(root))


if __name__ == "__main__":
    root = tk.Tk()
    show_auth(root)
    root.mainloop()

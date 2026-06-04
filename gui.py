import tkinter as tk
from tkinter import messagebox
import threading
import time

# ─── Color Palette ───────────────────────────────────────────────────────────
BG        = "#0a0a0a"
DARK_BG   = "#0d0d0d"
GREEN     = "#00ff41"
CYAN      = "#00e5ff"
RED       = "#ff2222"
DIM_GREEN = "#003b0f"
DIM_CYAN  = "#003344"
DIM_RED   = "#3b0000"
BORDER_G  = "#00ff41"
BORDER_C  = "#00e5ff"
BORDER_R  = "#ff2222"
FONT_MONO = ("Courier New", 10, "bold")
FONT_TITLE= ("Courier New", 18, "bold")
FONT_SUB  = ("Courier New", 8)
FONT_BTN  = ("Courier New", 11, "bold")
FONT_SMALL= ("Courier New", 9)

# ─── Fake user store ─────────────────────────────────────────────────────────
users = {}   # username -> password


class NeonEntry(tk.Frame):
    """A styled entry widget with neon border."""

    def __init__(self, parent, placeholder="", show="", width=24, **kwargs):
        super().__init__(parent, bg=DIM_CYAN, padx=1, pady=1)
        self._placeholder = placeholder
        self._show = show
        self._active = False

        self.entry = tk.Entry(
            self,
            font=FONT_MONO,
            bg="#0a1a22",
            fg=CYAN,
            insertbackground=CYAN,
            relief="flat",
            width=width,
            show=show,
            highlightthickness=0,
        )
        self.entry.pack(padx=6, pady=5)
        self._set_placeholder()
        self.entry.bind("<FocusIn>",  self._on_focus_in)
        self.entry.bind("<FocusOut>", self._on_focus_out)

    def _set_placeholder(self):
        if not self.entry.get():
            self.entry.config(fg="#336677", show="")
            self.entry.insert(0, self._placeholder)

    def _on_focus_in(self, _):
        if self.entry.get() == self._placeholder and self._show == "":
            pass
        if self.entry.get() == self._placeholder:
            self.entry.delete(0, tk.END)
            self.entry.config(fg=CYAN, show=self._show)
        self.config(bg=CYAN)

    def _on_focus_out(self, _):
        self.config(bg=DIM_CYAN)
        if not self.entry.get():
            self._set_placeholder()

    def get(self):
        val = self.entry.get()
        return "" if val == self._placeholder else val

    def clear(self):
        self.entry.delete(0, tk.END)
        self._set_placeholder()


def neon_button(parent, text, color, bg_dim, command, width=22):
    btn = tk.Button(
        parent,
        text=text,
        font=FONT_BTN,
        fg=color,
        bg=bg_dim,
        activebackground=color,
        activeforeground=BG,
        relief="flat",
        bd=0,
        width=width,
        cursor="hand2",
        command=command,
    )
    # Hover glow
    btn.bind("<Enter>", lambda e: btn.config(bg=color, fg=BG))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg_dim, fg=color))
    return btn


def bordered_frame(parent, color, **kwargs):
    outer = tk.Frame(parent, bg=color, padx=2, pady=2, **kwargs)
    inner = tk.Frame(outer, bg=BG)
    inner.pack(fill="both", expand=True)
    return outer, inner


# ═══════════════════════════════════════════════════════════════════════════════
class LoginFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()

    def _build(self):
        # Title bar
        bar = tk.Frame(self, bg="#111", height=28)
        bar.pack(fill="x")
        tk.Label(bar, text="⬡  Emmanuel Fake Login Detector", bg="#111",
                 fg=GREEN, font=("Courier New", 9, "bold")).pack(side="left", padx=8, pady=4)
        for sym, col in [("─","#333"),("□","#333"),("✕","#555")]:
            tk.Label(bar, text=sym, bg="#111", fg=col,
                     font=("Courier New", 9)).pack(side="right", padx=4)

        # Body
        body = tk.Frame(self, bg=BG)
        body.pack(expand=True)

        tk.Label(body, text="SECURE LOGIN SYSTEM", bg=BG,
                 fg=GREEN, font=("Courier New", 20, "bold")).pack(pady=(30, 2))
        tk.Label(body, text="AUTHORIZED ACCESS ONLY", bg=BG,
                 fg=CYAN, font=FONT_SUB).pack(pady=(0, 20))

        self.user_entry = NeonEntry(body, placeholder="  USERNAME")
        self.user_entry.pack(pady=6)

        self.pass_entry = NeonEntry(body, placeholder="  PASSWORD", show="●")
        self.pass_entry.pack(pady=6)

        self.msg_label = tk.Label(body, text="", bg=BG, fg=RED, font=FONT_SMALL)
        self.msg_label.pack(pady=4)

        neon_button(body, "LOGIN", GREEN, DIM_GREEN,
                    self._login).pack(pady=(8, 4))
        neon_button(body, "CREATE ACCOUNT", CYAN, DIM_CYAN,
                    lambda: self.app.show("register")).pack(pady=4)

        tk.Label(body, text="WARNING: UNAUTHORIZED ACCESS IS STRICTLY PROHIBITED",
                 bg=BG, fg=RED, font=("Courier New", 7)).pack(pady=(20, 10))

    def _login(self):
        u = self.user_entry.get().strip()
        p = self.pass_entry.get().strip()
        if u in users and users[u] == p:
            self.app.login_attempts = 0
            self.app.current_user = u
            self.app.show("hacking", username=u)
        else:
            self.app.login_attempts += 1
            remaining = 3 - self.app.login_attempts
            if remaining > 0:
                self.app.show("denied", attempts=remaining,
                              on_return=lambda: self.app.show("login"))
            else:
                self.app.login_attempts = 0
                self.app.show("bruteforce")


# ═══════════════════════════════════════════════════════════════════════════════
class RegisterFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()

    def _build(self):
        bar = tk.Frame(self, bg="#111", height=28)
        bar.pack(fill="x")
        tk.Label(bar, text="⬡  CREATE ACCOUNT", bg="#111",
                 fg=CYAN, font=("Courier New", 9, "bold")).pack(side="left", padx=8, pady=4)
        for sym in ["─","□","✕"]:
            tk.Label(bar, text=sym, bg="#111", fg="#333",
                     font=("Courier New", 9)).pack(side="right", padx=4)

        body = tk.Frame(self, bg=BG)
        body.pack(expand=True)

        # Lock icon (ASCII)
        tk.Label(body, text="🔒", bg=BG, fg=CYAN,
                 font=("Segoe UI Emoji", 40)).pack(pady=(20, 5))

        tk.Label(body, text="CREATE NEW ACCOUNT", bg=BG,
                 fg=CYAN, font=("Courier New", 18, "bold")).pack(pady=(0, 2))
        tk.Label(body, text="FILL IN THE DETAILS TO REGISTER", bg=BG,
                 fg="#888", font=FONT_SUB).pack(pady=(0, 20))

        for lbl, attr, show in [
            ("USERNAME",         "r_user", ""),
            ("PASSWORD",         "r_pass", "●"),
            ("CONFIRM PASSWORD", "r_conf", "●"),
        ]:
            row = tk.Frame(body, bg=BG)
            row.pack(pady=5)
            tk.Label(row, text=lbl, bg=BG, fg=CYAN,
                     font=("Courier New", 9, "bold"), width=16,
                     anchor="e").pack(side="left", padx=6)
            e = NeonEntry(row, show=show, width=20)
            e.pack(side="left")
            setattr(self, attr, e)

        self.msg = tk.Label(body, text="", bg=BG, fg=RED, font=FONT_SMALL)
        self.msg.pack(pady=6)

        neon_button(body, "CREATE ACCOUNT", CYAN, DIM_CYAN,
                    self._register, width=20).pack(pady=8)

        tk.Label(body, text="🔒  SECURE ENCRYPTION ENABLED",
                 bg=BG, fg="#336677", font=("Courier New", 7)).pack(pady=(10, 0))

    def _register(self):
        u  = self.r_user.get().strip()
        p  = self.r_pass.get().strip()
        c  = self.r_conf.get().strip()
        if not u:
            self.msg.config(text="⚠  USERNAME CANNOT BE EMPTY"); return
        if u in users:
            self.msg.config(text="⚠  USERNAME ALREADY EXISTS"); return
        if len(p) < 4:
            self.msg.config(text="⚠  PASSWORD TOO SHORT (MIN 4)"); return
        if p != c:
            self.msg.config(text="⚠  PASSWORDS DO NOT MATCH"); return
        users[u] = p
        messagebox.showinfo("SUCCESS",
                            f"Account '{u}' created!\nYou can now log in.")
        self.app.show("login")


# ═══════════════════════════════════════════════════════════════════════════════
class AccessDeniedFrame(tk.Frame):
    def __init__(self, parent, app, attempts=2, on_return=None):
        super().__init__(parent, bg=BG)
        self.app = app
        self.on_return = on_return
        self._build(attempts)

    def _build(self, attempts):
        bar = tk.Frame(self, bg="#111", height=28)
        bar.pack(fill="x")
        tk.Label(bar, text="⬡  LOGIN PROCESS", bg="#111",
                 fg=RED, font=("Courier New", 9, "bold")).pack(side="left", padx=8, pady=4)

        body = tk.Frame(self, bg=BG)
        body.pack(expand=True)

        # X icon
        tk.Label(body, text="✕", bg=BG, fg=RED,
                 font=("Courier New", 60, "bold")).pack(pady=(20, 5))

        tk.Label(body, text="ACCESS DENIED", bg=BG,
                 fg=RED, font=("Courier New", 22, "bold")).pack()
        tk.Label(body, text="INVALID USERNAME OR PASSWORD", bg=BG,
                 fg=RED, font=FONT_SMALL).pack(pady=4)

        tk.Label(body, text="RETURNING TO LOGIN...", bg=BG,
                 fg=RED, font=FONT_SMALL).pack(pady=(20, 4))

        # Progress bar
        pb_frame = tk.Frame(body, bg=BG)
        pb_frame.pack()
        self.canvas = tk.Canvas(pb_frame, width=260, height=18,
                                bg=DIM_RED, highlightthickness=1,
                                highlightbackground=RED)
        self.canvas.pack()
        self.bar_rect = self.canvas.create_rectangle(
            2, 2, 2, 16, fill=RED, outline="")

        tk.Label(body, text=f"ATTEMPTS LEFT: {attempts}", bg=BG,
                 fg=RED, font=("Courier New", 10, "bold")).pack(pady=8)

        self._animate(0)

    def _animate(self, step):
        total = 50
        if step <= total:
            x = int((step / total) * 256) + 2
            self.canvas.coords(self.bar_rect, 2, 2, x, 16)
            self.after(40, self._animate, step + 1)
        else:
            self.after(400, self._done)

    def _done(self):
        if self.on_return:
            self.on_return()


# ═══════════════════════════════════════════════════════════════════════════════
class HackingFrame(tk.Frame):
    STEPS = [
        "> CONNECTING TO SECURE SERVER...",
        "> BYPASSING FIREWALL...",
        "> DECRYPTING DATA...",
        "> VERIFYING CREDENTIALS...",
        "> ACCESSING SYSTEM...",
    ]

    def __init__(self, parent, app, username="CYBERUSER"):
        super().__init__(parent, bg=BG)
        self.app = app
        self.username = username.upper()
        self._build()

    def _build(self):
        bar = tk.Frame(self, bg="#111", height=28)
        bar.pack(fill="x")
        tk.Label(bar, text="⬡  HACKING SIMULATION", bg="#111",
                 fg=CYAN, font=("Courier New", 9, "bold")).pack(side="left", padx=8, pady=4)

        body = tk.Frame(self, bg=BG, padx=40)
        body.pack(expand=True, fill="both")

        tk.Label(body, text="INITIALIZING HACKING PROTOCOL...",
                 bg=BG, fg=GREEN, font=FONT_MONO, anchor="w").pack(
                     pady=(30, 10), fill="x")

        self.step_labels = []
        self.ok_labels = []
        for s in self.STEPS:
            row = tk.Frame(body, bg=BG)
            row.pack(fill="x", pady=2)
            lbl = tk.Label(row, text=s, bg=BG, fg="#335533",
                           font=FONT_MONO, anchor="w")
            lbl.pack(side="left")
            ok = tk.Label(row, text="", bg=BG, fg=GREEN,
                          font=FONT_MONO, anchor="e")
            ok.pack(side="right")
            self.step_labels.append(lbl)
            self.ok_labels.append(ok)

        tk.Label(body, text="\nLOADING...", bg=BG, fg=CYAN,
                 font=FONT_MONO, anchor="w").pack(fill="x", pady=(16, 4))

        pb_frame = tk.Frame(body, bg=BG)
        pb_frame.pack(fill="x")
        self.canvas = tk.Canvas(pb_frame, width=300, height=20,
                                bg=DIM_CYAN, highlightthickness=1,
                                highlightbackground=CYAN)
        self.canvas.pack(side="left")
        self.bar = self.canvas.create_rectangle(2, 2, 2, 18, fill=CYAN, outline="")
        self.pct_lbl = tk.Label(pb_frame, text="0%", bg=BG, fg=CYAN,
                                font=FONT_MONO)
        self.pct_lbl.pack(side="left", padx=8)

        self.after(300, self._start)

    def _start(self):
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        total_steps = len(self.STEPS)
        for i, lbl in enumerate(self.step_labels):
            time.sleep(0.5)
            self.after(0, lbl.config, {"fg": GREEN})
            # animate bar for this segment
            start_pct = int(i / total_steps * 100)
            end_pct   = int((i + 1) / total_steps * 100)
            for p in range(start_pct, end_pct + 1):
                time.sleep(0.018)
                x = int(p / 100 * 296) + 2
                self.after(0, self.canvas.coords, self.bar, 2, 2, x, 18)
                self.after(0, self.pct_lbl.config, {"text": f"{p}%"})
            if i < total_steps - 1:
                self.after(0, self.ok_labels[i].config, {"text": "[ OK ]"})
            else:
                self.after(0, self.ok_labels[i].config,
                           {"text": "[.........]", "fg": CYAN})
        time.sleep(0.6)
        self.after(0, self.app.show, "granted", self.username)


# ═══════════════════════════════════════════════════════════════════════════════
class AccessGrantedFrame(tk.Frame):
    def __init__(self, parent, app, username="CYBERUSER"):
        super().__init__(parent, bg=BG)
        self.app = app
        self.username = username.upper()
        self._build()

    def _build(self):
        bar = tk.Frame(self, bg="#111", height=28)
        bar.pack(fill="x")
        tk.Label(bar, text="⬡  ACCESS GRANTED", bg="#111",
                 fg=GREEN, font=("Courier New", 9, "bold")).pack(side="left", padx=8, pady=4)

        body = tk.Frame(self, bg=BG)
        body.pack(expand=True)

        # World map (ASCII art approximation)
        map_art = (
            "  ·  ████  ██████  ██   ████  ███   ███  ██ \n"
            " ████████████████████████████████████████████\n"
            "  ██████████████████████████████████████████ \n"
            "    █████████████████  ████████████████████  \n"
            "      ██████████████    ██████████████████   \n"
            "       █████████████     █████████████████   \n"
            "         ██████████        ██████████████    \n"
        )
        tk.Label(body, text=map_art, bg=BG, fg="#003b0f",
                 font=("Courier New", 7), justify="left").pack(pady=(20, 0))

        tk.Label(body, text="ACCESS\nGRANTED", bg=BG,
                 fg=GREEN, font=("Courier New", 46, "bold"),
                 justify="center").pack(pady=10)

        tk.Label(body, text=f"WELCOME, {self.username}", bg=BG,
                 fg=CYAN, font=("Courier New", 13, "bold")).pack()
        tk.Label(body, text="YOU HAVE SUCCESSFULLY ACCESSED THE SYSTEM",
                 bg=BG, fg="#336644", font=FONT_SMALL).pack(pady=4)

        neon_button(body, "LOG OUT", RED, DIM_RED,
                    lambda: self.app.show("login"), width=18).pack(pady=20)


# ═══════════════════════════════════════════════════════════════════════════════
class BruteForceFrame(tk.Frame):
    """Shown after 3 consecutive failed login attempts."""

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()

    def _build(self):
        bar = tk.Frame(self, bg="#111", height=28)
        bar.pack(fill="x")
        tk.Label(bar, text="⬡  Emmanuel Fake Login Detector", bg="#111",
                 fg=RED, font=("Courier New", 9, "bold")).pack(side="left", padx=8, pady=4)
        for sym, col in [("─","#333"),("□","#333"),("✕","#555")]:
            tk.Label(bar, text=sym, bg="#111", fg=col,
                     font=("Courier New", 9)).pack(side="right", padx=4)

        body = tk.Frame(self, bg=BG)
        body.pack(expand=True)

        # Flashing warning icon
        self.icon_lbl = tk.Label(body, text="⚠", bg=BG, fg=RED,
                                 font=("Courier New", 54, "bold"))
        self.icon_lbl.pack(pady=(30, 6))
        self._flash(True)

        tk.Label(body, text="ERROR — BRUTE-FORCE DETECTED", bg=BG,
                 fg=RED, font=("Courier New", 16, "bold")).pack()
        tk.Label(body, text="─" * 38, bg=BG, fg="#440000",
                 font=("Courier New", 9)).pack(pady=4)

        details = [
            "> SUSPICIOUS ACTIVITY LOGGED",
            "> IP ADDRESS FLAGGED & REPORTED",
            "> SESSION TERMINATED IMMEDIATELY",
            "> AUTHORITIES HAVE BEEN NOTIFIED",
        ]
        for line in details:
            tk.Label(body, text=line, bg=BG, fg="#cc2222",
                     font=("Courier New", 9, "bold")).pack(anchor="w", padx=60)

        tk.Label(body, text="\nACCESS PERMANENTLY BLOCKED FOR THIS SESSION",
                 bg=BG, fg="#550000", font=("Courier New", 8)).pack()

        # Countdown to close
        self.countdown = 10
        self.cd_lbl = tk.Label(body,
                               text=f"CLOSING IN {self.countdown}s...",
                               bg=BG, fg=RED,
                               font=("Courier New", 10, "bold"))
        self.cd_lbl.pack(pady=(18, 6))

        neon_button(body, "CLOSE APPLICATION", RED, DIM_RED,
                    self.app.destroy, width=22).pack(pady=4)

        self._tick()

    def _flash(self, visible):
        color = RED if visible else BG
        self.icon_lbl.config(fg=color)
        self.after(500, self._flash, not visible)

    def _tick(self):
        if self.countdown > 0:
            self.countdown -= 1
            self.cd_lbl.config(text=f"CLOSING IN {self.countdown}s...")
            self.after(1000, self._tick)
        else:
            self.app.destroy()


# ═══════════════════════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Emmanuel Fake Login Detector v2.0")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.geometry("480x520")
        self.current_user = None
        self.login_attempts = 0
        self._frame = None
        self.show("login")

    # ── footer ────────────────────────────────────────────────────────────────
    def _make_footer(self):
        tk.Label(self, text="NEON HACKER SYSTEM v2.0",
                 bg=BG, fg="#224422",
                 font=("Courier New", 8)).pack(side="bottom", pady=4)

    # ── frame switcher ────────────────────────────────────────────────────────
    def show(self, screen, *args, **kwargs):
        if self._frame:
            self._frame.destroy()

        if screen == "login":
            self._frame = LoginFrame(self, self)
        elif screen == "register":
            self._frame = RegisterFrame(self, self)
        elif screen == "denied":
            self._frame = AccessDeniedFrame(
                self, self,
                attempts=kwargs.get("attempts", 2),
                on_return=kwargs.get("on_return"))
        elif screen == "bruteforce":
            self._frame = BruteForceFrame(self, self)
        elif screen == "hacking":
            username = args[0] if args else kwargs.get("username", "CYBERUSER")
            self._frame = HackingFrame(self, self, username=username)
        elif screen == "granted":
            username = args[0] if args else kwargs.get("username", "CYBERUSER")
            self._frame = AccessGrantedFrame(self, self, username=username)

        self._frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    # Seed a demo account so you can log in right away
    users["admin"] = "1234"
    app = App()
    app.mainloop()
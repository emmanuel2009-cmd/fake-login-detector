import tkinter as tk
import hashlib
import json
import os

FILE = "users.json"
failed_attempts = 0

users = {}

if os.path.exists(FILE):
    with open(FILE, "r") as f:
        users = json.load(f)

def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

def login():
    global failed_attempts

    username = entry_user.get().lower()
    password = entry_pass.get()

    if username in users and users[username] == hash_password(password):
        result_label.config(text="ACCESS GRANTED", fg="lime")
        login_btn.config(state="disabled")

    else:
        failed_attempts += 1
        result_label.config(text="ACCESS DENIED", fg="red")

        if failed_attempts >= 3:
            result_label.config(text="BRUTE FORCE DETECTED", fg="orange")
            login_btn.config(state="disabled")

def create_account():
    username = entry_user.get().lower()
    password = entry_pass.get()

    users[username] = hash_password(password)

    with open(FILE, "w") as f:
        json.dump(users, f)

    result_label.config(text="ACCOUNT CREATED", fg="cyan")

# ---------------- GUI ----------------
root = tk.Tk()
root.title("NEON SECURITY SYSTEM")
root.geometry("450x300")
root.configure(bg="black")

tk.Label(root, text="SECURE LOGIN", fg="cyan", bg="black",
         font=("Arial", 18)).pack(pady=10)

entry_user = tk.Entry(root)
entry_user.pack()

entry_pass = tk.Entry(root, show="*")
entry_pass.pack()

tk.Button(root, text="LOGIN", command=login, bg="green", fg="white").pack(pady=5)
tk.Button(root, text="CREATE ACCOUNT", command=create_account, bg="blue", fg="white").pack(pady=5)

result_label = tk.Label(root, text="", bg="black", fg="white", font=("Arial", 14))
result_label.pack(pady=20)

root.mainloop()
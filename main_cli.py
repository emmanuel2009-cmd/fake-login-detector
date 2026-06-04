import time
import json
import os
import hashlib
import re

FILE = "users.json"
LOG_FILE = "logs.txt"

# ----------------------------
# HASH FUNCTION
# ----------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ----------------------------
# LOAD USERS
# ----------------------------
def load_users():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r") as f:
        return json.load(f)

# ----------------------------
# SAVE USERS
# ----------------------------
def save_users(users):
    with open(FILE, "w") as f:
        json.dump(users, f)

# ----------------------------
# LOG SYSTEM
# ----------------------------
def log_event(message):
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")

# ----------------------------
# PASSWORD STRENGTH CHECKER
# ----------------------------
def check_password_strength(password):
    if len(password) < 6:
        return "Weak"
    if re.search(r"[A-Z]", password) and re.search(r"[0-9]", password):
        return "Strong"
    return "Medium"

users = load_users()

failed_attempts = 0
blocked = False

# ----------------------------
# MENU
# ----------------------------
while True:

    print("\n==============================")
    print(" CYBER SECURITY TOOL SUITE ")
    print("==============================")
    print("1. Create Account")
    print("2. Login")
    print("3. Exit")

    choice = input("Select option: ")

    # ----------------------------
    # CREATE ACCOUNT
    # ----------------------------
    if choice == "1":
        username = input("Create Username: ").lower()

        if username in users:
            print("User already exists!")
        else:
            password = input("Create Password: ")

            strength = check_password_strength(password)
            print("Password Strength:", strength)

            users[username] = hash_password(password)
            save_users(users)

            print("Account created successfully!")
            log_event(f"ACCOUNT CREATED: {username}")

    # ----------------------------
    # LOGIN SYSTEM
    # ----------------------------
    elif choice == "2":

        if blocked:
            print("\n⛔ ACCESS DENIED - SYSTEM LOCKED")
            continue

        while True:
            login_username = input("Enter Username: ").lower()
            login_password = input("Enter Password: ")

            hashed = hash_password(login_password)

            if login_username in users and users[login_username] == hashed:
                print("\n[+] LOGIN SUCCESSFUL")
                log_event(f"LOGIN SUCCESS: {login_username}")
                failed_attempts = 0
                break

            else:
                failed_attempts += 1
                print("[-] LOGIN FAILED")
                print("Attempt:", failed_attempts)

                log_event(f"FAILED LOGIN: {login_username}")

                # ----------------------------
                # REAL-TIME ALERT SYSTEM
                # ----------------------------
                if failed_attempts == 1:
                    print("⚠ WARNING: Suspicious login activity detected")

                if failed_attempts == 2:
                    print("⚠ CRITICAL WARNING: Possible brute-force attack")

                if failed_attempts >= 3:
                    print("\n🚨 SECURITY ALERT TRIGGERED")
                    print("🚫 USER TEMPORARILY BLOCKED")

                    log_event("BLOCK EVENT TRIGGERED")

                    blocked = True

                    # simulate auto-unblock after delay
                    time.sleep(5)
                    print("\n🔓 SYSTEM AUTO-UNLOCKED")

                    blocked = False
                    failed_attempts = 0
                    break

    # ----------------------------
    # EXIT
    # ----------------------------
    elif choice == "3":
        print("Exiting system...")
        break

    else:
        print("Invalid option!")
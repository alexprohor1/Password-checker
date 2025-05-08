import tkinter as tk
from tkinter import messagebox
import math
from collections import Counter

# Lowercase variables (previously uppercase)
special_char = "!@#$%^&*(),.?\":{}|<>"
common_pw_file = "password_list.txt"
leaked_pw_file = "000webhost.txt"

# Approximate attack speed (1 billion guesses per second)
guesses_per_sec = 1e9
month = 30 * 24 * 3600
year = 365 * 24 * 3600

# Load common and leaked passwords (skip errors if files are missing)
try:
    with open(common_pw_file, "r", encoding="utf-8") as f:
        common_pw = set(f.read().splitlines())
except:
    common_pw = set()

try:
    with open(leaked_pw_file, "r", encoding="utf-8") as f:
        leaked_pw = set(f.read().splitlines())
except:
    leaked_pw = set()
#Function which calculates the entropy of the password based on the formula: entropy = (length) X log2(character set size)
def entropy(password):
    length = len(password)
    charset = 0
    if any(c.islower() for c in password):
        charset += 26
    if any(c.isupper() for c in password):
        charset += 26
    if any(c.isdigit() for c in password):
        charset += 10
    if any(c in special_char for c in password):
        charset += len(special_char)
    
    return length * math.log2(charset) if charset else 0
#Function which calculates the penalty based on repeated characters
def penalty(password):
    counts = Counter(password)
    # Each repeated character (beyond the first occurrence) adds a penalty of 2
    return sum((count - 1) * 2 for count in counts.values() if count > 1)
#Function wich calculates the time it takes for the password to be guessed based on the formula 2 ** entropy / guesses per sec
def crack_time(entropy_val):
    if entropy_val > 0:
        return (2 ** entropy_val) / guesses_per_sec
    else:
        return 0
    

def format_time(seconds):
    #Formating time from seconds in min, hours, days and years
    if seconds < 1:
        return f"{seconds * 1000:.1f} ms"
    elif seconds < 60:
        return f"{seconds:.1f} sec"
    elif seconds < 3600:
        return f"{seconds / 60:.1f} min"
    elif seconds < 86400:
        return f"{seconds / 3600:.1f} hrs"
    elif seconds < year:
        return f"{seconds / 86400:.1f} days"
    else:
        return f"{seconds / year:.1f} years"

def check_password():
    # Strips away potential space from the beginning and the end of the password
    pw = entry.get().strip()
    if not pw:
        messagebox.showwarning("Error", "Enter a password!")
        return

    # Checks if is in common password list
    if pw in common_pw:
        result_label.config(text="Very Weak\n(Found in common passwords)", fg="red")
        return

    base_entropy = entropy(pw)
    repeat_penalty = penalty(pw)

    # Calculate final entropy
    final_entropy = max(0, base_entropy - repeat_penalty)
    # 20 bits penalty if the password is found in the leaked passwords list
    if pw in leaked_pw:
        final_entropy -= 45 

    # Setting minimum entropy treshold at 0
    final_entropy = max(0, final_entropy)

    # Calculating the estimation of time that takes to succesfully guess the password
    crack_time_val = crack_time(final_entropy)

    # Classifying the password strength result based on the time it takes to guess
    if crack_time_val < month:
        strength, color = ("Weak", "red")
    elif crack_time_val < year:
        strength, color = ("Moderate", "orange")
    else:
        strength, color = ("Strong", "green")

    result_label.config(
        text=(
            f"{strength}\n"
            f"Crack Time: {format_time(crack_time_val)}\n"
            f"Entropy: {final_entropy:.2f} bits"
        ),
        fg=color
    )

# GUI Setup
root = tk.Tk()
root.title("Password Checker")
root.geometry("400x300")
root.resizable(False, False)

tk.Label(root, text="Enter password:", font=("Arial", 12)).pack(pady=10)
entry = tk.Entry(root, show="*", font=("Arial", 12), width=30)
entry.pack(pady=5)

tk.Button(root, text="Check Strength", command=check_password,
font=("Arial", 12), bg="#0078D7", fg="white").pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 10), wraplength=350)
result_label.pack(pady=20)

root.mainloop()

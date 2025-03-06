import random
import tkinter as tk
from tkinter import messagebox

# Word categories
words = {
    "Animals": ["cat", "dog", "zebra", "dolphin", "tiger"],
    "Fruits": ["banana", "apple", "mango", "watermelon", "blueberry"],
    "Countries": ["canada", "germany", "spain", "brazil", "japan"]
}

# Initialize game state
category = random.choice(list(words.keys()))
word = random.choice(words[category])
word_display = ["_" for _ in word]
guessed_letters = []
wrong_attempts = 0
max_attempts = 5
time_left = 90  # Time limit in seconds
hint_used = False

def update_timer():
    global time_left
    if time_left > 0:
        time_left -= 1
        timer_label.config(text=f"⏳ Time Left: {time_left}s")
        root.after(1000, update_timer)
    else:
        messagebox.showinfo("Hangman", f"Time's up! The word was: {word}")
        restart_game()

def guess_letter(letter):
    global wrong_attempts
    if letter in guessed_letters:
        return
    guessed_letters.append(letter)
    if letter in word:
        for i, l in enumerate(word):
            if l == letter:
                word_display[i] = letter
    else:
        wrong_attempts += 1
    update_display()

    if "_" not in word_display:
        messagebox.showinfo("Hangman", f"🎉 You guessed the word: {word}!")
        restart_game()
    elif wrong_attempts >= max_attempts:
        messagebox.showinfo("Hangman", f"💀 Game Over! The word was: {word}")
        restart_game()

def get_hint():
    global hint_used
    if not hint_used:
        hint_used = True
        hint_label.config(text=f"💡 Hint: The first letter is '{word[0]}'", fg="yellow")
    else:
        messagebox.showinfo("Hint", "You already used your hint!")

def update_display():
    word_label.config(text=" ".join(word_display))
    guessed_label.config(text="Guessed Letters: " + ", ".join(guessed_letters))

def restart_game():
    global category, word, word_display, guessed_letters, wrong_attempts, time_left, hint_used
    category = random.choice(list(words.keys()))
    word = random.choice(words[category])
    word_display = ["_" for _ in word]
    guessed_letters = []
    wrong_attempts = 0
    time_left = 90
    hint_used = False
    category_label.config(text=f"📌 Category: {category}")
    hint_label.config(text="💡 Hint: Press the button to get a hint", fg="white")
    update_display()
    update_timer()

# GUI Setup
root = tk.Tk()
root.title("Hangman Game")
root.geometry("600x600")
root.configure(bg="#222831")  # Dark Gray Background

# UI Elements
category_label = tk.Label(root, text=f"📌 Category: {category}", font=("Arial", 14, "bold"), fg="lightblue", bg="#222831")
category_label.pack(pady=10)

hint_label = tk.Label(root, text="💡 Hint: Press the button to get a hint", font=("Arial", 12), fg="white", bg="#222831")
hint_label.pack()

word_label = tk.Label(root, text=" ".join(word_display), font=("Arial", 24, "bold"), fg="white", bg="#222831")
word_label.pack(pady=20)

guessed_label = tk.Label(root, text="Guessed Letters: ", font=("Arial", 12), fg="orange", bg="#222831")
guessed_label.pack()

# Timer
timer_label = tk.Label(root, text=f"⏳ Time Left: {time_left}s", font=("Arial", 12, "bold"), fg="red", bg="#222831")
timer_label.pack()

# Letter Buttons
buttons_frame = tk.Frame(root, bg="#222831")
buttons_frame.pack(pady=20)

letters = "abcdefghijklmnopqrstuvwxyz"
row_count = 0
col_count = 0
for letter in letters:
    tk.Button(
        buttons_frame, text=letter.upper(), command=lambda l=letter: guess_letter(l),
        width=3, font=("Arial", 12, "bold"), bg="#393E46", fg="white", relief="raised"
    ).grid(row=row_count, column=col_count, padx=2, pady=2)
    
    col_count += 1
    if col_count > 7:
        col_count = 0
        row_count += 1

# Control Buttons
button_frame = tk.Frame(root, bg="#222831")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Restart", command=restart_game, bg="#00ADB5", fg="white", font=("Arial", 14, "bold")).pack(side=tk.LEFT, padx=10)
tk.Button(button_frame, text="Hint", command=get_hint, bg="#F08A5D", fg="white", font=("Arial", 14, "bold")).pack(side=tk.LEFT, padx=10)

update_display()
update_timer()
root.mainloop()

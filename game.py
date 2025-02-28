import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

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
time_left = 90  # Time limit in seconds (1m 30s)
hint_used = False

def update_timer():
    global time_left
    if time_left > 0:
        time_left -= 1
        timer_label.config(text=f"Time Left: {time_left}s")
        root.after(1000, update_timer)
    else:
        messagebox.showinfo("Hangman", f"⏳ Time's up! The word was: {word}")
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
        messagebox.showinfo("Hangman", f"🎉 Congratulations! You guessed the word: {word}")
        restart_game()
    elif wrong_attempts >= max_attempts:
        messagebox.showinfo("Hangman", f"💀 Game Over! The word was: {word}")
        restart_game()

def get_hint():
    global hint_used
    if not hint_used:
        hint_used = True
        hint_label.config(text=f"Hint: The first letter is '{word[0]}'")
    else:
        messagebox.showinfo("Hint", "You have already used your hint!")

def update_display():
    word_label.config(text=" ".join(word_display), fg="white")
    guessed_label.config(text="Guessed Letters: " + ", ".join(guessed_letters), fg="yellow")

def restart_game():
    global category, word, word_display, guessed_letters, wrong_attempts, time_left, hint_used
    category = random.choice(list(words.keys()))
    word = random.choice(words[category])
    word_display = ["_" for _ in word]
    guessed_letters = []
    wrong_attempts = 0
    time_left = 90  # Reset timer
    hint_used = False
    category_label.config(text=f"Category: {category}")
    hint_label.config(text="Hint: Press the button to get a hint")
    update_display()
    update_timer()

# GUI Setup
root = tk.Tk()
root.title("Hangman Game")
root.geometry("600x600")

# Load and set background image
bg_image = Image.open("backg.jpg").resize((600, 600))
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=600, height=600)
canvas.pack(fill="both", expand=True)
bg_canvas_image = canvas.create_image(0, 0, image=bg_photo, anchor=tk.NW)

# UI Elements
category_label = tk.Label(root, text=f"Category: {category}", font=("Arial", 14), fg="red", bg="black")
category_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

hint_label = tk.Label(root, text="Hint: Press the button to get a hint", font=("Arial", 12), fg="lightblue", bg="black")
hint_label.place(relx=0.5, rely=0.15, anchor=tk.CENTER)

word_label = tk.Label(root, text=" ".join(word_display), font=("Arial", 20), fg="white", bg="black")
word_label.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

guessed_label = tk.Label(root, text="Guessed Letters: ", font=("Arial", 12), fg="yellow", bg="black")
guessed_label.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

# Timer in top-right corner
timer_label = tk.Label(root, text=f"Time Left: {time_left}s", font=("Arial", 12), fg="red", bg="black")
timer_label.place(relx=0.95, rely=0.05, anchor=tk.NE)

buttons_frame = tk.Frame(root, bg="black")
buttons_frame.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

# Arrange buttons in multiple rows
letters = "abcdefghijklmnopqrstuvwxyz"
row_count = 0
col_count = 0
for letter in letters:
    tk.Button(buttons_frame, text=letter.upper(), command=lambda l=letter: guess_letter(l), width=3, bg="#1E90FF", fg="white", font=("Arial", 12, "bold")).grid(row=row_count, column=col_count, padx=2, pady=2)
    col_count += 1
    if col_count > 7:
        col_count = 0
        row_count += 1

button_frame = tk.Frame(root, bg="black")
button_frame.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

tk.Button(button_frame, text="Restart", command=restart_game, bg="green", fg="white", font=("Arial", 14, "bold")).pack(side=tk.LEFT, padx=10)
tk.Button(button_frame, text="Hint", command=get_hint, bg="orange", fg="white", font=("Arial", 14, "bold")).pack(side=tk.LEFT, padx=10)

update_display()
update_timer()
root.mainloop()
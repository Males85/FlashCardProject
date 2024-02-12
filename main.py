from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
word = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    new_data = original_data.to_dict(orient="records")
else:
    new_data = data.to_dict(orient="records")


def next_card_known():
    new_data.remove(word)
    words_to_learn = pandas.DataFrame(new_data)
    words_to_learn.to_csv("data/words_to_learn.csv", index=False)
    next_card()


def next_card():
    global word, flip_timer
    window.after_cancel(flip_timer)    #Canceling 3 sec delay to flip a card
    word = random.choice(new_data)
    canvas.itemconfig(canvas_image, image=flash_card_image)
    canvas.itemconfig(title_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=word["French"], fill="black")
    flip_timer = window.after(3000, func=flip_card)       #Again enabling flip card action


def flip_card():
    canvas.itemconfig(canvas_image, image=flipped_card_image)
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=word["English"], fill="white")


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)


#Flash card
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
flash_card_image = PhotoImage(file="images/card_front.png")
flipped_card_image = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=flash_card_image)
title_text = canvas.create_text(400, 150, font=("Arial", 40, "italic"), text="")
word_text = canvas.create_text(400, 263, font=("Arial", 60, "bold"), text="")
canvas.grid(row=0, column=0, columnspan=2)

#Buttons
checkmark_image = PhotoImage(file="images/right.png")
known_button = Button(image=checkmark_image, highlightthickness=0, bd=0, command=next_card_known)
known_button.grid(row=1, column=0)

wrong_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=wrong_image, highlightthickness=0, bd=0, command=next_card)
unknown_button.grid(row=1, column=1)

next_card()


window.mainloop()

import copy
import math
import tkinter as tk
from tkinter import messagebox, Button
from pygame import mixer
from PIL import ImageTk, Image


class NumberGame:
    def __init__(self):
        self.toggle_sound = False
        self.score_array = [-12, -17, -11, 1999, 100, 1000]
        self.subtraction_array = [-132, 2, 3, 55, 99, 199]
        self.depth = int(math.log(len(self.score_array), 2))
        self.game_state = copy.deepcopy(self.score_array)
        self.subtraction_state = copy.deepcopy(self.subtraction_array)
        self.selected = [False] * len(self.score_array)
        self.selected_sub = [False] * len(self.subtraction_array)
        self.humanTotalScore1 = 0
        self.humanTotalScore2 = 0
        self.aiTotalScore = 0
        self.current_player = "AI"

        self.window = tk.Tk()
        self.window.title("Number Game")
        self.window.geometry("1100x600")
        self.window.size()
        self.window.configure(bg="#ffffff")

        # Initialize mixer for sound playback
        mixer.init()

        # Load the sound icons and reduce their size by 20 pixels
        self.sound_icon = tk.PhotoImage(file="sound_on.png").subsample(18)
        self.mute_icon = tk.PhotoImage(file="sound_off.png").subsample(18)

        # Set initial sound state
        self.sound_on = True

        # Create the sound button
        self.sound_button_image = self.sound_icon  # Store a reference to the image object
        self.sound_button = tk.Button(self.window, image=self.sound_button_image, command=self.toggle_sound, bg="black")
        self.sound_button.place(relx=self.window.winfo_width() - .10, rely=0.05, anchor="ne")

        # Create labels and buttons
        self.create_labels()
        self.create_buttons()

        self.update_scores()
        self.window.after(1000, self.ai_turn)
        self.window.mainloop()

    def create_labels(self):
        background_image = tk.PhotoImage(file="back.png")
        canvas = tk.Canvas(self.window, width=700, height=3500)
        canvas.pack(fill=tk.BOTH, expand=True)
        canvas.create_image(0, 0, image=background_image, anchor='nw')

        self.score_array_text = tk.Label(self.window, text="Score Array", bg="#2ed573",
                                         fg="white",
                                         font=("8514oem", 14, "bold"), padx=10, pady=5, bd=1,
                                         relief="solid")
        self.score_array_text.place(relx=0.019, rely=0.500, anchor="w")

        self.subtract_array_text = tk.Label(self.window, text="Subtraction Array", bg="#ff4757",
                                            fg="white",
                                            font=("8514oem", 14, "bold"), padx=10, pady=5, bd=1,
                                            relief="solid")
        self.subtract_array_text.place(relx=0.019, rely=0.699, anchor="w")

        self.player_label = tk.Label(self.window, text="Current player: " + self.current_player, bg="#f8f9fa",
                                     fg="#495057",
                                     font=("8514oem", 14, "bold"), padx=10, pady=5, bd=1,
                                     relief="solid")
        self.player_label.place(relx=0.5, rely=0.15, anchor="center")

    def create_buttons(self):
        self.score_buttons = []
        self.subtract_buttons = []

        for i in range(len(self.score_array)):
            button = Button(self.window, text=str(self.score_array[i]), width=8, height=2,
                            command=lambda index=i: self.select_score(index))
            button.place(relx=0.019 + i * 0.056, rely=0.550, anchor="w")
            self.score_buttons.append(button)

        for i in range(len(self.subtraction_array)):
            button = Button(self.window, text=str(self.subtraction_array[i]), width=8, height=2,
                            command=lambda index=i: self.select_subtraction(index))
            button.place(relx=0.019 + i * 0.056, rely=0.749, anchor="w")
            self.subtract_buttons.append(button)

    def update_scores(self):
        self.player_label.config(text="Current player: " + self.current_player)
        self.player_label.update()

        for i in range(len(self.score_array)):
            if self.selected[i]:
                self.score_buttons[i].config(state="disabled")
            else:
                self.score_buttons[i].config(state="normal")

        for i in range(len(self.subtraction_array)):
            if self.selected_sub[i]:
                self.subtract_buttons[i].config(state="disabled")
            else:
                self.subtract_buttons[i].config(state="normal")

    def select_score(self, index):
        if self.current_player == "Human":
            self.selected[index] = True
            self.humanTotalScore1 += self.score_array[index]
            self.score_array[index] = 0
            self.current_player = "AI"
            self.update_scores()
            self.ai_turn()

    def select_subtraction(self, index):
        if self.current_player == "Human":
            self.selected_sub[index] = True
            self.humanTotalScore2 += self.subtraction_array[index]
            self.subtraction_array[index] = 0
            self.current_player = "AI"
            self.update_scores()
            self.ai_turn()

    def ai_turn(self):
        if self.current_player == "AI":
            if sum(self.score_array) > sum(self.subtraction_array):
                max_score = max(self.score_array)
                index = self.score_array.index(max_score)
                self.selected[index] = True
                self.aiTotalScore += max_score
                self.score_array[index] = 0
            else:
                max_subtraction = max(self.subtraction_array)
                index = self.subtraction_array.index(max_subtraction)
                self.selected_sub[index] = True
                self.aiTotalScore -= max_subtraction
                self.subtraction_array[index] = 0

            if self.current_player == "AI":
                self.current_player = "Human"

            self.update_scores()

            if sum(self.score_array) + sum(self.subtraction_array) > 0:
                self.window.after(1000, self.ai_turn)
            else:
                self.end_game()

    def end_game(self):
        self.score_array_text.config(text="Human Score: " + str(self.humanTotalScore1))
        self.subtract_array_text.config(text="AI Score: " + str(self.aiTotalScore))

        if self.humanTotalScore1 + self.humanTotalScore2 > self.aiTotalScore:
            messagebox.showinfo("Game Over", "Congratulations! You won!")
        elif self.humanTotalScore1 + self.humanTotalScore2 < self.aiTotalScore:
            messagebox.showinfo("Game Over", "Oops! AI won!")
        else:
            messagebox.showinfo("Game Over", "It's a tie!")

        self.window.quit()


game = Game()


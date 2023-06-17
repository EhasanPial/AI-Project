import copy
import math
import tkinter as tk
from tkinter import messagebox, Button
from pygame import mixer
from PIL import ImageTk, Image
from tkinter import *


def checkWins():
    if aiTotalScore > humanTotalScore1 and aiTotalScore > humanTotalScore2:
        gameOverSound()
        #messagebox.showinfo("Game Over", "...........AI WINS...........")
    elif humanTotalScore1 > aiTotalScore and humanTotalScore1 > humanTotalScore2:
        #messagebox.showinfo("Game Over", "...........Player 1 Wins...........")
    elif humanTotalScore2 > aiTotalScore and humanTotalScore2 > humanTotalScore1:
        #messagebox.showinfo("Game Over", "...........Player 2 Wins...........")
    else:
        #messagebox.showinfo("Game Over", "...........It's a tie...........")
    window.destroy()
    return


def generate_moves(scores, selected):
    # Generates a list of available moves (indices of unselected scores)
    return [i for i, score in enumerate(scores) if not selected[i]]


def evaluate(scores, selected):
    # Calculates the total score for the selected scores
    res = [score for i, score in enumerate(scores) if selected[i]]
    return sum(res)


def game_over(selected):
    # Returns True if all scores have been selected
    return all(selected)


def minimax(depth, alpha, beta, maximizing_player, scores, selected):
    if depth == 0 or game_over(selected):
        return evaluate(scores, selected)

    if maximizing_player:
        max_eval = float('-inf')
        for move in generate_moves(scores, selected):
            selected[move] = True
            eval_score = minimax(depth - 1, alpha, beta, False, scores, selected)
            selected[move] = False
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in generate_moves(scores, selected):
            selected[move] = True
            eval_score = minimax(depth - 1, alpha, beta, True, scores, selected)
            selected[move] = False
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval


# Global variables
score_array = [-12, -17, -11, 1999, 100, 1000]
subtraction_array = [-132, 2, 3, 55, 99, 199]

depth = int(math.log(len(score_array), 2))
game_state = copy.deepcopy(score_array)
subtraction_state = copy.deepcopy(subtraction_array)
selected = [False] * len(score_array)
selectedSub = [False] * len(subtraction_array)

humanTotalScore1 = 0
humanTotalScore2 = 0
aiTotalScore = 0
current_player = "AI"

# Create the main window


# Create the gradient label


window = tk.Tk()
window.title("Number Game")
window.geometry("1100x600")
window.size()
window.configure(bg="#ffffff")
background_image = tk.PhotoImage(file="back.png")

# Create a Canvas
canvas = Canvas(window, width=700, height=3500)
canvas.pack(fill=BOTH, expand=True)

# Add Image inside the Canvas
canvas.create_image(0, 0, image=background_image, anchor='nw')

score_array_text = tk.Label(window, text="Score Array", bg="#2ed573",
                            fg="white",
                            font=("8514oem", 14, "bold"), padx=10, pady=5,bd=1,
                          relief="solid")
subtract_array_text = tk.Label(window, text="Subtraction Array", bg="#ff4757",
                               fg="white",
                               font=("8514oem", 14, "bold"), padx=10, pady=5,bd=1,
                          relief="solid")

player_label = tk.Label(window, text="Current player: " + current_player, bg="#f8f9fa", fg="#495057",
                        font=("8514oem", 14, "bold"), padx=10, pady=5,bd=1,
                          relief="solid")
player_label.place(relx=0.019, rely=0.1, anchor="w")

p1_score_label = tk.Label(window, bg="#e056fd", fg="white", font=("8514oem", 14, "bold"), padx=10, pady=15, bd=1,
                          relief="solid")
p1_score_label.place(relx=0.019, rely=0.25, anchor="w")

p2_score_label = tk.Label(window, bg="#eccc68", fg="white", font=("8514oem", 14, "bold"), padx=10, pady=25, bd=1,
                          relief="solid")
p2_score_label.place(relx=0.019 + .17, rely=0.25, anchor="w")

ai_score_label = tk.Label(window, bg="#eccc68", fg="white", font=("8514oem", 14, "bold"), padx=10, pady=15, bd=1,
                          relief="solid")
ai_score_label.place(relx=0.019 + .17 + .17, rely=0.25, anchor="w")

# Create buttons
score_buttons = []
subtraction_buttons = []


def update_scores():
    # Create separate labels for each player
    p1_score_label.config(
        text="Player 1: " + str(humanTotalScore1),
        bg="#f9ca24",
        fg="white",
        font=("8514oem", 14, "bold"),
        padx=10,
        pady=15,
        bd=1,
        relief="solid"
    )
    p2_score_label.config(
        text="Player 2: " + str(humanTotalScore2),
        bg="#f0932b",
        fg="white",
        font=("8514oem", 14, "bold"),
        padx=10,
        pady=15,
        bd=1,
        relief="solid"
    )
    ai_score_label.config(
        text="AI: " + str(aiTotalScore),
        bg="#badc58",
        fg="white",
        font=("8514oem", 14, "bold"),
        padx=10,
        pady=15,
        bd=1,
        relief="solid"
    )


def game_over(selectedSub):
    return all(selectedSub)


def update_game_state():
    for button in score_buttons:
        button.config(state=tk.DISABLED if selected[button.index] else tk.NORMAL, disabledforeground="#535c68")

    for button in subtraction_buttons:
        button.config(state=tk.DISABLED if selectedSub[button.index] else tk.NORMAL, disabledforeground="#535c68")


def create_score_buttons():
    score_array_text.place(relx=0.019, rely=0.500, anchor="w")

    score_buttons_frame = tk.Frame(canvas, bg="")
    score_buttons_frame.place(relx=0.5, rely=0.5, anchor="center")

    for i, score in enumerate(game_state):
        button = Button(score_buttons_frame, text=str(score), command=lambda index=i: process_score_selection(index))
        button.config(
            bg="#2ed573",
            fg="black",
            font=("8514oem", 12), bd=1,
            relief="solid",
            padx=10,
            pady=5,
            width=4,
            height=1,

        )
        button.index = i
        button.pack(side="left", padx=5, pady=(10, 10))
        score_buttons.append(button)


def create_subtraction_buttons():
    subtract_array_text.place(relx=0.019, rely=0.699, anchor="w")

    subtraction_buttons_frame = tk.Frame(canvas, bg="")
    subtraction_buttons_frame.place(relx=0.5, rely=0.7, anchor="center")

    for i, sub in enumerate(subtraction_state):
        button = Button(subtraction_buttons_frame, text=str(sub),
                        command=lambda index=i: process_subtraction_selection(index))
        button.config(
            bg="#ff4757",
            fg="black",
            font=("8514oem", 12),
            bd=1,
            relief="solid",
            padx=10,
            pady=5,
            width=4,
            height=1
        )
        button.index = i
        button.pack(side="left", padx=5, pady=(10, 10))
        subtraction_buttons.append(button)


def ai_turn():
    global current_player, humanTotalScore1, humanTotalScore2, aiTotalScore
    #messagebox.showinfo("AI Turn", "AI's turn!")
    best_score = float('-inf')
    best_move = 0
    best_score_sub = float('-inf')
    best_move_sub = 0
    for move in generate_moves(game_state, selected):
        selected[move] = True
        eval_score = minimax(depth, float('-inf'), float('inf'), False, game_state, selected)
        selected[move] = False
        if eval_score > best_score:
            best_score = eval_score
            best_move = move
        print("AI explores:", move, "and best score:", eval_score)

    for move in generate_moves(subtraction_state, selectedSub):
        selectedSub[move] = True
        eval_score_sub = minimax(depth, float('-inf'), float('inf'), False, subtraction_state, selectedSub)
        selectedSub[move] = False
        if eval_score_sub > best_score_sub:
            best_score_sub = eval_score_sub
            best_move_sub = move
        print("AI explores:", move, "and best sub score:", eval_score_sub)

    selected[best_move] = True
    selectedSub[best_move_sub] = True

    aiTotalScore += game_state[best_move]
    humanTotalScore1 -= subtraction_array[best_move_sub]
    humanTotalScore2 -= subtraction_array[best_move_sub]

    update_scores()
    update_game_state()
    gameBounsSound()
    if game_over(selectedSub):
        checkWins()
    else:
        current_player = "Player 1"
        player1_turn()


def player1_turn():
    global current_player

    # for button in score_buttons:
    #     button.config(state=tk.NORMAL if not selected[button.index] else tk.DISABLED)
    # for button in subtraction_buttons:
    #     button.config(state=tk.NORMAL if not selectedSub[button.index] else tk.DISABLED)
    player_label.config(text="Current player: " + current_player)


def player2_turn():
    global current_player

    for button in score_buttons:
        button.config(state=tk.NORMAL if not selected[button.index] else tk.DISABLED)
    for button in subtraction_buttons:
        button.config(state=tk.NORMAL if not selectedSub[button.index] else tk.DISABLED)

    player_label.config(text="Current player: " + current_player)


def process_score_selection(index):
    global current_player, humanTotalScore1, humanTotalScore2, aiTotalScore

    if not selected[index]:
        chosen_index = index
        selected[chosen_index] = True
        score = game_state[chosen_index]
        if current_player == "Player 1":
            humanTotalScore1 += score

        elif current_player == "Player 2":
            humanTotalScore2 += score

        update_scores()
        update_game_state()


def process_subtraction_selection(index):
    global current_player, humanTotalScore1, humanTotalScore2, aiTotalScore

    if not selectedSub[index]:
        chosen_sub_index = index

        selectedSub[chosen_sub_index] = True
        score_sub = subtraction_state[chosen_sub_index]
        if current_player == "Player 1":
            humanTotalScore2 -= score_sub
            aiTotalScore -= score_sub
            #messagebox.showinfo(current_player, "Score " + str(humanTotalScore1))
        elif current_player == "Player 2":
            humanTotalScore1 -= score_sub
            aiTotalScore -= score_sub
            #messagebox.showinfo(current_player, "Score " + str(humanTotalScore2))

        update_scores()
        update_game_state()
        gameBounsSound()
        if game_over(selectedSub):
            checkWins()
        else:
            if current_player == 'Player 1':
                current_player = 'Player 2'
                player2_turn()
            else:
                ai_turn()


# Create score and subtraction buttons
create_score_buttons()
create_subtraction_buttons()


def toggle_sound():
    global sound_on, sound_button_image

    if sound_on:
        mixer.music.pause()
        sound_button.config(image=mute_icon)
        sound_on = False
    else:
        mixer.music.unpause()
        sound_button.config(image=sound_icon)
        sound_on = True


def gameBounsSound():
    button_sound = mixer.Sound("game-bonus.mp3")
    if sound_on:
        button_sound.play()


def gameOpenningSound():
    button_sound = mixer.Sound("game_openning.mp3")
    if sound_on:
        button_sound.play()


def gameOverSound():
    button_sound = mixer.Sound("game_over.wav")
    if sound_on:
        button_sound.play()


# Initialize mixer for sound playback
mixer.init()
# Load the sound icons and reduce their size by 20 pixels
sound_icon = tk.PhotoImage(file="sound_on.png").subsample(18)
mute_icon = tk.PhotoImage(file="sound_off.png").subsample(18)

# Set initial sound state
sound_on = True

# Create the sound button
sound_button_image = sound_icon  # Store a reference to the image object
sound_button = tk.Button(window, image=sound_button_image, command=toggle_sound, bg="black")
sound_button.place(relx=window.winfo_width() - .10, rely=0.05, anchor="ne")

# Start the game with Player 1
gameOpenningSound()
update_scores()

window.after(1000, ai_turn)
# Event handler for resizing the window
# Start the main loop


window.mainloop()

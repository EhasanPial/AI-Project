import copy
import math
import tkinter as tk
from tkinter import messagebox, Button

# Global variables
score_array = [-12, -17, -11, 1999, 100, 1000]
subtraction_array = [-132, 2, 3, 55, 99, 199]
# Create buttons
score_buttons = []
subtraction_buttons = []
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
window = tk.Tk()
window.title("Number Game")
window.configure(bg="#ffffff")

# Styling options
bg_color = "#ffffff"
font_family = "Helvetica"
font_size = 14
font_weight = "bold"
button_bg_color = "#eccc68"
button_fg_color = "white"
button_font_family = "Helvetica"
button_font_size = 12
button_width = 4
button_height = 1


# Helper functions
def check_wins():
    if aiTotalScore > humanTotalScore1 and aiTotalScore > humanTotalScore2:
        messagebox.showinfo("Game Over", "AI WINS")
    elif humanTotalScore1 > aiTotalScore and humanTotalScore1 > humanTotalScore2:
        messagebox.showinfo("Game Over", "Player 1 Wins")
    elif humanTotalScore2 > aiTotalScore and humanTotalScore2 > humanTotalScore1:
        messagebox.showinfo("Game Over", "Player 2 Wins")
    else:
        messagebox.showinfo("Game Over", "It's a tie")
    window.destroy()


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


# Create labels
score_array_text = tk.Label(window, text="Score Array", bg=bg_color)
score_array_text.pack()

subtract_array_text = tk.Label(window, text="Subtraction Array", bg=bg_color)
subtract_array_text.pack()

player_label = tk.Label(window, text="Current player: " + current_player, bg=bg_color)
player_label.pack()

total_score_label = tk.Label(window, text="Total Score: ", bg=bg_color, fg="white",
                             font=(font_family, font_size, font_weight), pady=5)
total_score_label.pack()

# Create buttons
score_buttons_frame = tk.Frame(window, bg=bg_color)
score_buttons_frame.pack()

subtraction_buttons_frame = tk.Frame(window, bg=bg_color)
subtraction_buttons_frame.pack()


def update_scores():
    total_score_label.config(
        text="Total Score: P1: " + str(humanTotalScore1) + " | P2: " + str(humanTotalScore2) + " | AI: " + str(
            aiTotalScore),
        bg=button_bg_color,
        fg=button_fg_color
    )

    for button in score_buttons:
        button.config(bg=button_bg_color, fg=button_fg_color)

    for button in subtraction_buttons:
        button.config(bg=button_bg_color, fg=button_fg_color)


def update_game_state():
    for button in score_buttons:
        button.config(state=tk.DISABLED if selected[button.index] else tk.NORMAL)

    for button in subtraction_buttons:
        button.config(state=tk.DISABLED if selectedSub[button.index] else tk.NORMAL)


def create_score_buttons():
    for i, score in enumerate(game_state):
        button = Button(score_buttons_frame, text=str(score), command=lambda index=i: process_score_selection(index))
        button.index = i
        button.config(
            bg=button_bg_color,
            fg=button_fg_color,
            font=(button_font_family, button_font_size),
            width=button_width,
            height=button_height
        )
        button.pack(side="left", padx=5, pady=(10, 10))
        score_buttons.append(button)


def create_subtraction_buttons():
    for i, sub in enumerate(subtraction_state):
        button = Button(subtraction_buttons_frame, text=str(sub),
                        command=lambda index=i: process_subtraction_selection(index))
        button.index = i
        button.config(
            bg=button_bg_color,
            fg=button_fg_color,
            font=(button_font_family, button_font_size),
            width=button_width,
            height=button_height
        )
        button.pack(side="left", padx=5, pady=(10, 10))
        subtraction_buttons.append(button)


def ai_turn():
    global current_player, humanTotalScore1, humanTotalScore2, aiTotalScore
    messagebox.showinfo("AI Turn", "AI's turn!")
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

    if game_over(selectedSub):
        check_wins()
    else:
        current_player = "Player 1"
        player1_turn()


def player1_turn():
    global current_player
    for button in score_buttons:
        button.config(state=tk.NORMAL if not selected[button.index] else tk.DISABLED)

    for button in subtraction_buttons:
        button.config(state=tk.NORMAL if not selectedSub[button.index] else tk.DISABLED)

    current_player = "Player 1"
    player_label.config(text="Current player: " + current_player)


def player2_turn():
    global current_player
    for button in score_buttons:
        button.config(state=tk.NORMAL if not selected[button.index] else tk.DISABLED)

    for button in subtraction_buttons:
        button.config(state=tk.NORMAL if not selectedSub[button.index] else tk.DISABLED)

    current_player = "Player 2"
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
            messagebox.showinfo(current_player, "Score " + str(humanTotalScore1))
        elif current_player == "Player 2":
            humanTotalScore1 -= score_sub
            aiTotalScore -= score_sub
            messagebox.showinfo(current_player, "Score " + str(humanTotalScore2))

        update_scores()
        update_game_state()

        if game_over(selectedSub):
            check_wins()
        else:
            if current_player == 'Player 1':
                current_player = 'Player 2'
                player2_turn()
            else:
                ai_turn()


# Create score and subtraction buttons
create_score_buttons()
create_subtraction_buttons()

# Start the game with Player 1
ai_turn()

# Start the main loop
window.mainloop()


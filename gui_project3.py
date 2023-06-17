import copy
import math
import tkinter as tk
from tkinter import messagebox, Button


def check_wins():
    if ai_total_score > human_total_score1 and ai_total_score > human_total_score2:
        messagebox.showinfo("Game Over", "...........AI WINS...........")
    elif human_total_score1 > ai_total_score and human_total_score1 > human_total_score2:
        messagebox.showinfo("Game Over", "...........Player 1 Wins...........")
    elif human_total_score2 > ai_total_score and human_total_score2 > human_total_score1:
        messagebox.showinfo("Game Over", "...........Player 2 Wins...........")
    else:
        messagebox.showinfo("Game Over", "...........It's a tie...........")
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


# Global variables
score_array = [-12, -17, -11, 1999, 100, 1000]
subtraction_array = [-132, 2, 3, 55, 99, 199]

depth = int(math.log(len(score_array), 2))
game_state = copy.deepcopy(score_array)
subtraction_state = copy.deepcopy(subtraction_array)
selected = [False] * len(score_array)
selectedSub = [False] * len(subtraction_array)

human_total_score1 = 0
human_total_score2 = 0
ai_total_score = 0
current_player = "AI"

# Create the main window
window = tk.Tk()
window.title("Number Game")
window.geometry("800x600")
window.config(bg="#ffffff")

score_array_text = tk.Label(window, text="Score Array")
score_array_text.grid(row=0, column=0, pady=(20, 10))

subtract_array_text = tk.Label(window, text="Subtraction Array")
subtract_array_text.grid(row=2, column=0, pady=(20, 10))

player_label = tk.Label(window, text="Current player: " + current_player, bg="#f8f9fa", fg="#495057",
                        font=("Helvetica", 14, "bold"), padx=10, pady=5)
player_label.grid(row=4, column=0, pady=(20, 10), columnspan=3)


def handle_score_click(index):
    global current_player, human_total_score1, human_total_score2, ai_total_score, selected

    if selected[index]:
        return

    selected[index] = True
    score_button = score_buttons[index]
    score_button.config(state="disabled", relief="sunken")

    total_score = evaluate(score_array, selected)
    if current_player == "Player 1":
        human_total_score1 = total_score
    elif current_player == "Player 2":
        human_total_score2 = total_score
    else:
        ai_total_score = total_score

    current_player = "Player 1" if current_player == "Player 2" else "Player 2"
    player_label.config(text="Current player: " + current_player)

    if game_over(selected):
        check_wins()
    elif current_player == "AI":
        ai_move()


def handle_subtraction_click(index):
    global current_player, subtraction_state, selectedSub

    if selectedSub[index]:
        return

    selectedSub[index] = True
    subtraction_button = subtraction_buttons[index]
    subtraction_button.config(state="disabled", relief="sunken")

    current_player = "AI" if current_player == "Player 2" else "Player 2"
    player_label.config(text="Current player: " + current_player)

    if game_over(selectedSub):
        check_wins()
    elif current_player == "AI":
        ai_move()

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
        checkWins()
    else:
        current_player = "Player 1"
        player1_turn()



# Create score buttons
score_buttons = []
for i, score in enumerate(score_array):
    score_button = Button(window, text=str(score), width=10, height=2, relief="raised",
                          command=lambda i=i: handle_score_click(i))
    score_button.grid(row=1, column=i, padx=10)
    score_buttons.append(score_button)

# Create subtraction buttons
subtraction_buttons = []
for i, subtract in enumerate(subtraction_array):
    subtraction_button = Button(window, text=str(subtract), width=10, height=2, relief="raised",
                                command=lambda i=i: handle_subtraction_click(i))
    subtraction_button.grid(row=3, column=i, padx=10)
    subtraction_buttons.append(subtraction_button)

window.mainloop()

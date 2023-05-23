import tkinter as tk
from tkinter import messagebox
import math
import copy

# Create the GUI window
window = tk.Tk()
window.title("Game GUI")

def new_game_state(scores, index):
    # Removes the selected score from the list and returns the score
    score = scores.pop(index)
    return score


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


# Start the game

# Game setup
score_array = [-12, -17, -11 ]
subtraction_array = [-132, 2, 3 ]

depth = int(math.log(len(score_array), 2))
game_state = copy.deepcopy(score_array)
subtraction_state = copy.deepcopy(subtraction_array)
selected = [False] * len(score_array)
selectedSub = [False] * len(subtraction_array)
aiTotalScore = 0
humanTotalScore1 = 0
humanTotalScore2 = 0
current_player = 'AI'

# GUI functions
def update_scores():
    ai_score_label.config(text="AI score: " + str(aiTotalScore))
    player1_score_label.config(text="Player 1 score: " + str(humanTotalScore1))
    player2_score_label.config(text="Player 2 score: " + str(humanTotalScore2))

def update_game_state():
    game_state_label.config(text="Current game state: " + str(game_state))

def ai_turn():
    global current_player, aiTotalScore, humanTotalScore1, humanTotalScore2

    messagebox.showinfo("AI Turn", "AI's turn!")

    best_score = float('-inf')
    best_move = 0

    best_score_sub = float('-inf')
    best_move_sub = 0
    for move in generate_moves(game_state, selected):
        selected[score_array.index(game_state[move])] = True
        selectedSub[subtraction_array.index(subtraction_state[move])] = True
        eval_score = minimax(depth, float('-inf'), float('inf'), False, game_state, selected)
        eval_score_sub = minimax(depth, float('-inf'), float('inf'), False, subtraction_state, selectedSub)
        selected[score_array.index(game_state[move])] = False
        selectedSub[subtraction_array.index(subtraction_state[move])] = False
        if eval_score > best_score:
            best_score = eval_score
            best_move = move
        if eval_score_sub > best_score_sub:
            best_score_sub = eval_score_sub
            best_move_sub = move
        print("AI explores:", move, "and best score:", eval_score)
        print("AI explores:", move, "and best sub score:", eval_score_sub)

    selected[score_array.index(game_state[best_move])] = True
    selectedSub[subtraction_array.index(subtraction_state[best_move_sub])] = True
    score = new_game_state(game_state, best_move)
    score_sub = new_game_state(subtraction_state, best_move_sub)

    aiTotalScore += score
    humanTotalScore1 -= score_sub
    humanTotalScore2 -= score_sub

    update_scores()
    update_game_state()

    messagebox.showinfo("AI Score", "AI score: " + str(aiTotalScore))
    print(game_over(selected))
    if game_over(selected):
        print(aiTotalScore, " AI")
        print(humanTotalScore1, " Player 1")
        print(humanTotalScore2, " Player 2")

        if aiTotalScore > humanTotalScore1 and aiTotalScore > humanTotalScore2:
            print("AI wins!")
        elif humanTotalScore1 > aiTotalScore and humanTotalScore1 > humanTotalScore2:
            print("Player 1 wins!")
        elif humanTotalScore2 > aiTotalScore and humanTotalScore2 > humanTotalScore1:
            print("Player 2 wins!")
        else:
            print("It's a tie!")
        return
    else:
        current_player = "Player 1"
        player1_turn()

def player1_turn():
    global current_player, humanTotalScore1

    messagebox.showinfo("Player 1 Turn", "Player 1's turn!")

    game_state_label.config(text="Current game state: " + str(game_state))
    game_state_label.pack()
    index_state_label.config(text="From Index 0 to "+str(len(game_state)-1))
    index_state_label.pack()
    player1_input_label.config(text="Enter the index of player 1 move:")
    player1_input_label.pack()

    player1_sub_input_label.config(text="Enter the subtraction index of player 1 move:")
    player1_sub_input_label.pack()
    player1_button.config(command=process_player1_turn)  # Set the command for button click
    player1_button.pack()
    window.update()  # Update the GUI



def process_player1_turn():
    global current_player, humanTotalScore1, humanTotalScore2,aiTotalScore

    try:
        chosen_index = int(player1_input_entry.get())
        chosen_sub_index = int(player1_sub_input_entry.get())
        player1_input_entry.delete(0, tk.END)
        player1_sub_input_entry.delete(0, tk.END)
        selected[score_array.index(game_state[chosen_index])] = True
        selectedSub[subtraction_array.index(subtraction_state[chosen_sub_index])] = True
        score = new_game_state(game_state, chosen_index)
        score_sub = new_game_state(subtraction_state, chosen_sub_index)
        humanTotalScore1 += score
        humanTotalScore2 -= score_sub
        aiTotalScore -= score_sub

        update_scores()
        update_game_state()

        messagebox.showinfo("Player 1 Score", "Your score: " + str(humanTotalScore1))

        if game_over(selected):
            print(aiTotalScore, " AI")
            print(humanTotalScore1, " Player 1")
            print(humanTotalScore2, " Player 2")

            if aiTotalScore > humanTotalScore1 and aiTotalScore > humanTotalScore2:
                print("AI wins!")
            elif humanTotalScore1 > aiTotalScore and humanTotalScore1 > humanTotalScore2:
                print("Player 1 wins!")
            elif humanTotalScore2 > aiTotalScore and humanTotalScore2 > humanTotalScore1:
                print("Player 2 wins!")
            else:
                print("It's a tie!")
            window.destroy()
            return
        else:
            current_player = "Player 2"
            player2_turn()
    except (ValueError, IndexError):
        messagebox.showerror("Invalid Input", "Please enter a valid index.")

def player2_turn():
    global current_player, humanTotalScore2

    messagebox.showinfo("Player 2 Turn", "Player 2's turn!")

    game_state_label.config(text="Current game state: " + str(game_state))
    game_state_label.pack()
    index_state_label.config(text="From Index 0 to "+str(len(game_state)-1))
    index_state_label.pack()
    player1_input_label.config(text="Enter the index of player 2 move:")
    player1_input_label.pack()

    player1_sub_input_label.config(text="Enter the subtraction index of player 2 move:")
    player1_sub_input_label.pack()
    player1_button.config(command=process_player2_turn)  # Set the command for button click
    player1_button.pack()
    window.update()  # Update the GUI


def process_player2_turn():
    global current_player, humanTotalScore2, humanTotalScore1, aiTotalScore

    try:
        chosen_index = int(player1_input_entry.get())
        chosen_sub_index = int(player1_sub_input_entry.get())
        player1_input_entry.delete(0, tk.END)
        player1_sub_input_entry.delete(0, tk.END)
        selected[score_array.index(game_state[chosen_index])] = True
        selectedSub[subtraction_array.index(subtraction_state[chosen_sub_index])] = True
        score = new_game_state(game_state, chosen_index)
        score_sub = new_game_state(subtraction_state, chosen_sub_index)
        humanTotalScore2 += score
        humanTotalScore1 -= score_sub
        aiTotalScore -= score_sub

        update_scores()
        update_game_state()

        messagebox.showinfo("Player 2 Score", "Your score: " + str(humanTotalScore2))

        if game_over(selected):
            print(aiTotalScore, " AI")
            print(humanTotalScore1, " Player 1")
            print(humanTotalScore2, " Player 2")

            if aiTotalScore > humanTotalScore1 and aiTotalScore > humanTotalScore2:
                print("AI wins!")
            elif humanTotalScore1 > aiTotalScore and humanTotalScore1 > humanTotalScore2:
                print("Player 1 wins!")
            elif humanTotalScore2 > aiTotalScore and humanTotalScore2 > humanTotalScore1:
                print("Player 2 wins!")
            else:
                print("It's a tie!")
            window.destroy()
            return
        else:
            current_player = "AI"
            ai_turn()
    except (ValueError, IndexError):
        messagebox.showerror("Invalid Input", "Please enter a valid index.")

# GUI elements
ai_score_label = tk.Label(window, text="AI score: " + str(aiTotalScore))
ai_score_label.pack()

player1_score_label = tk.Label(window, text="Player 1 score: " + str(humanTotalScore1))
player1_score_label.pack()

player2_score_label = tk.Label(window, text="Player 2 score: " + str(humanTotalScore2))
player2_score_label.pack()

index_state_label = tk.Label(window, text="From Index 0 to "+str(len(game_state)-1))
index_state_label.pack()
game_state_label = tk.Label(window, text="Current game state: " + str(game_state))
game_state_label.pack()




player1_input_label = tk.Label(window, text="")
player1_input_label.pack()
player1_input_entry = tk.Entry(window)
player1_input_entry.pack()


player1_sub_input_label = tk.Label(window, text="")
player1_sub_input_label.pack()
player1_sub_input_entry = tk.Entry(window)
player1_sub_input_entry.pack()


player1_button = tk.Button(window, text="Submit")
player1_button.pack()

# Initial turn
ai_turn()

# Start the GUI main loop
window.mainloop()
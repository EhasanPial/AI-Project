import math
import copy


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


def game_over(game_state):
    # Returns True if all scores have been selected
    return len(game_state) == 0


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


# Game setup
score_array = [-12, -17, -11, 25, -45, 10, 12, 15, 18, -20, 100, 120, 155]
subtraction_array = [-132, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

depth = int(math.log(len(score_array), 2))
print(f"%%%%%%%% ~LEVEL : {depth}%%%%%%%%")
game_state = copy.deepcopy(score_array)
subtraction_state = copy.deepcopy(subtraction_array)
current_player = 'AI'
selected = [False] * len(score_array)
selectedSub = [False] * len(subtraction_array)
aiTotalScore = 0
humanTotalScore1 = 0
humanTotalScore2 = 0

# Main game loop
while not game_over(game_state):

    if current_player == 'AI':
        best_score = float('-inf')
        best_move = 0

        best_score_sub = float('-inf')
        best_move_sub = 0
        for move in generate_moves(game_state, selected):
            selected[move] = True
            selectedSub[move] = True
            eval_score = minimax(depth, float('-inf'), float('inf'), False, game_state, selected)
            eval_score_sub = minimax(depth, float('-inf'), float('inf'), False, subtraction_state, selectedSub)
            selected[move] = False
            selectedSub[move] = False
            if eval_score > best_score:
                best_score = eval_score
                best_move = move
            if eval_score_sub > best_score_sub:
                best_score_sub = eval_score_sub
                best_move_sub = move
            print("Ai explores: ", move, " and best score ", eval_score)
            print("Ai explores: ", move, " and best sub score ", eval_score_sub)
        selected[best_move] = True
        selectedSub[best_move_sub] = True
        score = new_game_state(game_state, best_move)
        score_sub = new_game_state(subtraction_state, best_move_sub)

        aiTotalScore += score
        humanTotalScore1 -= score_sub
        humanTotalScore2 -= score_sub
        print("------------------------- || AI || ------------------------------------")
        print("Current game state:", game_state)
        print("AI selects index", best_move, " Value:", score)
        print("AI selects subtraction index", best_move_sub, " Value:", score_sub)
        print("AI score:", aiTotalScore)
        print("-------------------------------------------------------------")
        current_player = 'Player 1'

    elif current_player == 'Player 1':
        print("-------------------------|| Player 1 ||---------------------------------")
        print("Current game state:", game_state)
        print("-------------------------------------------------------------")
        ## ----------------------- Choosing Points ----------------------- ##
        print(f"Index range 0 to {len(game_state) - 1}")
        try:
            chosen_index = int(input("Enter the index of your move: "))
            selected[score_array.index(game_state[chosen_index])] = True
            score = new_game_state(game_state, chosen_index)
            humanTotalScore1 += score
            print("Your selects index", chosen_index, " Value:", score)
            print("Your score:", humanTotalScore1)
        except (ValueError, IndexError):
            print("Invalid input! Please enter a valid index.")
            continue

        ## ----------------------- Choosing Subtraction Point for others ----------------------- ##
        print(f"Index range 0 to {len(subtraction_state) - 1}")
        try:
            chosen_index = int(input("Enter the subtraction index of your move: "))
            selectedSub[subtraction_array.index(subtraction_state[chosen_index])] = True
            score_sub = new_game_state(subtraction_state, chosen_index)
            aiTotalScore -= score_sub
            humanTotalScore2 -= score_sub
            print("Your selects subtraction index", chosen_index, " Value:", score_sub)
            print("AI score:", aiTotalScore, "Player 2 score:", humanTotalScore2)
            print("-------------------------------------------------------------")
            current_player = 'Player 2'
        except (ValueError, IndexError):
            print("Invalid input! Please enter a valid index.")
            continue

    elif current_player == 'Player 2':
        print("-------------------------|| Player 2 ||------------------------------------")
        print("Current game state:", game_state)
        print("-------------------------------------------------------------")
        ## ----------------------- Choosing Points ----------------------- ##
        print(f"Index range 0 to {len(game_state) - 1}")
        try:
            chosen_index = int(input("Enter the index of your move: "))
            selected[score_array.index(game_state[chosen_index])] = True
            score = new_game_state(game_state, chosen_index)
            humanTotalScore2 += score
            print("Your selects index", chosen_index, " Value:", score)
            print("Your score:", humanTotalScore2)
        except (ValueError, IndexError):
            print("Invalid input! Please enter a valid index.")
            continue

        ## ----------------------- Choosing Subtraction Point for others ----------------------- ##
        print(f"Index range 0 to {len(subtraction_state) - 1}")
        try:
            chosen_index = int(input("Enter the subtraction index of your move: "))
            selectedSub[subtraction_array.index(subtraction_state[chosen_index])] = True
            score_sub = new_game_state(subtraction_state, chosen_index)
            aiTotalScore -= score_sub
            humanTotalScore1 -= score_sub
            print("Your selects subtraction index", chosen_index, " Value:", score_sub)
            print("AI score:", aiTotalScore, "Player 2 score:", humanTotalScore1)
            print("-------------------------------------------------------------")
            current_player = 'AI'
        except (ValueError, IndexError):
            print("Invalid input! Please enter a valid index.")
            continue

# Game over, determine the winner
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

import math
import copy


def make_move(scores, index):
    # Removes the selected score from the list and returns the score
    score = scores[index]
    scores = scores[:index] + scores[index + 1:]
    return score, scores


def generate_moves(scores, selected):
    # Generates a list of available moves (indices of unselected scores)
    return [i for i in range(len(scores)) if not selected[i]]


def evaluate(scores, selected):
    # Calculates the total score for the selected scores
    res = [scores[i] for i in range(len(scores)) if selected[i]]
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
            selected[move] = 1
            eval = minimax(depth - 1, alpha, beta, False, scores, selected)
            selected[move] = 0
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval

    else:
        min_eval = float('inf')
        for move in generate_moves(scores, selected):
            selected[move] = 1
            eval = minimax(depth - 1, alpha, beta, True, scores, selected)
            selected[move] = 0
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


# Game setup
score_array = [-12, -17, -11, 25, -45, 10, 12, 15, 18, -20, 100, 120, 155]
depth = int(math.log(len(score_array), 2))
print(f"%%%%%%%% ~LEVEL : {depth}~ %%%%%%%%")
# int(math.log(len(score_array), 2))
game_state = score_array.copy()
current_player = 'AI'
selected = [False] * len(score_array)
aiTotalScore = 0
humanTotalScore1 = 0
humanTotalScore2 = 0

# Main game loop
while not game_over(game_state):
    if current_player == 'AI':
        best_score = float('-inf')
        best_move = 0
        for move in generate_moves(game_state, selected):
            # new_state, score = make_move(game_state, move)
            selected[move] = True
            eval = minimax(depth, float('-inf'), float('inf'), False, game_state, selected)
            selected[move] = False
            if eval > best_score:
                best_score = eval
                best_move = move
            print("Ai explores: ", move, " and best score ", eval)
        selected[score_array.index(game_state[best_move])] = True
        score, game_state = make_move(game_state, best_move)
        aiTotalScore += score
        print("------------------------- || AI || ------------------------------------")
        print("Current game state:", game_state)
        print("AI selects index", best_move, " Value :", score)
        print("AI score:", aiTotalScore)
        print("-------------------------------------------------------------")
        current_player = 'Player 1'
    elif current_player == 'Player 1':
        print("-------------------------|| Player 1 ||---------------------------------")
        print("Current game state:", game_state)
        print("-------------------------------------------------------------")
        print(f"Index range 0 to {len(game_state) - 1}")
        chosen_index = int(input("Enter the index of your move: "))
        selected[score_array.index(game_state[chosen_index])] = True
        score, game_state = make_move(game_state, chosen_index)
        humanTotalScore1 += score
        print("Your selects index", chosen_index, " Value: ", score)
        print("Your score:", humanTotalScore1)
        print("-------------------------------------------------------------")
        current_player = 'Player 2'
    elif current_player == 'Player 2':
        print("-------------------------|| Player 2 ||------------------------------------")
        print("Current game state:", game_state)
        print("-------------------------------------------------------------")
        print(f"Index range 0 to {len(game_state) - 1}")
        chosen_index = int(input("Enter the index of your move: "))
        selected[score_array.index(game_state[chosen_index])] = True
        score, game_state = make_move(game_state, chosen_index)
        humanTotalScore2 += score
        print("Your selects index", chosen_index, " Value: ", score)
        print("Your score:", humanTotalScore2)
        print("-------------------------------------------------------------")
        current_player = 'AI'

# Game over, determine the winner
print(aiTotalScore, " AI")
print(humanTotalScore1, " Player 1")
print(humanTotalScore2, " Player 2")

if aiTotalScore > humanTotalScore1 and aiTotalScore > humanTotalScore2:
    print("AI wins!")
elif aiTotalScore < humanTotalScore1 and humanTotalScore1 > humanTotalScore2:
    print("Player 1 wins!")
elif humanTotalScore2 > aiTotalScore and humanTotalScore2 > humanTotalScore1:
    print("Player 2 wins!")
else:
    print("It's a tie!")

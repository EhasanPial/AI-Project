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
            selected_copy = copy.deepcopy(selected)
            selected_copy[move] = True
            score, new_state = make_move(scores, move)
            eval = minimax(depth - 1, alpha, beta, False, new_state, selected_copy)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval

    else:
        min_eval = float('inf')
        for move in generate_moves(scores, selected):
            selected_copy = copy.deepcopy(selected)
            selected_copy[move] = True
            score, new_state = make_move(scores, move)
            eval = minimax(depth - 1, alpha, beta, True, new_state, selected_copy)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


# Game setup
score_array = [-10, 3, 7, 2, 1, 9, 10, 12, 14]
depth = int(math.log(len(score_array), 2))
game_state = score_array.copy()
current_player = 'AI'
selected = [False] * len(score_array)
aiTotalScore = 0
humanTotalScore = 0

# Main game loop
while not game_over(game_state):
    if current_player == 'AI':
        best_score = float('-inf')
        best_move = 0
        for move in generate_moves(game_state, selected):
            new_state, score = make_move(game_state, move)
            selected[move] = True
            eval = minimax(depth, float('-inf'), float('inf'), False, game_state, selected)
            selected[move] = False
            if eval > best_score:
                best_score = eval
                best_move = move
        selected[score_array.index(game_state[best_move])] = True
        score, game_state = make_move(game_state, best_move)
        aiTotalScore += score
        print("-------------------------------------------------------------")
        print("AI selects index", best_move , " Value :", score)
        print("AI score:", aiTotalScore)
        print("-------------------------------------------------------------")
        current_player = 'Human'
    else:
        print("-------------------------------------------------------------")
        print("Current game state:", game_state)
        print("-------------------------------------------------------------")
        print(f"Index range 0 to {len(game_state) - 1}")
        chosen_index = int(input("Enter the index of your move: "))
        selected[score_array.index(game_state[chosen_index])] = True
        score, game_state = make_move(game_state, chosen_index)
        humanTotalScore += score
        print("Your selects index", chosen_index, " Value: ",score)
        print("Your score:", humanTotalScore)
        print("-------------------------------------------------------------")
        current_player = 'AI'

# Game over, determine the winner
print(aiTotalScore, "At last")
print(humanTotalScore, "Human At last")
if aiTotalScore > humanTotalScore:
    print("AI wins!")
elif aiTotalScore < humanTotalScore:
    print("Human wins!")
else:
    print("It's a tie")

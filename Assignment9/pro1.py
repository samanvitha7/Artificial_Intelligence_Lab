import math
import time

WIN_STATES = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6],
]


def opponent(player):
    return 'O' if player == 'X' else 'X'


def board_status(board):
    for a, b, c in WIN_STATES:
        if board[a] != ' ' and board[a] == board[b] == board[c]:
            return board[a]
    if ' ' not in board:
        return 'Draw'
    return None


def terminal_score(result, ai_symbol):
    if result == ai_symbol:
        return 1
    if result == 'Draw':
        return 0
    return -1


def print_board(board):
    print("Current board:")
    for r in range(3):
        row = []
        for c in range(3):
            idx = r * 3 + c
            row.append(str(idx + 1) if board[idx] == ' ' else board[idx])
        print(" | ".join(row))
    print()


def minimax(board, current_player, ai_symbol, stats):
    stats['nodes'] += 1
    result = board_status(board)
    if result is not None:
        stats['terminal_nodes'] += 1
        return terminal_score(result, ai_symbol)

    if current_player == ai_symbol:
        best = -math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = current_player
                value = minimax(board, opponent(current_player), ai_symbol, stats)
                board[i] = ' '
                best = max(best, value)
        return best

    best = math.inf
    for i in range(9):
        if board[i] == ' ':
            board[i] = current_player
            value = minimax(board, opponent(current_player), ai_symbol, stats)
            board[i] = ' '
            best = min(best, value)
    return best


def evaluate_position(board, player_to_move, ai_symbol):
    temp_stats = {'nodes': 0, 'terminal_nodes': 0}
    return minimax(board, player_to_move, ai_symbol, temp_stats)


def visualize_search_tree(board, player_to_move, ai_symbol, max_depth=2):
    print(f"Search tree (depth <= {max_depth}):")

    def recurse(state, player, depth, move_label):
        indent = "  " * depth
        result = board_status(state)
        if result is not None:
            score = terminal_score(result, ai_symbol)
            print(f"{indent}{move_label} -> terminal: {result}, score {score}")
            return

        if depth == max_depth:
            score = evaluate_position(state, player, ai_symbol)
            print(f"{indent}{move_label} -> evaluated score {score}")
            return

        score_here = evaluate_position(state, player, ai_symbol)
        print(f"{indent}{move_label} -> player {player}, score {score_here}")
        for i in range(9):
            if state[i] == ' ':
                state[i] = player
                recurse(state, opponent(player), depth + 1, f"move {i + 1} ({player})")
                state[i] = ' '

    recurse(board[:], player_to_move, 0, "root")
    print()


def find_best_move(board, ai_symbol):
    stats = {'nodes': 0, 'terminal_nodes': 0}
    start = time.perf_counter()

    best_move = -1
    best_score = -math.inf
    scored_moves = []

    for i in range(9):
        if board[i] == ' ':
            board[i] = ai_symbol
            score = minimax(board, opponent(ai_symbol), ai_symbol, stats)
            board[i] = ' '
            scored_moves.append((i, score))
            if score > best_score:
                best_score = score
                best_move = i

    elapsed_ms = (time.perf_counter() - start) * 1000.0
    return best_move, best_score, scored_moves, stats, elapsed_ms


def get_user_move(board):
    while True:
        try:
            pos = int(input("Enter your move (1-9): ")) - 1
            if 0 <= pos <= 8 and board[pos] == ' ':
                return pos
            print("Invalid move. Choose an empty position from 1 to 9.")
        except ValueError:
            print("Please enter a valid number from 1 to 9.")


def play_game():
    board = [' '] * 9

    print("Tic-Tac-Toe using Minimax")
    print("You will play against the AI agent.")
    print_board(board)

    while True:
        user_symbol = input("Choose your symbol (X/O): ").strip().upper()
        if user_symbol in ('X', 'O'):
            break
        print("Invalid symbol. Enter X or O.")

    ai_symbol = opponent(user_symbol)

    while True:
        first = input("Who plays first? (user/agent): ").strip().lower()
        if first in ('user', 'agent'):
            break
        print("Invalid input. Type user or agent.")

    current_player = user_symbol if first == 'user' else ai_symbol
    total_nodes = 0
    total_terminal_nodes = 0
    total_time_ms = 0.0
    ai_turns = 0
    tree_depth = 2
    turn_no = 1

    while True:
        print(f"Turn {turn_no} - {'User' if current_player == user_symbol else 'Agent'} ({current_player})")
        print_board(board)

        result = board_status(board)
        if result is not None:
            break

        if current_player == user_symbol:
            move = get_user_move(board)
            board[move] = user_symbol
            print(f"User played move {move + 1}.\n")
        else:
            visualize_search_tree(board, ai_symbol, ai_symbol, max_depth=tree_depth)
            move, score, scored_moves, stats, elapsed_ms = find_best_move(board, ai_symbol)
            board[move] = ai_symbol
            ai_turns += 1
            total_nodes += stats['nodes']
            total_terminal_nodes += stats['terminal_nodes']
            total_time_ms += elapsed_ms

            print("Agent move evaluations:")
            for m, s in scored_moves:
                print(f"  move {m + 1} -> score {s}")
            print(f"Agent selected move {move + 1} with score {score}.")
            print(f"Performance: {stats['nodes']} nodes, {stats['terminal_nodes']} terminal nodes, {elapsed_ms:.2f} ms\n")

        result = board_status(board)
        if result is not None:
            break

        current_player = opponent(current_player)
        turn_no += 1

    print("Final board:")
    print_board(board)

    final_result = board_status(board)
    if final_result == 'Draw':
        print("Game result: Draw")
    elif final_result == user_symbol:
        print("Game result: User wins")
    else:
        print("Game result: Agent wins")

    print("\nAI Performance Summary:")
    print(f"  AI turns: {ai_turns}")
    print(f"  Total nodes explored: {total_nodes}")
    print(f"  Total terminal nodes: {total_terminal_nodes}")
    print(f"  Total compute time: {total_time_ms:.2f} ms")
    if ai_turns > 0:
        print(f"  Average nodes/turn: {total_nodes / ai_turns:.2f}")
        print(f"  Average time/turn: {total_time_ms / ai_turns:.2f} ms")


if __name__ == '__main__':
    play_game()


            
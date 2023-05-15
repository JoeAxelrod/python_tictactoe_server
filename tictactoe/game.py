def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != ' ':
            return row[0]

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != ' ':
            return board[0][col]

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
        return board[0][0]

    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
        return board[0][2]

    return None


def minimax(board, depth, maximizing_player):
    winner = check_winner(board)
    if winner or depth == 0:
        if winner == 'X':
            return -10 + depth
        elif winner == 'O':
            return 10 - depth
        else:
            return 0

    if maximizing_player:
        best_value = float('-inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == ' ':
                    board[row][col] = 'O'
                    value = minimax(board, depth - 1, False)
                    board[row][col] = ' '
                    best_value = max(best_value, value)
        return best_value
    else:
        best_value = float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == ' ':
                    board[row][col] = 'X'
                    value = minimax(board, depth - 1, True)
                    board[row][col] = ' '
                    best_value = min(best_value, value)
        return best_value


def best_move(board):
    best_value = float('-inf')
    move = (-1, -1)  # Initialize move with a sentinel value
    empty_spaces = sum([row.count(' ') for row in board])

    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':
                board[row][col] = 'O'
                value = minimax(board, empty_spaces - 1, False)
                board[row][col] = ' '
                if value > best_value:
                    best_value = value
                    move = (row, col)

    return move


def player_move(board, move):
    row, col = move.split()
    row, col = int(row), int(col)

    if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == ' ':
        return row, col
    else:
        return -1, -1


def string2board(board_string):
    lines = [line for line in board_string.split('\n')[:5]]
    rows = [row for row in lines if '---------' not in row]
    board = [[cell.strip() or " " for cell in row.split(" | ")] for row in rows]
    return board


def board2string(board):
    output = ""
    for i, row in enumerate(board):
        output += (row[0] or " ") + " | " + (row[1] or " ") + " | " + (row[2] or " ") + "\n"
        if i < 2:
            output += "---------\n"
    return output


# = [[' ' for _ in range(3)] for _ in range(3)]
def main(board_string, action):
    board = string2board(board_string)
    print("Tic Tac Toe")

    result = ''
    winner = None
    if action:
        row, col = player_move(board, action)

        if row != -1 and col != -1:
            board[row][col] = 'X'
        else:
            result = "Invalid move. Please try again."

        if not result:
            row, col = best_move(board)
            if row != -1 and col != -1:
                board[row][col] = 'O'

            winner = check_winner(board)

            if winner:
                result = f"{winner} wins!"
            elif all(board[row][col] != ' ' for row in range(3) for col in range(3)):
                result = "It's a draw!"
                winner = 'draw'

    print(board2string(board))
    return board2string(board), board, result, winner

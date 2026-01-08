import time   

# Initial chess board
board = [
["r","n","b","q","k","b","n","r"],
["p","p","p","p","p","p","p","p"],
[".",".",".",".",".",".",".","."],
[".",".",".",".",".",".",".","."],
[".",".",".",".",".",".",".","."],
[".",".",".",".",".",".",".","."],
["P","P","P","P","P","P","P","P"],
["R","N","B","Q","K","B","N","R"]
]

initial_board = [row[:] for row in board]   
move_history = []                            
MOVE_TIME = 15                             

def print_board():
    print("\n a b c d e f g h")
    for i in range(8):
        print(8-i, end=" ")
        for j in range(8):
            print(board[i][j], end=" ")
        print()

def convert(pos):
    col = ord(pos[0]) - ord('a')
    row = 8 - int(pos[1])
    return row, col

# Piece-wise validation
def valid_move(piece, sr, sc, er, ec):
    dr, dc = er - sr, ec - sc

    if piece.lower() == "p":   # Pawn
        step = -1 if piece.isupper() else 1
        return dc == 0 and dr == step and board[er][ec] == "."

    if piece.lower() == "r":   # Rook
        return sr == er or sc == ec

    if piece.lower() == "b":   # Bishop
        return abs(dr) == abs(dc)

    if piece.lower() == "q":   # Queen
        return sr == er or sc == ec or abs(dr) == abs(dc)

    if piece.lower() == "n":   # Knight
        return (abs(dr), abs(dc)) in [(2,1),(1,2)]

    if piece.lower() == "k":   # King
        return abs(dr) <= 1 and abs(dc) <= 1

    return False

# Check detection
def find_king(color):
    k = "K" if color == "White" else "k"
    for r in range(8):
        for c in range(8):
            if board[r][c] == k:
                return r, c

def is_check(color):
    kr, kc = find_king(color)
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if p != "." and (p.isupper() != (color == "White")):
                if valid_move(p, r, c, kr, kc):
                    return True
    return False

def move_piece(start, end):
    sr, sc = convert(start)
    er, ec = convert(end)

    if board[sr][sc] == ".":
        print("No piece at source!")
        return False

    piece = board[sr][sc]

    # turn-wise piece restriction
    if (turn == "White" and piece.islower()) or (turn == "Black" and piece.isupper()):
        print("Wrong turn!")
        return False

    # move validation
    if not valid_move(piece, sr, sc, er, ec):
        print("Invalid move for piece!")
        return False

    board[er][ec] = board[sr][sc]
    board[sr][sc] = "."

    move_history.append(f"{turn}: {start} -> {end}")   

    # self-check prevention
    if is_check(turn):
        board[sr][sc] = piece
        board[er][ec] = "."
        move_history.pop()
        print("King in check!")
        return False

    return True

turn = "White"

while True:
    print_board()
    print(f"\n{turn}'s move (Time: {MOVE_TIME}s)")
    start_time = time.time()          

    move = input("Enter move (e2 e4), history, restart or 'exit': ")

    # Timer check
    if time.time() - start_time > MOVE_TIME:
        print("Time over! Turn skipped.")
        turn = "Black" if turn == "White" else "White"
        continue

    if move == "exit":
        break

    # Restart game
    if move == "restart":
        board = [row[:] for row in initial_board]
        move_history.clear()
        turn = "White"
        print("Game restarted!")
        continue

    # Move history
    if move == "history":
        print("\nMove History:")
        for i, m in enumerate(move_history, 1):
            print(i, m)
        continue

    try:
        start, end = move.split()
        if move_piece(start, end):
            opponent = "Black" if turn == "White" else "White"
            if is_check(opponent):
                print("CHECK!")
            turn = opponent
    except:
        print("Invalid input format!")

BOARD_SIZE = 5
FIRST_PLAYER = "X"
SECOND_PLAYER = "O"
EMPTY_CELL = "."

def init_board():
    new_empty_board = []
    #cols
    for _ in range(BOARD_SIZE):
        row = []
        #rows
        for _ in range(BOARD_SIZE):
            row.append(EMPTY_CELL)
        new_empty_board.append(row)
    return new_empty_board

def draw_game_board(game_board):
    #margin from left for header A B C
    out_string = " " * 4
    #header A B C
    for i in range(BOARD_SIZE):
        out_string += f'{chr(65 + i):^4}|'
    out_string += "\n"
    #cols
    for i in range(BOARD_SIZE):
        #header 1 2 3
        out_string += f'{i + 1:<3}|'
        #rows
        for j in range(BOARD_SIZE):
            out_string += f'{game_board[i][j]:^4}|'
        out_string += "\n"
    
    print(out_string)
    
    
def next_move(player, board):
    #input move
    move_data = input(f"Player {player}, enter your move (e.g. A1): ")
    
    try:
        row = int(move_data[1]) - 1
        col = ord(move_data[0].upper()) - 65
    except (IndexError, ValueError):
        print("Invalid format! Try again! 🔁")
        return False

    if row < 0 or row >= BOARD_SIZE or col < 0 or col >= BOARD_SIZE:
        print("Invalid move! Out of bounds. Try again! 🔁")
        return False

    if board[row][col] != EMPTY_CELL:
        print("Cell is already occupied! Try again! 🔁")
        return False

    #process move 
    board[row][col] = player
    return True
 
def stop_game(board):
    #check for win
    for i in range(BOARD_SIZE):
        #check for gorizontal win
        if board[i].count(board[i][0]) == BOARD_SIZE and board[i][0] != EMPTY_CELL:
            print(f"Player {board[i][0]} wins in gorizontal 🎉!")
            return True 
        
        #check for vertical win
        if all(board[j][i] == board[0][i] and board[0][i] != EMPTY_CELL for j in range(BOARD_SIZE)):
            print(f"Player {board[0][i]} wins in vertical! 🎉")
            return True
    #check for diagonal win
    if all(board[i][i] == board[0][0] and board[0][0] != EMPTY_CELL for i in range(BOARD_SIZE)):
        print(f"Player {board[0][0]} wins in diagonal! 🎉")
        return True
    #empty cells was not found
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == EMPTY_CELL:
                return False
    return True
    
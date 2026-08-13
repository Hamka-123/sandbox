import utils as u

game_board = []
#initialize the game board
current_player = u.FIRST_PLAYER

game_board = u.init_board()

while True:
    u.draw_game_board(game_board)

    success = u.next_move(current_player, game_board)

    if success:
            # If move was successful, change the player
            current_player = (
                u.SECOND_PLAYER if current_player == u.FIRST_PLAYER else u.FIRST_PLAYER
            )
        
    if u.stop_game(game_board):
        print("Result:")
        u.draw_game_board(game_board)
        break
        
    
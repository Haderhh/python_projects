import random

# Constants
BOARD_SIZE = 10  # The size of the game board
SHIP_NAMES = ["Carrier", "Battleship", "Cruiser", "Submarine", "Destroyer"]  # Names of the ships
SHIP_LENGTHS = [5, 4, 3, 3, 2]  # Length of each ship

def create_board():
    """
    Creates an empty game board.

    Returns:
    list: A 2D list representing the empty game board
    """
    return [[" " for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def display_ship_placement_board(player_board):
    """
    Displays the board when ship is placed

    Args:
    player_board (list): The player's game board to display
    """
    header = "   " + " ".join(str(i) for i in range(BOARD_SIZE))
    print(header)
    for i in range(BOARD_SIZE):
        row = ""
        for j in range(BOARD_SIZE):
            row += "|" + player_board[i][j]
        print(f"{i:2} {row}|")

def display_board(player_board, show_hits=False, player_num=None):
    """
    Displays the game board

    Args:
    player_board (list): The player's game board to display
    show_hits (bool): Whether to show hits and misses
    player_num (int): The player number (1 or 2)
    """
    header = "   " + " ".join(str(i) for i in range(BOARD_SIZE))
    print(header)
    for i in range(BOARD_SIZE):
        row = ""
        for j in range(BOARD_SIZE):
            if show_hits and player_board[i][j] == "X":
                row += "|X"
            elif show_hits and player_board[i][j] == "-":
                row += "|-"
            elif show_hits and player_board[i][j] != " " and player_board[i][j] != "X" and player_board[i][j] != "-":
                if player_num == 1:
                    row += "| "
                else:
                    row += "|" + player_board[i][j]
            else:
                row += "|" + player_board[i][j]
        print(f"{i:2} {row}|")

def place_ships(player_board):
    """
    Places ships on the game board.

    Args:
    player_board (list): The player's game board.
    """
    for i in range(len(SHIP_NAMES)):
        ship = SHIP_NAMES[i]
        length = SHIP_LENGTHS[i]
        placed = False
        while not placed:
            print(f"Enter x y coordinates to place the {ship}:")
            display_ship_placement_board(player_board)
            start_x, start_y = [int(coord) for coord in input().split()]
            direction = input("Enter Right or Down (r or d): ").lower()

            if direction == 'r' and start_x + length <= BOARD_SIZE:
                positions = [(start_x + j, start_y) for j in range(length)]
                invalid_position = False
                for x, y in positions:
                    if player_board[y][x] != " ":
                        invalid_position = True
                if not invalid_position:
                    for x, y in positions:
                        player_board[y][x] = ship[0]
                    placed = True
                else:
                    print("Invalid position or overlapping ships, try again.")
            elif direction == 'd' and start_y + length <= BOARD_SIZE:
                positions = [(start_x, start_y + j) for j in range(length)]
                invalid_position = False
                for x, y in positions:
                    if player_board[y][x] != " ":
                        invalid_position = True
                if not invalid_position:
                    for x, y in positions:
                        player_board[y][x] = ship[0]
                    placed = True
                else:
                    print("Invalid position or overlapping ships, try again.")
            else:
                print("Invalid position or overlapping ships, try again.")




def register_shot(grid):
    """
    Registers a shot

    Args:
    grid (list): The opponent's game board

    Returns:
    tuple: The coordinates (x, y) of the shot
    """
    valid_input = False
    while not valid_input:
        print("Enter x y coordinates to fire:")
        user_input = input().split()
        if len(user_input) != 2:
            print("Invalid input, try again.")
            continue
        x, y = user_input
        if not x.isdigit() or not y.isdigit():
            print("Invalid input, try again.")
            continue
        x, y = int(x), int(y)
        if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and grid[x][y] not in ['X', '-']:
            valid_input = True
        else:
            print("Invalid coordinates or already shot, try again.")
    return x, y

def check_shot(target_board, x, y):
    """
    Checks if a shot hits a ship.

    Args:
    target_board (list): The opponent's game board
    x (int): The x-coordinate of the shot
    y (int): The y-coordinate of the shot

    Returns:
    tuple: (hit, ship_hit) where:
        hit (bool): True if the shot hits a ship or else it is false
        ship_hit (str or None): The name of the ship hit, or None if no ship is hit
    """
    if target_board[x][y] != " ":
        ship_hit = target_board[x][y]
        target_board[x][y] = "X"
        return True, ship_hit
    else:
        target_board[x][y] = "-"
        return False, None

def check_win_condition(board):
    """
    Checks if all ships are sunk

    Args:
    board (list): The game board

    Returns:
    bool: True if all ships are sunk, False otherwise
    """
    for row in board:
        for cell in row:
            if cell != " ":
                return False
    return True

def run_game():
    """
    Runs the game
    """
    # Create player boards
    player_boards = [create_board(), create_board()]

    hit_miss_board = create_board()

    # Place ships for each player
    for player in range(2):
        print(f"\nPlayer {player + 1}, prepare to place your fleet.")
        place_ships(player_boards[player])

    current_player = 0
    game_over = False
    while not game_over:
        # Display current player's board
        print(f"\nPlayer {current_player + 1}'s turn:")
        if current_player == 0:
            print("    Your Fleet:")
            display_ship_placement_board(player_boards[current_player])
            print("    Opponent's Shots:")
            display_board(hit_miss_board, show_hits=True)
        else:
            print("    Your Shots:")
            display_board(player_boards[current_player], show_hits=True, player_num=current_player + 1)

        # Display hits and misses
        print("\nHits and Misses:")
        display_board(hit_miss_board, show_hits=True)

        x, y = register_shot(player_boards[1 - current_player])

        hit, ship_hit = check_shot(player_boards[1 - current_player], x, y)
        if hit:
            print(f"Hit! You hit the {ship_hit}.")
            hit_miss_board[x][y] = "X"
        else:
            print("Miss!")
            hit_miss_board[x][y] = "-"

        # Check win condition
        if check_win_condition(player_boards[1 - current_player]):
            print(f"\nPlayer {current_player + 1} wins!")
            game_over = True


        current_player = 1 - current_player

if __name__ == '__main__':
    run_game()

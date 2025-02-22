import random

GRID_WIDTH = 8
GRID_HEIGHT = 3
DICE_SIDES = 6


def generate_random_map(length, the_seed=0):
    """
        :param length - the length of the map
        :param the_seed - the seed of the map
        :return: a randomly generated map based on a specific seed, and length.
    """
    if the_seed:
        random.seed(the_seed)
    map_list = []
    for _ in range(length - 2):
        random_points = random.randint(1, 100)
        random_position = random.randint(0, length - 1)
        map_list.append(random.choices(['nop', f'add {random_points}', f'sub {random_points}', f'mul {random_points}', f'jmp {random_position}', 'hlt'], weights=[5, 2, 2, 2, 3, 1], k=1)[0])

    return ['nop'] + map_list + ['hlt']


def make_grid(table_size):
    """
    :param table_size: this needs to be the length of the map
    :return: returns a display grid that you can then modify with fill_grid_square (it's a 2d-grid of characters)
    """
    floating_square_root = table_size ** (1 / 2)

    int_square_root = int(floating_square_root) + (1 if floating_square_root % 1 else 0)
    table_height = int_square_root
    if int_square_root * (int_square_root - 1) >= table_size:
        table_height -= 1

    the_display_grid = [[' ' if j % GRID_WIDTH else '*' for j in range(GRID_WIDTH * int_square_root + 1)]
                        if i % GRID_HEIGHT else ['*' for j in range(GRID_WIDTH * int_square_root + 1)]
                        for i in range(table_height * GRID_HEIGHT + 1)]
    return the_display_grid


def fill_grid_square(display_grid, size, index, message):
    """
    :param display_grid:  the grid that was made from make_grid
    :param size:  this needs to be the length of the total map, otherwise you may not be able to place things correctly.
    :param index: the index of the position where you want to display the message
    :param message: the message to display in the square at position index, separated by line returns.
    """
    floating_square_root = size ** (1 / 2)
    int_square_root = int(floating_square_root) + (1 if floating_square_root % 1 else 0)
    table_row = index // int_square_root
    table_col = index % int_square_root

    if table_row % 2 == 0:
        column_start = GRID_WIDTH * table_col
    else:
        column_start = GRID_WIDTH * (int_square_root - table_col - 1)

    for r, message_line in enumerate(message.split('\n')):
        for k, c in enumerate(message_line):
            display_grid[GRID_HEIGHT * table_row + 1 + r][column_start + 1 + k] = c


def roll_dice():
    """
        Call this function once per turn.

        :return: returns the dice roll
    """
    return random.randint(1, DICE_SIDES)

def math_command(score, command):
    """
    Handles math commands (add, sub, mul) and updates the score.
    """
    operation, value = command.split()
    value = int(value)
    if operation == 'add':
        score += value
    elif operation == 'sub':
        score -= value
    elif operation == 'mul':
        score *= value
    return score

def jump(position, command):
    """
    Handles jump commands and updates the position.
    """
    _, new_position = command.split()
    return int(new_position)

def display_board(game_map):
    """
    displays the board
    :param game_map: a list representing the game map.
    """
    board_size = len(game_map)
    display_grid = make_grid(board_size)

    index = 0
    for row_index in range(board_size):
        for col_index in range(board_size):
            if index < len(game_map):  # Check if index is within game_map range
                fill_grid_square(display_grid, board_size, index, f"{index}\n{game_map[index]}")
            index += 1

    for row in display_grid:
        print(''.join(row))


def play_game(game_map):
    """
    Main function to play the game with the given game map.
    """
    position = 0
    score = 0
    game_over = False

    display_board(game_map)

    while not game_over:
        roll = roll_dice()
        position = (position + roll) % len(game_map)
        command = game_map[position].lower()

        if command[:3] == 'add' or command[:3] == 'sub' or command[:3] == 'mul':
            score = math_command(score, command)
        elif command[:3] == 'jmp':
            position = jump(position, command)
            command = game_map[position].lower()  # Update command after jump

        print(f"Pos: {position} Score: {score}, instruction {command} Rolled: {roll}")

        if command == 'hlt':
            game_over = True
        elif command != 'nop':
            if command[:3] == 'jmp':
                roll = 0
            elif command[:3] == 'add' or command[:3] == 'sub' or command[:3] == 'mul':
                roll = 0

    print(f"Final Pos: {position} Final Score: {score}, Instruction {game_map[position]}")
    if input("Play again? (yes/no): ").lower() == 'yes':
        play()




def play():
    play_again = True
    while play_again:
        board_size, seed = input("Board Size and Seed: ").split()
        board_size = int(board_size)
        seed = int(seed)
        game_map = generate_random_map(board_size, seed)
        play_game(game_map)
        play_again = input("Play again? (yes/no): ").lower() == 'yes'



if __name__ == '__main__':
    play()
 

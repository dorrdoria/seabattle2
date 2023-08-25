import random

HIT_CHAR = 'x'
MISS_CHAR = 'o'
BLANK_CHAR = '.'
HORIZONTAL = 'г'
VERTICAL = 'в'
MAX_MISSES = 20
SHIP_SIZES = {
    "корабль на 3 клетки": 3,
    "корабль на 2 клетки": 2,
    "корабль на 2 клетки": 2,
    "корабль на 1 клетку": 1,
    "корабль на 1 клетку": 1,
    "корабль на 1 клетку": 1,
    "корабль на 1 клетку": 1,
}
NUM_ROWS = 6
NUM_COLS = 6
ROW_IDX = 0
COL_IDX = 1
MIN_ROW_LABEL = 'А'
MAX_ROW_LABEL = 'Е'


def get_random_position():

    row_choice = chr(
                    random.choice(
                        range(
                            ord(MIN_ROW_LABEL),
                            ord(MIN_ROW_LABEL) + NUM_ROWS
                        )
                    )
    )

    col_choice = random.randint(0, NUM_COLS - 1)

    return (row_choice, col_choice)


def play_battleship():

    print("Давайте сыграем в Морской Бой!\n")

    game_over = False

    while not game_over:

        game = Game()
        game.display_board()

        while not game.is_complete():
            pos = game.get_guess()
            result = game.check_guess(pos)
            game.update_game(result, pos)
            game.display_board()

        game_over = end_program()

    print("Спасибо за игру")



class Ship:

    def __init__(self, name, start_position, orientation):

        self.name = name
        num_positions = SHIP_SIZES[name]
        self.positions = {}
        self.sunk = False

        for pos in range(num_positions):
            if orientation == VERTICAL:
                vertical_position, horizontal_position = start_position
                self.positions[(chr(ord(vertical_position) + pos), horizontal_position)] = False

            elif orientation == HORIZONTAL:
                vertical_position, horizontal_position = start_position
                self.positions[(vertical_position, horizontal_position + pos)] = False



class Game:

    _ship_types = ["корабль на 3 клетки", "корабль на 2 клетки", "корабль на 2 клетки", "корабль на 1 клетку", "корабль на 1 клетку", "корабль на 1 клетку", "корабль на 1 клетку"]


    def display_board(self):

        print()
        print("  " + ' '.join('{}'.format(i) for i in range(len(self.board))))
        for row_label in self.board.keys():
            print('{} '.format(row_label) + ' '.join(self.board[row_label]))
        print()


    def __init__(self, max_misses = MAX_MISSES):

        self.max_misses = MAX_MISSES
        self.ships = []
        self.guesses = []
        self.board = {}
        self.initialize_board()
        self.create_and_place_ships()



    def update_game(self, guess_status, position):

        row, column = position

        if guess_status == True and self.board[row][column] == BLANK_CHAR:
            self.board[row][column] = HIT_CHAR

        elif guess_status == False and self.board[row][column] == BLANK_CHAR:
            self.board[row][column] = MISS_CHAR


        if guess_status == False:
            self.guesses.append(position)


    def is_complete(self):

        if len(self.guesses) == self.max_misses:
            print("Простите! Ходы закончились")
            return True

        ships_sunk = []

        for ship in self.ships:
            ships_sunk.append(ship.sunk)

        if ships_sunk == ([True] * len(SHIP_SIZES)):
            print("Вы выиграли!")
            return True

        return False



    def check_guess(self, position):


        for ship in self.ships:
            for occupied_position in list(ship.positions.keys()):

                if occupied_position == position and ship.positions[occupied_position] == False:
                    ship.positions[occupied_position] = True
                    if list(ship.positions.values()) == ([True] * len(ship.positions)):
                        ship.sunk = True
                        print("Вы утопили {}!".format(ship.name))
                    return True
        return False





    def get_guess(self):

        min_row_ord_allowed = ord(MIN_ROW_LABEL)
        max_row_ord_allowed = ord(MAX_ROW_LABEL)

        min_column_allowed = ROW_IDX
        max_column_allowed = NUM_COLS - COL_IDX

        row_checker = False
        column_checker = False


        while row_checker ==  False:
            user_row_input = input("Выбирете линию: ")
            if min_row_ord_allowed <= ord(user_row_input) <= max_row_ord_allowed:
                row_checker = True



        while column_checker == False:
            user_column_input = int(input("Выбирете колонну: "))
            if min_column_allowed <= user_column_input <= max_column_allowed:
                column_checker = True

        return (user_row_input, user_column_input)



    def create_and_place_ships(self):

        for ship_name in self._ship_types:
            starting_position = get_random_position()
            size_ship = SHIP_SIZES[ship_name]
            orientation = self.place_ship(starting_position, size_ship)
            while orientation == None:
                starting_position = get_random_position()
                orientation = self.place_ship(starting_position, size_ship)

            ship = Ship(ship_name, starting_position, orientation)
            self.ships.append(ship)


    def place_ship(self, start_position, ship_size):

        horizontal_in_bounds = self.in_bounds(start_position, ship_size, HORIZONTAL)

        horizontal_overlaps = self.overlaps_ship(start_position, ship_size, HORIZONTAL)

        vertical_in_bounds = self.in_bounds(start_position, ship_size, VERTICAL)

        vertical_overlaps = self.overlaps_ship(start_position, ship_size, VERTICAL)

        if horizontal_in_bounds == True and horizontal_overlaps == False:
            return HORIZONTAL

        elif vertical_in_bounds == True and vertical_overlaps == False:
            return VERTICAL

        else:
            return None




    def overlaps_ship(self, start_position, ship_size, orientation):

        current_ship_positions = []

        start_position_letter, start_position_number = start_position

        for num in range(ship_size):
            if orientation == VERTICAL:
                current_ship_positions.append((chr(ord(start_position_letter) + num), start_position_number))

            elif orientation == HORIZONTAL:
                current_ship_positions.append((start_position_letter, start_position_number + num))


        already_taken_positions = []

        for ship in self.ships:
            for position in list(ship.positions.keys()):
                already_taken_positions.append(position)


        for position1 in current_ship_positions:
            for position2 in already_taken_positions:

                if position1 == position2:
                    return True


        return False



    def in_bounds(self, start_position, ship_size, orientation):

        start_position_letter, start_position_number = start_position

        if orientation == VERTICAL:
            if (ord(start_position_letter) + ship_size) > ord(MAX_ROW_LABEL):
                return False

        elif orientation == HORIZONTAL:
            if (start_position_number + ship_size) > (NUM_COLS - COL_IDX):
                return False

        return True






    def initialize_board(self):

        alphabets = []

        for num in range(NUM_COLS):
            alphabets.append(chr(ord(MIN_ROW_LABEL) + num))

        for letter in alphabets:
            self.board[letter] = ["."] * NUM_COLS




def end_program():

    user_input = input("Сыграем еще раз? ")

    allowed_inputs= "даДанетНет"

    while not user_input in allowed_inputs:
        user_input = input("Сыграем еще раз? ")

    if user_input == "Да" or user_input == "да":
        return False

    if user_input == "Нет" or user_input == "нет":
        return True


def main():

    play_battleship()


if __name__ == "__main__":
    main()
import random


class Player:

    def __init__(self, name, pieces):
        self.name = name
        self.pieces = pieces


class DominoesGame:

    def __init__(self):

        self.stock = []
        self.snake = []
        self.user = Player("user", [])
        self.computer = Player("computer", [])
        self.active_player = self.user
        self.status = "playing"
        # create dominoes set

        for i in range(0, 7):
            for j in range(0, 7):
                piece = [min(i, j), max(i, j)]
                if piece not in self.stock:
                    self.stock.append(piece)

        self.distribute_pieces()
        self.starting_player()

        self.game_loop()

    def distribute_pieces(self):

        for player in [self.user, self.computer]:
            for j in range(0, 7):
                piece = random.choice(self.stock)
                self.stock.remove(piece)
                player.pieces.append(piece)

    def starting_player(self):

        highest = []
        for player in [self.user, self.computer]:
            high = [0, 0]
            for i in player.pieces:
                # print("i", i)
                if (i[0] + i[1]) > (high[0] + high[1]):
                    high = i
            highest.append([player.name, high])

        if (highest[0][1][0] + highest[0][1][1]) > (highest[1][1][0] + highest[1][1][1]):
            self.active_player = self.computer
            self.snake.append(highest[0][1])
            self.user.pieces.remove(highest[0][1])
        else:
            self.active_player = self.user
            self.snake.append(highest[1][1])
            self.computer.pieces.remove(highest[1][1])

    def show_game(self):

        print("======================================================================")
        print("Stock size:", len(self.stock))
        print("Computer pieces:", len(self.computer.pieces))
        print("")

        if len(self.snake) > 6:
            print("{}{}{}...{}{}{}".format(self.snake[0], self.snake[1], self.snake[2],
                                           self.snake[-3], self.snake[-2], self.snake[-1]))
        else:
            for i in self.snake:
                print(i, end="")

        print("\n")
        print("Your pieces")
        for i in range(1, len(self.user.pieces)+1):
            print("{}:{}".format(i, self.user.pieces[i-1]))

        print("\n")

    def validate_input(self):

        digit = None
        valid = None
        legal = None

        while not all([digit, valid, legal]):
            move = input()
            digit = None
            if move.isdigit() or move.lstrip("-").isdigit():
                digit = True
            valid = None
            if digit:
                size = len(self.user.pieces)
                if int(move) in range(-1 * size, size + 1):
                    valid = True

            if not (digit and valid):
                print("Invalid input. Please try again..")
            else:
                move = int(move)
                legal = self.validate_legal(move)

                if not legal:
                    print("Illegal move. Please try again.")

                if all([digit, valid, legal]):
                    self.play_turn(move)

    def validate_legal(self, move):

        if move == 0:
            legal = True
            return legal
        else:
            piece = self.user.pieces[abs(move) - 1]
            ends = [self.snake[0][0], self.snake[-1][1]]

            if (piece[0] == ends[0] or piece[1] == ends[0]) and move < 0:
                legal = True
            elif (piece[0] == ends[1] or piece[1] == ends[1]) and move > 0:
                legal = True
            else:
                legal = False

            return legal

    def computer_move(self):
        # print("computer moving")
        # new AI code
        occurs = {}
        for i in range(0, 7):
            occurs[i] = 0
            for j in self.computer.pieces:
                if j[0] == i:
                    occurs[i] += 1
                if j[1] == i:
                    occurs[i] += 1
            for k in self.snake:
                if k[0] == i:
                    occurs[i] += 1
                if k[1] == i:
                    occurs[i] += 1

        # print(occurs)

        # create dictionary of pieces piece position in list: [piece, score]
        dict_pieces = {}
        for i in range(0, len(self.computer.pieces)):
            score = occurs[self.computer.pieces[i][0]] + occurs[self.computer.pieces[i][1]]
            dict_pieces[i] = [self.computer.pieces[i], score]

        # print(dict_pieces)

        # find highest
        played = False
        while not played:
            high_score = 0
            high_piece = 0
            for i in dict_pieces.keys():
                if dict_pieces[i][1] > high_score:
                    high_score = dict_pieces[i][1]
                    high_piece = i
            # print(high_score)
            # print(high_piece)

            #check legal
            move = 0
            if dict_pieces[high_piece][1] == self.snake[0][0] or dict_pieces[high_piece][0] == self.snake[0][0]:
                move = -1 * high_piece
                self.play_turn(move)
                played = True
            elif dict_pieces[high_piece][1] == self.snake[-1][1] or dict_pieces[high_piece][0] == self.snake[-1][1]:
                move = high_piece
                self.play_turn(move)
                played = True
            else:
                del dict_pieces[high_piece]

            if len(dict_pieces.keys()) == 0:
                move = 0
                self.play_turn(move)
                played = True

    def play_turn(self, move):

        # print("move", move)

        if move == 0:
            if len(self.stock) >= 1:
                new_piece = random.choice(self.stock)
                self.stock.remove(new_piece)
                self.active_player.pieces += [new_piece]
        elif move < 0:
            piece = self.active_player.pieces[abs(move) - 1]
            self.active_player.pieces.remove(piece)
            if piece[0] != piece[1]:
                if piece[0] == self.snake[0][0]:
                    piece = piece[::-1]
            self.snake = [piece] + self.snake
        elif move > 0:
            piece = self.active_player.pieces[move - 1]
            self.active_player.pieces.remove(piece)
            if piece[0] != piece[1]:
                if piece[1] == self.snake[-1][1]:
                    piece = piece[::-1]
            self.snake = self.snake + [piece]

    def game_loop(self):

        self.show_game()

        while self.status == "playing":

            if self.active_player == self.user:
                print("Status: It's your turn to make a move. Enter your command.")
                self.validate_input()
            elif self.active_player == self.computer:
                print("Status: Computer is about to make a move. Press Enter to continue...")
                enter = input()
                while not enter == "":
                    print("Invalid input. Please try again.")
                    enter = input()
                self.computer_move()

            if self.active_player.name == "user":
                self.active_player = self.computer
            elif self.active_player.name == "computer":
                self.active_player = self.user

            self.show_game()

            if len(self.user.pieces) == 0:
                print("Status: The game is over. You won!")
                self.status = "finished"
                break
            if len(self.computer.pieces) == 0:
                print("Status: The game is over. The computer won!")
                self.status = "finished"
                break
            if len(self.stock) == 0:
                print("Status: The game is over. It's a draw!")
                self.status = "finished"
                break


def main():

    game = DominoesGame()


main()

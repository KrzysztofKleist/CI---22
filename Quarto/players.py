
import numpy as np
import random
from objects import Player, Quarto
from copy import deepcopy

import sys


class RandomPlayer(Player):
    """Random player"""

    def __init__(self, quarto: Quarto) -> None:
        super().__init__(quarto)

    def choose_piece(self) -> int:
        return random.randint(0, 15)

    def place_piece(self) -> tuple[int, int]:
        return random.randint(0, 3), random.randint(0, 3)


class Agent(Player):
    """RL Agent player"""

    # initial alpha = 0.15, random_factor=0.2
    def __init__(self, quarto: Quarto, alpha=0.15, random_factor=0.2) -> None:
        super().__init__(quarto)

        self.state_history_board = []  # state, reward
        self.state_history_pieces = []  # state, reward

        self.alpha = alpha
        self.random_factor = random_factor

        self.G_board = {}
        self.G_pieces = {}  # list 0-15 to represent the pieces

        self.states_board = self.get_game().get_board_status()
        self.init_reward_board(self.states_board)

        self.states_pieces = list(range(16))
        self.init_reward_pieces(self.states_pieces)

    def reset(self, quarto: Quarto) -> None:

        if self.get_game().check_winner() == 0:
            reward = -10
        elif self.get_game().check_winner() == 1:
            reward = 10
        else:
            reward = 0

        self.learn(reward)

        super().__init__(quarto)

    def init_reward_board(self, states_board) -> None:
        for i, row in enumerate(states_board):
            for j, col in enumerate(row):
                self.G_board[(j, i)] = np.random.uniform(low=1.0, high=0.1)

    def init_reward_pieces(self, states_pieces) -> None:
        for i in states_pieces:
            self.G_pieces[(i)] = np.random.uniform(low=1.0, high=0.1)

    def place_piece(self) -> tuple[int, int]:
        maxG = -10e15
        next_move = None
        randomN = np.random.random()

        BOARD_SIDE = 4

        allowedMoves = list()

        for row in range(BOARD_SIDE):
            for col in range(BOARD_SIDE):
                if self.get_game().get_board_status()[row, col] == -1:
                    allowedMoves.append((col, row))

        # print("board:")
        # print(self.get_game().get_board_status())

        if randomN < self.random_factor:
            # if random number below random factor, choose random action
            next_move = allowedMoves[np.random.choice(len(allowedMoves))]
        else:
            # if exploiting, gather all possible actions and choose one with the highest G (reward)
            for move in allowedMoves:
                if self.G_board[move] >= maxG:
                    next_move = move
                    maxG = self.G_board[move]

        self.update_state_history_board(next_move, 0)
        return next_move

    def choose_piece(self) -> int:
        maxG = -10e15
        next_piece = None
        randomN = np.random.random()

        disallowedPieces = sum(self.get_game().get_board_status().tolist(), [])
        disallowedPieces_copy = deepcopy(disallowedPieces)

        for val in disallowedPieces_copy:
            if val == -1:
                disallowedPieces.remove(-1)

        allPieces = list(range(16))
        allowedPieces = [
            item for item in allPieces if item not in disallowedPieces]

        if randomN < self.random_factor:
            # if random number below random factor, choose random action
            next_piece = np.random.choice(allowedPieces)
        else:
            # if exploiting, gather all possible actions and choose one with the highest G (reward)
            for piece in allowedPieces:
                if self.G_pieces[piece] >= maxG:
                    next_piece = piece
                    maxG = self.G_pieces[piece]

        self.update_state_history_pieces(next_piece, 0)
        return next_piece

    def update_state_history_board(self, state, reward) -> None:
        self.state_history_board.append((state, reward))

    def update_state_history_pieces(self, state, reward) -> None:
        self.state_history_pieces.append((state, reward))

    def learn(self, reward):

        last_state_board = (self.state_history_board[-1][0], reward)
        last_state_pieces = (self.state_history_pieces[-1][0], reward)

        self.state_history_board = self.state_history_board[:-1] + [
            last_state_board]
        self.state_history_pieces = self.state_history_pieces[:-1] + [
            last_state_pieces]

        target = 0
        for prev, reward in reversed(self.state_history_board):
            self.G_board[prev] = self.G_board[prev] + \
                self.alpha * (target - self.G_board[prev])
            target += reward
        self.state_history_board = []

        target = 0
        for prev, reward in reversed(self.state_history_pieces):
            self.G_pieces[prev] = self.G_pieces[prev] + \
                self.alpha * (target - self.G_pieces[prev])
            target += reward
        self.state_history_pieces = []

        self.random_factor -= 10e-5  # decrease random factor each episode of play


class GAPlayer(Player):
    """Genetic algorithm player"""

    def __init__(self, genome: tuple, quarto: Quarto) -> None:
        super().__init__(quarto)
        self.__genome_choose = genome[:5]
        self.__genome_place = genome[-7:]

    # Strategies for choosing a piece

    def lowest_piece(self) -> int:
        # chooses an available piece with lowest number assigned
        disallowedPieces = sum(
            self.get_game().get_board_status().tolist(), [])
        disallowedPieces_copy = deepcopy(disallowedPieces)

        for val in disallowedPieces_copy:
            if val == -1:
                disallowedPieces.remove(-1)

        allPieces = list(range(16))
        allowedPieces = [
            item for item in allPieces if item not in disallowedPieces]
        return allowedPieces[0]

    def highest_piece(self) -> int:
        # chooses an available piece with highest number assigned
        disallowedPieces = sum(
            self.get_game().get_board_status().tolist(), [])
        disallowedPieces_copy = deepcopy(disallowedPieces)

        for val in disallowedPieces_copy:
            if val == -1:
                disallowedPieces.remove(-1)

        allPieces = list(range(16))
        allowedPieces = [
            item for item in allPieces if item not in disallowedPieces]
        return allowedPieces[-1]

    def random_piece(self) -> int:
        # chooses random available piece
        disallowedPieces = sum(
            self.get_game().get_board_status().tolist(), [])
        disallowedPieces_copy = deepcopy(disallowedPieces)

        for val in disallowedPieces_copy:
            if val == -1:
                disallowedPieces.remove(-1)

        allPieces = list(range(16))
        allowedPieces = [
            item for item in allPieces if item not in disallowedPieces]
        return random.choice(allowedPieces)

        return random.randint(0, 15)

    def get_pieces(self):
        # returns stats on currently placed pieces
        pieces_stats = [0, 0, 0, 0]
        available_pieces = list()
        pieces_used = 0
        for i in range(16):
            if not self.get_game().select(i):
                piece = self.get_game().get_piece_charachteristics(i)
                pieces_stats = [
                    x + y for x, y in zip(pieces_stats, [piece.HIGH, piece.COLOURED, piece.SOLID, piece.SQUARE])]
                pieces_used += 1
            else:
                available_pieces.append(i)
        return pieces_stats, pieces_used, available_pieces

    def compare_characteristics(self, available_pieces, most_unique_piece) -> int:
        for p_no in available_pieces:
            for i in range(4):
                piece_obj = deepcopy(
                    self.get_game().get_piece_charachteristics(p_no))
                piece = [piece_obj.HIGH, piece_obj.COLOURED,
                         piece_obj.SOLID, piece_obj.SQUARE]
                comparison_piece = deepcopy(most_unique_piece)
                del piece[i]
                del comparison_piece[i]
                if piece == comparison_piece:
                    return p_no

    def unique_piece(self) -> int:
        # print("unique")
        # chooses the piece that stands out most
        pieces_stats, pieces_used, available_pieces = self.get_pieces()
        most_unique_piece = [(x - pieces_used/2) < 0 for x in pieces_stats]
        # print(most_unique_piece)
        final_p_no = -10
        for p_no in available_pieces:
            piece = self.get_game().get_piece_charachteristics(p_no)
            # print(p_no, [piece.HIGH, piece.COLOURED, piece.SOLID, piece.SQUARE], [
            #       piece.HIGH, piece.COLOURED, piece.SOLID, piece.SQUARE] == most_unique_piece)
            if [piece.HIGH, piece.COLOURED, piece.SOLID, piece.SQUARE] == most_unique_piece:
                final_p_no = p_no

        if final_p_no == -10:
            final_p_no = self.compare_characteristics(
                available_pieces, most_unique_piece)

        if final_p_no == None:
            final_p_no = self.random_piece()

        return final_p_no

    def similar_piece(self) -> int:
        # print("similar")
        # chooses the piece that will fit most pieces already on the board
        pieces_stats, pieces_used, available_pieces = self.get_pieces()
        most_similar_piece = [(x - pieces_used/2) < 0 for x in pieces_stats]
        # print(most_similar_piece)
        final_p_no = -10
        for p_no in available_pieces:
            piece = self.get_game().get_piece_charachteristics(p_no)
            # print(p_no, [piece.HIGH, piece.COLOURED, piece.SOLID, piece.SQUARE], [
            #       piece.HIGH, piece.COLOURED, piece.SOLID, piece.SQUARE] == most_similar_piece)
            if [piece.HIGH, piece.COLOURED, piece.SOLID, piece.SQUARE] == most_similar_piece:
                final_p_no = p_no

        if final_p_no == -10:
            final_p_no = self.compare_characteristics(
                available_pieces, most_similar_piece)

        if final_p_no == None:
            final_p_no = self.random_piece()

        return final_p_no

    # Strategies for placing a piece

    def left_upper(self) -> tuple[int, int]:
        # chooses the most upper left place on the board available
        BOARD_SIDE = 4
        allowedMoves = list()
        for row in range(BOARD_SIDE):
            for col in range(BOARD_SIDE):
                if self.get_game().get_board_status()[row, col] == -1:
                    allowedMoves.append((col, row))
        return allowedMoves[0]

    def left_lower(self) -> tuple[int, int]:
        # chooses the most lower left place on the board available
        BOARD_SIDE = 4
        allowedMoves = list()
        for row in range(BOARD_SIDE):
            for col in range(BOARD_SIDE):
                if self.get_game().get_board_status()[row, col] == -1:
                    allowedMoves.append((col, row))

        sorted_allowedMoves = sorted(allowedMoves, key=lambda x: (x[0], -x[1]))
        return sorted_allowedMoves[0]

    def right_lower(self) -> tuple[int, int]:
        # chooses the most lower right place on the board available
        BOARD_SIDE = 4
        allowedMoves = list()
        for row in range(BOARD_SIDE):
            for col in range(BOARD_SIDE):
                if self.get_game().get_board_status()[row, col] == -1:
                    allowedMoves.append((col, row))
        return allowedMoves[-1]

    def right_upper(self) -> tuple[int, int]:
        # chooses the most upper right place on the board available
        BOARD_SIDE = 4
        allowedMoves = list()
        for row in range(BOARD_SIDE):
            for col in range(BOARD_SIDE):
                if self.get_game().get_board_status()[row, col] == -1:
                    allowedMoves.append((col, row))

        sorted_allowedMoves = sorted(allowedMoves, key=lambda x: (x[0], -x[1]))
        return sorted_allowedMoves[-1]

    def random_place(self) -> tuple[int, int]:
        # chooses random available place on the board
        BOARD_SIDE = 4
        allowedMoves = list()
        for row in range(BOARD_SIDE):
            for col in range(BOARD_SIDE):
                if self.get_game().get_board_status()[row, col] == -1:
                    allowedMoves.append((col, row))
        return random.choice(allowedMoves)

    def far_place(self) -> tuple[int, int]:
        # chooses place the furthest from other pieces
        BOARD_SIDE = 4
        allowedMoves = list()
        for row in range(BOARD_SIDE):
            for col in range(BOARD_SIDE):
                if self.get_game().get_board_status()[row, col] == -1:
                    allowedMoves.append((col, row))

        board = self.get_game().get_board_status()

        counter_list = list()

        for move in allowedMoves:
            counter = 0
            for j in [-2, -1, 0, 1, 2]:
                for i in [-2, -1, 0, 1, 2]:
                    y = move[1] + j
                    x = move[0] + i
                    if y <= -1 or y >= 4 or x <= -1 or x >= 4:
                        pass
                    elif j == 0 and i == 0:
                        pass
                    else:
                        if board[y, x] == -1:
                            counter += 1
            counter_list.append(counter)
        dictionary = dict(
            sorted(dict(zip(allowedMoves, counter_list)).items()))
        first_key = next(iter(dictionary))
        return first_key

    def close_place(self) -> tuple[int, int]:
        # chooses place the closest to the other pieces
        BOARD_SIDE = 4
        allowedMoves = list()
        for row in range(BOARD_SIDE):
            for col in range(BOARD_SIDE):
                if self.get_game().get_board_status()[row, col] == -1:
                    allowedMoves.append((col, row))

        board = self.get_game().get_board_status()

        counter_list = list()

        for move in allowedMoves:
            counter = 0
            for j in [-2, -1, 0, 1, 2]:
                for i in [-2, -1, 0, 1, 2]:
                    y = move[1] + j
                    x = move[0] + i
                    if y <= -1 or y >= 4 or x <= -1 or x >= 4:
                        pass
                    elif j == 0 and i == 0:
                        pass
                    else:
                        if board[y, x] == -1:
                            counter += 1
            counter_list.append(counter)
        dictionary = dict(zip(allowedMoves, counter_list))
        sorted_dictionary = dict(
            sorted(dictionary.items(), key=lambda item: item[0], reverse=True))
        first_key = next(iter(sorted_dictionary))
        return first_key
    
    ###

    def choose_strategy_choose(self) -> int:
        # multiply scores to get int values
        genome_100 = tuple(int(g * 100)
                           for g in self.__genome_choose)
        # list of values of scores with numbers assigned to each strategy
        prob_list = list()
        # strategy value changing at each iteration
        strategy_value = 1
        for i in genome_100:
            for j in range(i):
                prob_list.append(strategy_value)
            strategy_value += 1
        # returned values are equivalent to:
        # lowest_piece: 1
        # highest_piece: 2
        # random_piece: 3
        # unique_piece: 4
        # similar_piece: 5
        # at the end we choose the strategy randomly but the distribution of them
        # in the list is weighted
        return random.choice(prob_list)

    def choose_strategy_place(self) -> int:
        # multiply scores to get int values
        genome_100 = tuple(int(g * 100)
                           for g in self.__genome_place)
        # list of values of scores with numbers assigned to each strategy
        prob_list = list()
        # strategy value changing at each iteration
        strategy_value = 1
        for i in genome_100:
            for j in range(i):
                prob_list.append(strategy_value)
            strategy_value += 1
        # returned values are equivalent to:
        # left_upper: 1
        # left_lower: 2
        # right_lower: 3
        # right_upper: 4
        # random_place: 5
        # far_place: 6
        # close_place: 7
        # at the end we choose the strategy randomly but the distribution of them
        # in the list is weighted
        return random.choice(prob_list)

    ###

    def make_strategy_choose(self) -> int:

        choice = self.choose_strategy_choose()

        if choice == 1:  # lowest_piece
            piece = self.lowest_piece()

        if choice == 2:  # highest_piece
            piece = self.highest_piece()

        if choice == 3:  # random_piece
            piece = self.random_piece()

        if choice == 4:  # unique_piece
            piece = self.unique_piece()

        if choice == 5:  # unique_piece
            piece = self.similar_piece()

        return piece

    def make_strategy_place(self) -> tuple[int, int]:

        choice = self.choose_strategy_place()

        if choice == 1:  # left_upper
            place = self.left_upper()

        if choice == 2:  # left_lower
            place = self.left_lower()

        if choice == 3:  # right_lower
            place = self.right_lower()

        if choice == 4:  # right_upper
            place = self.right_upper()

        if choice == 5:  # random_place
            place = self.random_place()
            
        if choice == 6:  # far_place
            place = self.random_place()
            
        if choice == 7:  # close_place
            place = self.random_place()

        return place

    ###

    def choose_piece(self) -> int:
        return self.make_strategy_choose()

    def place_piece(self) -> tuple[int, int]:
        return self.make_strategy_place()

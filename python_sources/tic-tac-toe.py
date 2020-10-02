#!/usr/bin/env python
# coding: utf-8

# # Tic-Tac-Toe
# 
# Inspired by the [**Blackjack Microchallenge**](https://www.kaggle.com/learn/microchallenges) from the kaggle teams, I decided to create an AI for playing tic-tac-toe autonomously.
# 
# <img src="https://upload.wikimedia.org/wikipedia/commons/3/32/Tic_tac_toe.svg" alt="Tic tac toe.svg" height="145" width="163">
# 
# In the Blackjack exercise the results of the AI are not much better than play randomly. So I want to test the performance of a machine learning resolution approach with another game.
# 
# # Rules
# 
# 1. The game is played on a grid that's 3 squares by 3 squares.
# 
# 2. You are X, your friend (or the computer in this case) is O. Players take turns putting their marks in empty squares.
# 
# 3. The first player to get 3 of her marks in a row (up, down, across, or diagonally) is the winner.
# 
# 4. When all 9 squares are full, the game is over. If no player has 3 marks in a row, the game ends in a tie.
# 
# # Code
# 
# I created a python implementation of the game with an opponent that play random moves.

# In[ ]:


import random

class TicTacToe:
    X_MARK = 'X'
    O_MARK = 'O'

    def __init__(self, callback):
        if not callable(callback):
            raise Exception('TicTacToe need a function to retrieve the next move')
        self.callback = callback

    def _resetBoard(self):
        self.board = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]

    def _getMark(self, mark):
        if mark == TicTacToe.X_MARK:
            return TicTacToe.O_MARK
        else:
            return TicTacToe.X_MARK

    def _getEmpty(self):
        empty = []
        for ri, row in enumerate(self.board):
            for ci, cell in enumerate(row):
                if cell is None:
                    empty.append((ri, ci))
        return empty

    def _getRandomMove(self):
        empty = self._getEmpty()
        return random.choice(empty)

    def _playMove(self, move, mark=None):
        if not mark:
            mark = self._getMark(self.mark)
        row, col = move
        if self.board[row][col] != None:
            return -1
        self.board[row][col] = mark
        return 1 if not self._getEmpty() else 0

    def _checkBoard(self):
        b = self.board
        for i in range(3):
            if (b[i][0] and b[i][0] == b[i][1] and b[i][1] == b[i][2]): # row
                return b[i][0]
            if (b[0][i] and b[0][i] == b[1][i] and b[1][i] == b[2][i]): # column
                return b[0][i]
        if (b[0][0] and b[0][0] == b[1][1] and b[1][1] == b[2][2]): # diagonal
            return b[0][0]
        if (b[0][2] and b[0][2] == b[1][1] and b[1][1] == b[2][0]): # diagonal
            return b[0][2]
        return None

    def _printBoard(self):
        p = lambda row, col: self.board[row][col] or ' '
        print( '\n -----')
        print( '|' + p(0,0) + '|' + p(0,1) + '|' + p(0,2) + '|')
        print( ' -----')
        print( '|' + p(1,0) + '|' + p(1,1) + '|' + p(1,2) + '|')
        print( ' -----')
        print( '|' + p(2,0) + '|' + p(2,1) + '|' + p(2,2) + '|')
        print( ' -----\n')       

    def simulateGame(self, mark='X', play_first=False, verbose=False):
        self.mark = mark
        self._resetBoard()
        printBoard = lambda: self._printBoard() if verbose else None
        if not play_first:
            move = self._getRandomMove()
            self._playMove(move)
        empty = self._getEmpty()
        win = None
        while empty and not win:
            printBoard()
            move = self.callback(self.board, empty, mark)
            self._playMove(move, mark)
            win = self._checkBoard()
            if not self._getEmpty() or win:
                break
            printBoard()
            move = self._getRandomMove()
            self._playMove(move)
            empty = self._getEmpty()
            win = self._checkBoard()
        printBoard()

        if win == mark:
            return 1    # win
        elif win == self._getMark(mark):
            return -1   # lose
        else:
            return 0    # draw

    def simulate(self, n_games):
        win = 0
        for _ in range(n_games):
            mark = random.choice([TicTacToe.X_MARK, TicTacToe.O_MARK])
            play_first = random.choice([True, False])
            res = self.simulateGame(mark=mark, play_first=play_first)
            if res == 1:
                win += 1
        return win


def placeMark(board_state, empty_cells, mark):
    return random.choice(empty_cells)

if __name__ == '__main__':
    from datetime import datetime
    random.seed(datetime.now())

    n_games = 5000
    win = TicTacToe(placeMark).simulate(n_games)
    print(f'Player won {win} out of {n_games} games (win rate = {round((win/n_games) * 100, 2)}%)')


# # Tic-Tac-Toe Player
# 
# To play you need a function that return the next move expressed with a tuple of integer (row, col) in a range 0-8. The function receive the `board_state` parameter as a list of rows with the value inside or `None` otherwhise. The parameter `empty_cells` with a list of positions (tuples) that are currently empty and the parameter `mark` choosen by the user (X or O).
# 
# Here is a simple (though unintelligent) example.

# In[ ]:


import random
from datetime import datetime

random.seed(datetime.now())

def placeMark(board_state, empty_cells, mark):
    """ Return the position to place the mark.
    Ex:
        board_state: [[X, O, X], [X, None, O], [O, None, X]]
        empty_cells: [(1, 1), (2, 1)]
        mark: 'X'
    """
    return random.choice(empty_cells)


# The `TicTacToe` instance receive the place-mark function as a parameter. We can try to simulate a single game.

# In[ ]:


win = TicTacToe(placeMark).simulateGame(verbose=True)
if win == 1:
    print('Won')
elif win == -1:
    print('Lost')
else:
    print('Draw') 


# Or try to simulate multiple random games

# In[ ]:


n_games = 5000
win = TicTacToe(placeMark).simulate(n_games)
print(f'Player won {win} out of {n_games} games (win rate = {round((win/n_games) * 100, 2)}%)')


# # Simulate lots of random games
# 
# I simulated 100K games saving info and results for each of them. Initial conditions for each game and the next move are choosen randomly from the empty-cells bucket. Finally, we put all the games logs into a new DataFrame.

# In[ ]:


import pandas as pd
import copy

def toStr(o):
    """ Makes list/tuple readable and clean
    """
    if isinstance(o, list):
        return str(o).translate(str.maketrans('','', '\'[]'))
    elif isinstance(o, tuple):
        return str(o).strip('()').replace(', ', '-')

def playGame(n_games):
    games = []
    logs = []
    def placeMark(board_state, empty_cells, mark):
        move = random.choice(empty_cells) # randomly choose next move from empty cells
        logs.append((copy.deepcopy(board_state), move)) # deepcopy for list of lists
        return move
    
    tic = TicTacToe(placeMark)
    for _ in range(n_games):
        logs = []
        mark = random.choice([TicTacToe.X_MARK, TicTacToe.O_MARK])
        play_first = random.choice([True, False])
        win = tic.simulateGame(mark=mark, play_first=play_first)
        for i, (board_state, move) in enumerate(reversed(logs)):
            winner = win == 1
            result = 1.0 * winner if i == 0 else .4 + .2 * winner
            games.append({
                'mark': mark,
#                 'play_first': play_first,
                'board_state': toStr(board_state),
                'move': toStr(move),
                'result': result,
            })
    return games

N_GAMES = 100000
games = playGame(N_GAMES)
df = pd.DataFrame(games)


# In[ ]:


df.head()


# # Encode features
# I encode all the categorical features, saving the `LabelEncoder` instances for later.

# In[ ]:


from sklearn.preprocessing import LabelEncoder

train = pd.DataFrame() # dataset for train the model
bs_encoder = LabelEncoder()
train['board_state'] = bs_encoder.fit_transform(df['board_state'])
mark_encoder = LabelEncoder()
train['mark'] = mark_encoder.fit_transform(df['mark'])
move_encoder = LabelEncoder()
train['move'] = move_encoder.fit_transform(df['move'])
train['result'] = df['result']


# In[ ]:


train.head()


# # Model fitting

# In[ ]:


y = train['result']
X = train.drop('result', axis=1)


# In[ ]:


from sklearn.tree import DecisionTreeRegressor

model = DecisionTreeRegressor()
model.fit(X, y)


# # Testing our AI
# For using the AI in our `placeMark` function, I created a loop for each empty cell, where we test the predicted results with the model. After that, I retrieved the move with the best predicted result and returned for placing my mark. I used the previously saved encoders to inverse transform the move from the integer value to the string one.

# In[ ]:


import numpy as np

def getMoveFromPred(preds, empty):
    """ Decode and format the predicted move
    """
    p = max(preds, key=lambda x: x[0]) # get the max value for predicted result
    move_dec = move_encoder.inverse_transform([p[1]])[0] # decode from int to categorical value
    row, col = move_dec.split('-')
    return (int(row), int(col))

def placeMark(board_state, empty_cells, mark):
    """ Predict the result for each possible move
    """
    preds = []
    empty_index = move_encoder.transform([toStr(e) for e in empty_cells]) # transform empty cells to index using encoder
    for i in empty_index:
        p = np.reshape([
            bs_encoder.transform([toStr(board_state)])[0],
            mark_encoder.transform([mark])[0],
            i
        ],  (1, -1))
        preds.append((model.predict(p), i)) # predict result for each possible move and store in a list
    move = getMoveFromPred(preds, empty_cells)
    
    return move


# We can try to simulate a single game or a lots of games and check the accuracy of the model.

# In[ ]:


win = TicTacToe(placeMark).simulateGame()
if win == 1:
    print('Won')
elif win == -1:
    print('Lost')
else:
    print('Draw') 


# In[ ]:


n_games = 500
win = TicTacToe(placeMark).simulate(n_games)
print(f'Player won {win} out of {n_games} games (win rate = {round((win/n_games) * 100, 2)}%)')


# # Discuss Your Results

# [My attemps](https://www.kaggle.com/ikarus777/blackjack-microchallenge-812b68) to improve the obtained results when I played blackjack randomly didn't go very well. Actually, the differences from random playing vs AI are very little with an accuracy of 41.7% vs 42.7%. So for my blackjack solution, the machine learning approach didn't improve the score obtained when I played randomly.
# 
# In this case the results are different. While play randomly gave us an accuracy around ~44%, the results obtained using the trained model are around ~92%. So a very good **increase**. Anyway, we should keep in mind that the adversary play *completely random* and cannot learn from the mistakes.

# # AI vs AI
# Can we train another model and play some games with **AI vs AI**?

# In[ ]:


class TicTacToeAI:
    X_MARK = 'X'
    O_MARK = 'O'

    def __init__(self, callback_X, callback_O):
        if not callable(callback_X) or not callable(callback_O):
            raise Exception('TicTacToeAI need two functions to retrieve next moves')
        self.callback_X = callback_X
        self.callback_O = callback_O

    def _resetBoard(self):
        self.board = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]

    def _getEmpty(self):
        empty = []
        for ri, row in enumerate(self.board):
            for ci, cell in enumerate(row):
                if cell is None:
                    empty.append((ri, ci))
        return empty

    def _playMove(self, move, mark):
        row, col = move
        if self.board[row][col] != None:
            return -1
        self.board[row][col] = mark
        return 1 if not self._getEmpty() else 0

    def _checkBoard(self):
        b = self.board
        for i in range(3):
            if (b[i][0] and b[i][0] == b[i][1] and b[i][1] == b[i][2]): # row
                return b[i][0]
            if (b[0][i] and b[0][i] == b[1][i] and b[1][i] == b[2][i]): # column
                return b[0][i]
        if (b[0][0] and b[0][0] == b[1][1] and b[1][1] == b[2][2]): # diagonal
            return b[0][0]
        if (b[0][2] and b[0][2] == b[1][1] and b[1][1] == b[2][0]): # diagonal
            return b[0][2]
        return None

    def _printBoard(self):
        p = lambda row, col: self.board[row][col] or ' '
        print( '\n -----')
        print( '|' + p(0,0) + '|' + p(0,1) + '|' + p(0,2) + '|')
        print( ' -----')
        print( '|' + p(1,0) + '|' + p(1,1) + '|' + p(1,2) + '|')
        print( ' -----')
        print( '|' + p(2,0) + '|' + p(2,1) + '|' + p(2,2) + '|')
        print( ' -----\n')

    def _getSeq(self, play_first):
        if play_first == 'X':
            return [('X', self.callback_X), ('O', self.callback_O)]
        else:
            return [('O', self.callback_O), ('X', self.callback_X)]

    def simulateGame(self, play_first='X', verbose=False):
        self._resetBoard()
        sequence = self._getSeq(play_first)
        printBoard = lambda: self._printBoard() if verbose else None
        empty = self._getEmpty()
        win = None
        while empty and not win:
            for mark, callback in sequence:
                printBoard()
                move = callback(self.board, empty, mark)
                self._playMove(move, mark)
                win = self._checkBoard()
                empty = self._getEmpty()
                if not empty or win:
                    break
        return win if win in ['X', 'O'] else 'D'

    def simulate(self, n_games):
        win_X = 0
        win_O = 0
        for _ in range(n_games):
            play_first = random.choice(['X', 'O'])
            res = self.simulateGame(play_first=play_first)
            if res == 'X':
                win_X += 1
            elif res == 'O':
                win_O += 1
        return (win_X, win_O)


def placeMark1(board_state, empty_cells, mark):
    # X
    return random.choice(empty_cells)

def placeMark2(board_state, empty_cells, mark):
    # O
    return random.choice(empty_cells)

if __name__ == '__main__':
    from datetime import datetime
    random.seed(datetime.now())

    n_games = 5000
    win_X, win_O = TicTacToeAI(placeMark1, placeMark2).simulate(n_games)
    print(f'Player X won {win_X} out of {n_games} games (win rate = {round((win_X/n_games) * 100, 2)}%)')
    print(f'Player O won {win_O} out of {n_games} games (win rate = {round((win_O/n_games) * 100, 2)}%)')


# In[ ]:


from sklearn.ensemble import RandomForestRegressor

rf = RandomForestRegressor(n_estimators=100)
rf.fit(X.values, y.ravel())


# In[ ]:


def placeMarkRF(board_state, empty_cells, mark):
    """ Predict the result for each possible move
    """
    preds = []
    empty_index = move_encoder.transform([toStr(e) for e in empty_cells]) # transform empty cells to index using encoder
    for i in empty_index:
        p = np.reshape([
            bs_encoder.transform([toStr(board_state)])[0],
            mark_encoder.transform([mark])[0],
            i
        ],  (1, -1))
        preds.append((rf.predict(p), i)) # predict result for each possible move and store in a list
    move = getMoveFromPred(preds, empty_cells)
    
    return move


# In[ ]:


def placeMark1(board_state, empty_cells, mark):
    return random.choice(empty_cells)

def placeMark2(board_state, empty_cells, mark):
    return empty_cells[0]


# In[ ]:


n_games = 100
win_X, win_O = TicTacToeAI(placeMark1, placeMark2).simulate(n_games)
print(f'Player X won {win_X} out of {n_games} games (win rate = {round((win_X/n_games) * 100, 2)}%)')
print(f'Player O won {win_O} out of {n_games} games (win rate = {round((win_O/n_games) * 100, 2)}%)')


# In[ ]:


win_X, win_O = TicTacToeAI(placeMark1, placeMarkRF).simulate(n_games)
print(f'Player X won {win_X} out of {n_games} games (win rate = {round((win_X/n_games) * 100, 2)}%)')
print(f'Player O won {win_O} out of {n_games} games (win rate = {round((win_O/n_games) * 100, 2)}%)')


# In[ ]:


win_X, win_O = TicTacToeAI(placeMark, placeMarkRF).simulate(n_games)
print(f'Player X won {win_X} out of {n_games} games (win rate = {round((win_X/n_games) * 100, 2)}%)')
print(f'Player O won {win_O} out of {n_games} games (win rate = {round((win_O/n_games) * 100, 2)}%)')


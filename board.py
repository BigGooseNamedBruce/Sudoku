"""This file contains all the logic for solving and generating the sudoku board"""

class Board():

    def __init__(self, board):
        """Constructor method"""
        self.board = board
        self.solutions = []
        self.solution = []
        self.solutionIndex = -1

    def is_valid(self, row, column, number):
        """This method returns true if a number is valid given the row and column and false if it isn't"""

        for i in range(9):
            # Checks if the number can fit into the row
            if self.board[row][i] == number:
                return False

            # Checks if the number can fit into the column
            if self.board[i][column] == number:
                return False

        # Checks if the number can fit into its box
        for i in range(3):
            for j in range(3):
                if self.board[(row // 3) * 3 + i][(column // 3) * 3 + j] == number:
                    return False

        return True

    def solve(self):
        """This method will solve the sudoku board by using recursive backtracking"""

        # Goes through every cell in the board
        for row in range(9):
            for column in range(9):

                # Skips the square if the cell isn't empty
                if self.board[row][column] != 0:
                    continue

                # Tests every valid number if the cell is empty
                for testNumber in range(1, 10):
                    if not self.is_valid(row, column, testNumber):
                        continue

                    else:
                        # Tests the number
                        self.board[row][column] = testNumber
                        self.solve()

                        # Backtracks because the number isn't right
                        self.board[row][column] = 0

                # There are no valid solutions
                return None

        # Adds a solution to a list of possible solutions
        self.solutions.append([board[:] for board in self.board])
        self.set_solution(self.solutions[self.solutionIndex])

    def get_next_solution(self):

        if self.solutionIndex >= len(self.solutions) - 1:
            self.solutionIndex = 0
        else:
            self.solutionIndex += 1

        self.set_solution(self.solutions[self.solutionIndex])


    def get_board(self):
        """This is a accesor method that returns a copy of the board"""
        return [row[:] for row in self.board]

    def set_board(self, board):
        self.board = [row[:] for row in board]

    def set_solution(self, board):
        self.solution = [row[:] for row in board]

    def get_solved_board(self):
        """This is a accesor method that returns a copy of the solved board"""
        return [row[:] for row in self.solution]
"""This file contains all the code for creating the board"""


import pygame


def find_width_intervals(width):
    """This helper function calculates and returns a dictionary with the row number as the value
       and of the lengths between each vertical line as the value"""

    widthIntervals = [width // 9] * 10
    widthRemainders = width % 9

    for remainder in range(widthRemainders):
        widthIntervals[remainder] += 1

    return widthIntervals




def find_height_intervals(height):
    """This helper function calculates and returns a list of the lengths between each horizontal line"""
    heightIntervals = [height // 9] * 10
    heightRemainders = height % 9

    for remainder in range(heightRemainders):
        heightIntervals[remainder] += 1

    return heightIntervals



class Cell(pygame.sprite.Sprite):

    def __init__(self, screen, width, height, alpha, colour):

        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.width = width
        self.height = height
        self.widthIntervals = find_width_intervals(width)
        self.heightIntervals = find_height_intervals(height)

        self.alpha = alpha
        self.colour = colour
        self.coordinates = (None, None)


    def get_cell_coordinate(self):
        """This is an accesor method that will return the current coordinate of the cell"""
        return self.coordinates

    def set_cell_coordinate(self, coordinate):
        """This mutator method accepts a tuple as a paramter. It will check if that coordinate is valid position and set the
        coordinate instance variable to that position. If it isn't will set it to a nearby valid position"""

        if coordinate == (None, None):
            return

        coordinateX = coordinate[0]
        coordinateY = coordinate[1]

        # The coordinate is above the screen and will set it to the bottom of the screen
        if coordinate[1] < 0:
            coordinateY = 8

        # The coordinate is below the screen and will set it to the top of the screen
        if coordinate[1] > 8:
            coordinateY = 0

        # The coordinate is left of the screen and will set it to the right side of the screen
        if coordinate[0] < 0:
            coordinateX = 8

        # The coordinate is right of the screen and will set it to the left side of the screen
        if coordinate[0] > 8:
            coordinateX = 0

        self.coordinates = (coordinateX, coordinateY)


    def find_cell_coordinate(self, mousePosX, mousePosY):
        """Given the coordinates of the mouse, this method will calculate the coordinates of where a cell box should be placed
        This method will return a tuple of the coordinates of where the cell box should be placed"""

        if 0 > mousePosX or mousePosX > self.width:
            return (None, None)
        elif 0 > mousePosY or mousePosY > self.height:
            return (None, None)

        widthIntervalIndex = 0
        heighIntervaltIndex = 0

        for i in range(len(self.widthIntervals) - 1):
            if mousePosX >= sum(self.widthIntervals[:i]) and mousePosX <= sum(self.widthIntervals[:i + 1]):
                widthIntervalIndex = i

        for i in range(len(self.heightIntervals) - 1):
            if mousePosY >= sum(self.heightIntervals[:i]) and mousePosY <= sum(self.heightIntervals[:i + 1]):
                heighIntervaltIndex = i

        return (widthIntervalIndex, heighIntervaltIndex)


class Opaque(Cell):

    def __init__(self, screen, width, height, alpha, colour):

        super().__init__(screen, width, height, alpha, colour)


        self.image = pygame.Surface((0, 0))
        self.image = self.image.convert()
        self.image.set_alpha(alpha)
        self.image.fill(colour)

        self.rect = self.image.get_rect()

        self.rect.left = -100
        self.rect.top = -100


    def update(self):

        # Skips drawing the cell since the cell is currently in an invalid position
        if self.coordinates == (None, None):
            return

        self.image = pygame.Surface((self.widthIntervals[self.coordinates[0]], self.heightIntervals[self.coordinates[1]]))
        self.image = self.image.convert()
        self.image.set_alpha(self.alpha)
        self.image.fill(self.colour)

        self.rect = self.image.get_rect()

        self.rect.left = sum(self.widthIntervals[:self.coordinates[0]])
        self.rect.top = sum(self.heightIntervals[:self.coordinates[1]])



class Darken(Cell):

    def __init__(self, screen, width, height, alpha, colour):

        super().__init__(screen, width, height, alpha, colour)

        self.image = pygame.Surface((0, 0))
        self.image = self.image.convert()
        self.image.set_alpha(alpha)
        self.image.fill(colour)

        self.rect = self.image.get_rect()

        self.rect.left = 0
        self.rect.top = 0


    def update(self):

        # Skips drawing the cell since the cell is currently in an invalid position
        if self.coordinates == (None, None):
            return

        self.image = pygame.Surface((self.widthIntervals[self.coordinates[0]], self.heightIntervals[self.coordinates[1]]))
        self.image = self.image.convert()
        self.image.set_alpha(self.alpha)
        self.image.fill(self.colour)

        self.rect = self.image.get_rect()

        self.rect.left = sum(self.widthIntervals[:self.coordinates[0]])
        self.rect.top = sum(self.heightIntervals[:self.coordinates[1]])




class Lines(pygame.sprite.Sprite):

    def __init__(self, screen, width, height, lineNumber, thickness, isHorizontal):

        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.width = width
        self.height = height
        self.widthIntervals = [0] + find_width_intervals(width)
        self.heightIntervals = [0] + find_height_intervals(height)

        self.lineNumber = lineNumber
        self.thickness = thickness
        self.isHorizontal = isHorizontal

        if self.isHorizontal:
            self.image = pygame.Surface((self.width, self.thickness))
        else:
            self.image = pygame.Surface((self.thickness, self.height))

        self.image = self.image.convert()
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()

        if self.isHorizontal:
            self.rect.left = 0
            self.rect.top = sum(self.heightIntervals[:self.lineNumber + 1]) - round(self.thickness / 2)
        else:
            self.rect.left = sum(self.widthIntervals[:self.lineNumber + 1]) - round(self.thickness / 2)
            self.rect.top = 0


class Number(pygame.sprite.Sprite):
    def __init__(self, screen, width, height, number, colour, font, fontSize):

        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.width = width
        self.height = height
        self.widthIntervals = find_width_intervals(width)
        self.heightIntervals = find_height_intervals(height)

        self.number = number
        self.colour = colour
        self.font = pygame.font.Font(f"./assets/fonts/{font}", fontSize)

class BoardNumber(Number):

    def __init__(self, screen, width, height, number, colour, font, fontSize, row, column):

        super().__init__(screen, width, height, number, colour, font, fontSize)

        self.row = row
        self.column = column

        self.image = self.font.render(str(self.number), True, self.colour)

        # Makes the space looks empty if the number is zero
        if self.number == 0:
            self.image.set_alpha(0)

        self.rect = self.image.get_rect()
        # Centres the number to the cell
        self.rect.left = sum(self.widthIntervals[:self.column]) + int(self.widthIntervals[self.column] / 2) - int(self.image.get_width() / 2)
        self.rect.top = sum(self.heightIntervals[:self.row]) + int(self.heightIntervals[self.row] / 2) - int(self.image.get_height() / 2)

    def update(self):

        self.image = self.font.render(str(self.number), True, self.colour)

        # Makes the space looks empty if the number is zero
        if self.number == 0:
            self.image.set_alpha(0)
        else:
            self.image.set_alpha(255)

        self.rect = self.image.get_rect()

        # Centres the number to the cell
        self.rect.left = sum(self.widthIntervals[:self.column]) + int(self.widthIntervals[self.column] / 2) - int(self.image.get_width() / 2)
        self.rect.top = sum(self.heightIntervals[:self.row]) + int(self.heightIntervals[self.row] / 2) - int(self.image.get_height() / 2)

class ButtonNumber(Number):

    def __init__(self, screen, width, height, number, colour, font, fontSize, column):

        super().__init__(screen, width, height, number, colour, font, fontSize)

        self.column = column

        self.image = self.font.render(str(self.number), True, self.colour)
        self.rect = self.image.get_rect()

        # Centres the number to the cell
        self.rect.left = sum(self.widthIntervals[:self.column]) + int(self.widthIntervals[self.column] / 2) - int(self.image.get_width() / 2)
        self.rect.top = self.height + 10

    def update(self):
        self.image = self.font.render(str(self.number), True, self.colour)
        self.rect = self.image.get_rect()

        # Centres the number to the cell
        self.rect.left = sum(self.widthIntervals[:self.column]) + int(self.widthIntervals[self.column] / 2) - int(self.image.get_width() / 2)
        self.rect.top = self.height + 10



'''

class Cell(pygame.sprite.Sprite):

    def __init__(self, screen, width, height, alpha, colour):

        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.width = width
        self.height = height
        self.widthIntervals = find_width_intervals(width)
        self.heightIntervals = find_height_intervals(height)

        self.alpha = alpha
        self.colour = colour
        self.coordinates = (-1, -1)
        self.mousePosX = -1
        self.mousePosY = -1

    def find_cell_coordinate(self, mousePosX, mousePosY):
        """Given the coordinates of the mouse, this method will calculate the coordinates of where a cell box should be placed
        This method will return a tuple of the coordinates of where the cell box should be placed"""

        if 0 > mousePosX or mousePosX > self.width:
            return (-1, -1)
        elif 0 > mousePosY or mousePosY > self.height:
            return (-1, -1)

        widthIntervalIndex = 0
        heighIntervaltIndex = 0

        for i in range(len(self.widthIntervals) - 1):
            if mousePosX >= sum(self.widthIntervals[:i]) and mousePosX <= sum(self.widthIntervals[:i + 1]):
                widthIntervalIndex = i

        for i in range(len(self.heightIntervals) - 1):
            if mousePosY >= sum(self.heightIntervals[:i]) and mousePosY <= sum(self.heightIntervals[:i + 1]):
                heighIntervaltIndex = i

        return (widthIntervalIndex, heighIntervaltIndex)

    def line_width_adjustment_factor(self):
        """To account for the width of the lines, this method will calculate the new dimensions of the cell"""
        pass

class Opaque(Cell):

    def __init__(self, screen, width, height, alpha, colour):

        super().__init__(screen, width, height, alpha, colour)


        self.image = pygame.Surface((0, 0))
        self.image = self.image.convert()
        self.image.set_alpha(alpha)
        self.image.fill(colour)

        self.rect = self.image.get_rect()

        self.rect.left = -100
        self.rect.top = -100


    def update(self):
        
        self.coordinates = super().find_cell_coordinate(self.mousePosX, self.mousePosY)

        # Invalid position
        if self.coordinates == (-1, -1):
            return

        self.image = pygame.Surface((self.widthIntervals[self.coordinates[0]], self.heightIntervals[self.coordinates[1]]))
        self.image = self.image.convert()
        self.image.set_alpha(self.alpha)
        self.image.fill(self.colour)

        self.rect = self.image.get_rect()

        if self.mousePosX == -1 or self.mousePosY == -1:
            self.rect.left = -100
            self.rect.top = -100
        else:

            self.rect.left = sum(self.widthIntervals[:self.coordinates[0]])
            self.rect.top = sum(self.heightIntervals[:self.coordinates[1]])



class Darken(Cell):

    def __init__(self, screen, width, height, alpha, colour):

        super().__init__(screen, width, height, alpha, colour)

        self.image = pygame.Surface((0, 0))
        self.image = self.image.convert()
        self.image.set_alpha(alpha)
        self.image.fill(colour)

        self.rect = self.image.get_rect()

        self.rect.left = 0
        self.rect.top = 0

    def update(self):
        self.coordinates = super().find_cell_coordinate(self.mousePosX, self.mousePosY)

        # Invalid position
        if self.coordinates == (-1, -1):
            return

        self.image = pygame.Surface((self.widthIntervals[self.coordinates[0]], self.heightIntervals[self.coordinates[1]]))
        self.image = self.image.convert()
        self.image.set_alpha(self.alpha)
        self.image.fill(self.colour)

        self.rect = self.image.get_rect()

        if self.mousePosX == -1 or self.mousePosY == -1:
            self.rect.left = -100
            self.rect.top = -100
        else:

            self.rect.left = sum(self.widthIntervals[:self.coordinates[0]])
            self.rect.top = sum(self.heightIntervals[:self.coordinates[1]])




'''
import pygame
import pprint

import board as solver
import grid


def main():

    '''board = [[0, 0, 5, 3, 0, 0, 0, 0, 0],
             [8, 0, 0, 0, 0, 0, 0, 2, 0],
             [0, 7, 0, 0, 1, 0, 5, 0, 0],
             [4, 0, 0, 0, 0, 5, 3, 0, 0],
             [0, 1, 0, 0, 7, 0, 0, 0, 6],
             [0, 0, 3, 2, 0, 0, 0, 8, 0],
             [0, 6, 0, 5, 0, 0, 0, 0, 9],
             [0, 0, 4, 0, 0, 0, 0, 3, 0],
             [0, 0, 0, 0, 0, 9, 7, 0, 0]]'''

    board = [[0, 0, 5, 3, 0, 0, 0, 0, 0],
             [8, 0, 0, 0, 0, 0, 0, 2, 0],
             [0, 7, 0, 0, 1, 0, 5, 0, 0],
             [4, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 1, 0, 0, 7, 0, 0, 0, 6],
             [0, 0, 3, 2, 0, 0, 0, 8, 0],
             [0, 6, 0, 5, 0, 0, 0, 0, 9],
             [0, 0, 4, 0, 0, 0, 0, 3, 0],
             [0, 0, 0, 1, 0, 9, 7, 0, 0]]

    solvedBoard = solver.Board(board)
    solvedBoard.solve()
    solvedBoard.set_board(solvedBoard.solution)

    print(f'There are {len(solvedBoard.solutions)} solutions')

    pygame.init()

    BOARD_SIZE = (750, 750)
    BUTTON_ADJUSTMENT_FACTOR = 1.15
    screen = pygame.display.set_mode((BOARD_SIZE[0], round(BOARD_SIZE[1] * BUTTON_ADJUSTMENT_FACTOR)))

    pygame.display.set_caption("Sudoku")

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))
    screen.blit(background, (0, 0))

    lines = []

    for horizontalLine in range(10):
        # Line is bold
        if horizontalLine % 3 == 0:
            lines.append(grid.Lines(screen, BOARD_SIZE[0], BOARD_SIZE[1], horizontalLine, 3, True))
        # Line is not bold
        else:
            lines.append(grid.Lines(screen, BOARD_SIZE[0], BOARD_SIZE[1], horizontalLine, 1, True))

    for verticalLine in range(10):
        # Line is bold
        if verticalLine % 3 == 0:
            lines.append(grid.Lines(screen, BOARD_SIZE[0], BOARD_SIZE[1], verticalLine, 3, False))
        # Line is not bold
        else:
            lines.append(grid.Lines(screen, BOARD_SIZE[0], BOARD_SIZE[1], verticalLine, 1, False))

    lineSprites = pygame.sprite.OrderedUpdates(lines)


    opaqueCell = grid.Opaque(screen, BOARD_SIZE[0], BOARD_SIZE[1], 100, (0, 255, 0))

    darkenCell = grid.Darken(screen, BOARD_SIZE[0], BOARD_SIZE[1], 200, (0, 255, 0))


    boardNumbers = []

    for row in range(len(board)):
        rowBoardNumbers = []
        for column in range(len(board[0])):
            rowBoardNumbers.append(grid.BoardNumber(screen, BOARD_SIZE[0], BOARD_SIZE[1], board[row][column], (0, 0, 0), "Lato-Light.ttf", 72, row, column))

        boardNumbers.append(rowBoardNumbers)

    boardNumberSprites = pygame.sprite.OrderedUpdates(boardNumbers)


    buttonNumbers = []

    for number in range(1, 10):
        buttonNumbers.append(grid.ButtonNumber(screen, BOARD_SIZE[0], BOARD_SIZE[1], number, (0, 0, 0), "Lato-Light.ttf", 72, number - 1))

    buttonNumberSprites = pygame.sprite.OrderedUpdates(buttonNumbers)


    allSprites = pygame.sprite.OrderedUpdates(opaqueCell, darkenCell, boardNumberSprites, buttonNumberSprites, lineSprites)

    clock = pygame.time.Clock()
    clickedButton = 0
    run = True

    while run:
        clock.tick(30)
        screen.blit(background, (0, 0))



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                #darkenCell.mousePosX = pygame.mouse.get_pos()[0]
                #darkenCell.mousePosY = pygame.mouse.get_pos()[1]
                darkenCell.set_cell_coordinate(darkenCell.find_cell_coordinate(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
                #print(darkenCell.mousePosX, darkenCell.mousePosY, darkenCell.coordinates)

                for button in buttonNumbers:
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        clickedButton = button.number

            # User inputted a number using the keyboard
            if event.type == pygame.KEYDOWN and darkenCell.get_cell_coordinate() != (None, None):
                if event.key == pygame.K_1:
                    board[darkenCell.coordinates[1]][darkenCell.coordinates[0]] = 1
                elif event.key == pygame.K_2:
                    board[darkenCell.coordinates[1]][darkenCell.coordinates[0]] = 2
                elif event.key == pygame.K_3:
                    board[darkenCell.coordinates[1]][darkenCell.coordinates[0]] = 3
                elif event.key == pygame.K_4:
                    board[darkenCell.coordinates[1]][darkenCell.coordinates[0]] = 4
                elif event.key == pygame.K_5:
                    board[darkenCell.coordinates[1]][darkenCell.coordinates[0]] = 5
                elif event.key == pygame.K_6:
                    board[darkenCell.coordinates[1]][darkenCell.coordinates[0]] = 6
                elif event.key == pygame.K_7:
                    board[darkenCell.coordinates[1]][darkenCell.coordinates[0]] = 7
                elif event.key == pygame.K_8:
                    board[darkenCell.coordinates[1]][darkenCell.coordinates[0]] = 8
                elif event.key == pygame.K_9:
                    board[darkenCell.coordinates[1]][darkenCell.coordinates[0]] = 9

                elif event.key == pygame.K_BACKSPACE:
                    board[darkenCell.coordinates[1]][darkenCell.coordinates[0]] = 0

                # Moving the selected cell using the arrow keys
                elif event.key == pygame.K_UP:
                    darkenCell.set_cell_coordinate((darkenCell.get_cell_coordinate()[0], darkenCell.get_cell_coordinate()[1] - 1))

                elif event.key == pygame.K_DOWN:
                    darkenCell.set_cell_coordinate((darkenCell.get_cell_coordinate()[0], darkenCell.get_cell_coordinate()[1] + 1))

                elif event.key == pygame.K_LEFT:
                    darkenCell.set_cell_coordinate((darkenCell.get_cell_coordinate()[0] - 1, darkenCell.get_cell_coordinate()[1]))

                elif event.key == pygame.K_RIGHT:
                    darkenCell.set_cell_coordinate((darkenCell.get_cell_coordinate()[0] + 1, darkenCell.get_cell_coordinate()[1]))

            #print(clickedButton)
            if clickedButton and darkenCell.get_cell_coordinate() != (None, None):

                if clickedButton == 1:
                    board[darkenCell.coordinates[1]][darkenCell.coordinates[0]] = 1
                elif clickedButton == 2:
                    board[darkenCell.coordinates[1]][darkenCell.coordinates[0]] = 2
                elif clickedButton == 3:
                    board[darkenCell.coordinates[1]][darkenCell.coordinates[0]] = 3
                elif clickedButton == 4:
                    board[darkenCell.coordinates[1]][darkenCell.coordinates[0]] = 4
                elif clickedButton == 5:
                    board[darkenCell.coordinates[1]][darkenCell.coordinates[0]] = 5
                elif clickedButton == 6:
                    board[darkenCell.coordinates[1]][darkenCell.coordinates[0]] = 6
                elif clickedButton == 7:
                    board[darkenCell.coordinates[1]][darkenCell.coordinates[0]] = 7
                elif clickedButton == 8:
                    board[darkenCell.coordinates[1]][darkenCell.coordinates[0]] = 8
                elif clickedButton == 9:
                    board[darkenCell.coordinates[1]][darkenCell.coordinates[0]] = 9

                # Reset which button is currently being clicked
                clickedButton = 0

            # Displays a potential solution onto the board
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                solvedBoard.get_next_solution()
                board = solvedBoard.get_solved_board()


        # Updates the game board
        for row in range(len(board)):
            for column in range(len(board[0])):
                if boardNumbers[row][column].number != board[row][column]:
                    boardNumbers[row][column].number = board[row][column]

                # User entered the wrong number
                if board[row][column] != solvedBoard.solution[row][column] and board[row][column] != 0:
                    boardNumbers[row][column].colour = (255, 0, 0)

                # User entered the right number
                else:
                    boardNumbers[row][column].colour = (0, 0, 0)


        # Stops drawing the opaque cell over the darken cell
        if opaqueCell.coordinates == darkenCell.coordinates:
            opaqueCell.alpha = 0
        else:
            opaqueCell.alpha = 100


        # Avoids drawing an opaque cell when the cursor hasn't been on screen yet
        if pygame.mouse.get_pos() != (0, 0):
            opaqueCell.set_cell_coordinate(opaqueCell.find_cell_coordinate(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))




        # Updates all the sprites
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
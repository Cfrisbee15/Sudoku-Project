import sys
import pygame
from board import Board

WIDTH = 660
HEIGHT = 780
FPS = 60

WHITE = (255, 255, 255)
BLACK = (25, 25, 25)
NAVY = (19, 41, 93)
ORANGE = (232, 127, 53)
LIGHT_BG = (247, 247, 247)
BUTTON_FILL = (244, 159, 74)
BUTTON_BORDER = (130, 72, 35)
GRAY = (100, 100, 100)
GREEN = (50, 140, 70)
RED = (170, 50, 50)


class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self, screen, font):
        pygame.draw.rect(screen, BUTTON_FILL, self.rect)
        pygame.draw.rect(screen, BUTTON_BORDER, self.rect, 4)

        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


def draw_header(screen, title_font, subtitle=None):
    title = title_font.render("Sudoku", True, NAVY)
    title_rect = title.get_rect(center=(WIDTH // 2, 45))
    screen.blit(title, title_rect)
    pygame.draw.line(screen, ORANGE, (40, 70), (WIDTH - 40, 70), 4)

    if subtitle:
        sub_font = pygame.font.SysFont("arial", 24)
        sub = sub_font.render(subtitle, True, BLACK)
        sub_rect = sub.get_rect(center=(WIDTH // 2, 145))
        screen.blit(sub, sub_rect)


def draw_start_screen(screen, fonts, buttons, bg):
    screen.blit(bg, (0, 0))

    welcome = fonts["big"].render("Welcome to Sudoku", True, BLACK)
    welcome_rect = welcome.get_rect(center=(WIDTH // 2, 210))
    screen.blit(welcome, welcome_rect)

    instructions = fonts["medium"].render("Choose Game Mode:", True, BLACK)
    instructions_rect = instructions.get_rect(center=(WIDTH // 2, 315))
    screen.blit(instructions, instructions_rect)

    for button in buttons:
        button.draw(screen, fonts["button"])


def draw_game_screen(screen, fonts, board, reset_button, restart_button, exit_button):
    screen.fill(LIGHT_BG)
    draw_header(screen, fonts["title"], "Fill the board")

    info = fonts["small"].render(
        "Click a cell, type 1-9 to sketch, Enter to place, Backspace/Delete to clear.",
        True,
        GRAY,
    )
    info2 = fonts["small"].render("Arrow keys can move the selected cell.", True, GRAY)
    screen.blit(info, (40, 80))
    screen.blit(info2, (40, 102))

    board.draw()

    reset_button.draw(screen, fonts["button"])
    restart_button.draw(screen, fonts["button"])
    exit_button.draw(screen, fonts["button"])


def draw_end_screen(screen, fonts, won, button):
    screen.fill(LIGHT_BG)
    draw_header(screen, fonts["title"])

    if won:
        text = fonts["end"].render("Game Won!", True, GREEN)
        sub_text = fonts["medium"].render("Nice job solving the puzzle.", True, BLACK)
    else:
        text = fonts["end"].render("Game Over", True, RED)
        sub_text = fonts["medium"].render("The board is full, but it is not correct.", True, BLACK)

    text_rect = text.get_rect(center=(WIDTH // 2, 250))
    sub_rect = sub_text.get_rect(center=(WIDTH // 2, 315))
    screen.blit(text, text_rect)
    screen.blit(sub_text, sub_rect)

    button.draw(screen, fonts["button"])


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    bg = pygame.image.load("sudoku_background.jpg")
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku")
    clock = pygame.time.Clock()

    fonts = {
        "title": pygame.font.SysFont("arial", 36, bold=True),
        "big": pygame.font.SysFont("arial", 44, bold=True),
        "medium": pygame.font.SysFont("arial", 26, bold=True),
        "small": pygame.font.SysFont("arial", 20),
        "button": pygame.font.SysFont("arial", 24, bold=True),
        "end": pygame.font.SysFont("arial", 56, bold=True),
    }

    easy_button = Button(90, 350, 140, 70, "EASY")
    medium_button = Button(260, 350, 140, 70, "MEDIUM")
    hard_button = Button(430, 350, 140, 70, "HARD")

    reset_button = Button(120, 710, 120, 55, "RESET")
    restart_button = Button(270, 710, 120, 55, "RESTART")
    exit_button = Button(420, 710, 120, 55, "EXIT")

    end_button = Button(255, 390, 150, 65, "RESTART")

    state = "start"
    board = None

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if state == "start":
                    if easy_button.is_clicked(mouse_pos):
                        board = Board(WIDTH, HEIGHT, screen, 30)
                        state = "game"
                    elif medium_button.is_clicked(mouse_pos):
                        board = Board(WIDTH, HEIGHT, screen, 40)
                        state = "game"
                    elif hard_button.is_clicked(mouse_pos):
                        board = Board(WIDTH, HEIGHT, screen, 50)
                        state = "game"

                elif state == "game":
                    clicked_cell = board.click(mouse_pos[0], mouse_pos[1])
                    if clicked_cell is not None:
                        board.select(clicked_cell[0], clicked_cell[1])
                    elif reset_button.is_clicked(mouse_pos):
                        board.reset_to_original()
                    elif restart_button.is_clicked(mouse_pos):
                        state = "start"
                        board = None
                    elif exit_button.is_clicked(mouse_pos):
                        pygame.quit()
                        sys.exit()

                elif state == "won" or state == "lost":
                    if end_button.is_clicked(mouse_pos):
                        state = "start"
                        board = None

            if event.type == pygame.KEYDOWN and state == "game" and board is not None:
                if event.key == pygame.K_UP:
                    board.move_selection(-1, 0)
                elif event.key == pygame.K_DOWN:
                    board.move_selection(1, 0)
                elif event.key == pygame.K_LEFT:
                    board.move_selection(0, -1)
                elif event.key == pygame.K_RIGHT:
                    board.move_selection(0, 1)
                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    board.clear()
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    board.place_number()
                    if board.is_full():
                        if board.check_board():
                            state = "won"
                        else:
                            state = "lost"
                elif pygame.K_1 <= event.key <= pygame.K_9:
                    board.sketch(event.key - pygame.K_0)
                elif pygame.K_KP1 <= event.key <= pygame.K_KP9:
                    board.sketch(event.key - pygame.K_KP0)

        if state == "start":
            draw_start_screen(screen, fonts, [easy_button, medium_button, hard_button], bg)
        elif state == "game" and board is not None:
            draw_game_screen(screen, fonts, board, reset_button, restart_button, exit_button)
        elif state == "won":
            draw_end_screen(screen, fonts, True, end_button)
        elif state == "lost":
            draw_end_screen(screen, fonts, False, end_button)

        pygame.display.update()


if __name__ == "__main__":
    main()

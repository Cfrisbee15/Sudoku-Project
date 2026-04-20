import pygame
from cell import Cell
from sudoku_generator import SudokuGenerator

class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.rows = 9
        self.cols = 9
        self.selected_cell = None

        self.board_x = 60
        self.board_y = 160
        self.cell_size = 60
        self.board_size = self.cell_size * 9

        sudoku = SudokuGenerator(9, difficulty)
        sudoku.fill_values()

        self.solution = []
        for row in sudoku.get_board():
            self.solution.append(row[:])

        sudoku.remove_cells()

        self.original_board = []
        for row in sudoku.get_board():
            self.original_board.append(row[:])

        self.board = []
        for row in sudoku.get_board():
            self.board.append(row[:])

        self.cells = []
        for r in range(self.rows):
            cell_row = []
            for c in range(self.cols):
                cell_row.append(Cell(self.board[r][c], r, c, screen))
            self.cells.append(cell_row)

    def draw(self):
        colors = {
            "grid": (40, 40, 40),
            "selected": (220, 70, 60),
            "fixed_number": (20, 20, 20),
            "user_number": (30, 70, 180),
            "sketch": (120, 120, 120),
        }
        fonts = {
            "cell": pygame.font.SysFont("arial", 32, bold=True),
            "sketch": pygame.font.SysFont("arial", 32, bold=False),
        }

        board_rect = pygame.Rect(self.board_x, self.board_y, self.board_size, self.board_size)
        pygame.draw.rect(self.screen, (235, 242, 250), board_rect)

        for r in range(self.rows):
            for c in range(self.cols):
                x = self.board_x + c * self.cell_size
                y = self.board_y + r * self.cell_size
                editable = self.original_board[r][c] == 0
                self.cells[r][c].draw(x, y, self.cell_size, self.cell_size, fonts, colors, editable)

        for i in range(10):
            line_width = 4 if i % 3 == 0 else 1
            pygame.draw.line(
                self.screen,
                colors["grid"],
                (self.board_x, self.board_y + i * self.cell_size),
                (self.board_x + self.board_size, self.board_y + i * self.cell_size),
                line_width,
            )
            pygame.draw.line(
                self.screen,
                colors["grid"],
                (self.board_x + i * self.cell_size, self.board_y),
                (self.board_x + i * self.cell_size, self.board_y + self.board_size),
                line_width,
            )

    def select(self, row, col):
        for r in range(self.rows):
            for c in range(self.cols):
                self.cells[r][c].selected = False
        self.cells[row][col].selected = True
        self.selected_cell = (row, col)

    def click(self, x, y):
        if not (self.board_x <= x < self.board_x + self.board_size and
                self.board_y <= y < self.board_y + self.board_size):
            return None

        col = (x - self.board_x) // self.cell_size
        row = (y - self.board_y) // self.cell_size
        return row, col

    def clear(self):
        if self.selected_cell is None:
            return

        row, col = self.selected_cell
        if self.original_board[row][col] == 0:
            self.cells[row][col].set_cell_value(0)
            self.cells[row][col].set_sketched_value(0)
            self.update_board()

    def sketch(self, value):
        if self.selected_cell is None:
            return

        row, col = self.selected_cell
        if self.original_board[row][col] == 0 and self.cells[row][col].value == 0:
            self.cells[row][col].set_sketched_value(value)

    def place_number(self, value=None):
        if self.selected_cell is None:
            return False

        row, col = self.selected_cell
        cell = self.cells[row][col]

        if self.original_board[row][col] != 0:
            return False

        if value is None:
            value = cell.sketched_value

        if value == 0:
            return False

        cell.set_cell_value(value)
        cell.set_sketched_value(0)
        self.update_board()
        return True

    def reset_to_original(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.cells[r][c].set_cell_value(self.original_board[r][c])
                self.cells[r][c].set_sketched_value(0)
        self.update_board()

        if self.selected_cell is not None:
            row, col = self.selected_cell
            self.select(row, col)

    def is_full(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.cells[r][c].value == 0:
                    return False
        return True

    def update_board(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.board[r][c] = self.cells[r][c].value

    def find_empty(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.cells[r][c].value == 0:
                    return (r, c)
        return None

    def check_board(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.cells[r][c].value != self.solution[r][c]:
                    return False
        return True

    def move_selection(self, dr, dc):
        if self.selected_cell is None:
            self.select(0, 0)
            return

        row, col = self.selected_cell
        new_row = max(0, min(8, row + dr))
        new_col = max(0, min(8, col + dc))
        self.select(new_row, new_col)
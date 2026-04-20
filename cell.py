import pygame

class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.selected = False
        self.sketched_value = 0

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self, x, y, width, height, fonts, colors, editable):
        rect = pygame.Rect(x, y, width, height)

        if self.selected:
            pygame.draw.rect(self.screen, colors["selected"], rect, 3)

        if self.value != 0:
            if editable:
                text_color = colors["user_number"]
            else:
                text_color = colors["fixed_number"]
            text = fonts["cell"].render(str(self.value), True, text_color)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
        elif self.sketched_value != 0:
            sketch = fonts["sketch"].render(str(self.sketched_value), True, colors["sketch"])
            sketch_rect = sketch.get_rect(center=(x + width // 2, y + height // 2))
            self.screen.blit(sketch, sketch_rect)
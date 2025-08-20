import pygame

class Button:
    def __init__(self, rect, text, font, on_click):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.on_click = on_click
        self.hover = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.on_click()

    def draw(self, surf):
        bg = (230,230,230) if self.hover else (210,210,210)
        pygame.draw.rect(surf, bg, self.rect, border_radius=8)
        pygame.draw.rect(surf, (80,80,80), self.rect, 2, border_radius=8)
        txt = self.font.render(self.text, True, (20,20,20))
        surf.blit(txt, txt.get_rect(center=self.rect.center))


class TextInput:
    def __init__(self, rect, font, placeholder=""):
        self.rect = pygame.Rect(rect)
        self.font = font
        self.placeholder = placeholder
        self.caret_visible = True
        self._timer = 0

    def draw(self, surf, value, dt):
        self._timer += dt
        if self._timer >= 500:
            self.caret_visible = not self.caret_visible
            self._timer = 0

        pygame.draw.rect(surf, (255,255,255), self.rect, border_radius=8)
        pygame.draw.rect(surf, (80,80,80), self.rect, 2, border_radius=8)

        text = value if value else self.placeholder
        color = (20,20,20) if value else (140,140,140)
        txt = self.font.render(text, True, color)
        surf.blit(txt, (self.rect.x+10, self.rect.y+10))

        if self.caret_visible and value is not None:
            caret_x = self.rect.x + 10 + txt.get_width() + 2
            caret_y = self.rect.y + 8
            pygame.draw.rect(surf, (30,30,30), (caret_x, caret_y, 2, self.rect.height-16))

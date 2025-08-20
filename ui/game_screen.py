import pygame
from ui.components import Button

WIDTH, HEIGHT = 560, 720

class TitleScreen:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.big  = pygame.font.SysFont(None, 64)

        cx = WIDTH // 2
        w, h, gap = 240, 64, 20
        top = 320

        self.next_state = None  # "game" or "quit"

        self.buttons = [
            Button((cx - w//2, top,          w, h), "Start", self.font, self._start),
            Button((cx - w//2, top + h + gap, w, h), "Quit",  self.font, self._quit),
        ]

    def _start(self): self.next_state = "game"
    def _quit(self):  self.next_state = "quit"

    def run_once(self):
        dt = self.clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.next_state = "quit"
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._start()
            for b in self.buttons:
                b.handle_event(event)

        # draw
        self.screen.fill((245,246,250))
        title = self.big.render("NumberGame", True, (40,40,60))
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 160))

        subtitle = self.font.render("Click Start or press Enter", True, (90,90,110))
        self.screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 230))

        for b in self.buttons:
            b.draw(self.screen)

        pygame.display.flip()
        return self.next_state

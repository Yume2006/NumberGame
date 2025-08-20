import pygame, random
from ui.components import Button, TextInput

WIDTH, HEIGHT = 560, 720

class GameScreen:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.big  = pygame.font.SysFont(None, 56)
        self.input_buffer = ""
        self.message = "0-999の数を当ててみて！"
        self.secret = random.randint(0, 999)
        self.input_view = TextInput((80, 80, 400, 60), self.big, placeholder="数字を入力…")
        self.buttons = []
        self._create_keypad()
        self.exit_to_title = False

    def _create_keypad(self):
        def add_button(x, y, w, h, label, cb):
            self.buttons.append(Button((x, y, w, h), label, self.font, cb))
        start_x, start_y = 80, 200
        w, h, gap = 120, 70, 10
        labels = [["1","2","3"],["4","5","6"],["7","8","9"]]
        for r, row in enumerate(labels):
            for c, lab in enumerate(row):
                add_button(start_x + c*(w+gap), start_y + r*(h+gap), w, h, lab,
                           lambda lab=lab: self._push_digit(lab))
        add_button(start_x,                start_y+3*(h+gap), w, h, "0",     lambda: self._push_digit("0"))
        add_button(start_x+(w+gap),        start_y+3*(h+gap), w, h, "BACK",  self._backspace)
        add_button(start_x+2*(w+gap),      start_y+3*(h+gap), w, h, "ENTER", self._submit)

    def _push_digit(self, d):
        if len(self.input_buffer) < 3:
            if self.input_buffer == "0":
                self.input_buffer = d
            else:
                self.input_buffer += d

    def _backspace(self):
        self.input_buffer = self.input_buffer[:-1]

    def _submit(self):
        guess = int(self.input_buffer or "0")
        if guess == self.secret:
            self.message = f"正解！ {guess} 🎉  (R:リセット / Esc:タイトルへ)"
        elif guess < self.secret:
            self.message = f"{guess} は小さい…↑  (Esc:タイトルへ)"
        else:
            self.message = f"{guess} は大きい…↓  (Esc:タイトルへ)"

    def _handle_key(self, event):
        if event.key == pygame.K_RETURN:
            self._submit()
        elif event.key == pygame.K_BACKSPACE:
            self._backspace()
        elif event.key == pygame.K_r:
            self._reset()
        elif event.key == pygame.K_ESCAPE:
            self.exit_to_title = True
        else:
            if event.unicode.isdigit():
                self._push_digit(event.unicode)

    def _reset(self):
        import random
        self.secret = random.randint(0, 999)
        self.input_buffer = ""
        self.message = "リセット！ 0-999の数を当てよう"

    def run_once(self):
        dt = self.clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                self._handle_key(event)
            for b in self.buttons:
                b.handle_event(event)

        if self.exit_to_title:
            return "title"

        self.screen.fill((245,246,250))
        title = self.big.render("NumberGame", True, (40,40,60))
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))
        self.input_view.draw(self.screen, self.input_buffer, dt)
        msg = self.font.render(self.message, True, (50,50,50))
        self.screen.blit(msg, (80, 160))
        for b in self.buttons:
            b.draw(self.screen)
        pygame.display.flip()
        return None

import pygame
from ui.menu_screen import TitleScreen, WIDTH as W1, HEIGHT as H1
from ui.game_screen import GameScreen, WIDTH as W2, HEIGHT as H2

def main():
    pygame.init()
    # どちらかのサイズを採用（同じにしてある前提）
    WIDTH, HEIGHT = W1, H1
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("NumberGame")

    state = "title"
    title = TitleScreen(screen)
    game  = None

    running = True
    while running:
        if state == "title":
            next_state = title.run_once()
            if next_state == "game":
                game = GameScreen(screen)
                state = "game"
            elif next_state == "quit":
                running = False

        elif state == "game":
            next_state = game.run_once()
            if next_state == "title":
                title = TitleScreen(screen)
                state = "title"
            elif next_state == "quit":
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()

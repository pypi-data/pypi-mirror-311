import pygame
import pathlib
import sys
from . import _ultimate_tic_tac_toe

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    icon = pygame.image.load(pathlib.Path(__file__).parent / "icon.png")
    pygame.display.set_icon(icon)
    pygame.display.set_caption("ultttt")
    clock = pygame.time.Clock()
    dt = 0
    game = _ultimate_tic_tac_toe.UltimateTicTacToe()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        screen.fill("black")
        # The big board is 600x600.
        # The big board is 3x3 200x200 squares.
        for i in range(1, 3):
            pygame.draw.line(screen, "gray", (i * 200, 0), (i * 200, 600), 4)
        for j in range(1, 3):
            pygame.draw.line(screen, "gray", (0, j * 200), (600, j * 200), 4)
        # The small boards are 150x150 inside a 200x200 square.
        # The small boards are 3x3 50x50 squares.
        for i in range(0, 3):
            for j in range(0, 3):
                for k in range(1, 3):
                    pygame.draw.line(screen, "white", (i * 200 + 25 + k * 50, j * 200 + 25), (i * 200 + 25 + k * 50, j * 200 + 175), 2)
                for l in range(1, 3):
                    pygame.draw.line(screen, "white", (i * 200 + 25, j * 200 + 25 + l * 50), (i * 200 + 175, j * 200 + 25 + l * 50), 2)
        for i, iv in enumerate(game.grid):
            for j, jv in enumerate(iv):
                for k, kv in enumerate(jv.grid):
                    for l, lv in enumerate(kv):
                        if lv:
                            x = i * 200 + 25 + k * 50
                            y = j * 200 + 25 + l * 50
                            if lv == "X":
                                pygame.draw.line(screen, "red", (x, y), (x + 50, y + 50), 4)
                                pygame.draw.line(screen, "red", (x, y + 50), (x + 50, y), 4)
                            else:
                                pygame.draw.circle(screen, "blue", (x + 25, y + 25), 25, 4)
        for i, iv in enumerate(game.grid):
            for j, jv in enumerate(iv):
                if jv.winner:
                    x = i * 200
                    y = j * 200
                    if jv.winner == "X":
                        pygame.draw.line(screen, "red", (x, y), (x + 200, y + 200), 8)
                        pygame.draw.line(screen, "red", (x, y + 200), (x + 200, y), 8)
                    else:
                        pygame.draw.circle(screen, "blue", (x + 100, y + 100), 100, 8)
        if game.winner:
            font = pygame.font.Font(None, 100)
            text = font.render(f"{game.winner} wins!", True, "purple")
            text_rect = text.get_rect(center=(300, 300))
            screen.blit(text, text_rect)
        else:
            # The next small board is outlined in green.
            if game.next_small_board:
                for i, iv in enumerate(game.grid):
                    for j, jv in enumerate(iv):
                        if jv == game.next_small_board:
                            pygame.draw.rect(screen, "green", (i * 200, j * 200, 200, 200), 4)
            # If one of the 89 small squares is hovered over it is outlined in yellow.
            for i, iv in enumerate(game.grid):
                for j, jv in enumerate(iv):
                    for k, kv in enumerate(jv.grid):
                        for l, lv in enumerate(kv):
                            if game.can_play((i, j), (k, l)):
                                r = pygame.Rect(i * 200 + 25 + k * 50, j * 200 + 25 + l * 50, 50, 50)
                                if r.collidepoint(mouse_pos):
                                    pygame.draw.rect(screen, "yellow", (i * 200 + 25 + k * 50, j * 200 + 25 + l * 50, 50, 50), 4)
                                    if mouse_pressed[0]:
                                            game.play((i, j), (k, l))

        pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
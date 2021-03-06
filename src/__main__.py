"""
    __main__.py
"""

from os import path, mkdir
from random import choice, randint
import pygame
from src.obstacles import Ground, Pipe
from src.bird import Bird
from src.button import Button

# Set up game window
WIDTH, HEIGHT = 850, 680
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
pygame.display.set_icon(pygame.image.load("flappy.ico"))

# Set up Clock
CLOCK = pygame.time.Clock()
FPS = 60

# Background Music and Sound effects
pygame.mixer.init()
pygame.mixer.music.load(path.join("music", "background.mp3"))
pygame.mixer.music.play(-1)

SCORE_SCOUND = pygame.mixer.Sound(path.join("sfx", "point.wav"))
HIGH_SCORE_SOUND = pygame.mixer.Sound(path.join("sfx", "woohoo.wav"))

# Ground
GROUND = Ground(path.join("sprites", "base.png"), (0, HEIGHT-168))

# Bird
BIRDS = ["redbird", "bluebird", "yellowbird"]
COLOR = choice(BIRDS)
BIRD = Bird(path.join("sprites", "{}-{}.png"),
            COLOR, (200, 300))

# Pipes
pipes = []
pipe_img = path.join("sprites", "pipe-green.png")

# Game over image and Button image, obj
GAME_OVER_IMG = pygame.image.load(path.join("sprites", "gameover.png"))
BTN_IMG = pygame.image.load(path.join("sprites", "btn.png"))
BUTTON = Button((WIDTH/2 - 60, HEIGHT/2 - 50), BTN_IMG)

# FONT
pygame.font.init()
FONT_COLOR = (255, 255, 255)
FONT = pygame.font.SysFont("Secular One", 70, bold=True)

# Background and Menu
BACKGROUND = pygame.image.load(path.join("sprites", "background.png"))
MENU = pygame.image.load(path.join("sprites", "message.png"))
MENU = pygame.transform.scale(MENU, (300, 400))


def draw_score(score):
    """Display score"""

    FONT_IMG = FONT.render(score, True, FONT_COLOR)
    WIN.blit(FONT_IMG, (WIDTH/2 - 20, 20))


def reset_game():
    """
        Reset the game
    """

    # Delete all pipes
    while len(pipes) > 0:
        del pipes[0]

    pygame.mixer.music.play(-1)
    BIRD.rect.topleft = (200, 300)
    BIRD.times = 0

    return False, 0, 70, False


def create_pipes(pipe_counter, pipe_delay):
    """
        Create pipe objs

        :pipe_counter: Keeps on increasing till it
                       equals the global pipe_delay

        When pipe_counter hits global pipe_delay,
        two pipes get created and pipe_counter
        resets to 0

        For the first time, pipe_counter is -1
        just to create two pipes at the start
        of the game!
    """

    if pipe_counter >= pipe_delay or pipe_counter == -1:
        pipe_height = randint(-180, 20)
        flip = False

        for i in range(2):
            if i == 1:
                flip = True

            pipe = Pipe(pipe_img, (WIDTH, (HEIGHT/2) + pipe_height), flip=flip)
            pipes.append(pipe)

        pipe_counter = 0
    else:
        pipe_counter += 1

    return pipe_counter


def draw(game_over, score, ready, woohoo, action=False) -> bool:
    """
        Draw game objs
    """

    WIN.blit(BACKGROUND, (0, 0))

    if ready:
        # Display pipes
        for pipe in pipes:
            pipe.draw(WIN, game_over)

        # Display score
        draw_score(str(score))

        # Display bird
        BIRD.draw(WIN, game_over)

    # Display ground
    GROUND.draw(WIN, game_over or not ready)
    GROUND.check_scroll()

    if not ready:
        WIN.blit(MENU, (WIDTH/2 - 150, HEIGHT/2 - 230))

    if game_over:

        # Update score file if player makes a new record
        if woohoo:
            try:
                with open(path.join("score", "high.txt"), mode="w") as score_file:
                    score_file.write(str(score))
            except FileNotFoundError:
                if not path.exists("score"):
                    mkdir("score")
                with open(path.join("score", "high.txt"), mode="w") as score_file:
                    score_file.write(str(score))

        WIN.blit(GAME_OVER_IMG, (WIDTH/2 - 96, HEIGHT/2 - 100))
        action = BUTTON.draw(WIN)

    pygame.display.update()
    CLOCK.tick(FPS)
    return action


def main():
    """ Main function """
    pipe_counter = -1
    game_over = False
    pipe_crossed = False
    woohoo = False
    pipe_delay = 70
    score = 0
    score_gained = 0

    # Read score from the score file
    try:
        with open(path.join("score", "high.txt")) as h_score:
            high_score = int(h_score.read())
    except FileNotFoundError:
        if not path.exists("score"):
            mkdir("score")
        with open(path.join("score", "high.txt"), mode="w") as h_score:
            h_score.write("0")
            high_score = 0

    ready = False
    game_on = True
    while game_on:

        # Create and draw pipes
        if not game_over and ready:
            pipe_counter = create_pipes(pipe_counter, pipe_delay)

        # Check it crossed a pipe
        if len(pipes) > 0:
            if BIRD.rect.left > pipes[0].rect.left \
                    and BIRD.rect.right < pipes[0].rect.right \
                    and pipe_crossed == False:

                pipe_crossed = True

            # Increase score if passed a pipe
            if pipe_crossed == True:
                if BIRD.rect.left > pipes[0].rect.right:
                    score += 5
                    score_gained += 5

                    if score_gained == 10:
                        score_gained = 0
                        GROUND.__class__.__base__.scroll_speed += 0.05
                        pipe_delay -= 0.3

                    if score > high_score:
                        high_score = score
                        if not woohoo:
                            HIGH_SCORE_SOUND.play()
                            woohoo = True
                        else:
                            SCORE_SCOUND.play()
                    else:
                        SCORE_SCOUND.play()

                    pipe_crossed = False

        if len(pipes) > 0:

            # Check for collisions
            for pipe in pipes:
                if BIRD.rect.colliderect(pipe.rect) \
                        or BIRD.rect.bottom >= 490 \
                        or BIRD.rect.top <= 0:
                    game_over = True
                    GROUND.__class__.__base__.scroll_speed = 4
                    pygame.mixer.music.stop()
                    break

            # Delete pipes that crossed the window
            if pipes[0].rect.right < 0:
                del pipes[0]

        # Handle events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                game_on = False
                pygame.quit()

            if (event.type == pygame.MOUSEBUTTONUP or event.type == pygame.KEYUP) and not game_over:
                BIRD.clicked = True

            if (event.type == pygame.MOUSEBUTTONUP or event.type == pygame.KEYUP) and not game_over \
                    and not ready:
                ready = True
                BIRD.flying = True

        # Display the game
        if draw(game_over, score, ready, woohoo):
            game_over, score, pipe_delay, woohoo = reset_game()


if __name__ == "__main__":
    main()

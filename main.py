import pygame, sys, random

pygame.init()

screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption('Flappy Bird')
pygame.display.set_icon(pygame.image.load('assets/bluebird-midflap.png'))
clock = pygame.time.Clock()

gravity = 0.20

bird_movement = 0

bg_surface = pygame.transform.scale(pygame.image.load('assets/background-day.png').convert(), (400, 600))
floor_surface = pygame.transform.scale(pygame.image.load('assets/base.png').convert(), (400, 100))
floor_x_pos = 0

bird_downflap = pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('assets/bluebird-upflap.png').convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 300))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipe_surface = pygame.image.load('assets/pipe-green.png').convert()

pipe_list = []

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 700)
pipe_height = [200, 300, 400]
game_active = False
game_font = pygame.font.Font('04B_19.ttf', 30)

high_score = 0
score = 0
score_sound_countdown = 100

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 500))
    screen.blit(floor_surface, (floor_x_pos + 400, 500))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(400, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(400, random_pipe_pos - 150))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 500:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collisions(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False

    if bird_rect.top <= 0 or bird_rect.bottom >= 500:
        death_sound.play()
        return False

    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == "main_game":
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(200, 40))

        screen.blit(score_surface, score_rect)

    if game_state == "game_over":
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(200, 40))

        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(200, 460))

        screen.blit(high_score_surface, high_score_rect)

def display_message(message, pos):
    cFont = pygame.font.Font('04B_19.ttf', 20)
    message_surfacea = cFont.render(message, True, (255, 255, 255))
    message_recta = message_surfacea.get_rect(center=pos)

    screen.blit(message_surfacea, message_recta)

game_over_surface = pygame.transform.scale(pygame.image.load('assets/gameover.png').convert_alpha(), (300, 100))
game_over_rect = game_over_surface.get_rect(center=(200, 150))

message_surface = pygame.transform.scale(pygame.image.load('assets/message.png').convert_alpha(), (250, 350))
message_rect = message_surface.get_rect(center=(200, 300))

pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 300)
                bird_movement = 0
                score = 0

            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6
                flap_sound.play()

        if event.type == SPAWNPIPE and game_active:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP and game_active:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()

    floor_x_pos -= 1

    screen.blit(bg_surface, (0, 0))

    if game_active:
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)

        bird_rect.centery += bird_movement

        screen.blit(rotated_bird, bird_rect)

        game_active = check_collisions(pipe_list)

        score += 0.01

        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        score_display('main_game')
        score_sound_countdown -= 1

        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        if score > high_score:
            high_score = score
        if score == 0:
            screen.blit(message_surface, message_rect)
        else:
            score_display('game_over')
            display_message("Press SPACE to play again", (200, 300))
            screen.blit(game_over_surface, game_over_rect)

    draw_floor()

    if floor_x_pos <= -400:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(100)
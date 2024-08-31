import pygame
import random

# pygame setup
pygame.init()
pygame.font.init()

# score font setup
scoreFont = pygame.font.SysFont('Courier New', 60)

# set screen resolution
screen = pygame.display.set_mode((1280, 720))

# set screen caption
pygame.display.set_caption("Pong")

# set clock
clock = pygame.time.Clock()

# boolean for running
running = True

# delta time
dt = 0

# postiions for the player position, divider, and the cpu position
player_pos = pygame.Vector2(90,screen.get_height()/2)
paddle_height = 150
paddle_width = 25
half_screen = pygame.Vector2(screen.get_width()/2, 0)
cpu_pos = pygame.Vector2(1190, screen.get_height()/2)
ball_pos = pygame.Vector2(screen.get_width()/2, screen.get_height()/2)
ball_radius = 14

# variables for the player and cpu score
player_score = 0
cpu_score = 0

# ball movement with random numbers at start
ball_movement = pygame.Vector2(random.randint(-300, 300), random.randint(-300, 300))

# print the ball movement at the start of the game
print(ball_movement.x, ball_movement.y)

# while the ball movement for x is too slow, keep generating random integers until you get a faster one
while abs(ball_movement.x) < 150:
    ball_movement.x = random.randint(-300, 300)

# while the ball movement for y is too slow, keep generating random integers until you get a faster one
while abs(ball_movement.y) < 150:
    ball_movement.y = random.randint(-300, 300) 

# function for controlling how the ball moves
def ball_move(ball_pos):

    # ball positions being affected by ball_movement times delta time
    ball_pos.x += ball_movement.x * dt
    ball_pos.y += ball_movement.y * dt

    # if the ball goes past the wall reset it and give it another random movement speed
    if ball_pos.x <= 0 or ball_pos.x >= screen.get_width():
        ball_pos.x = screen.get_width()/2
        ball_pos.y = screen.get_height()/2
        ball_movement.x = random.randint(-300, 300)
        ball_movement.y = random.randint(-300, 300)

        # while ball movements are slow generate random integers to make them faster        
        while abs(ball_movement.x) < 150:
            ball_movement.x = random.randint(-300, 300)
        while abs(ball_movement.y) < 150:
            ball_movement.y = random.randint(-300, 300)

        # print the ball movement
        print(ball_movement.x, ball_movement.y)

    # if the ball tries to go above then make it bounce off the top wall
    if ball_pos.y <= 0:
        ball_movement.y = random.randint(150, 300)
        
        # while ball movement for y is slow generate random integers to make them faster
        while abs(ball_movement.y) < 150:
            ball_movement.y = random.randint(-300, 300)

        # print the ball movement for y
        print(ball_movement.y)
    
    # if it tries to go below the screen make it bounce off the bottom wall
    if ball_pos.y >= screen.get_height():
        ball_movement.y = random.randint(-300, -150) 

        # not typing this again
        while abs(ball_movement.y) < 150:
            ball_movement.y = random.randint(-300, 300)

        # not typing this again
        print(ball_movement.y)
       
# main loop
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # draw player paddle
    player = pygame.draw.rect(screen, "blue", pygame.Rect(player_pos.x, player_pos.y, paddle_width, paddle_height))

    # draw dividing line
    divider = pygame.draw.rect(screen, "white", pygame.Rect(half_screen.x, half_screen.y,5, screen.get_height()))

    # draw CPU paddle
    CPU = pygame.draw.rect(screen, "red", pygame.Rect(cpu_pos.x, cpu_pos.y, paddle_width, paddle_height))

    # draw ball
    ball = pygame.draw.circle(screen, "purple", ball_pos, ball_radius)

    # render player score
    playerScore = scoreFont.render(str(player_score), True, "white")
    playerScoreRect = playerScore.get_rect()
    playerScoreRect.center = ((screen.get_width()/2) - 100, 64)
    screen.blit(playerScore, playerScoreRect)

    # render CPU score
    cpuScore = scoreFont.render(str(cpu_score), True, "white")
    cpuScoreRect = cpuScore.get_rect()
    cpuScoreRect.center = ((screen.get_width()/2) + 100, 64)
    screen.blit(cpuScore, cpuScoreRect)

    # move player paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt

    # little thing to test score system
    if keys[pygame.K_j]:
        player_score += 1 
    elif keys[pygame.K_k]:
        player_score -= 1

    # stop player from moving off the map
    if player_pos.y >= 567:
        player_pos.y = 567
    elif player_pos.y <= 4:
        player_pos.y = 4

    # collision with paddles
    if player_pos.x <= ball_pos.x <= player_pos.x + paddle_width + ball_radius and player_pos.y <= ball_pos.y <= player_pos.y + paddle_height:
        ball_movement.x *= -1 


        if ball_pos.y > player_pos.y + (paddle_height / 4):
            ball_movement.y = random.randint(150, 300)
        elif ball_pos.y < player_pos.y - (paddle_height / 4):
            ball_movement.y = random.randint(-300, -150)
        else:
            ball_movement.y = random.choice([-150, 150])

    if cpu_pos.x >= ball_pos.x >= cpu_pos.x - paddle_width + ball_radius and cpu_pos.y <= ball_pos.y <= cpu_pos.y + paddle_height:
        ball_movement.x *= -1

        if ball_pos.y > cpu_pos.y + (paddle_height / 4):
            ball_movement.y = random.randint(150, 300)
        elif ball_pos.y < cpu_pos.y - (paddle_height / 4):
            ball_movement.y = random.randint(-300, -150)
        else:
            ball_movement.y = random.choice([-150, 150])
        
    # call ball_movve
    ball_move(ball_pos)
    # flip() the display to put your work on screen 
    pygame.display.flip()
    print(player_pos)
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
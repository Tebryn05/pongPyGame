# Tebryn J. Branch
# Started: August 30th, 2024
# Last updated: September 3rd, 2024
# Pong in Pygame

# Planned Updates
#   Local Multiplayer
#   Main Menu
#   Hard Difficulty
#   Ability to choose how much points you want to get


# import modules needed
import pygame
import random
import time

# pygame setup
pygame.init()
pygame.font.init()
pygame.mixer.init()

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

# pause variable
paused = False

# Paddle Speed
paddle_speed = 300

# ball movement with random numbers at start
ball_movement = pygame.Vector2(random.randint(-400, 400), random.randint(-400, 400))

# sound effects (Temporary)
ballWallHit = pygame.mixer.Sound("wallhit.mp3")
paddleHitBall = pygame.mixer.Sound("paddlehit.mp3")
scoreSound = pygame.mixer.Sound("[Sound Library] Score - Sound Effect for editing.mp3")

# win bools
cpu_win = False
player_win = False

# print the ball movement at the start of the game
print(ball_movement.x, ball_movement.y)

# while the ball movement for x is too slow, keep generating random integers until you get a faster one
while abs(ball_movement.x) < 150:
    ball_movement.x = random.randint(-400, 400)

# while the ball movement for y is too slow, keep generating random integers until you get a faster one
while abs(ball_movement.y) < 150:
    ball_movement.y = random.randint(-400, 400) 

# function for controlling how the ball moves
def ball_move(ball_pos, player_score, cpu_score):

    # ball positions being affected by ball_movement times delta time
    ball_pos.x += ball_movement.x * dt
    ball_pos.y += ball_movement.y * dt

    # if the ball goes past the left wall add a point to CPU then reset the ball and give it another random movement speed
    if ball_pos.x <= 0:
        ball_pos.x = screen.get_width()/2
        ball_pos.y = screen.get_height()/2
        ball_movement.x = random.randint(-400, 400)
        ball_movement.y = random.randint(-400, 400)

        # while ball movements are slow generate random integers to make them faster        
        while abs(ball_movement.x) < 150:
            ball_movement.x = random.randint(-400, 400)
        while abs(ball_movement.y) < 150:
            ball_movement.y = random.randint(-400, 400)

        # add a point to cpu score
        cpu_score += 1

        # play the score sound
        scoreSound.play()

        # print the ball movement
        print(ball_movement.x, ball_movement.y)
        print(cpu_score)

    # if the ball goes past the right wall add a point to player then reset the ball and give it another random movement speed
    if ball_pos.x >= screen.get_width():
        ball_pos.x = screen.get_width()/2
        ball_pos.y = screen.get_height()/2
        ball_movement.x = random.randint(-400, 400)
        ball_movement.y = random.randint(-400, 400)

        # while ball movements are slow generate random integers to make them faster        
        while abs(ball_movement.x) < 150:
            ball_movement.x = random.randint(-400, 400)
        while abs(ball_movement.y) < 150:
            ball_movement.y = random.randint(-400, 400)

        # give a point to the player
        player_score += 1

        # play score sound
        scoreSound.play()

        # print the ball movement
        print(ball_movement.x, ball_movement.y)
        print(player_score)

    # if the ball tries to go above then make it bounce off the top wall
    if ball_pos.y <= 0:
        # play the sound effect of the ball hitting off the wall
        ballWallHit.play()

        # readjust ball movement
        ball_movement.y = random.randint(150, 400)
        
        # while ball movement for y is slow generate random integers to make them faster
        while abs(ball_movement.y) < 150:
            ball_movement.y = random.randint(-400, 400)

        # print the ball movement for y
        print("ball movement y",ball_movement.y)
    
    # if it tries to go below the screen make it bounce off the bottom wall
    if ball_pos.y >= screen.get_height():

        # play ball hitting the wall sound effect
        ballWallHit.play()

        # readjust ball movement
        ball_movement.y = random.randint(-400, -150) 

        # not typing this again
        while abs(ball_movement.y) < 150:
            ball_movement.y = random.randint(-400, 400)

        # not typing this again
        print("ball movement y",ball_movement.y)

    return player_score, cpu_score # return the player_score and cpu_score integers

# function for the CPU's AI (bit shifty now it jitters in place, might need to fix that later)
def CPU_AI(cpu_pos, paddle_speed, dt, ball_pos):

    '''Basically, if the ball's y position is lower than the cpu's y position, move towards it
    same if its y position is higher than the cpu's position'''
    if ball_pos.y < cpu_pos.y:
        cpu_pos.y -= paddle_speed * dt
    elif ball_pos.y > cpu_pos.y:
        cpu_pos.y += paddle_speed * dt

    # if the cpu runs into the wall then keep it there
    if cpu_pos.y >= 567:
        cpu_pos.y = 567
    elif cpu_pos.y <= 4:
        cpu_pos.y = 4


# main loop
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # key down events in game
        if event.type == pygame.KEYDOWN:
            # if the space key is pressed, pause or un pause the game depending on what the user did
            if event.key == pygame.K_SPACE:
                paused = not paused
            # only if the player wins or the cpu wins
            if player_win == True or cpu_win == True:
                # restart game 
                if event.key == pygame.K_r:
                    # set everything back to defaults
                    player_pos = pygame.Vector2(90, screen.get_height()/2)
                    cpu_pos = pygame.Vector2(1190, screen.get_height()/2)
                    ball_pos = pygame.Vector2(screen.get_width()/2, screen.get_height()/2)
                    player_score = 0
                    cpu_score = 0
                    player_win = False
                    cpu_win = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # draw player paddle
    player = pygame.draw.rect(screen, "blue", pygame.Rect(player_pos.x, player_pos.y, paddle_width, paddle_height))

    # draw dividing line
    divider = pygame.draw.rect(screen, "white", pygame.Rect(half_screen.x, half_screen.y,5, screen.get_height()))

    # draw CPU paddle
    CPU = pygame.draw.rect(screen, "red", pygame.Rect(cpu_pos.x, cpu_pos.y, paddle_width, paddle_height))

    if player_win == False and cpu_win == False:
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

    # pause mechanic
    if paused:
        # render pause_message and set in the middle of the screen
        pause_message = scoreFont.render("PAUSED", True, "gray")
        pause_message_rect = pause_message.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
        screen.blit(pause_message, pause_message_rect)
    else:
        # move player paddle
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_pos.y -= 300 * dt
        if keys[pygame.K_s]:
            player_pos.y += 300 * dt
            

        # stop player from moving off the map
        if player_pos.y >= 567:
            player_pos.y = 567
        elif player_pos.y <= 4:
            player_pos.y = 4

        

        # collision with paddles
        if player_pos.x <= ball_pos.x <= player_pos.x + paddle_width + ball_radius and player_pos.y <= ball_pos.y <= player_pos.y + paddle_height:
            # reverse the ball's x movement
            ball_movement.x *= -1 
            
            # play the sound effect of the ball hitting off the paddle
            paddleHitBall.play()

            # depending on where the ball hits the paddle, move it accordingly
            if ball_pos.y > player_pos.y + (paddle_height / 3):
                ball_movement.y = random.randint(150, 400)
            elif ball_pos.y < player_pos.y - (paddle_height / 3):
                ball_movement.y = random.randint(-400, -150)
            else:
                ball_movement.y = random.choice([-150, 150])

        # if the ball hits the cpu's paddle
        if cpu_pos.x >= ball_pos.x >= cpu_pos.x - paddle_width + ball_radius and cpu_pos.y <= ball_pos.y <= cpu_pos.y + paddle_height:
            # reverse the ball's x movement
            ball_movement.x *= -1

            # play paddle hiting ball sound effect
            paddleHitBall.play()

            # depending on where the ball hits the paddle change the ball's y movement accordingly
            if ball_pos.y > cpu_pos.y + (paddle_height / 3):
                ball_movement.y = random.randint(150, 400)
            elif ball_pos.y < cpu_pos.y - (paddle_height / 3):
                ball_movement.y = random.randint(-400, -150)
            else:
                ball_movement.y = random.choice([-150, 150])


        if player_win == False and cpu_win == False:
            # call ball_move
            player_score, cpu_score = ball_move(ball_pos, player_score, cpu_score)
            # call CPU_AI
            CPU_AI(cpu_pos, paddle_speed, dt, ball_pos)

        
        # if the player score is at 5 or more and the cpu hasn't won yet, make it so that the player's win message is printed
        if player_score >= 5 and cpu_win == False:
            win_message = scoreFont.render("Player Wins!", True, "Gray")
            win_message_rect = win_message.get_rect(center=((screen.get_width() / 2) - 225, screen.get_height() / 2))
            screen.blit(win_message, win_message_rect)
            player_win = True # change player win to true so that the below if statement can't be run

            # show player how to restart
            restartFont = pygame.font.SysFont('Courier New', 40)
            restart_message = restartFont.render("R to Restart", True, "Gray")
            restart_message_rect = restart_message.get_rect(center=((screen.get_width()/ 2) - 225, (screen.get_height()/ 2) + 75))
            screen.blit(restart_message, restart_message_rect)

        # if the cpu score is at 5 or more and the player hasn't won yet, make it so that the cpu's win message is printed
        if cpu_score >= 5 and player_win == False:
            win_message = scoreFont.render("CPU Wins!", True, "Gray")
            win_message_rect = win_message.get_rect(center=((screen.get_width() / 2) + 225, screen.get_height() / 2))
            screen.blit(win_message, win_message_rect)
            cpu_win = True # change cpu win to true so that the above if statement can't be run
            
            # show player how to restart
            restartFont = pygame.font.SysFont('Courier New', 40)
            restart_message = restartFont.render("R to Restart", True, "Gray")
            restart_message_rect = restart_message.get_rect(center=((screen.get_width()/ 2) + 225, (screen.get_height()/ 2) + 75))
            screen.blit(restart_message, restart_message_rect)
        
        

    # flip() the display to put your work on screen 
    pygame.display.flip()
    print(player_pos)

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000


pygame.quit()
import pygame

# pygame setup
pygame.init()
pygame.font.init()
scoreFont = pygame.font.SysFont('Courier New', 60)
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(140,screen.get_height()/2)
half_screen = pygame.Vector2(screen.get_width()/2, 0)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    pygame.draw.rect(screen, "white", pygame.Rect(player_pos.x, player_pos.y, 25, 150))

    pygame.draw.rect(screen, "white", pygame.Rect(half_screen.x, half_screen.y,5, screen.get_height()))

    playerScore = scoreFont.render('0', True, "white")
    
    playerScoreRect = playerScore.get_rect()

    playerScoreRect.center = ((screen.get_width()/2) - 100, 64)

    screen.blit(playerScore, playerScoreRect)

    cpuScore = scoreFont.render('0', True, "white")

    cpuScoreRect = cpuScore.get_rect()

    cpuScoreRect.center = ((screen.get_width()/2) + 100, 64)

    screen.blit(cpuScore, cpuScoreRect)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt

    if player_pos.y >= 567:
        player_pos.y = 567
    elif player_pos.y <= 4:
        player_pos.y = 4
    # flip() the display to put your work on screen 
    pygame.display.flip()

    print(player_pos.x, player_pos.y)

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
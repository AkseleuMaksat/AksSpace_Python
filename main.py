import pygame
import random
import sys

pygame.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Aks Space')


background = pygame.image.load('background.jpg')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

player_width, player_height = 50, 50
player_img = pygame.transform.scale(pygame.image.load('player.png'), (player_width, player_height))

enemy_width, enemy_height = 50, 50
enemy_img = pygame.transform.scale(pygame.image.load('enemy.png'), (enemy_width, enemy_height))

bullet_width, bullet_height = 30, 50
bullet_img = pygame.transform.scale(pygame.image.load('bullet.png'), (bullet_width, bullet_height))

explosion_width, explosion_height = 50, 50
explosion_img = pygame.transform.scale(pygame.image.load('explosion.png'), (explosion_width, explosion_height))


shoot_sound = pygame.mixer.Sound("shoot.wav")
explosion_sound = pygame.mixer.Sound("explosion.wav")


player_x, player_y = WIDTH // 2 - player_width // 2, HEIGHT - player_height - 20
player_velocity = 8
player_lives = 3


enemy_velocity = 3
enemies = []
spawn_delay = 100
spawn_timer = 0


bullet_velocity = 10
bullets = []


score = 0
font = pygame.font.Font(None, 36)

game_over = False

running = True
clock = pygame.time.Clock()

while running:
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_velocity
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_velocity
        if keys[pygame.K_SPACE]:
            if len(bullets) < 5:
                bullets.append([player_x + player_width // 2 - bullet_width // 2, player_y])
                shoot_sound.play()

        spawn_timer += 1
        if spawn_timer == spawn_delay:
            spawn_timer = 0
            enemy_x = random.randint(0, WIDTH - enemy_width)
            enemies.append([enemy_x, -enemy_height])


        for enemy in enemies:
            enemy[1] += enemy_velocity
            screen.blit(enemy_img, (enemy[0], enemy[1]))


        for bullet in bullets:
            bullet[1] -= bullet_velocity
            screen.blit(bullet_img, (bullet[0], bullet[1]))


        for bullet in bullets[:]:
            if bullet[1] < 0:
                bullets.remove(bullet)


        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if pygame.Rect(bullet[0], bullet[1], bullet_width, bullet_height).colliderect(
                        pygame.Rect(enemy[0], enemy[1], enemy_width, enemy_height)):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    explosion_sound.play()
                    score += 1


        if score >= 5:
            player_velocity = 10

        text = font.render(f'Score: {score}', True, (255, 255, 255))
        screen.blit(text, (10, 10))


        lives_text = font.render(f'Life: {player_lives}', True, (255, 255, 255))
        screen.blit(lives_text, (WIDTH - 120, 10))


        screen.blit(player_img, (player_x, player_y))



        for enemy in enemies:
            if enemy[1] > HEIGHT:
                player_lives -= 1
                enemies.remove(enemy)
                if player_lives <= 0:
                    game_over = True


        pygame.display.update()


        clock.tick(60)

    else:
        screen.fill((0, 0, 0))
        game_over_text = font.render("Game Over", True, (255, 255, 255))
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
        score_text = font.render(f'Your Score: {score}', True, (255, 255, 255))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 50))
        restart_text = font.render("Press 'R' to Restart", True, (255, 255, 255))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 100))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:

                    player_x, player_y = WIDTH // 2 - player_width // 2, HEIGHT - player_height - 20
                    bullets = []
                    enemies = []
                    score = 0
                    game_over = False
                    player_lives = 3

pygame.quit()
sys.exit()

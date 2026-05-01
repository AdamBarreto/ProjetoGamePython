import pygame
import time
import random
pygame.font.init()


WIDTH, HEIGHT = 1000, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Protótipo")

BG = pygame.transform.scale(pygame.image.load("fundoArena.jpg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 100
PLAYER_HEIGHT = 120
PLAYER_POS_X = 400
PLAYER_POS_Y = 530

ENEMY_WIDTH = 40 #PLAYER_WIDTH*0.5, para ter alguma perspectiva de profundidade
ENEMY_HEIGHT = 60 #PLAYER_HEIGHT*0.5
ENEMY_POS_X = 700
ENEMY_POS_Y = 294

CENTER_X, CENTER_Y = PLAYER_POS_X, PLAYER_POS_Y
SPACING = 100

PLAYER_VEL = 5
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL= 3

FONT = pygame.font.SysFont("comicsans", 30)

def draw(player, elapsed_time, stars, enemy):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Tempo: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))
    pygame.draw.rect(WIN, (255, 0, 0), player)
    pygame.draw.rect(WIN, (0, 0, 255), enemy)

    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.update()

def main():
    run = True

    player = pygame.Rect(PLAYER_POS_X, PLAYER_POS_Y,
                          PLAYER_WIDTH, PLAYER_HEIGHT)
    enemy = pygame.Rect(ENEMY_POS_X, ENEMY_POS_Y,
                         ENEMY_WIDTH, ENEMY_HEIGHT)

    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

    grid_x = 1
    grid_y = 1
    target_x = PLAYER_POS_X
    target_y = PLAYER_POS_Y

    stars = []
    hit = False

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3):
                star_pos = random.randint(0, 3)
                match star_pos:
                    case 0:
                        star_x = enemy.x + 100
                        star_y = enemy.y + ENEMY_HEIGHT - 55
                    case 1:
                        star_x = enemy.x + 55
                        star_y = enemy.y + ENEMY_HEIGHT - 110
                    case 2:
                        star_x = enemy.x - 20
                        star_y = enemy.y + ENEMY_HEIGHT - 110
                    case 3:
                        star_x = enemy.x - 70
                        star_y = enemy.y + ENEMY_HEIGHT - 55

                star = pygame.Rect(star_x, star_y, STAR_WIDTH, STAR_HEIGHT) #Se fosse 'star_x, 0', o projétil começaria no topo
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0
            
        
        target_x = CENTER_X + (grid_x - 1) * SPACING
        target_y = CENTER_Y + (grid_y - 1) * SPACING

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and grid_x > 0:
                    grid_x -= 1
                if event.key == pygame.K_RIGHT and grid_x < 2: #movimentação 3x3
                    grid_x += 1
                if event.key == pygame.K_UP and grid_y > 0:
                    grid_y -= 1
                if event.key == pygame.K_DOWN and grid_y < 2:
                    grid_y += 1
        
        player.x += (target_x - player.x) * 0.1 #quanto maior a constante, mais rápido se descola 
        player.y += (target_y - player.y) * 0.1


        for star in stars[:]:
            star.y += STAR_VEL
            star.x += STAR_VEL * (-0.5)
            if star.y > HEIGHT or star.x < -STAR_WIDTH:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player): #posição 
                stars.remove(star)
                hit = True
                break
        
        if hit:
            lost_text = FONT.render("Você perdeu!", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(10000)
            break

        draw(player, elapsed_time, stars, enemy)
        
    pygame.quit()

if __name__ == "__main__":  #Detecta se iniciou diretamente pelo arquivo
    main()
import pygame
import time
import random
pygame.font.init()


WIDTH, HEIGHT = 1000, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Protótipo")

BG = pygame.transform.scale(pygame.image.load("fundoArena.jpg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 80
PLAYER_HEIGHT = 120

ENEMY_WIDTH = 40 #PLAYER_WIDTH*0.5, para ter alguma perspectiva de profundidade
ENEMY_HEIGHT = 60 #PLAYER_HEIGHT*0.5

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

    player = pygame.Rect(340, HEIGHT - 220,
                          PLAYER_WIDTH, PLAYER_HEIGHT)
    enemy = pygame.Rect(700, HEIGHT - 456,
                         ENEMY_WIDTH, ENEMY_HEIGHT)

    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

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
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL

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
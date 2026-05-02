import pygame
import time
import random
pygame.font.init()


WIDTH, HEIGHT = 1000, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Protótipo")

BG = pygame.transform.scale(pygame.image.load("fundoArena.jpg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 50
PLAYER_HEIGHT = 60
PLAYER_POS_X = 400
PLAYER_POS_Y = 530

ENEMY_WIDTH = 25 #PLAYER_WIDTH*0.5, para ter alguma perspectiva de profundidade
ENEMY_HEIGHT = 30 #PLAYER_HEIGHT*0.5
ENEMY_POS_X = 500
ENEMY_POS_Y = 294

CENTER_X, CENTER_Y = PLAYER_POS_X, PLAYER_POS_Y
SPACING = 100

PLAYER_VEL = 5
STAR_WIDTH = 15
STAR_HEIGHT = 20
STAR_VEL= 1

FONT = pygame.font.SysFont("comicsans", 30)

def draw(player, elapsed_time, stars, enemy):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Tempo: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))
    pygame.draw.rect(WIN, (255, 0, 0), player)
    pygame.draw.rect(WIN, (0, 0, 255), enemy)

    for star in stars:
        pygame.draw.rect(WIN, "white", star["rect"])

    pygame.display.update()


def get_target_pixels(alvo):
    # Traduz o número 1-9 para linha e coluna (0, 1 ou 2)
    row = (alvo - 1) // 3
    col = (alvo - 1) % 3
    
    # Calcula o pixel central baseado no seu CENTER e SPACING
    mira_x = CENTER_X + (col - 1) * SPACING
    mira_y = CENTER_Y + (row - 1) * SPACING
    return mira_x, mira_y

def spawn_star(origem_x, origem_y, alvo_num):
    # 1. Descobre para onde atirar
    mira_x, mira_y = get_target_pixels(alvo_num)
    
    # 2. Calcula a distância e a direção (Vetor)
    dx = mira_x - origem_x
    dy = mira_y - origem_y
    distancia = (dx**2 + dy**2)**0.5
    
    # 3. Normaliza e aplica a velocidade
    # Se a distância for 0 (evitar erro), a velocidade é 0
    vel_x = (dx / distancia) * STAR_VEL if distancia != 0 else 0
    vel_y = (dy / distancia) * STAR_VEL if distancia != 0 else 0
    
    # 4. Cria o retângulo e empacota tudo no dicionário
    rect = pygame.Rect(origem_x, origem_y, STAR_WIDTH, STAR_HEIGHT)
    
    return {"rect": rect, "vx": vel_x, "vy": vel_y}


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
            if star_count > star_add_increment:
            # O inimigo decide atirar 3 vezes
                for i in range(3):
                    star_pos_saida = random.randint(0, 3)
                    if star_pos_saida == 0: star_x, star_y = enemy.x + 100, enemy.y - 25
                    elif star_pos_saida == 1: star_x, star_y = enemy.x + 55, enemy.y - 80
                    elif star_pos_saida == 2: star_x, star_y = enemy.x - 20, enemy.y - 80
                    else: star_x, star_y = enemy.x - 70, enemy.y - 25

                    alvo_sorteado = i + 1
                
                    nova_estrela = spawn_star(star_x, star_y, alvo_sorteado)
                    stars.append(nova_estrela)
                
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
        
        player.x += (target_x - player.x) * 0.2 #quanto maior a constante, mais rápido se descola 
        player.y += (target_y - player.y) * 0.2

        
        for star in stars[:]:
            # Move usando a velocidade individual guardada no nascimento
            star["rect"].x += star["vx"]
            star["rect"].y += star["vy"]
            
            # Checa se saiu da tela ou bateu no jogador
            if star["rect"].y > HEIGHT or star["rect"].x < -STAR_WIDTH or star["rect"].x > WIDTH:
                stars.remove(star)
            elif star["rect"].colliderect(player):
                hit = True
                break
        
        if hit:
            lost_text = FONT.render("Você perdeu!", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(1000)
            break

        draw(player, elapsed_time, stars, enemy)
        
    pygame.quit()

if __name__ == "__main__":  #Detecta se iniciou diretamente pelo arquivo
    main()
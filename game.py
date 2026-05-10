import pygame

# Inicializa o pygame
pygame.init()

# Configurações da tela
LARGURA, ALTURA = 500, 500
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Quadrado Movível")

# Configurações do quadrado
quadrado_tamanho = 50
quadrado_x = (LARGURA - quadrado_tamanho) // 2
quadrado_y = (ALTURA - quadrado_tamanho) // 2
velocidade = 5

# Cores
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)

# Configuração do FPS
FPS = 60
clock = pygame.time.Clock()

# Loop principal
dejogando = True
while dejogando:
    clock.tick(FPS)  # Define o FPS para 60
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            dejogando = False
    
    # Captura as teclas pressionadas
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_a] and quadrado_x > 0:  # Esquerda
        quadrado_x -= velocidade
    if teclas[pygame.K_d] and quadrado_x < LARGURA - quadrado_tamanho:  # Direita
        quadrado_x += velocidade
    if teclas[pygame.K_w] and quadrado_y > 0:  # Cima
        quadrado_y -= velocidade
    if teclas[pygame.K_s] and quadrado_y < ALTURA - quadrado_tamanho:  # Baixo
        quadrado_y += velocidade
    
    # Desenha o fundo e o quadrado
    TELA.fill(BRANCO)
    pygame.draw.rect(TELA, VERMELHO, (quadrado_x, quadrado_y, quadrado_tamanho, quadrado_tamanho))
    
    # Atualiza a tela
    pygame.display.update()

pygame.quit()
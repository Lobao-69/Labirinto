import pygame
import sys
from leitor_de_arquivo import *
from img import *
from time import sleep

# Inicialização do pygame
pygame.init()
sys.setrecursionlimit(10000)


maze = criar_labirinto('labirintos/maze.txt')
# Definir as dimensões da janela do jogo
WIDTH, HEIGHT = 1500, 900
win = pygame.display.set_mode((WIDTH, HEIGHT))

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Tamanho do jogador e posição inicial
player_size = 50
player_x = 50
player_y = 50

# Validação das posições do labirinto

def resolve_labirinto(maze, posicao_jogador, posicao_queijo):
    caminho_visitados = []
    caminho_correto = []
    
    def is_valid(x, y):
        return 0 <= x < len(maze[0]) and 0 <= y < len(maze)
    
    while (posicao_jogador["linha"], posicao_jogador["coluna"]) != (posicao_queijo["linha"], posicao_queijo["coluna"]):
        posicao = (posicao_jogador["linha"], posicao_jogador["coluna"])
        
        if is_valid(posicao_jogador["coluna"] + 1, posicao_jogador["linha"]) and maze[posicao_jogador["linha"]][posicao_jogador["coluna"] + 1] in ["0", "e"] and (posicao_jogador["linha"], posicao_jogador["coluna"] + 1) not in caminho_visitados:
            posicao_jogador["coluna"] += 1
            print("direita")
            caminho_visitados.append((posicao_jogador["linha"], posicao_jogador["coluna"]))
            caminho_correto.append(posicao)

        elif is_valid(posicao_jogador["coluna"] - 1, posicao_jogador["linha"]) and maze[posicao_jogador["linha"]][posicao_jogador["coluna"] - 1] in ["0", "e"] and (posicao_jogador["linha"], posicao_jogador["coluna"] - 1) not in caminho_visitados:
            posicao_jogador["coluna"] -= 1
            print("esquerda")
            caminho_visitados.append((posicao_jogador["linha"], posicao_jogador["coluna"]))
            caminho_correto.append(posicao)

        elif is_valid(posicao_jogador["coluna"], posicao_jogador["linha"] + 1) and maze[posicao_jogador["linha"] + 1][posicao_jogador["coluna"]] in ["0", "e"] and (posicao_jogador["linha"] + 1, posicao_jogador["coluna"]) not in caminho_visitados:
            posicao_jogador["linha"] += 1
            print("baixo")
            caminho_visitados.append((posicao_jogador["linha"], posicao_jogador["coluna"]))
            caminho_correto.append(posicao)

        elif is_valid(posicao_jogador["coluna"], posicao_jogador["linha"] - 1) and maze[posicao_jogador["linha"] - 1][posicao_jogador["coluna"]] in ["0", "e"] and (posicao_jogador["linha"] - 1, posicao_jogador["coluna"]) not in caminho_visitados:
            posicao_jogador["linha"] -= 1
            print("cima")
            caminho_visitados.append((posicao_jogador["linha"], posicao_jogador["coluna"]))
            caminho_correto.append(posicao)
        else:
            print("backingtrack")
            if caminho_correto:
                last_posicao = caminho_correto.pop()
                posicao_jogador["linha"], posicao_jogador["coluna"] = last_posicao
            else:
                return False
                
    return caminho_correto, caminho_visitados
            
            
def buscar_posicao(maze):
    posicao_jogador = {}
    posicao_queijo = {}
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 'm':
                posicao_jogador = { 
                                   "linha": i, 
                                   "coluna": j
                                   }
            if maze[i][j] == 'e':
                posicao_queijo = { 
                                   "linha": i, 
                                   "coluna": j
                                   }
    return posicao_jogador, posicao_queijo
# Função para desenhar o jogador

def draw_player(x, y):
    pygame.draw.rect(win, (x, y, player_size, player_size))

# Função para desenhar o labirinto
queijo = pygame.image.load("img/queijo.jpg")
rato = pygame.image.load("img/rato.png")
cv = pygame.image.load("img/cv.png")

def redimensionar_imagem(imagem, largura, altura):
    return pygame.transform.scale(imagem, (largura, altura))

def draw_maze(maze):
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            # Desenha a imagem correspondente à condição
            if maze[i][j] == "0":
                caminho_livre = pygame.surface.Surface((player_x, player_y))
                caminho_livre.fill((WHITE))
                win.blit(caminho_livre, (j * player_x, i * player_y))
            if maze[i][j] == "1":
                coluna = pygame.surface.Surface((player_x, player_y))
                coluna.fill((BLACK))
                win.blit(coluna, (j * player_x, i * player_y))
            if maze[i][j] == 'e':
                imagem_redimensionada = redimensionar_imagem(queijo, player_x,player_y)
                win.blit(imagem_redimensionada, (j * player_x, i * player_y))
            if maze[i][j] == 'm':
                imagem_redimensionada = redimensionar_imagem(rato, player_x, player_y)
                win.blit(imagem_redimensionada, (j * player_x, i * player_y))
    pygame.display.update()

# Loop principal do jogo
running = True
path = []  # Lista para armazenar a trilha percorrida pelo rato
caminho_correto_path = [] # Lista para o caminho correto
caminho_errado_path = [] # Lista para o caminho errado

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    coordenadas_path = caminho_correto_path[:]
    coordenadas_path.reverse()
    
    
    if coordenadas_path:
        for x, y in coordenadas_path:
            pygame.draw.rect(win, (x * player_size, y * player_size, player_size, player_size))
            
        for x, y in caminho_errado_path:
            pygame.draw.rect(win, (x * player_size, y * player_size, player_size, player_size))
            
        player_x, player_y = coordenadas_path.pop(0)
        pygame.display.update()

    # Checar se o jogador alcançou a saída
    if player_x == (len(maze[0]) - 1) * player_size and player_y == (len(maze) - 1) * player_size:
        for pos in path:
            maze[pos[1] // player_size][pos[0] // player_size] = 2
        path.clear()
        player_x = 50
        player_y = 50

    # Limpar a janela
    win.fill(WHITE)

    #resolver labirinto
    posicao_jogador, posicao_queijo = buscar_posicao(maze)
    
    # Desenhar o labirinto e o jogador
    draw_maze(maze)
    
    #resolver labirinto
    solucao = resolve_labirinto(maze, posicao_jogador, posicao_queijo)
    if solucao is False:
        print("Não há mais posições no caminho correto. Labirinto insolúvel.")
        break
    
    caminho_correto, caminho_visitado = solucao
    if len(caminho_correto)  > 0 and len(caminho_visitado) > 0:
        for caminho in caminho_correto:
            linha, coluna = caminho
            sleep(0.1)
            imagem_redimensionada = redimensionar_imagem(rato, player_x, player_y)        
            win.blit(imagem_redimensionada, (coluna*player_y, linha*player_x))
            pygame.display.update()
        
        for caminho in caminho_visitado:
            if caminho not in caminho_correto:
                linha, coluna = caminho
                imagem_redimensionada = redimensionar_imagem(cv, player_x, player_y)        
                win.blit(imagem_redimensionada, (coluna*player_y, linha*player_x))
                pygame.display.update()
            
        sleep(5)
        pygame.quit()
        sys.exit()

    # Atualizar a janela
    pygame.display.update()

# Encerrar o pygame
pygame.quit()
sys.exit()
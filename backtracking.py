from leitor_de_arquivo import *

cache = {}


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.finished = False  # Adicione um atributo para controlar se o jogador terminou
        

maze = criar_labirinto('labirintos/maze.txt')
posicao_inicial = encontrar_posicao_inicial(maze)
posicao_final = encontrar_posicao_saida(maze)
player = Player(posicao_inicial[0], posicao_inicial[1])


def is_valid(x, y, maze):
    return 0 <= x < len(maze[0]) and 0 <= y < len(maze)

def find_exit(maze, x, y, path, correct_path, wrong_path):
    if not is_valid(x, y, maze) or maze[y][x] == 1:
        print(is_valid(x, y, maze))
        return False

    if (x, y) in cache:
        print(cache)
        return cache[(x, y)]

    if maze[y][x] == 0:
        #player.finished = True
        return True

    if (x, y) in path:
        return False

    path.append((x, y))
    
    if find_exit(maze, x + 1, y, path, correct_path, wrong_path):
        correct_path.append((x+1, y))
        cache[(x + 1, y)] = True
        return True
    
    elif find_exit(maze, x - 1, y, path, correct_path, wrong_path):
        correct_path.append((x-1, y))
        cache[(x - 1, y)] = True
        return True

    elif find_exit(maze, x, y - 1, path, correct_path, wrong_path):
        correct_path.append((x, y-1))
        cache[(x, y - 1)] = True
        return True

    elif find_exit(maze, x, y + 1, path, correct_path, wrong_path):
        correct_path.append((x, y+1))
        cache[(x, y + 1)] = True
        return True

    wrong_path.append((x, y))
    cache[(x, y)] = False

    path.pop()
    return False
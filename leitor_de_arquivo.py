def criar_labirinto(arquivo):
    with open(arquivo, "r") as arquivo:
        primeira_linha = arquivo.readline()
        primeira_linha = primeira_linha.split(' ')

        labirinto = []
        
        for linha in arquivo:
           labirinto.append(list(linha.strip()))
    return labirinto

def encontrar_posicao_inicial(labirinto):
    for i in range(len(labirinto)):
        for j in range(len(labirinto[i])):
            if labirinto[i][j] == 'm':
                # Invertendo as coordenadas para corresponder à ordem (x, y)
                return (j, i)
            
def encontrar_posicao_saida(labirinto):
    for i in range(len(labirinto)):
        for j in range(len(labirinto[i])):
            if labirinto[i][j] == 'e':
                # Invertendo as coordenadas para corresponder à ordem (x, y)
                return (j, i)
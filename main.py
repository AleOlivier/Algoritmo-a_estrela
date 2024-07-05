import sys

def draw_path(grid_map, path):
    symbols = {
        'start': 'X',
        'end': 'O',
        'up': '^',
        'down': 'v',
        'left': '<',
        'right': '>',
        'obstacle': '*',
        'free': ' '
    }

    result_map = [[' ' for _ in row] for row in grid_map]

    current_position = path[0]
    for next_position in path[1:]:
        if current_position[0] > next_position[0]:
            result_map[next_position[0]][next_position[1]] = symbols['up']
        elif current_position[0] < next_position[0]:
            result_map[next_position[0]][next_position[1]] = symbols['down']
        elif current_position[1] > next_position[1]:
            result_map[next_position[0]][next_position[1]] = symbols['left']
        elif current_position[1] < next_position[1]:
            result_map[next_position[0]][next_position[1]] = symbols['right']
        current_position = next_position
    
    result_map[path[0][0]][path[0][1]] = symbols['start']
    result_map[path[-1][0]][path[-1][1]] = symbols['end']

    for i in range(len(grid_map)):
        for j in range(len(grid_map[i])):
            if grid_map[i][j] == 1:
                result_map[i][j] = symbols['obstacle']
    
    return result_map

def print_map(result_map):
    for row in result_map:
        print(' '.join(row))
    print()

def find_neighbors(position, grid_map, closed_list):
    neighbors = []
    row, col = position

    if row > 0 and grid_map[row - 1][col] == 0 and (row - 1, col) not in closed_list:
        neighbors.append((row - 1, col))
    if row < len(grid_map) - 1 and grid_map[row + 1][col] == 0 and (row + 1, col) not in closed_list:
        neighbors.append((row + 1, col))
    if col > 0 and grid_map[row][col - 1] == 0 and (row, col - 1) not in closed_list:
        neighbors.append((row, col - 1))
    if col < len(grid_map[0]) - 1 and grid_map[row][col + 1] == 0 and (row, col + 1) not in closed_list:
        neighbors.append((row, col + 1))

    return neighbors

def manhattan_distance(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])

def search_path(start, end, grid_map):
    open_list = [(start, 0 + manhattan_distance(start, end))]
    closed_list = set()
    came_from = {}
    g_score = {start: 0}

    while open_list:
        open_list.sort(key=lambda x: x[1])
        current, _ = open_list.pop(0)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        closed_list.add(current)
        for neighbor in find_neighbors(current, grid_map, closed_list):
            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + manhattan_distance(neighbor, end)
                if neighbor not in [pos for pos, _ in open_list]:
                    open_list.append((neighbor, f_score))

    return []

def create_map(filename):
    with open(filename, 'r') as file:
        return [[int(cell) for cell in line.split()] for line in file]

def input_positions(grid_map):
    while True:
        start = tuple(map(int, input("Entre com o ponto inicial (x y): ").split()))
        if grid_map[start[0]][start[1]] != 1:
            break
        print("O ponto inicial não pode ser um obstáculo. Tente novamente.")

    while True:
        end = tuple(map(int, input("Entre com o ponto final (x y): ").split()))
        if grid_map[end[0]][end[1]] != 1:
            break
        print("O ponto final não pode ser um obstáculo. Tente novamente.")

    return start, end

def main():
    print("Este programa encontra um caminho de um ponto inicial (X) até um ponto final (O) em um mapa.")
    print("O mapa é uma matriz onde '1' representa obstáculos e '0' representa espaços livres.")
    print("Você deve fornecer as coordenadas dos pontos inicial e final no formato '0 0'.")
    print("A coordenada 'x' representa a linha e a coordenada 'y' representa a coluna.\n")

    filename = input("Digite o nome do arquivo do mapa: ")
    grid_map = create_map(filename)
    
    start, end = input_positions(grid_map)

    if start == end:
        print("Você já chegou ao destino!")
    else:
        print("\nPonto inicial (X):", start)
        print("Ponto final (O):", end)
        path = search_path(start, end, grid_map)
        if path:
            result_map = draw_path(grid_map, path)
            print("\nMapa inicial com o ponto inicial e final:")
            print_map(draw_path(grid_map, [start, end]))
            print("\nMapa com o caminho encontrado:")
            print_map(result_map)
        else:
            print("Não foi possível encontrar um caminho.")

if __name__ == "__main__":
    main()

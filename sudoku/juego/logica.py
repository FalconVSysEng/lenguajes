import random

# Paradigma IMPERATIVO

def obtener_tablero():
    return [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

def movimiento_vali(board, row, col, num):
    if num in board[row]:
        return False
    for i in range(9):
        if board[i][col] == num:
            return False
    start_row, start_col = (row // 3) * 3, (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def completo(board):
    for row in board:
        if 0 in row:
            return False
    return True

def tablero_vali(board):
    for row in range(9):
        for col in range(9):
            num = board[row][col]
            if num != 0:
                board[row][col] = 0
                if not movimiento_vali(board, row, col, num):
                    return False
                board[row][col] = num
    return True

def resolver_imp(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                for num in range(1, 10):
                    if movimiento_vali(board, i, j, num):
                        board[i][j] = num
                        if resolver_imp(board):
                            return True
                        board[i][j] = 0
                return False
    return True


# Paradigma funcional
def generar_tablero_completo():
    tablero = [[0 for _ in range(9)] for _ in range(9)]
    rellenar(tablero)
    return tablero

def rellenar(tablero):
    for i in range(9):
        for j in range(9):
            if tablero[i][j] == 0:
                numeros = list(range(1, 10))
                random.shuffle(numeros)
                for num in numeros:
                    if movimiento_vali(tablero, i, j, num):
                        tablero[i][j] = num
                        if rellenar(tablero):
                            return True
                        tablero[i][j] = 0
                return False
    return True

def borrar_casillas(tablero, cantidad=40):
    borrados = 0
    while borrados < cantidad:
        i = random.randint(0, 8)
        j = random.randint(0, 8)
        if tablero[i][j] != 0:
            tablero[i][j] = 0
            borrados += 1
    return tablero

def generar_tablero_aleatorio():
    tablero_completo = generar_tablero_completo()
    tablero_con_espacios = borrar_casillas([fila[:] for fila in tablero_completo], cantidad=40)
    return tablero_con_espacios


def es_valido(tablero, fila, col, num):
    return (num not in tablero[fila] and
            all(fila_actual[col] != num for fila_actual in tablero) and
            all(tablero[i][j] != num
                for i in range(fila//3*3, fila//3*3+3)
                for j in range(col//3*3, col//3*3+3)))

def siguiente_casilla(tablero):
    for i in range(9):
        for j in range(9):
            if tablero[i][j] == 0:
                return i, j
    return None

def resolver_funcional(tablero):
    pos = siguiente_casilla(tablero)
    if not pos:
        return tablero  # Resuelto

    fila, col = pos
    for num in range(1, 10):
        if es_valido(tablero, fila, col, num):
            nuevo_tablero = [r[:] for r in tablero]
            nuevo_tablero[fila][col] = num
            resultado = resolver_funcional(nuevo_tablero)
            if resultado:
                return resultado
    return None  # Sin solución válida

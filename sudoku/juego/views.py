from django.shortcuts import render
from .logica import obtener_tablero,movimiento_vali,completo,tablero_vali, resolver_imp, es_valido, siguiente_casilla, resolver_funcional, generar_tablero_aleatorio
import subprocess,tempfile,os,json
import copy

def menu(request):
    print("⚠️ Esta llamada a menu viene de:", request.method, "con tipo:", request.POST.get("tipo"))
    if request.method == "POST":
        tipo = request.POST.get("tipo")
        print("Tipo de tablero elegido:", tipo)
        if tipo == "aleatorio":
            board = generar_tablero_aleatorio()
        else:
            board = obtener_tablero()
        print("Tablero generado en menu():", board)
        request.session["tablero_inicial"] = json.dumps(board)
        return render(request, "sudoku.html", {"board": board})
    return render(request, "inicio.html")



def sudoku(request):
    if request.method == "POST":
        tablero_guardado = request.session.get("tablero_inicial")
        print("Tablero guardado en sesión:", tablero_guardado)

        board = json.loads(tablero_guardado) if tablero_guardado else obtener_tablero()
        print("Tablero base para reconstrucción (board):", board)

        # ✅ Reconstruye el tablero según inputs del usuario
        new_board = []
        for i in range(9):
            row = []
            for j in range(9):
                cell_name = f"cell_{i}_{j}"
                value = request.POST.get(cell_name)
                if value and value.isdigit():
                    row.append(int(value))
                else:
                    row.append(board[i][j] if board[i][j] != 0 else 0)  # Mantén las celdas originales
            new_board.append(row)
        print("Tablero reconstruido por el usuario (new_board):", new_board)

        acc = request.POST.get('acc')
        print("Acción solicitada:", acc)

        paradigma = request.POST.get('paradigma')
        print("Paradigma elegido:", paradigma)

        if acc == 'verificar':
            if sin_aportes_usuario(board, new_board):
                mensaje = "⚠️ No has ingresado ningún número nuevo."
                return render(request, "sudoku.html", {"board": new_board, "mensaje": mensaje})
            
            if paradigma == 'imperativo':
                if not tablero_vali(new_board):
                    mensaje = "❌ El tablero tiene errores según las reglas del Sudoku."
                elif completo(new_board):
                    mensaje = "🎉 ¡Felicidades! Sudoku completo y correcto."
                else:
                    mensaje = "✅ Sudoku válido, pero aún incompleto."
            elif paradigma == 'logico':
                
                ruta_plantilla = os.path.join(os.path.dirname(__file__), "plantillaProlog.pl")
                with open(ruta_plantilla, "r", encoding="utf-8") as f:
                    plantilla = f.read()

                tablero_prolog = convertir_a_prolog(new_board)
                codigo_final = plantilla.replace("__TABLERO__", tablero_prolog)

                with tempfile.NamedTemporaryFile(delete=False, suffix=".pl", mode="w", encoding="utf-8") as archivo:
                    archivo.write(codigo_final)
                    ruta_archivo = archivo.name

                print(ruta_archivo)
                resultado = subprocess.run(
                    ["swipl", "-s", ruta_archivo, "-g", "verificar"],
                    capture_output=True, text=True
                )

                os.remove(ruta_archivo)

                if "invalido" in resultado.stdout or "ERROR" in resultado.stderr:
                    mensaje = "❌ El tablero no cumple con las reglas del Sudoku (según Prolog)."
                else:
                    mensaje = "🟢 ¡Sudoku válido según Prolog!"
            else:
                mensaje = "❌ Elija otro paradigma"
                return render(request, "sudoku.html", {"board": new_board, "mensaje": mensaje})
            
            return render(request, "sudoku.html", {"board": new_board, "mensaje": mensaje})

        elif acc == 'completar':
            if paradigma == 'imperativo':
                tablero_copia = [fila[:] for fila in new_board]
                if resolver_imp(tablero_copia):
                    mensaje = "🧠 Sudoku resuelto automáticamente con Python."
                    return render(request, "sudoku.html", {"board": tablero_copia, "mensaje": mensaje})
                else:
                    mensaje = "❌ No se pudo resolver con Python."
                    return render(request, "sudoku.html", {"board": new_board, "mensaje": mensaje})
            elif paradigma == 'funcional':
                solucion = resolver_funcional(new_board)
                if solucion:
                    mensaje = "🧠 Sudoku resuelto con programación funcional."
                    return render(request, "sudoku.html", {"board": solucion, "mensaje": mensaje})
                else:
                    mensaje = "❌ No se pudo resolver con programación funcional."
                    return render(request, "sudoku.html", {"board": new_board, "mensaje": mensaje})
            else:
                mensaje = "❌ Elija otro paradigma"
                return render(request, "sudoku.html", {"board": new_board, "mensaje": mensaje})
            return render(request, "sudoku.html", {"board": new_board, "mensaje": mensaje})

    else:
        tablero_guardado = request.session.get("tablero_inicial")
        board = json.loads(tablero_guardado) if tablero_guardado else obtener_tablero()
        return render(request, "sudoku.html", {"board": board})

def sin_aportes_usuario(original, nuevo):
    for i in range(9):
        for j in range(9):
            if original[i][j] == 0 and nuevo[i][j] != 0:
                return False 
    return True 


def convertir_a_prolog(board):
    var_counter = 1
    prolog = "[\n"
    for fila in board:
        fila_prolog = []
        for val in fila:
            if val == 0:
                fila_prolog.append(f"X{var_counter}")
                var_counter += 1
            else:
                fila_prolog.append(str(val))
        prolog += "[" + ", ".join(fila_prolog) + "],\n"
    return prolog.rstrip(",\n") + "\n]"

def parsear_tablero_prolog(salida):
    lineas = salida.strip().splitlines()
    tablero = []
    for linea in lineas:
        try:
            fila = eval(linea)  # Convierte '[5,3,4,...]' en [5,3,4,...]
            if isinstance(fila, list) and len(fila) == 9:
                tablero.append(fila)
        except:
            pass  # Ignora líneas que no sean listas válidas
    return tablero if len(tablero) == 9 else None

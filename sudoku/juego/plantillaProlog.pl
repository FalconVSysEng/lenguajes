% --- PLANTILLA PARA VERIFICAR SUDOKU (SIN COMPLETAR) ---

sin_repetidos([]).
sin_repetidos([X|Xs]) :-
    \+ member(X, Xs),
    sin_repetidos(Xs).

verificar :-
    Tablero = __TABLERO__,
    filas_validas(Tablero),
    columnas(Tablero, Columnas),
    filas_validas(Columnas),
    bloques(Tablero, Bloques),
    filas_validas(Bloques),
    writeln("valido"), 
    halt.

verificar :-
    writeln("invalido"),
    halt.

filas_validas([]).
filas_validas([Fila|Resto]) :-
    sin_repetidos(Fila),
    filas_validas(Resto).

columnas([[],[],[],[],[],[],[],[],[]], []).
columnas(Filas, [Col|Resto]) :-
    extraer_primera(Filas, Col, NuevasFilas),
    columnas(NuevasFilas, Resto).

extraer_primera([], [], []).
extraer_primera([[X|Xs]|Rest], [X|Col], [Xs|Nuevas]) :-
    extraer_primera(Rest, Col, Nuevas).

bloques([], []).
bloques([A,B,C|Resto], Bloques) :-
    dividir3(A, A1,A2,A3),
    dividir3(B, B1,B2,B3),
    dividir3(C, C1,C2,C3),
    BloquesFila = [
        [A1,B1,C1],
        [A2,B2,C2],
        [A3,B3,C3]
    ],
    bloques(Resto, Otros),
    append(BloquesFila, Otros, Bloques).

dividir3([], [], [], []).
dividir3([X,Y,Z|Resto], [X|L1], [Y|L2], [Z|L3]) :-
    dividir3(Resto, L1, L2, L3).

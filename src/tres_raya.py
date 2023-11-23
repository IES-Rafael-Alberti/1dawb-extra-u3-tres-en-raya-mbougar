import os


FICHAS = (" ", "X", "O")

POSICIONES_POSIBLES = (
    (
        {(0, 1), (1, 0), (1, 1)},
        {(0, 0), (0, 2), (1, 1)},
        {(0, 1), (1, 1), (1, 2)}
    ),
    (
        {(0, 0), (1, 1), (2, 0)},
        {(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)},
        {(0, 2), (1, 1), (2, 2)}
    ),
    (
        {(1, 0), (1, 2), (2, 1)},
        {(1, 1), (2, 0), (2, 2)},
        {(1, 1), (1, 2), (2, 1)}
    )
)


def clear_console():
    """Clears the console.

    In the os module if the Operating system is Windows 'os.name' will be 'nt', if the operating system is mac or linux-based it will be 'posix' 
    """
    if os.name == "nt":
        return os.system("cls")
    else:
        return os.system("clear")
    

def pulse_tecla_para_continuar():
    os.system("pause")
    

def crear_fila():
    list_fila = list(0 for _ in range(3))
    return list_fila


def crear_tablero():
    tuple_tablero = tuple(crear_fila() for _ in range(3))
    return tuple_tablero


def mostrar_fila(lista: list):
    fila_str = "║"
    for i in range(3):
        fila_str += f" {FICHAS[lista[i]]} ║"
    print(fila_str)


def mostar_tablero(tablero: tuple):
    clear_console()
    print("""    ╔═══╦═══╦═══╗
    ║ 1 ║ 2 ║ 3 ║
╔═══╬═══╬═══╬═══╣""")
    for i in range(3):
        print(f"║ {i + 1} ", end="")
        mostrar_fila(tablero[i])
        if i != 2:
            print("╠═══╬═══╬═══╬═══╣")
    print("╚═══╩═══╩═══╩═══╝")


def cambiar_turno(turno: int, ronda: int) -> tuple:
    if turno % 2 == 0:
        ronda += 1
        turno = 1
        print(f"\n RONDA {ronda}\n")
    else:
        turno = 2
        print(f"\n RONDA {ronda}\n")

    return turno, ronda


def pedir_numero(texto: str):
    loop = True
    while loop:
        try:
            numero = int(input(f"    ({texto})=>"))
            if 1 <= numero <= 3:
                return numero - 1
            else:
                raise ValueError
        except ValueError:
            print("Error, no has introducido un valor correcto.")


def colocar_ficha(tablero: tuple, turno: int):
    pos_ficha = {"fila": None, "columna": None}
    pos_correcta = False

    while not pos_correcta:
        print(f"Jugador {turno}, introduzca la posición de la fila y de la columna (1, 2 o 3)")
        pos_ficha["fila"] = pedir_numero("fila")
        pos_ficha["columna"] = pedir_numero("columna")
        if tablero[pos_ficha["fila"]][pos_ficha["columna"]] == 0:
            pos_correcta = True
            tablero[pos_ficha["fila"]][pos_ficha["columna"]] = turno
        else:
            print("La casilla ya esta ocupada.")
            pulse_tecla_para_continuar()
            mostar_tablero(tablero)


def comprobar_movimientos_posibles(tablero: tuple, fila: int, columna: int) -> bool:
    for posicion in POSICIONES_POSIBLES[fila][columna]:
        if tablero[posicion[0]][posicion[1]] == 0:
            movimiento_posible = True
            return movimiento_posible
        else:
            movimiento_posible = False
    return movimiento_posible



def mover_ficha(tablero: tuple, turno: int):
    pos_ficha = {"fila": None, "columna": None}
    antigua_pos_ficha = {"fila": None, "columna": None}
    todo_ok = False

    while not todo_ok:
        pos_correcta = False

        while not pos_correcta:
            print(f"Jugador {turno}, introduzca la posición de la ficha que quiere mover")
            antigua_pos_ficha["fila"] = pedir_numero("fila")
            antigua_pos_ficha["columna"] = pedir_numero("columna")
            if tablero[antigua_pos_ficha["fila"]][antigua_pos_ficha["columna"]] == turno:
                if comprobar_movimientos_posibles(tablero, antigua_pos_ficha["fila"], antigua_pos_ficha["columna"]) == False:
                    print("La ficha seleccionada no puede realizar ningún movimiento.")
                else:
                    pos_correcta = True
            else:
                print("En esa posición no hay ninguna ficha que puedas mover")
                pulse_tecla_para_continuar()
                mostar_tablero(tablero)

        pos_correcta = False

        while not pos_correcta:
            print(f"Jugador {turno}, introduzca la posición donde quieres colocar la ficha")
            pos_ficha["fila"] = pedir_numero("fila")
            pos_ficha["columna"] = pedir_numero("columna")

            if (pos_ficha["fila"], pos_ficha["columna"]) in POSICIONES_POSIBLES[antigua_pos_ficha["fila"]][antigua_pos_ficha["columna"]]:
                if tablero[pos_ficha["fila"]][pos_ficha["columna"]] == 0:
                    pos_correcta = True
                    todo_ok = True
                    tablero[pos_ficha["fila"]][pos_ficha["columna"]] = turno
                    tablero[antigua_pos_ficha["fila"]][antigua_pos_ficha["columna"]] = 0
                else:
                    print("La casilla ya esta ocupada.")
                    pulse_tecla_para_continuar()
                    mostar_tablero(tablero)
            else:
                print("Error, no es posible mover la ficha a esa posición.")


def comprobar_ganador(tablero: tuple, turno: int) -> bool:
    ganador = False
    for i in range(3):
        if tablero[i][0] == tablero[i][1] == tablero[i][2] == turno:
            ganador = True
        elif tablero[0][i] == tablero[1][i] == tablero[2][i] == turno:
            ganador = True
    if tablero[0][0] == tablero[1][1] == tablero[2][2] == turno:
        ganador = True
    elif tablero[0][2] == tablero[1][1] == tablero[2][0] == turno:
        ganador = True 
    return ganador


def jugar(tablero: tuple):
    ronda = 0
    turno = 0
    loop = True

    while loop:
        mostar_tablero(tablero)
        turno, ronda = cambiar_turno(turno, ronda)
        if ronda <= 3:
            colocar_ficha(tablero, turno)
        else:
            mover_ficha(tablero, turno)
        if comprobar_ganador(tablero, turno) == True:
            mostar_tablero(tablero)
            print(f"El jugador {turno} ha ganado.")
            loop = False


def main():
    clear_console()
    tuple_tablero = crear_tablero()
    mostar_tablero(tuple_tablero)
    jugar(tuple_tablero)



if __name__ == "__main__":
    main()
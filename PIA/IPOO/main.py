import random

class Carta:
    def __init__(self, valor, figura):
        self.valor = valor
        self.figura = figura

    def __str__(self):
        return f"{self.valor} de {self.figura}"

class Baraja:
    def __init__(self):
        figuras = ['Corazón', 'Trébol', 'Diamante', 'Picas']
        valores = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cartas = [Carta(valor, figura) for valor in valores for figura in figuras]

    def barajar(self):
        random.shuffle(self.cartas)

    def repartir_carta(self):
        if len(self.cartas) > 0:
            return self.cartas.pop()
        else:
            return None

class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.cartas = []
        self.puntuacion = 0

    def recibir_carta(self, carta):
        self.cartas.append(carta)
        self.calcular_puntuacion()

    def calcular_puntuacion(self):
        self.puntuacion = sum([self.valor_carta(carta) for carta in self.cartas])
        if self.puntuacion > 21 and any(carta.valor == 'A' for carta in self.cartas):
            self.puntuacion -= 10

    def valor_carta(self, carta):
        if carta.valor in ['K', 'Q', 'J']:
            return 10
        elif carta.valor == 'A':
            return 11
        else:
            return int(carta.valor)
    def mostrar_cartas(self):
        print(f"\nCartas de {self.nombre}:")
        for carta in self.cartas:
            print(f"  {carta}")
        print(f"Puntuación total: {self.puntuacion}")

class Juego:
    def __init__(self, jugadores, num_partidas):
        self.jugadores = [Jugador(nombre) for nombre in jugadores]
        self.baraja = Baraja()
        self.num_partidas = num_partidas
        self.partidas_ganadas = {jugador.nombre: 0 for jugador in self.jugadores}

    def jugar_partida(self):
        self.baraja.barajar()
        for jugador in self.jugadores:
            jugador.cartas = []
            jugador.recibir_carta(self.baraja.repartir_carta())
            jugador.recibir_carta(self.baraja.repartir_carta())

        for jugador in self.jugadores:
            while jugador.puntuacion <= 16:
                carta_nueva = self.baraja.repartir_carta()
                if carta_nueva:
                    jugador.recibir_carta(carta_nueva)
                else:
                    break

        self.mostrar_resultados()

    def mostrar_resultados(self):
        for jugador in self.jugadores:
            jugador.mostrar_cartas()

        ganadores = [jugador for jugador in self.jugadores if jugador.puntuacion <= 21]
        if ganadores:
            ganador = max(ganadores, key=lambda x: x.puntuacion)
            print(f"\nEl ganador de esta partida es: {ganador.nombre}")
            self.partidas_ganadas[ganador.nombre] += 1
        else:
            print("\nNo hay ganadores en esta partida.")

    def jugar(self):
        for _ in range(self.num_partidas):
            print(f"\n----- Partida {_ + 1} -----")
            self.jugar_partida()

        print("\n----- Resultados finales -----")
        for jugador, partidas_ganadas in self.partidas_ganadas.items():
            print(f"{jugador}: {partidas_ganadas} partidas ganadas")

        ganador_final = max(self.partidas_ganadas, key=self.partidas_ganadas.get)
        print(f"\nEl ganador final es: {ganador_final}!")

jugadores = [input("Nombre del jugador 1: "), input("Nombre del jugador 2: ")]
num_partidas = int(input("Número de partidas a jugar: "))

juego = Juego(jugadores, num_partidas)
juego.jugar()
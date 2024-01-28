import numpy as np
import pygame
from pygame.locals import *
import time
import sys

# Inicializar Pygame
pygame.init()

# Tamaño de la ventana
WIDTH, HEIGHT = 500, 500

# Crear la ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Definir título a la ventana
pygame.display.set_caption("LABECUA")

# Cargar las imágenes
pared = pygame.image.load('Images/pared1.png')
suelo = pygame.image.load('Images/ground1.png')
niña = pygame.image.load('Images/niña_rigth.png')
niña_left = pygame.image.load('Images/niña_left.png')

out1 = pygame.image.load('Images/out1.png') 
fin_bg = pygame.image.load('Images/winn.png') 
objeto = pygame.image.load('Images/coin.png')
objeto2 = pygame.image.load('Images/llave.png')
objeto3 = pygame.image.load('Images/casa.png')
objeto4 = pygame.image.load('Images/duende.png')

# Escala de las imágenes
pared = pygame.transform.scale(pared, (50, 50))
suelo = pygame.transform.scale(suelo, (50, 50))
niña = pygame.transform.scale(niña, (50, 50))
niña_left = pygame.transform.scale(niña_left, (50, 50))

out1 = pygame.transform.scale(out1, (50, 50))
fin_bg = pygame.transform.scale(fin_bg, (WIDTH, HEIGHT))
objeto = pygame.transform.scale(objeto, (50, 50))
objeto2 = pygame.transform.scale(objeto2, (50, 50))
objeto3 = pygame.transform.scale(objeto3, (50, 50))
objeto4 = pygame.transform.scale(objeto4, (50, 50))

# Carga de la imagen de "Game Over"
game_over_image = pygame.image.load('Images/game_over.png')
game_over_image = pygame.transform.scale(game_over_image, (WIDTH, HEIGHT))

sonido_objeto = pygame.mixer.Sound("Audio/short-success-sound-glockenspiel-treasure-video-game-6346.mp3")

# Cantidad de columnas y filas
columnas, filas = 10, 10

# Matrices de los dos niveles
mapa_nivel1 = np.array([[0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
                        [1, 1, 0, 1, 1, 1, 0, 0, 0, 1],
                        [1, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                        [1, 0, 1, 1, 1, 1, 0, 0, 0, 1],
                        [1, 0, 0, 0, 0, 1, 1, 1, 0, 1],
                        [1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
                        [1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
                        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0]])

mapa_nivel2 = np.array([[0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
                        [0, 1, 0, 1, 0, 1, 0, 0, 0, 1],
                        [0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
                        [0, 1, 0, 1, 1, 1, 0, 1, 0, 1],
                        [0, 1, 0, 0, 0, 1, 0, 1, 0, 1],
                        [0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
                        [0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
                        [0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
                        [0, 1, 0, 0, 0, 0, 0, 1, 0, 0]])

# Inicialización de variables de nivel
nivel_actual = 1
num_niveles = 2
mapa = mapa_nivel1
salida_x_nivel1, salida_y_nivel1 = 9, 9
salida_x_nivel2, salida_y_nivel2 = 9, 9
pos_x, pos_y = 0, 0
salida_x, salida_y = salida_x_nivel1, salida_y_nivel1
objeto_x, objeto_y = 6, 6
objeto2_x, objeto2_y = 3, 3
objeto3_x, objeto3_y = 4, 5
objeto4_x, objeto4_y = 2, 2
puntaje = 0
tiempo_inicial = time.time()
tiempo_limite = 60
longitud_linea_feliz = 0
objeto_visible = True
objeto2_visible = True
objeto3_visible = True
objeto4_visible = True
fin = False
direccion = 'derecha'

# Tamaño de una celda en la ventana
cell_width = WIDTH // columnas
cell_height = HEIGHT // filas

# Font para el menú
menu_font = pygame.font.Font(None, 36)

def map_draw():
    global puntaje

    # Usar np.where para crear máscaras
    pared_mask = np.where(mapa == 1, 1, 0)
    suelo_mask = np.where(mapa == 0, 1, 0)

    # Tamaño de una celda en la ventana
    cell_width = WIDTH // columnas
    cell_height = HEIGHT // filas

    # Dibujar imágenes de "niña" y "pared" usando las máscaras
    for fil, col in np.argwhere(pared_mask == 1):
        screen.blit(pared, (col * cell_width, fil * cell_height))

    for fil, col in np.argwhere(suelo_mask == 1):
        screen.blit(suelo, (col * cell_width, fil * cell_height))

    # Dibuja a la niña en función de su dirección
    if direccion == 'derecha' or direccion == 'arriba' or direccion == 'abajo':
        screen.blit(niña, (pos_x * cell_width, pos_y * cell_height))

    elif direccion == 'izquierda':
        screen.blit(niña_left, (pos_x * cell_width, pos_y * cell_height))

    # Dibujar la salida en la posición de salida actual
    screen.blit(out1, (salida_x * cell_width, salida_y * cell_height))

    # Dibujar el objeto que da puntaje solo si está visible
    if objeto_visible:
        screen.blit(objeto, (objeto_x * cell_width, objeto_y * cell_height))

    # Dibujar puntaje y tiempo
    font = pygame.font.Font(None, 36)
    text_puntaje = font.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    text_tiempo = font.render(f"Tiempo: {int(tiempo_limite - (time.time() - tiempo_inicial))}s", True, (255, 255, 255))
    screen.blit(text_puntaje, (10, 10))
    screen.blit(text_tiempo, (WIDTH - 200, 10))

    # Dibujar línea de felicidad
    green_intensity = min(puntaje * 2.55, 255)
    pygame.draw.line(screen, (0, green_intensity, 0), (0, HEIGHT - 10), (WIDTH * puntaje / 100, HEIGHT - 10), 10)

    if fin:
        screen.blit(fin_bg, (0, 0))
        font = pygame.font.Font(None, 36)
        text = font.render("Presione ESC para salir", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 40))
        screen.blit(text, text_rect)
        pygame.display.flip()


# Función para cambiar de nivel
def cambiar_nivel():
    global mapa, pos_x, pos_y, salida_x, salida_y, nivel_actual, objeto_visible, objeto2_visible, objeto3_visible, objeto4_visible, fin

    # Cambia al siguiente nivel
    if nivel_actual < num_niveles:
        nivel_actual += 1
        if nivel_actual == 2:
            mapa = mapa_nivel2
            pos_x, pos_y = 0, 0
            salida_x, salida_y = salida_x_nivel2, salida_y_nivel2
            objeto_visible = True
            objeto2_visible = True
            objeto3_visible = True
            objeto4_visible = True
            fin = False



# Funciones de menú
def mostrar_menu():
    font = pygame.font.Font(None, 36)
    text_iniciar = font.render("1. Iniciar", True, (255, 255, 255))
    text_creditos = font.render("2. Créditos", True, (255, 255, 255))

    screen.blit(text_iniciar, (WIDTH // 2 - 70, HEIGHT // 2 - 50))
    screen.blit(text_creditos, (WIDTH // 2 - 70, HEIGHT // 2 + 10))

def mostrar_creditos():
    font = pygame.font.Font(None, 36)
    text_desarrollado = font.render("Desarrollado por:", True, (255, 255, 255))
    text_desarrollador = font.render("EQUIPO 4", True, (255, 255, 255))
    text_evento = font.render("GLOBAL GAME JAM", True, (255, 255, 255))
    text_volver = font.render("S para salir", True, (255, 255, 255))

    screen.blit(text_desarrollado, (WIDTH // 2 - 120, HEIGHT // 2 - 50))
    screen.blit(text_desarrollador, (WIDTH // 2 - 70, HEIGHT // 2 - 10))
    screen.blit(text_evento, (WIDTH // 2 - 70, HEIGHT // 2 + 40))
    screen.blit(text_volver, (WIDTH // 2 - 180, HEIGHT - 80))

# Carga de la música del menú
menu_music = pygame.mixer.Sound("Audio/Menu.mp3")
menu_music.set_volume(0.3)
menu_music.play(-1)

# Carga de la imagen para el menú
menu_image = pygame.image.load('Images/menu.png')
menu_image = pygame.transform.scale(menu_image, (WIDTH, HEIGHT))
creditos_image = pygame.image.load('Images/creditos.png')
creditos_image = pygame.transform.scale(creditos_image, (WIDTH, HEIGHT))

def mostrar_historia_parte(parte):
    historia_font = pygame.font.Font(None, 24)
    historia_texto = {
        1: [
            "Dos niños están jugando en un hermoso jardín.",
            "De repente, el juguete favorito de uno de,",
            "los niños se rompe y comienza a llorar.", 
            "La niña, queriendo animarlo, decide recorrer",
            "el jardín en busca de cosas divertidas para hacer",
            "reír al niño. Mientras recorre el jardín, se encuentra",
            "con diferentes obstáculos y desafíos que",
            "debe superar para encontrar las cosas ",
            "que harán reír al niño.", 
            "El objetivo del juego es ayudar a la niña a",
            "superar estos obstáculos y encontrar las cosas más",
            "divertidas para hacer reír al niño",
            "y restaurar su felicidad."
        ]
    }

    screen.blit(menu_image, (0, 0))  # Fondo de la imagen del menú

    for i, linea in enumerate(historia_texto[parte]):
        text = historia_font.render(linea, True, (0, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 30))
        screen.blit(text, (50, 50 + i * 30))  # Ajusta las coordenadas según sea necesario
    pygame.display.flip()

    esperando_avance = True
    while esperando_avance:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_SPACE:
                esperando_avance = False
                return  # Salir de la función después de presionar ESPACIO

# Bucle del menú
# Bucle del menú
menu_running = True
parte_historia = 1
while menu_running and parte_historia <= 3:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            menu_running = False
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_1:
                menu_running = False
                mostrar_historia_parte(parte_historia)  # Llama a la función para mostrar la historia
                parte_historia += 1
                menu_music.stop() #Detener musica del menú
            elif event.key == K_2:
                screen.blit(creditos_image, (0, 0))
                mostrar_creditos()
                pygame.display.flip()

                creditos_running = True
                regresar_menu = False
                while creditos_running:
                    for event in pygame.event.get():
                        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                            creditos_running = False
                            menu_running = False
                            pygame.quit()
                            sys.exit()
                        elif event.type == KEYDOWN:
                            if event.key == K_s:  # Tecla 'S' para salir
                                regresar_menu = True
                                creditos_running = False

                # Al salir de los créditos, volver al menú
                if regresar_menu:
                    menu_running = True
                    mostrar_menu()
                    screen.blit(menu_image, (0, 0))
                    pygame.display.flip()

    # Limpiar al regresar al menú
    if menu_running:
        screen.fill((0, 0, 0))
        screen.blit(menu_image, (0, 0))
        mostrar_menu()
        pygame.display.flip()

# Carga control de volumen de la música del juego
pygame.mixer.init()
pygame.mixer.music.load("Audio/GameJam.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

pygame.display.flip()

# Carga control de volumen de la música del juego
pygame.mixer.init()
pygame.mixer.music.load("Audio/GameJam.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

pygame.display.flip()
# Bucle principal del programa
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False
        elif event.type == KEYDOWN:
            if not fin:
                if event.key == K_UP and (pos_y > 0) and mapa[pos_y-1, pos_x] == 0:
                    pos_y -= 1
                    direccion = 'arriba'
                elif event.key == K_DOWN and (pos_y < filas-1) and mapa[pos_y+1, pos_x] == 0:
                    pos_y += 1
                    direccion = 'abajo'
                elif event.key == K_RIGHT and (pos_x < columnas - 1) and mapa[pos_y, pos_x + 1] == 0:
                    pos_x += 1
                    direccion = 'derecha'
                elif event.key == K_LEFT and (pos_x > 0) and mapa[pos_y, pos_x - 1] == 0:
                    pos_x -= 1
                    direccion = 'izquierda'

    if not fin and pos_x == salida_x and pos_y == salida_y:
        fin = True
        cambiar_nivel()

    if not fin and objeto_visible and pos_x == objeto_x and pos_y == objeto_y:
        objeto_visible = False
        puntaje += 5
        sonido_objeto.play()
        longitud_linea_feliz += 2

    if not fin and objeto2_visible and pos_x == objeto2_x and pos_y == objeto2_y:
        objeto2_visible = False
        puntaje += 5
        sonido_objeto.play()
        longitud_linea_feliz += 5
    
    if not fin and objeto3_visible and pos_x == objeto3_x and pos_y == objeto3_y:
        objeto3_visible = False
        puntaje += 7
        sonido_objeto.play()
        longitud_linea_feliz += 7

    if not fin and objeto4_visible and pos_x == objeto4_x and pos_y == objeto4_y:
        objeto4_visible = False
        puntaje += 10
        sonido_objeto.play()
        longitud_linea_feliz += 10

    map_draw()

    # Dibujar el objeto solo si está visible
    if objeto_visible:
        screen.blit(objeto, (objeto_x * cell_width, objeto_y * cell_height))

    # Dibujar el primer objeto solo si está visible
    if objeto_visible:
        screen.blit(objeto, (objeto_x * cell_width, objeto_y * cell_height))

    # Dibujar el segundo objeto solo si está visible
    if objeto2_visible:
        screen.blit(objeto2, (objeto2_x * cell_width, objeto2_y * cell_height))

    # Dibujar el tercer objeto solo si está visible
    if objeto3_visible:
        screen.blit(objeto3, (objeto3_x * cell_width, objeto3_y * cell_height))

    # Dibujar el cuarto objeto solo si está visible
    if objeto4_visible:
        screen.blit(objeto4, (objeto4_x * cell_width, objeto4_y * cell_height))

    # Verificar si se alcanzó el tiempo límite
    if int(time.time() - tiempo_inicial) >= tiempo_limite:
        fin = True
        puntaje = 0
        screen.blit(game_over_image, (0, 0))
        pygame.display.flip()
        pygame.time.delay(3000)  # Espera 3 segundos antes de salir del juego
        running = False

    pygame.display.flip()

# Cerrar Pygame
pygame.quit()

# Importación de las bibliotecas necesarias
import pygame, sys, random

# Función para dibujar el suelo
def dibuja_piso():
    pygame.draw.rect(pantalla, (0, 128, 0), pygame.Rect(piso_x_pos, 900, 576, 124))
    pygame.draw.rect(pantalla, (0, 128, 0), pygame.Rect(piso_x_pos + 536, 900, 576, 124))

# Función para crear obstáculos
def crea_obstaculo():
    random_obstaculo_pos = random.choice(obstaculo_height)
    bottom_obstaculo = pygame.Rect(700, random_obstaculo_pos, 80, 300)
    top_obstaculo = pygame.Rect(700, random_obstaculo_pos - 550, 80, 300)
    return bottom_obstaculo, top_obstaculo

# Función para mover obstáculos
def mover_obstaculo(obstaculos):
    for obstaculo in obstaculos:
        obstaculo.x -= 6
    return obstaculos

# Función para dibujar obstáculos
def dibuja_obstaculo(obstaculos):
    for obstaculo in obstaculos:
        pygame.draw.rect(pantalla, (0, 255, 0), obstaculo)

# Función para eliminar obstáculos que salen de la pantalla
def quitar_obstaculos(obstaculos):
    obstaculos = [obstaculo for obstaculo in obstaculos if obstaculo.x > -800]
    return obstaculos

# Función para verificar colisiones
def check_collision(obstaculos, bird):
    for obstaculo in obstaculos:
        if bird.colliderect(obstaculo):
            return  False
    if bird.top <= 0 or bird.bottom >= 900:
        return False
    return True

# Función para mostrar la puntuación en pantalla
def Puntuacion_display(game_state):
    if game_state == 'main_game':
        Puntuacion_surface = game_font.render(str(int(Puntuacion)), True, (0, 0, 0))
        Puntuacion_rect = Puntuacion_surface.get_rect(center=(288, 100))
        pantalla.blit(Puntuacion_surface, Puntuacion_rect)
    if game_state == 'Perdiste xd':
        Puntuacion_surface = game_font.render(f'Puntuacion: {int(Puntuacion)}', True, (0, 0, 0))
        Puntuacion_rect = Puntuacion_surface.get_rect(center=(288, 100))
        pantalla.blit(Puntuacion_surface, Puntuacion_rect)

        Puntos_mas_altos_surface = game_font.render(f'Puntos mas altos: {int(Puntos_mas_altos)}', True, (0, 0, 0))
        Puntos_mas_altos_rect = Puntos_mas_altos_surface.get_rect(center=(288, 850))
        pantalla.blit(Puntos_mas_altos_surface, Puntos_mas_altos_rect)

# Función para actualizar la puntuación más alta
def update_Puntuacion(Puntuacion, Puntos_mas_altos):
    if Puntuacion > Puntos_mas_altos:
        Puntos_mas_altos = Puntuacion
    return Puntos_mas_altos

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
pantalla = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font(None, 40)

# Carga de la imagen del pájaro y ajuste de tamaño
condor_img = pygame.image.load('C:/Users/Usuario/Downloads/condor.png')
condor_img = pygame.transform.scale(condor_img, (50, 50))

# Configuración de la gravedad y la velocidad de movimiento del pájaro
gravity = 0.25 
bird_movement = 0
game_active = True
Puntuacion = 0
Puntos_mas_altos = 0
piso_x_pos = 0

# Rectángulo que representa al pájaro
bird_rect = pygame.Rect(100, 512, 30, 30)

# Lista que contiene los obstáculos
obstaculo_list = []

# Configuración de un evento para generar obstáculos
Generar = pygame.USEREVENT
pygame.time.set_timer(Generar, 600)

# Alturas posibles para los obstáculos
obstaculo_height = [400, 600, 800]

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        # Evento de cierre de la ventana
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Evento de tecla presionada
        if event.type == pygame.KEYDOWN:
            # Tecla espaciadora para saltar si el juego está activo
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 8.5
            # Tecla espaciadora para reiniciar si el juego no está activo
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True 
                obstaculo_list.clear()
                bird_rect.topleft = (100, 512)
                bird_movement = 0
                Puntuacion = 0
        # Evento para generar obstáculos a intervalos regulares
        if event.type == Generar:
            obstaculo_list.extend(crea_obstaculo())

    # Relleno de la pantalla con color blanco
    pantalla.fill((255, 255, 255))

    if game_active:
        # Actualización del movimiento del pájaro y verificación de colisiones
        bird_movement += gravity
        bird_rect.y += bird_movement
        game_active = check_collision(obstaculo_list, bird_rect)

        # Movimiento, dibujo y gestión de obstáculos
        obstaculo_list = mover_obstaculo(obstaculo_list)
        obstaculo_list = quitar_obstaculos(obstaculo_list)
        dibuja_obstaculo(obstaculo_list)

        # Incremento de la puntuación y visualización en pantalla
        Puntuacion += 0.01
        Puntuacion_display('main_game')

        # Configuración y visualización de la imagen del pájaro
        condor_rect = condor_img.get_rect(center=bird_rect.center)
        pantalla.blit(condor_img, condor_rect)

    else:
        # Visualización de la puntuación y la puntuación más alta si el juego ha terminado
        Puntuacion_display('Perdiste xd')
        Puntos_mas_altos = update_Puntuacion(Puntuacion, Puntos_mas_altos)

    # Desplazamiento del suelo y su visualización
    piso_x_pos -= 0.05
    dibuja_piso()

    # Actualización de la pantalla
    pygame.display.update()
    clock.tick(60)

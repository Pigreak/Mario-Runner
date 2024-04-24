import pygame
from sys import exit
from random import randint, choice

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        jugador_walk1 = pygame.image.load('Personaje/mario_walk_1.png').convert_alpha()
        jugador_walk2 = pygame.image.load('Personaje/mario_walk_2.png').convert_alpha()
        self.jugador_walk = [jugador_walk1,jugador_walk2]
        self.jugador_index = 0
        self.jugador_jump = pygame.image.load('Personaje/mario_jump.png').convert_alpha()

        self.image = self.jugador_walk[self.jugador_index]
        self.rect = self.image.get_rect(midbottom = (100,208))
        self.gravedad = 0

        self.sonido_salto = pygame.mixer.Sound('Audio/salto.mp3')
        self.sonido_salto.set_volume(0.3)

    def jugador_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 208:
            self.sonido_salto.play()
            self.gravedad = -3
    
    def aplicar_gravedad(self):
        self.gravedad += 0.1
        self.rect.y += self.gravedad
        if self.rect.bottom >= 208:
            self.rect.bottom = 208

    def animaciones(self):
        if self.rect.bottom < 208:
            self.image = self.jugador_jump
        else:
            self.jugador_index += 0.1
            if self.jugador_index >= len(self.jugador_walk):self.jugador_index = 0
            self.image = self.jugador_walk[int(self.jugador_index)]
    
    def update(self):
        self.jugador_input()
        self.aplicar_gravedad()
        self.animaciones()

class Obstaculos(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == 'tortuga':
            tortuga_walk1 = pygame.image.load('Personaje/tortuga1.png').convert_alpha()
            tortuga_walk2 = pygame.image.load('Personaje/tortuga2.png').convert_alpha()
            self.frames = [tortuga_walk1,tortuga_walk2]
            y_pos = 208
        elif type == 'goomba':
            goomba_walk1 = pygame.image.load('Personaje/goomba1.png').convert_alpha()
            goomba_walk2 = pygame.image.load('Personaje/goomba2.png').convert_alpha()
            self.frames = [goomba_walk1,goomba_walk2]
            y_pos = 208
        else:
            self.frames = [pygame.image.load('Personaje/bala.png').convert_alpha()]
            y_pos = 160

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(400,500),y_pos))

    def animaciones(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animaciones()
        self.rect.x -= 1
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def mostrar_puntuacion():
    puntuacion = int(pygame.time.get_ticks()/1000) - tiempo_inicio
    puntuacion_surf = fuente.render(f'Score: {puntuacion}',False,'Black')
    puntuacion_rec = puntuacion_surf.get_rect(center = (160, 20))
    pantalla.blit(puntuacion_surf,puntuacion_rec)
    return puntuacion

def colisiones_sprite():
    if pygame.sprite.spritecollide(jugador.sprite,obstaculos_group,False):
        sonido_tema.stop()
        sonido_muerte.play()
        obstaculos_group.empty()
        return False
    else: return True

pygame.init()



pantalla = pygame.display.set_mode((320,240)) # Pantalla y tamaño
pygame.display.set_caption('Runner') # Nombre del programa
reloj = pygame.time.Clock() # Reloj de frecuencia
fuente = pygame.font.Font('Fuentes/Minecraft.ttf', 20) # Tipo de texto
juego_activo = False
tiempo_inicio = 0
puntuacion = 0

#MUSICA
iniciar_musica = False
sonido_tema = pygame.mixer.Sound('Audio/tema.mp3')
sonido_tema.set_volume(0.5)

sonido_muerte = pygame.mixer.Sound('Audio/dead.mp3')
sonido_muerte.set_volume(0.3)

#SINGLE GROUP
jugador = pygame.sprite.GroupSingle()
jugador.add(Jugador())

#GROUP
obstaculos_group = pygame.sprite.Group()

# Cargar un surface de imagen
cielo = pygame.image.load('Graficos/fondo.png').convert_alpha()
suelo = pygame.image.load('Graficos/suelo.png').convert_alpha()
texto_surf = fuente.render('Mi Juego', False, 'Black') # False para que sea tipo pixelart
texto_rec = texto_surf.get_rect(center = (160, 20))

# INTRO DEL JUEGO
jugador_intro_surf = pygame.image.load('Personaje/mario.png').convert_alpha()
jugador_intro_surf = pygame.transform.scale(jugador_intro_surf,(50,50))
jugador_intro_rect= jugador_intro_surf.get_rect(center = (160, 120))

nombre_juego = fuente.render('Mario Runner', False, 'Red')
nombre_juego_rec = nombre_juego.get_rect(center = (160, 80))

mensaje_juego = fuente.render('Presiona espacio para jugar',False,('Red'))
mensaje_juego_rec = mensaje_juego.get_rect(center = (160, 160))

# TIMER
obastaculos_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obastaculos_timer,2000) # Frecuencia con la que salen los enemigos

tortuga_animacion_timer = pygame.USEREVENT + 2
pygame.time.set_timer(tortuga_animacion_timer,250)

goomba_animacion_timer = pygame.USEREVENT + 3
pygame.time.set_timer(goomba_animacion_timer,250)

while True:
    # Capturador de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit() # Salida correcta de python (para no generar errores)
        if  juego_activo:
            if event.type == obastaculos_timer:
                obstaculos_group.add(Obstaculos(choice(['tortuga','tortuga','goomba','goomba','bala'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if iniciar_musica == False:
                    iniciar_musica = True
                    sonido_tema.play(loops = -1)
                juego_activo = True
                tiempo_inicio = int(pygame.time.get_ticks()/1000)
                
    if juego_activo:
        pantalla.blit(cielo,(0,0)) # Localizar un surface en la pantalla
        pantalla.blit(suelo,(0,208))
        
        puntuacion = mostrar_puntuacion()
        
        jugador.draw(pantalla) 
        jugador.update() 

        obstaculos_group.draw(pantalla)
        obstaculos_group.update()

        juego_activo = colisiones_sprite()

    else:
        iniciar_musica = False
        pantalla.fill('Black')
        pantalla.blit(jugador_intro_surf, jugador_intro_rect)

        mensaje_puntuacion = fuente.render(f'Score: {puntuacion}',False,'Red')
        mensaje_puntuacion_rec = mensaje_puntuacion.get_rect(center = (160, 160))
        pantalla.blit(nombre_juego,nombre_juego_rec)
        if puntuacion == 0:
            pantalla.blit(mensaje_juego,mensaje_juego_rec)
        else:
            pantalla.blit(mensaje_puntuacion,mensaje_puntuacion_rec)

    pygame.display.update()
    reloj.tick(60) # Corre a 60 fps
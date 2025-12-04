import pygame
import sys
import random

ANCHO = 800
ALTO = 400
FPS = 60
VELOCIDAD_NIVEL = 6 
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS_SUELO = (150, 150, 150)

AZUL = (0, 150, 255)    # Cubo
ROJO = (255, 50, 0)     # Nave
VERDE = (0, 200, 0)     # Bola
AMARILLO = (255, 200, 0) # OVNI

pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("PyDash - El Juego Final")
reloj = pygame.time.Clock()
font = pygame.font.Font(None, 30)

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size = 30
        self.image = pygame.Surface([self.size, self.size])
        self.rect = self.image.get_rect()
        self.gravedad_base = 0.8
        self.gravedad_bola_dir = 1 
        
        self.direccion_y = 1  # 1: Mundo Normal, -1: Mundo Reverso (Teclas R)
        self.reiniciar_posicion()

    def reiniciar_posicion(self):
        self.rect.x = 50
        self.rect.y = ALTO - 30 - self.size 
        self.velocidad_y = 0
        self.esta_en_suelo = True
        self.direccion_y = 1 
        self.gravedad_bola_dir = 1
        self.cambiar_modo("Cubo") 

    def cambiar_modo(self, nuevo_modo):
        self.modo = nuevo_modo
        
        color_base = NEGRO
        if self.modo == "Cubo": color_base = AZUL
        elif self.modo == "Nave": color_base = ROJO
        elif self.modo == "Bola": color_base = VERDE
        elif self.modo == "OVNI": color_base = AMARILLO
        
        self.image.fill(color_base)
        if self.direccion_y == -1:
             self._aplicar_color_reverso()

    def _aplicar_color_reverso(self):
        if self.modo == "Cubo": self.image.fill((0, 255, 255)) 
        elif self.modo == "Nave": self.image.fill((255, 100, 100))
        elif self.modo == "Bola": self.image.fill((100, 255, 100))
        elif self.modo == "OVNI": self.image.fill((255, 255, 100))

    def invertir_gravedad_mundo(self):
        #Invierte el mundo entero (Tecla R)
        self.direccion_y *= -1
        self.velocidad_y = 0 
        self._aplicar_color_reverso() if self.direccion_y == -1 else self.cambiar_modo(self.modo)
        
        if self.direccion_y == 1:
            self.rect.bottom = ALTO - 30 
        else:
            self.rect.top = 30 

    def accion_principal(self):
        """Maneja el SALTO o cambio de gravedad con ESPACIO."""
        
        suelo_y = ALTO - 30
        techo_y = 30

        if self.modo == "Cubo" and self.esta_en_suelo:
            self.velocidad_y = -13 * self.direccion_y
            self.esta_en_suelo = False
            
        elif self.modo == "Nave":
            self.velocidad_y = -5 * self.direccion_y
            
        elif self.modo == "Bola":
            en_piso = self.rect.bottom >= suelo_y
            en_techo = self.rect.top <= techo_y
            
            if en_piso or en_techo:
                self.gravedad_bola_dir *= -1 
                self.velocidad_y = 5 * self.gravedad_bola_dir
            
        elif self.modo == "OVNI":
            self.velocidad_y = -8 * self.direccion_y

    def update(self):
        if self.modo == "Bola":
            self.velocidad_y += 0.8 * self.gravedad_bola_dir
        elif self.modo == "Nave":
             self.velocidad_y += 0.3 * self.direccion_y 
        else:
            self.velocidad_y += self.gravedad_base * self.direccion_y
            
        self.rect.y += self.velocidad_y
        suelo_y = ALTO - 30  
        techo_y = 30     
        if self.rect.bottom >= suelo_y:
            self.rect.bottom = suelo_y
            if self.velocidad_y > 0:
                self.velocidad_y = 0
                self.esta_en_suelo = True
        if self.rect.top <= techo_y:
            self.rect.top = techo_y
            if self.velocidad_y < 0:
                self.velocidad_y = 0
                if self.modo == "Bola":
                    self.esta_en_suelo = True 
        if self.modo != "Bola":
            if (self.direccion_y == 1 and self.rect.bottom < suelo_y) or \
               (self.direccion_y == -1 and self.rect.top > techo_y):
                self.esta_en_suelo = False
                
class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, x, y, size, direccion=1):
        super().__init__()
        self.direccion = direccion 
        self.image = pygame.Surface([size, size], pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0)) 

        color_pico = BLANCO
        if self.direccion == 1:
            puntos = [(0, size), (size // 2, 0), (size, size)]
            self.rect = self.image.get_rect(x=x, bottom=y)
        else:
            puntos = [(0, 0), (size // 2, size), (size, 0)]
            self.rect = self.image.get_rect(x=x, top=y)
            
        pygame.draw.polygon(self.image, color_pico, puntos)

    def update(self):
        self.rect.x -= VELOCIDAD_NIVEL
        if self.rect.right < 0:
            self.kill()
            
def generar_obstaculo(obstaculos_group, todos_sprites_group):
    y_spawn_suelo = ALTO - 30      
    y_spawn_techo = 30              
    
    posiciones = [y_spawn_suelo, y_spawn_techo]
    y_spawn = random.choice(posiciones)
    direccion = 1 if y_spawn == y_spawn_suelo else -1

    nuevo_obstaculo = Obstaculo(ANCHO, y_spawn, 30, direccion=direccion)
    obstaculos_group.add(nuevo_obstaculo)
    todos_sprites_group.add(nuevo_obstaculo)

jugador = Jugador()
todos_los_sprites = pygame.sprite.Group()
obstaculos = pygame.sprite.Group()
todos_los_sprites.add(jugador)

game_over = False
score = 0
spawn_timer = 0
spawn_delay = 90 

corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        
        if not game_over:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    if jugador.modo != "Nave":
                        jugador.accion_principal()
                if evento.key == pygame.K_c: jugador.cambiar_modo("Cubo")
                if evento.key == pygame.K_n: jugador.cambiar_modo("Nave")
                if evento.key == pygame.K_b: jugador.cambiar_modo("Bola")
                if evento.key == pygame.K_o: jugador.cambiar_modo("OVNI")
                if evento.key == pygame.K_r: jugador.invertir_gravedad_mundo()
        else: 
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                game_over = False
                score = 0
                jugador.reiniciar_posicion()
                obstaculos.empty()
                todos_los_sprites.empty()
                todos_los_sprites.add(jugador)
                spawn_timer = 0
                spawn_delay = 90
    if not game_over:
        keys = pygame.key.get_pressed()
        if jugador.modo == "Nave" and keys[pygame.K_SPACE]:
            jugador.accion_principal()
        
        todos_los_sprites.update()
        score += 1 

        spawn_timer += 1
        if spawn_timer >= spawn_delay:
            generar_obstaculo(obstaculos, todos_los_sprites)
            spawn_timer = 0
            spawn_delay = max(40, spawn_delay - 0.5) 

        if pygame.sprite.spritecollide(jugador, obstaculos, False):
            game_over = True
    pantalla.fill(NEGRO) 
    pygame.draw.rect(pantalla, GRIS_SUELO, [0, ALTO - 30, ANCHO, 30])
    pygame.draw.rect(pantalla, GRIS_SUELO, [0, 0, ANCHO, 30])

    todos_los_sprites.draw(pantalla)
    modo_texto = font.render(f"MODO: {jugador.modo}", True, BLANCO)
    score_texto = font.render(f"SCORE: {score // 10}", True, BLANCO)
    pantalla.blit(modo_texto, (10, 50))
    pantalla.blit(score_texto, (ANCHO - 150, 50))

    if game_over:
        texto_final = font.render("GAME OVER", True, ROJO)
        rect_final = texto_final.get_rect(center=(ANCHO // 2, ALTO // 2 - 20))
        pantalla.blit(texto_final, rect_final)
        texto_reiniciar = font.render("ENTER para reiniciar", True, BLANCO)
        rect_reiniciar = texto_reiniciar.get_rect(center=(ANCHO // 2, ALTO // 2 + 20))
        pantalla.blit(texto_reiniciar, rect_reiniciar)

    pygame.display.flip()
    reloj.tick(FPS)

pygame.quit()
sys.exit()
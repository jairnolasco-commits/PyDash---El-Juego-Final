## 🚀 Manual de "PyDash - El Juego Final"

Este juego es un ***runner* rítmico de desplazamiento lateral**, similar a Geometry Dash, donde el jugador debe alternar modos y controlar la gravedad para evitar obstáculos triangulares.

***

## 🕹️ 1. Instrucciones de Juego

### 1.1. Controles Principales

| Tecla | Función | Modos Afectados | Descripción |
| :---: | :---: | :---: | :---: |
| **ESPACIO** | **Acción Principal** | Todos | Inicia el Salto (**Cubo, OVNI**), Impulsa (**Nave**) o invierte la gravedad interna (**Bola**). |
| **R** | **Gravedad Mundial** | Todos | **Invierte la gravedad** de todo el nivel, cambiando el "suelo" por el "techo" y viceversa. |
| **ENTER** | **Reiniciar** | GAME OVER | Reinicia el juego después de chocar contra un obstáculo. |

### 1.2. Teclas de Cambio de Modo

El jugador puede cambiar de modo en cualquier momento para adaptar su movimiento al nivel:

| Tecla | Modo | Color | Características de Movimiento |
| :---: | :---: | :---: | :---: |
| **C** | **Cubo** | Azul | **Salto Único:** Solo puede saltar si está tocando el suelo. |
| **N** | **Nave** | Rojo | **Vuelo:** Puede volar continuamente manteniendo presionado **ESPACIO**. La gravedad es suave. |
| **B** | **Bola** | Verde | **Gravedad Invertida:** La gravedad del jugador se invierte al tocar un límite. **ESPACIO** fuerza un cambio inmediato. |
| **O** | **OVNI** | Amarillo | **Salto Continuo:** Puede saltar repetidamente en el aire al pulsar **ESPACIO**. |

***

## 💡 2. Estructura y Componentes del Código

Tu código utiliza la librería Pygame y se basa en el concepto fundamental del **Game Loop** (Bucle Principal).

### 2.1. El Bucle Principal (Game Loop) 🔄

El corazón del juego es el ciclo `while corriendo:`, que ejecuta las tres fases principales por *frame* (60 veces por segundo):

1.  **Entrada:** Procesa eventos de teclado y salida (`pygame.event.get()`).
2.  **Actualización (Lógica):** Mueve el jugador y obstáculos, genera nuevos obstáculos y comprueba la colisión.
3.  **Dibujado:** Pinta todos los elementos en la pantalla.


---

### 2.2. Clases de Entidades

#### A. Clase `Jugador`
Es el *sprite* que controla el movimiento y la adaptación a los modos.

* **Hitbox:** Siempre es un **cuadrado de $\text{30} \times \text{30}$ píxeles** (`self.rect`).
* **Modos de Gravedad:**
    * `self.direccion_y` (1 o -1): Controla la **Gravedad Mundial** (afectada por la tecla **R**).
    * `self.gravedad_bola_dir` (1 o -1): Controla la **Gravedad Interna** (solo para el Modo Bola).

#### B. Clase `Obstaculo`
Representa los picos que se mueven hacia la izquierda.

* **Hitbox:** A pesar de dibujarse como un triángulo, su **caja de colisión es un cuadrado de $\text{30} \times \text{30}$ píxeles** (`self.rect`) que envuelve la forma triangular.
* **Colisión:** El juego usa la función estándar `pygame.sprite.spritecollide`. Esto significa que la colisión se detecta si los **rectángulos delimitadores** del jugador y del obstáculo se superponen.


---

### 2.3. Dificultad Progresiva

* **Velocidad Constante:** Los obstáculos se mueven a una velocidad fija (`VELOCIDAD_NIVEL = 6`).
* **Frecuencia Aumentada:** El juego se vuelve más difícil porque el tiempo de espera entre la generación de nuevos obstáculos (`spawn_delay`) se **reduce gradualmente** (`spawn_delay = max(40, spawn_delay - 0.5)`). Esto fuerza al jugador a reaccionar más rápido a los objetos que aparecen.
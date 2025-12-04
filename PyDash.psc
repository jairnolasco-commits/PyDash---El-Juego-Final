Algoritmo PyDash_Logica
	Definir modo Como Entero
	Definir direccion_y Como Entero
	Definir gravedad_bola_dir Como Entero
	Definir vel_y Como Real
	Definir pos_y Como Real
	Definir suelo_y Como Entero
	Definir techo_y Como Entero
	Definir tecla Como Entero
	Definir score Como Entero
	Definir spawn_timer Como Entero
	Definir spawn_delay Como Entero
	Definir game_over Como Lógico
	Definir corriendo Como Lógico
	// MODOS: 1=Cubo , 2=Nave , 3=Bola , 4=Ovni
	modo <- 1
	direccion_y <- 1
	gravedad_bola_dir <- 1
	vel_y <- 0
	suelo_y <- 370
	techo_y <- 30
	pos_y <- suelo_y
	game_over <- Falso
	corriendo <- Verdadero
	score <- 0
	spawn_timer <- 0
	spawn_delay <- 90
	Mientras corriendo=Verdadero Hacer
		Escribir 'Presiona (1=Cubo,2=Nave,3=Bola,4=OVNI,5=Accion,6=Invertir,7=Reiniciar,0=Salir): '
		Leer tecla
		Si tecla=0 Entonces
			corriendo <- Falso
		FinSi
		Si game_over=Falso Entonces
			// --- CAMBIAR MODO ---
			Si tecla=1 Entonces
				modo <- 1
			FinSi
			Si tecla=2 Entonces
				modo <- 2
			FinSi
			Si tecla=3 Entonces
				modo <- 3
			FinSi
			Si tecla=4 Entonces
				modo <- 4
			FinSi
			// --- INVERTIR GRAVEDAD ---
			Si tecla=6 Entonces
				direccion_y <- direccion_y*(-1)
				vel_y <- 0
			FinSi
			// --- ACCIÓN PRINCIPAL ---
			Si tecla=5 Entonces
				Si modo=1 Entonces
					Si pos_y=suelo_y Entonces
						vel_y <- (-13)*direccion_y
					FinSi
				FinSi
				Si modo=2 Entonces
					vel_y <- (-5)*direccion_y
				FinSi
				Si modo=3 Entonces
					Si pos_y=suelo_y Entonces
						gravedad_bola_dir <- gravedad_bola_dir*(-1)
						vel_y <- 5*gravedad_bola_dir
					FinSi
					Si pos_y=techo_y Entonces
						gravedad_bola_dir <- gravedad_bola_dir*(-1)
						vel_y <- 5*gravedad_bola_dir
					FinSi
				FinSi
				Si modo=4 Entonces
					vel_y <- (-8)*direccion_y
				FinSi
			FinSi
		SiNo
			// GAME OVER
			Si tecla=7 Entonces
				game_over <- Falso
				modo <- 1
				direccion_y <- 1
				gravedad_bola_dir <- 1
				vel_y <- 0
				pos_y <- suelo_y
				score <- 0
				spawn_delay <- 90
			FinSi
		FinSi
		// ======= FISICA =======
		Si modo=3 Entonces
			vel_y <- vel_y+(0.8*gravedad_bola_dir)
		SiNo
			Si modo=2 Entonces
				vel_y <- vel_y+(0.3*direccion_y)
			SiNo
				vel_y <- vel_y+(1*direccion_y)
			FinSi
		FinSi
		pos_y <- pos_y+vel_y
		// LIMITE INFERIOR
		Si pos_y>suelo_y Entonces
			pos_y <- suelo_y
			vel_y <- 0
		FinSi
		// LIMITE SUPERIOR
		Si pos_y<techo_y Entonces
			pos_y <- techo_y
			vel_y <- 0
		FinSi
		// ===== PUNTOS =====
		Si game_over=Falso Entonces
			score <- score+1
		FinSi
		Escribir 'Modo: ', modo
		Escribir 'Posición Y: ', pos_y
		Escribir 'Puntaje: ', score
		Escribir ' '
	FinMientras
FinAlgoritmo

import tkinter as tk
import math
import time

class Car:
    def __init__(self, canvas):
        self.canvas = canvas
        self.car_x = 100
        self.car_y = 200
        self.car_angle = 0  # 0: derecha, 90: abajo, 180: izquierda, 270: arriba
        self.speed = 4
        self.last_time = time.time()
        
        # Rutas: recto -> parar -> girar -> seguir
        self.ruta = [
            ("recto", 600),
            ("parar", None),
            ("girar", 90),
            ("recto", 200),
            ("parar", None),
            ("girar", 90),
            ("recto", 600),
            ("parar", None),
            ("girar", 90),
            ("recto", 200),
            ("girar", 90)
        ]
        self.ruta_index = 0
        self.distance_travelled = 0
        self.stopping = False
        self.stop_start_time = None
        
    self.body = self.create_car_body()

    def create_car_body(self):
        return self.canvas.create_polygon(
            [0, 0, 40, 0, 40, 20, 0, 20],
            fill='#3498DB', outline='#21618C', width=2
        )

    def update_car(self):
        angle_rad = math.radians(self.car_angle)
        cos_angle = math.cos(angle_rad)
        sin_angle = math.sin(angle_rad)

        body_coords = [
            self.car_x + 20*cos_angle - 10*sin_angle,
            self.car_y + 20*sin_angle + 10*cos_angle,
            
            self.car_x + 20*cos_angle + 10*sin_angle,
            self.car_y + 20*sin_angle - 10*cos_angle,
            
            self.car_x - 20*cos_angle + 10*sin_angle,
            self.car_y - 20*sin_angle - 10*cos_angle,
            
            self.car_x - 20*cos_angle - 10*sin_angle,
            self.car_y - 20*sin_angle + 10*cos_angle
        ]
        self.canvas.coords(self.body, *body_coords)

def move(self):
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time
        
        if self.stopping:
            if current_time - self.stop_start_time >= 3:
                self.stopping = False
                self.ruta_index += 1
            else:
                return  # Quieto mientras para
        else:
            if self.ruta_index >= len(self.ruta):
                self.ruta_index = 0  # <-- Reiniciar ruta aquí
                self.distance_travelled = 0

            accion, valor = self.ruta[self.ruta_index]
            
            if accion == "recto":
                dx = self.speed * math.cos(math.radians(self.car_angle))
                dy = self.speed * math.sin(math.radians(self.car_angle))
                self.car_x += dx
                self.car_y += dy
                self.distance_travelled += math.hypot(dx, dy)

                if self.distance_travelled >= valor:
                    self.distance_travelled = 0
                    self.ruta_index += 1
            elif accion == "parar":
                self.stopping = True
                self.stop_start_time = current_time
            elif accion == "girar":
                self.car_angle += valor
                self.car_angle %= 360
                self.ruta_index += 1

        self.update_car()

# Configuración de ventana
window = tk.Tk()
window.title("Carro haciendo cuadrado infinito")
canvas = tk.Canvas(window, width=800, height=600, bg='#ECF0F1')
canvas.pack()

# Dibujar pista cuadrada
canvas.create_line(100, 200, 700, 200, width=20, fill='gray')
canvas.create_line(700, 200, 700, 400, width=20, fill='gray')
canvas.create_line(700, 400, 100, 400, width=20, fill='gray')
canvas.create_line(100, 400, 100, 200, width=20, fill='gray')

# Inicializar carro
car = Car(canvas)

def game_loop():
 car.move()
window.after(30, game_loop)

game_loop()
window.mainloop()

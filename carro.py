import tkinter as tk
import math
import time

class PIDController:
    def __init__(self, Kp, Ki, Kd, output_limits=(-30, 30)):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.prev_error = 0
        self.integral = 0
        self.output_limits = output_limits

    def compute(self, error, dt):
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt if dt > 0 else 0
        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative
        self.prev_error = error
        min_output, max_output = self.output_limits
        output = max(min_output, min(max_output, output))  # limitar salida
        return output

class LineFollowerCar:
    def __init__(self, canvas):
        self.canvas = canvas
        self.car_x = 150
        self.car_y = 150
        self.car_angle = 0
        self.speed = 3
        self.turn_speed = 0
        self.max_turn_speed = 4
        self.pid = PIDController(1.8, 0.0, 0.8, output_limits=(-15, 15))
        self.last_time = time.time()

        self.path = [(650, 150), (650, 450), (150, 450), (150, 150)]
        self.current_target_idx = 0

        self.body = self.create_car_body()
        self.left_wheel = self.create_wheel()
        self.right_wheel = self.create_wheel()
        self.update_car()

    def create_car_body(self):
        return self.canvas.create_polygon(
            [0, 0, 50, 0, 50, 30, 0, 30],
            fill='#2E86C1', outline='#1B4F72', width=2
        )
    
    def create_wheel(self):
        return self.canvas.create_oval(
            0, 0, 12, 12,
            fill='#2C3E50', outline='#1B2631'
        )

    def update_car(self):
        angle_rad = math.radians(self.car_angle)
        cos_angle = math.cos(angle_rad)
        sin_angle = math.sin(angle_rad)
        body_coords = [
            self.car_x + 45*cos_angle - 15*sin_angle,
            self.car_y + 45*sin_angle + 15*cos_angle,
            self.car_x + 25*cos_angle + 15*sin_angle,
            self.car_y + 25*sin_angle - 15*cos_angle,
            self.car_x - 25*cos_angle + 15*sin_angle,
            self.car_y - 25*sin_angle - 15*cos_angle,
            self.car_x - 25*cos_angle - 15*sin_angle,
            self.car_y - 25*sin_angle + 15*cos_angle
        ]
        self.canvas.coords(self.body, *body_coords)

        wheel_offset = 20
        self.update_wheel(self.left_wheel, -wheel_offset, angle_rad)
        self.update_wheel(self.right_wheel, wheel_offset, angle_rad)

    def update_wheel(self, wheel, offset, angle_rad):
        wheel_x = self.car_x + offset * math.sin(angle_rad)
        wheel_y = self.car_y - offset * math.cos(angle_rad)
        self.canvas.coords(wheel, wheel_x-6, wheel_y-6, wheel_x+6, wheel_y+6)

    def move(self):
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time

        # Target actual
        target_x, target_y = self.path[self.current_target_idx]

        # Calcular ángulo objetivo
        dx = target_x - self.car_x
        dy = target_y - self.car_y
        desired_angle = math.degrees(math.atan2(dy, dx))

        # Error angular corregido
        error_angle = (desired_angle - self.car_angle + 180) % 360 - 180

        # PID para controlar giro
        steering = self.pid.compute(error_angle, dt)

        # Aplicar steering limitado
        self.turn_speed += steering * dt
        self.turn_speed = max(-self.max_turn_speed, min(self.max_turn_speed, self.turn_speed))
        self.car_angle += self.turn_speed

        # Mover el carro hacia adelante
        self.car_x += self.speed * math.cos(math.radians(self.car_angle))
        self.car_y += self.speed * math.sin(math.radians(self.car_angle))

        # Si estamos cerca del objetivo, cambiar al siguiente
        distance = math.hypot(dx, dy)
        if distance < 30:
            self.current_target_idx = (self.current_target_idx + 1) % len(self.path)

        self.update_car()

# Configuración ventana
window = tk.Tk()
window.title("Carro Recorrido Cuadrado - Mejorado")
canvas = tk.Canvas(window, width=800, height=600, bg='#EAEDED')
canvas.pack()

# Dibujar pista cuadrada
canvas.create_rectangle(150, 150, 650, 450, outline='#2C3E50', width=5)

# Inicializar carro
car = LineFollowerCar(canvas)

def game_loop():
    car.move()
    # Marcar la trayectoria
    canvas.create_oval(car.car_x-2, car.car_y-2, car.car_x+2, car.car_y+2, fill='#F1C40F', outline='')
    window.after(30, game_loop)

game_loop()
window.mainloop()

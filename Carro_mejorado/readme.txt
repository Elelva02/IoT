
README.txt
===========

Título: Simulación de Carro Seguidor de Trayectoria con PID en una Pista Cuadrada

Descripción General:
--------------------
Este proyecto consiste en una simulación visual, hecha en Python con la librería Tkinter, de un carro que recorre automáticamente una trayectoria cuadrada como si estuviera siguiendo una pista. El sistema fue mejorado progresivamente a partir de una versión inicial con comportamiento manual o sin control de trayectoria.

Mejoras respecto al código inicial:
-----------------------------------
1. **Implementación del Control PID**:
   - Se integró un controlador PID que calcula el error angular entre la dirección actual del carro y la dirección deseada hacia el siguiente punto objetivo.
   - Esto permite suavizar y corregir el giro del carro de manera automática, logrando que gire progresivamente sin sobrepasarse o zigzaguear.

2. **Definición de una Trayectoria Automática**:
   - Se definió una trayectoria cuadrada usando una lista de coordenadas: [(650,150), (650,450), (150,450), (150,150)].
   - El carro identifica el punto actual a alcanzar y, al estar suficientemente cerca, cambia al siguiente, repitiendo el ciclo en bucle.

3. **Control de Giro Progresivo**:
   - Se agregó una variable `turn_speed` que simula la inercia o velocidad angular, y se limita para evitar giros abruptos.
   - Esto mejora el realismo del movimiento del carro.

4. **Separación en Clases**:
   - El código fue modularizado con las clases `PIDController` y `LineFollowerCar`, mejorando la legibilidad y el mantenimiento del código.

5. **Visualización Estética y Funcional**:
   - Se usaron formas geométricas para representar el cuerpo y las ruedas del carro.
   - Se dibuja la trayectoria recorrida con puntos amarillos que muestran visualmente el camino seguido.

Funcionamiento del Sistema:
---------------------------
- Al iniciar el programa, se muestra una ventana con una pista cuadrada.
- El carro se desplaza automáticamente desde un punto inicial hacia el primer vértice de la pista.
- Utiliza el PID para corregir su ángulo y alinear su trayectoria hacia el objetivo.
- Al llegar cerca de un vértice, pasa al siguiente punto y continúa recorriendo el cuadrado indefinidamente.

Cómo ejecutar:
--------------
1. Asegúrate de tener Python 3 instalado.
2. Guarda el código en un archivo con extensión `.py` (por ejemplo: `carro_pid.py`).
3. Ejecuta el archivo desde tu terminal o entorno de desarrollo con:
4. Se abrirá una ventana con la simulación del carro recorriendo la pista cuadrada.

Parámetros PID utilizados:
--------------------------
- Proporcional (Kp): 1.8
- Integral (Ki): 0.0
- Derivativo (Kd): 0.8
- Límites de salida: [-15, 15]

Notas Finales:
--------------
- El sistema puede ajustarse para diferentes trayectorias o caminos.
- Puedes experimentar con los valores del PID para ver cómo cambia el comportamiento del carro.
- Este proyecto es ideal como base para simulaciones de robots seguidores de línea o navegación autónoma.


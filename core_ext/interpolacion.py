import cv2
import numpy as np
from scipy.interpolate import CubicSpline

class LienzoConInterpolacion:
    def __init__(self, ruta_imagen_fondo, fps=24, segundos=5):
        self.imagen_fondo = cv2.imread(ruta_imagen_fondo, cv2.IMREAD_UNCHANGED)
        
        if self.imagen_fondo is None:
            raise FileNotFoundError("Error: No se pudo cargar la imagen de fondo.")
        
        self.alto, self.ancho = self.imagen_fondo.shape[:2]
        self.lienzo = np.copy(self.imagen_fondo)
        self.puntos_anclaje = []
        self.fps = fps
        self.segundos = segundos
        self.segmentos = fps * segundos

    def agregar_punto_anclaje(self, x, y):
        if 0 <= x < self.ancho and 0 <= y < self.alto:
            self.puntos_anclaje.append((x, y))
            self.lienzo[y, x] = (0, 255, 0)

    def interpolar(self):
        if len(self.puntos_anclaje) < 2:
            print("Se necesitan al menos 2 puntos de anclaje para interpolar.")
            return

        puntos_anclaje = np.array(self.puntos_anclaje)
        x = puntos_anclaje[:, 0]
        y = puntos_anclaje[:, 1]
        spline = CubicSpline(x, y)
        x_interpolado = np.linspace(min(x), max(x), self.segmentos)
        y_interpolado = spline(x_interpolado)

        for xi, yi in zip(x_interpolado, y_interpolado):
            if 0 <= int(xi) < self.ancho and 0 <= int(yi) < self.alto:
                self.lienzo[int(yi), int(xi)] = (255, 0, 0)

        puntos_interpolados = list(zip(x_interpolado, y_interpolado))
        return puntos_interpolados

    def mostrar_lienzo(self):
        cv2.imshow("Lienzo con Interpolación", self.lienzo)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def guardar_lienzo(self, ruta_salida):
        cv2.imwrite(ruta_salida, self.lienzo)
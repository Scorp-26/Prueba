from abc import ABC, abstractmethod
from datetime import datetime
import random


class Lectura:
    def __init__(self, valor, fecha=None):
        self.valor = round(valor, 2)
        self.fecha = fecha or datetime.now()


class Sensor(ABC):
    def __init__(self, variable, unidad, linea_base, limite_min=None, limite_max=None, punto="cercano"):
        self.variable = variable
        self.unidad = unidad
        self.linea_base = linea_base
        self.limite_min = limite_min
        self.limite_max = limite_max
        self.punto = punto
        self.lecturas = []

    def simular_lectura(self, factor):
        """factor: 0 = selva virgen, 1 = mina activa"""
        if self.limite_max:
            media = self.linea_base + (self.limite_max - self.linea_base) * factor
        elif self.limite_min:
            media = self.linea_base - (self.linea_base - self.limite_min) * factor
        else:
            media = self.linea_base
        valor = random.gauss(media, abs(media) * 0.05 + 0.1)
        return Lectura(valor)

    def agregar(self, lectura):
        self.lecturas.append(lectura)

    @abstractmethod
    def evaluar(self, lectura):
        pass

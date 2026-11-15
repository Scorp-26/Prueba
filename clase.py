from abc import ABC, abstractmethod
from datetime import datetime
import random


class Lectura:
    def __init__(self, valor, fecha=None):
        self.valor = round(valor, 2)
        self.fecha = fecha or datetime.now()


class Sensor(ABC):
    def __init__(self, variable, unidad, linea_base,
                 limite_min=None, limite_max=None, punto="cercano"):
        self.variable = variable
        self.unidad = unidad
        self.linea_base = linea_base
        self.limite_min = limite_min
        self.limite_max = limite_max
        self.punto = punto
        self.lecturas = []

    def simular_lectura(self, factor):
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


class SensorAgua(Sensor):
    def evaluar(self, lectura):
        if self.limite_max and lectura.valor > self.limite_max:
            return f"ALERTA: {self.variable} = {lectura.valor} {self.unidad}"
        if self.limite_min and lectura.valor < self.limite_min:
            return f"ALERTA: {self.variable} = {lectura.valor} {self.unidad}"
        return None


class SensorAire(Sensor):
    def evaluar(self, lectura):
        if lectura.valor > self.limite_max:
            return f"ALERTA: {self.variable} = {lectura.valor} {self.unidad}"
        return None


class SensorSuelo(Sensor):
    def evaluar(self, lectura):
        if self.limite_min and lectura.valor < self.limite_min:
            return f"ALERTA: {self.variable} = {lectura.valor} {self.unidad}"
        if self.limite_max and lectura.valor > self.limite_max:
            return f"ALERTA: {self.variable} = {lectura.valor} {self.unidad}"
        return None


class SensorRuido(Sensor):
    def evaluar(self, lectura):
        if lectura.valor > self.limite_max:
            return f"ALERTA: {self.variable} = {lectura.valor} {self.unidad}"
        return None


class SensorClima(Sensor):
    def evaluar(self, lectura):
        if self.limite_max and lectura.valor > self.limite_max:
            return f"ALERTA: {self.variable} = {lectura.valor} {self.unidad}"
        if self.limite_min and lectura.valor < self.limite_min:
            return f"ALERTA: {self.variable} = {lectura.valor} {self.unidad}"
        return None


class PuntoMonitoreo:
    def __init__(self, nombre, tipo):
        self.nombre = nombre
        self.tipo = tipo
        self.sensores = []

    def agregar_sensor(self, sensor):
        sensor.punto = self.tipo
        self.sensores.append(sensor)


class Mina:
    def __init__(self, nombre):
        self.nombre = nombre
        self.puntos = []

    def agregar_punto(self, punto):
        self.puntos.append(punto)

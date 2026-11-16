from abc import ABC, abstractmethod
from datetime import datetime
import random


class Lectura:
    def __init__(self, valor, fecha=None):
        self.valor = round(valor, 2)
        self.fecha = fecha or datetime.now()


class Sensor(ABC):
    def __init__(self, variable, unidad, linea_base, limite_min=None, limite_max=None):
        self.variable = variable
        self.unidad = unidad
        self.linea_base = linea_base
        self.limite_min = limite_min
        self.limite_max = limite_max
        self.punto = None
        self.lecturas = []

    def simular_lectura(self, factor):
        """factor: 0 = selva virgen, 1 = mina activa"""
        if self.limite_max is not None:
            media = self.linea_base + (self.limite_max - self.linea_base) * factor
        elif self.limite_min is not None:
            media = self.linea_base - (self.linea_base - self.limite_min) * factor
        else:
            media = self.linea_base
        valor = random.gauss(media, abs(media) * 0.05 + 0.1)
        return Lectura(valor)

    def agregar(self, lectura):
        self.lecturas.append(lectura)

    def revisar_limites(self, lectura):
        v = lectura.valor
        if self.limite_max is not None and v > self.limite_max:
            return f"{self.variable} = {v} {self.unidad} (máx {self.limite_max})"
        if self.limite_min is not None and v < self.limite_min:
            return f"{self.variable} = {v} {self.unidad} (mín {self.limite_min})"
        return None

    @abstractmethod
    def evaluar(self, lectura):
        pass


class SensorAgua(Sensor):
    def evaluar(self, lectura):
        problema = self.revisar_limites(lectura)
        return f"ALERTA AGUA: {problema}" if problema else None


class SensorAire(Sensor):
    def evaluar(self, lectura):
        problema = self.revisar_limites(lectura)
        return f"ALERTA AIRE: {problema}" if problema else None


class SensorSuelo(Sensor):
    def evaluar(self, lectura):
        problema = self.revisar_limites(lectura)
        return f"ALERTA SUELO: {problema}" if problema else None


class SensorRuido(Sensor):
    def evaluar(self, lectura):
        problema = self.revisar_limites(lectura)
        return f"ALERTA RUIDO: {problema}" if problema else None


class SensorClima(Sensor):
    def evaluar(self, lectura):
        problema = self.revisar_limites(lectura)
        return f"ALERTA CLIMA: {problema}" if problema else None


class PuntoMonitoreo:
    def __init__(self, nombre, tipo):
        self.nombre = nombre
        self.tipo = tipo          # "cercano" o "lejano"
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

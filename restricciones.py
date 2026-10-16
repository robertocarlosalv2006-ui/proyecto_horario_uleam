from abc import ABC, abstractmethod

class TipoAula:
    NORMAL = "Normal"
    LABORATORIO = "Laboratorio"

class Materia:
    def __init__(self, codigo: str, nombre: str, horas_semanales: int, requiere_laboratorio: bool = False):
        self.codigo = codigo
        self.nombre = nombre
        self.horas_semanales = horas_semanales
        self.requiere_laboratorio = requiere_laboratorio

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

class Docente:
    def __init__(self, id_docente: str, nombre: str):
        self.id = id_docente
        self.nombre = nombre
        self.materias_habilitadas = set()
        # Ejemplo de disponibilidad: {(dia, bloque)}
        self.disponibilidad = set() 

    def puede_dictar(self, materia: Materia) -> bool:
        return materia in self.materias_habilitadas

    def esta_disponible(self, dia: int, bloque: int) -> bool:
        return (dia, bloque) in self.disponibilidad

    def __str__(self):
        return self.nombre

class Aula:
    def __init__(self, id_aula: str, nombre: str, capacidad: int, tipo: str = TipoAula.NORMAL):
        self.id = id_aula
        self.nombre = nombre
        self.capacidad = capacidad
        self.tipo = tipo

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"

class Nivel:
    def __init__(self, numero: int, num_estudiantes: int):
        self.numero = numero
        self.materias = []
        self.num_estudiantes = num_estudiantes

    def __str__(self):
        return f"Nivel {self.numero}"

class Sesion:
    def __init__(self, materia: Materia, nivel: Nivel, duracion: int):
        self.materia = materia
        self.nivel = nivel
        self.duracion = duracion

    def __str__(self):
        return f"Sesión de {self.materia.nombre} (Nivel {self.nivel.numero})"

class Asignacion:
    def __init__(self, sesion: Sesion, docente: Docente, aula: Aula, dia: int, bloque_inicio: int):
        self.sesion = sesion
        self.docente = docente
        self.aula = aula
        self.dia = dia
        self.bloque_inicio = bloque_inicio

    def __str__(self):
        return f"[{self.sesion}] con {self.docente} en {self.aula} - Día {self.dia}, Bloque {self.bloque_inicio}"

class Horario:
    def __init__(self):
        self.asignaciones = []

    def agregar_asignacion(self, asig: Asignacion):
        self.asignaciones.append(asig)

    def quitar_asignacion(self, asig: Asignacion):
        if asig in self.asignaciones:
            self.asignaciones.remove(asig)

    def docente_libre(self, docente: Docente, dia: int, bloque: int) -> bool:
        for a in self.asignaciones:
            if a.docente == docente and a.dia == dia and a.bloque_inicio == bloque:
                return False
        return True

    def aula_libre(self, aula: Aula, dia: int, bloque: int) -> bool:
        for a in self.asignaciones:
            if a.aula == aula and a.dia == dia and a.bloque_inicio == bloque:
                return False
        return True

# --- SISTEMA DE RESTRICCIONES ---

class RestriccionDura(ABC):
    @abstractmethod
    def cumple(self, horario: Horario, docente: Docente, aula: Aula, nivel: Nivel, dia: int, bloque: int) -> bool:
        pass

class AulaCompatible(RestriccionDura):
    def cumple(self, horario: Horario, docente: Docente, aula: Aula, nivel: Nivel, dia: int, bloque: int) -> bool:
        # Verificar capacidad y si requiere laboratorio
        if nivel.num_estudiantes > aula.capacidad:
            return False
        return True

class NivelSinChoque(RestriccionDura):
    def cumple(self, horario: Horario, docente: Docente, aula: Aula, nivel: Nivel, dia: int, bloque: int) -> bool:
        for a in horario.asignaciones:
            if a.sesion.nivel == nivel and a.dia == dia and a.bloque_inicio == bloque:
                return False
        return True

class DocenteDisponible(RestriccionDura):
    def cumple(self, horario: Horario, docente: Docente, aula: Aula, nivel: Nivel, dia: int, bloque: int) -> bool:
        return docente.esta_disponible(dia, bloque)

class DocenteSinChoque(RestriccionDura):
    def cumple(self, horario: Horario, docente: Docente, aula: Aula, nivel: Nivel, dia: int, bloque: int) -> bool:
        return horario.docente_libre(docente, dia, bloque)

class AulaSinChoque(RestriccionDura):
    def cumple(self, horario: Horario, docente: Docente, aula: Aula, nivel: Nivel, dia: int, bloque: int) -> bool:
        return horario.aula_libre(aula, dia, bloque)

class RestriccionBlanda(ABC):
    @abstractmethod
    def costo(self, horario: Horario) -> int:
        pass

class MinimizarHuecos(RestriccionBlanda):
    def costo(self, horario: Horario) -> int:
        # Lógica para penalizar espacios libres entre clases
        return 0

class BalanceCargaDocente(RestriccionBlanda):
    def costo(self, horario: Horario) -> int:
        # Lógica para equilibrar la cantidad de horas asignadas por día a los docentes
        return 0
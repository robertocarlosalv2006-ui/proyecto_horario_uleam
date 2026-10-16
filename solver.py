class GeneradorHorarios:
    def __init__(self, niveles: list, docentes: list, aulas: list, max_pasos: int = 400000):
        self.niveles = niveles
        self.docentes = docentes
        self.aulas = aulas
        self.max_pasos = max_pasos
        self.restricciones_duras = [
            AulaCompatible(),
            NivelSinChoque(),
            DocenteDisponible(),
            DocenteSinChoque(),
            AulaSinChoque()
        ]
        self.restricciones_blandas = [
            MinimizarHuecos(),
            BalanceCargaDocente()
        ]

    def generar(self) -> Horario:
        sesiones = self._construir_sesiones()
        horario_inicial = Horario()
        
        exito = self._backtracking(sesiones, 0, horario_inicial)
        if exito:
            self._optimizar(horario_inicial)
            return horario_inicial
        else:
            raise Exception("No se encontró una solución válida para el horario.")

    def _construir_sesiones(self) -> list:
        sesiones = []
        for nivel in self.niveles:
            for materia in nivel.materias:
                # Se asume una sesión por cada hora semanal requerida
                for _ in range(materia.horas_semanales):
                    sesiones.append(Sesion(materia, nivel, duracion=1))
        return sesiones

    def _backtracking(self, sesiones: list, indice: int, horario: Horario) -> bool:
        if indice >= len(sesiones):
            return True  # Todas las sesiones fueron asignadas con éxito

        sesion_actual = sesiones[indice]
        
        # Espacio de búsqueda simulado para días (ej. 1 a 5) y bloques (ej. 1 a 6)
        for dia in range(1, 6):
            for bloque in range(1, 7):
                for docente in self.docentes:
                    if not docente.puede_dictar(sesion_actual.materia):
                        continue
                    for aula in self.aulas:
                        # Validar restricciones duras
                        valido = True
                        for rd in self.restricciones_duras:
                            if not rd.cumple(horario, docente, aula, sesion_actual.nivel, dia, bloque):
                                valido = False
                                break
                        
                        if valido:
                            asignacion = Asignacion(sesion_actual, docente, aula, dia, bloque)
                            horario.agregar_asignacion(asignacion)
                            
                            if self._backtracking(sesiones, indice + 1, horario):
                                return True
                            
                            # Backtrack (deshacer asignación)
                            horario.quitar_asignacion(asignacion)
                            
        return False

    def _optimizar(self, horario: Horario):
        # Aquí se aplicarían algoritmos de mejora iterativa (como Búsqueda Local o Simulated Annealing)
        # utilizando las restricciones blandas.
        pass
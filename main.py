if __name__ == "__main__":
    # 1. Crear datos de prueba
    materia_prog = Materia("INF-01", "Programación I", horas_semanales=2)
    
    nivel1 = Nivel(1, num_estudiantes=30)
    nivel1.materias.append(materia_prog)
    
    docente_juan = Docente("D01", "Juan Pérez")
    docente_juan.materias_habilitadas.add(materia_prog)
    # Habilitar disponibilidad de ejemplo (Día 1, Bloques 1 y 2)
    docente_juan.disponibilidad.update({(1, 1), (1, 2)})
    
    aula_101 = Aula("A01", "Laboratorio 1", capacidad=40, tipo=TipoAula.LABORATORIO)
    
    # 2. Inicializar el generador
    solver = GeneradorHorarios(niveles=[nivel1], docentes=[docente_juan], aulas=[aula_101])
    
    try:
        horario_generado = solver.generar()
        print("¡Horario generado exitosamente!")
        for asig in horario_generado.asignaciones:
            print(asig)
    except Exception as e:
        print(f"Error: {e}")
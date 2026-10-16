from restricciones import Materia, Nivel, Docente, Aula, TipoAula
from solver import GeneradorHorarios

print("Bienvenido al Generador Horarios ULEAM.")
print("Por favor, elige tu rol:")
print("1. Estudiante")
print("2. Docente")

while True:
    try:
        rol_opcion = int(input("Ingresa el número correspondiente a tu rol: "))
        if rol_opcion == 1:
            rol = "Estudiante"
            break
        elif rol_opcion == 2:
            rol = "Docente"
            break
        else:
            print("Opción no válida. Elija 1 o 2.")
    except ValueError:
        print("Entrada inválida. Por favor, ingresa un número.")

# Contadores globales para IDs automáticos
contador_materia = 0
contador_nivel = 0
contador_docente = 0
contador_aula = 0

def anadir():
    global contador_materia, contador_nivel, contador_docente, contador_aula
    lista_horario = []
    
    print("\n--- Registro de Datos para Generación ---")
    nombre_materia = input("Ingrese el nombre de la materia: ")
    try:
        hora_materia = int(input("Ingrese las horas semanales de la materia: "))
        num_estudiantes = int(input("Ingrese el número de estudiantes que cursan la materia: "))
    except ValueError:
        print("Error: Debe ingresar un valor numérico válido.")
        return

    contador_materia += 1
    materia = Materia(f"M{contador_materia}", nombre_materia, hora_materia)

    contador_nivel += 1
    nivel = Nivel(contador_nivel, num_estudiantes)
    nivel.materias.append(materia)

    nombre_docente = input("Ingrese el nombre del docente: ")
    contador_docente += 1
    docente = Docente(f"D{contador_docente}", nombre_docente)
    docente.materias_habilitadas.add(materia)
    # Disponibilidad de ejemplo (Día 1 a 5, Bloques 1 a 6)
    docente.disponibilidad.update({(1, 1), (1, 2), (2, 1), (2, 2)})

    nombre_aula = input("Ingrese el nombre del aula: ")
    try:
        capacidad_aula = int(input("Ingrese la capacidad del aula: "))
    except ValueError:
        print("Error: Capacidad inválida.")
        return

    print("Seleccione el tipo de aula:")
    print("1. Normal")
    print("2. Laboratorio")
    
    while True:
        try:
            opcion_tipo = int(input("Ingrese el número según el tipo de aula: "))
            if opcion_tipo == 1:
                tipo_aula = TipoAula.NORMAL
                break
            elif opcion_tipo == 2:
                tipo_aula = TipoAula.LABORATORIO
                break
            else:
                print("Opción no válida. Intente de nuevo.")
        except ValueError:
            print("Entrada inválida. Ingrese un número.")

    contador_aula += 1
    aula = Aula(f"A{contador_aula}", nombre_aula, capacidad_aula, tipo=tipo_aula)

    # Inicializar el generador y ejecutar
    try:
        solver = GeneradorHorarios(niveles=[nivel], docentes=[docente], aulas=[aula])
        horario_generado = solver.generar()
        print("\n¡Horario generado exitosamente!\n")
        for asig in horario_generado.asignaciones:
            print(asig)
    except Exception as e:
        print(f"Error al generar el horario: {e}")

# Menú principal según rol
if rol == "Estudiante":
    while True:
        print("\n--- Menú Estudiante ---")
        print("1. Planificar horario de clases")
        print("2. Salir")
        try:
            opcion = int(input("Ingresa el número de la opción deseada: "))
            if opcion == 1:
                anadir()
            elif opcion == 2:
                print("Saliendo del programa...")
                break
            else:
                print("Opción no válida.")
        except ValueError:
            print("Entrada inválida.")

elif rol == "Docente":
    while True:
        print("\n--- Menú Docente ---")
        print("1. Ver horario de clases (Simulación)")
        print("2. Salir")
        try:
            opcion = int(input("Ingresa el número de la opción deseada: "))
            if opcion == 1:
                print("Mostrando horario asignado al docente...")
            elif opcion == 2:
                print("Saliendo del programa...")
                break
            else:
                print("Opción no válida.")
        except ValueError:
            print("Entrada inválida.")


""" if __name__ == "__main__":
    # 1. Crear datos de prueba
    materia_prog = Materia("INF-01", "Programación I", horas_semanales=2)
    
    nivel1 = Nivel(1, num_estudiantes=30)
    nivel1.materias.append(materia_prog)
    
    docente_juan = Docente("D01", "Juan Pérez")
    docente_juan.materias_habilitadas.add(materia_prog)
    docente_juan.disponibilidad.update({(1, 1), (1, 2)})
    
    aula_101 = Aula("A01", "Laboratorio 1", capacidad=40, tipo=TipoAula.LABORATORIO)
    
    # 2. Inicializar el generador
    solver = GeneradorHorarios(niveles=[nivel1], docentes=[docente_juan], aulas=[aula_101])
    
    try:
        horario_generado = solver.generar()
        print("¡Horario generado exitosamente!\n")
        for asig in horario_generado.asignaciones:
            print(asig)
    except Exception as e:
        print(f"Error: {e}") """
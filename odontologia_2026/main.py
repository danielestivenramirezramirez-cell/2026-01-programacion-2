import os

class Paciente:
    def __init__(self, cedula, nombre, telefono, tipo_cliente, tipo_atencion, cantidad, prioridad, fecha):
        self.cedula = cedula
        self.nombre = nombre
        self.telefono = telefono
        self.tipo_cliente = tipo_cliente
        self.tipo_atencion = tipo_atencion
        self.cantidad = int(cantidad)
        self.prioridad = prioridad
        self.fecha = fecha
        self.valor_total = self.calcular_pago()

    def calcular_pago(self):
        precios_cita = {"Particular": 80000, "EPS": 5000, "Prepagada": 30000}
        precios_atencion = {
            "Particular": {"Limpieza": 60000, "Calzas": 80000, "Extracción": 100000, "Diagnóstico": 50000},
            "EPS": {"Limpieza": 0, "Calzas": 40000, "Extracción": 40000, "Diagnóstico": 0},
            "Prepagada": {"Limpieza": 0, "Calzas": 10000, "Extracción": 10000, "Diagnóstico": 0}
        }
        v_cita = precios_cita[self.tipo_cliente]
        v_atencion = precios_atencion[self.tipo_cliente][self.tipo_atencion]
        return v_cita + (v_atencion * self.cantidad)

def menu():
    lista_pacientes = []
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== SISTEMA CONSULTORIO ODONTOLÓGICO ===")
        print("1. Registrar nuevo paciente")
        print("2. Ver reporte general (Ordenado por valor)")
        print("3. Buscar por cédula")
        print("4. Salir")
        
        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "4":
            print("Saliendo del sistema...")
            break

        elif opcion == "1":
            # 1. CÉDULA: Solo números y no vacío
            while True:
                cedula = input("Cédula: ").strip()
                if cedula.isdigit() and len(cedula) > 0:
                    break
                print("❌ Error: La cédula debe ser solo números.")

            # 2. NOMBRE: Solo letras/espacios y no vacío
            while True:
                nombre = input("Nombre completo: ").strip()
                if nombre.replace(" ", "").isalpha() and len(nombre) > 0:
                    break
                print("❌ Error: El nombre solo debe contener letras.")

            # 3. TELÉFONO: Solo números y no vacío
            while True:
                telefono = input("Teléfono: ").strip()
                if telefono.isdigit() and len(telefono) > 0:
                    break
                print("❌ Error: El teléfono debe ser numérico.")
            
            # 4. TIPO CLIENTE: Validación contra diccionario
            while True:
                print("\nTipos: Particular, EPS, Prepagada")
                t_cliente = input("Tipo Cliente: ").strip().capitalize()
                if t_cliente == "Eps": t_cliente = "EPS"
                if t_cliente in ["Particular", "EPS", "Prepagada"]:
                    break
                print("❌ Error: Opción no válida.")

            # 5. ATENCIÓN: Validación contra diccionario
            while True:
                print("\nAtenciones: Limpieza, Calzas, Extracción, Diagnóstico")
                t_atencion = input("Tipo Atención: ").strip().capitalize()
                if t_atencion == "Extraccion": t_atencion = "Extracción"
                if t_atencion in ["Limpieza", "Calzas", "Extracción", "Diagnóstico"]:
                    break
                print("❌ Error: Atención no reconocida.")

            # 6. CANTIDAD: Regla de negocio (1 para limpieza/diagnóstico)
            if t_atencion in ["Limpieza", "Diagnóstico"]:
                cantidad = 1
            else:
                while True:
                    cant_in = input(f"Cantidad de {t_atencion}: ")
                    if cant_in.isdigit() and int(cant_in) > 0:
                        cantidad = int(cant_in)
                        break
                    print("❌ Error: Ingrese un número mayor a 0.")

            prioridad = input("Prioridad (Normal/Urgente): ").strip().capitalize()
            fecha = input("Fecha cita (DD/MM/AAAA): ")

            # Guardar en el arreglo en memoria
            nuevo_p = Paciente(cedula, nombre, telefono, t_cliente, t_atencion, cantidad, prioridad, fecha)
            lista_pacientes.append(nuevo_p)
            print(f"\n✅ ¡Paciente {nombre} registrado!")
            input("Presione Enter para continuar...")

        elif opcion == "2":
            if not lista_pacientes:
                print("\nNo hay pacientes registrados.")
            else:
                # Ordenamiento de mayor a menor por valor total
                lista_pacientes.sort(key=lambda x: x.valor_total, reverse=True)
                print("\n" + "="*75)
                print(f"{'NOMBRE':<20} | {'TIPO':<10} | {'ATENCIÓN':<12} | {'TOTAL':<10}")
                print("-" * 75)
                for p in lista_pacientes:
                    print(f"{p.nombre[:20]:<20} | {p.tipo_cliente:<10} | {p.tipo_atencion:<12} | ${p.valor_total:,}")
                print("-" * 75)
                # Cálculos finales solicitados
                ingresos = sum(p.valor_total for p in lista_pacientes)
                extrac = sum(1 for p in lista_pacientes if p.tipo_atencion == "Extracción")
                print(f"Total Clientes: {len(lista_pacientes)} | Ingresos: ${ingresos:,} | Extracciones: {extrac}")
            input("\nPresione Enter para volver...")

        elif opcion == "3":
            busqueda = input("\nCédula a buscar: ")
            encontrado = next((p for p in lista_pacientes if p.cedula == busqueda), None)
            if encontrado:
                print(f"\n✅ Encontrado: {encontrado.nombre} | Total: ${encontrado.valor_total:,}")
            else:
                print("\n❌ Cédula no registrada.")
            input("\nPresione Enter para volver...")

if __name__ == "__main__":
    menu()

import os
from datetime import datetime

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
            "EPS":         {"Limpieza": 0,     "Calzas": 40000, "Extracción": 40000,  "Diagnóstico": 0},
            "Prepagada":   {"Limpieza": 0,     "Calzas": 10000, "Extracción": 10000,  "Diagnóstico": 0}
        }
        v_cita = precios_cita.get(self.tipo_cliente, 0)
        v_atencion = precios_atencion.get(self.tipo_cliente, {}).get(self.tipo_atencion, 0)
        return v_cita + (v_atencion * self.cantidad)

def menu():
    lista_pacientes = []
    
    while True:
        # SE ELIMINÓ os.system('cls') PARA MANTENER EL TEXTO EN CONSOLA
        print("\n" + "="*40)
        print("=== SISTEMA CONSULTORIO ODONTOLÓGICO ===")
        print("1. Registrar nuevo paciente")
        print("2. Ver reporte general (Detallado)")
        print("3. Buscar por cédula")
        print("4. Salir")
        print("="*40)
        
        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "4":
            print("\nSaliendo del sistema...")
            break

        elif opcion == "1":
            continuar = "s"
            while continuar.lower() == "s":
                print("\n--- NUEVO REGISTRO ---")
                # 1. CÉDULA
                while True:
                    cedula = input("Cédula (Máximo 10 dígitos): ").strip()
                    if cedula.isdigit() and 1 <= len(cedula) <= 10: break
                    print("❌ Error: Use entre 1 y 10 números.")

                # 2. NOMBRE
                while True:
                    nombre = input("Nombre completo: ").strip()
                    if nombre.replace(" ", "").isalpha() and len(nombre) > 0: break
                    print("❌ Error: Solo letras.")

                # 3. TELÉFONO
                while True:
                    telefono = input("Teléfono (10 dígitos): ").strip()
                    if telefono.isdigit() and len(telefono) == 10: break
                    print("❌ Error: Debe tener 10 números.")
                
                # 4. TIPO CLIENTE
                while True:
                    t_cliente = input("Tipo (Particular/EPS/Prepagada): ").strip().capitalize()
                    if t_cliente.upper() == "EPS": t_cliente = "EPS"
                    if t_cliente in ["Particular", "EPS", "Prepagada"]: break
                    print("❌ Error: Opción no válida.")

                # 5. ATENCIÓN
                while True:
                    t_atencion = input("Atención (Limpieza/Calzas/Extracción/Diagnóstico): ").strip().capitalize()
                    if "extrac" in t_atencion.lower(): t_atencion = "Extracción"
                    if t_atencion in ["Limpieza", "Calzas", "Extracción", "Diagnóstico"]: break
                    print("❌ Error: Atención no reconocida.")

                # 6. CANTIDAD
                cantidad = 1
                if t_atencion not in ["Limpieza", "Diagnóstico"]:
                    while True:
                        cant_in = input(f"Cantidad de {t_atencion}: ")
                        if cant_in.isdigit() and int(cant_in) > 0:
                            cantidad = int(cant_in); break
                        print("❌ Error: Ingrese un número mayor a 0.")

                # 7. PRIORIDAD
                while True:
                    pri_in = input("Prioridad (Normal/Urgente): ").strip().capitalize()
                    if pri_in in ["Normal", "Urgente"]: break
                    print("❌ Error: Elija 'Normal' o 'Urgente'.")
                
                # 8. FECHA
                while True:
                    fecha_in = input("Fecha (DD/MM/AAAA): ").strip()
                    try:
                        f_dt = datetime.strptime(fecha_in, "%d/%m/%Y")
                        if f_dt.year >= 2026: fecha = fecha_in; break
                        else: print("❌ Error: Año 2026 o posterior.")
                    except ValueError: print("❌ Error: Formato DD/MM/AAAA.")

                nuevo_p = Paciente(cedula, nombre, telefono, t_cliente, t_atencion, cantidad, pri_in, fecha)
                lista_pacientes.append(nuevo_p)
                print(f"\n✅ ¡Paciente {nombre} registrado!")
                
                # PREGUNTA SI QUIERE SEGUIR REGISTRANDO
                continuar = input("\n¿Desea registrar otro paciente ahora mismo? (s/n): ").strip().lower()

        elif opcion == "2":
            if not lista_pacientes:
                print("\n⚠️ No hay pacientes en el historial.")
            else:
                lista_pacientes.sort(key=lambda x: x.valor_total, reverse=True)
                print("\n" + "="*110)
                print(f"{'NOMBRE':<18} | {'CÉDULA':<11} | {'ATENCIÓN':<12} | {'PRIORIDAD':<10} | {'FECHA':<10} | {'TOTAL':<10}")
                print("-" * 110)
                for p in lista_pacientes:
                    pri_visual = f"*{p.prioridad}*" if p.prioridad == "Urgente" else p.prioridad
                    print(f"{p.nombre[:18]:<18} | {p.cedula:<11} | {p.tipo_atencion:<12} | {pri_visual:<10} | {p.fecha:<10} | ${p.valor_total:,}")
                print("-" * 110)
                ingresos = sum(p.valor_total for p in lista_pacientes)
                print(f"Total Pacientes: {len(lista_pacientes)} | Ingresos: ${ingresos:,}")

        elif opcion == "3":
            busqueda = input("\nCédula a buscar: ").strip()
            encontrado = next((p for p in lista_pacientes if p.cedula == busqueda), None)
            if encontrado:
                print(f"\n✅ Encontrado: {encontrado.nombre} | Total: ${encontrado.valor_total:,}")
            else:
                print("\n❌ Cédula no registrada.")

if __name__ == "__main__":
    menu()
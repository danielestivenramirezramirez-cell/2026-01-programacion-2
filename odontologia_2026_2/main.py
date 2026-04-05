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
        self.prioridad = prioridad.capitalize()
        self.fecha_str = fecha
        # Convertimos fecha a objeto datetime para poder ordenar
        try:
            self.fecha_obj = datetime.strptime(fecha, "%d/%m/%Y")
        except ValueError:
            self.fecha_obj = datetime.now()
        
        self.valor_total = self.calcular_pago()

    def calcular_pago(self):
        precios_cita = {"Particular": 80000, "EPS": 5000, "Prepagada": 30000}
        precios_atencion = {
            "Particular": {"Limpieza": 60000, "Calzas": 80000, "Extracción": 100000, "Diagnóstico": 50000},
            "EPS": {"Limpieza": 0, "Calzas": 40000, "Extracción": 40000, "Diagnóstico": 0},
            "Prepagada": {"Limpieza": 0, "Calzas": 10000, "Extracción": 10000, "Diagnóstico": 0}
        }
        # Validación de seguridad para evitar errores de clave
        v_cita = precios_cita.get(self.tipo_cliente, 80000)
        v_atencion = precios_atencion.get(self.tipo_cliente, {}).get(self.tipo_atencion, 0)
        return v_cita + (v_atencion * self.cantidad)

class GestionOdontologica:
    def __init__(self):
        self.lista_general = []
        self.cola_atencion = [] # Agenda diaria (Cola - FIFO)
        self.pila_urgencias = [] # Contingencia (Pila - LIFO)

    def registrar_paciente(self, paciente):
        self.lista_general.append(paciente)
        self.cola_atencion.append(paciente)
        print(f"\n✅ Paciente {paciente.nombre} registrado en la agenda diaria.")

    def generar_pila_contingencia(self):
        # Filtramos: Solo Extracciones + Urgente
        # Usamos .lower() y reemplazamos tildes para que la búsqueda sea flexible
        filtrados = [p for p in self.lista_general 
                     if ("extrac" in p.tipo_atencion.lower()) and (p.prioridad == "Urgente")]
        
        # Ordenar por fecha (de lejana a cercana para que el pop() saque la más próxima)
        filtrados.sort(key=lambda x: x.fecha_obj, reverse=True)
        self.pila_urgencias = filtrados

    def mostrar_pila_informe(self):
        print("\n" + "="*45)
        print("📋 PILA DE CONTINGENCIA (EXTRACCIONES URGENTES)")
        print("Orden: Primero los de fecha más cercana")
        print("="*45)
        if not self.pila_urgencias:
            print("No hay pacientes urgentes para extracción.")
        else:
            temp_pila = list(self.pila_urgencias)
            while temp_pila:
                p = temp_pila.pop() 
                print(f"FECHA: {p.fecha_str} | ID: {p.cedula} | {p.nombre}")
        print("="*45)

    def atender_cola_diaria(self):
        print("\n" + "="*45)
        print("🕒 ATENCIÓN DE AGENDA (COLA POR LLEGADA)")
        print("="*45)
        if not self.cola_atencion:
            print("No hay pacientes en la cola de hoy.")
        else:
            paciente = self.cola_atencion.pop(0) 
            print(f"ATENDIENDO A: {paciente.nombre}")
            print(f"PROCEDIMIENTO: {paciente.tipo_atencion}")
            print(f"Quedan {len(self.cola_atencion)} pacientes en espera.")
        print("="*45)

def menu():
    gestion = GestionOdontologica()
    
    while True:
        print("\n=== SISTEMA CONSULTORIO ODONTOLÓGICO PRO ===")
        print("1. Registrar nuevo paciente (Añadir a Agenda)")
        print("2. Generar Plan de Contingencia (Pila de Urgencias)")
        print("3. Atender siguiente paciente (Cola Diaria)")
        print("4. Ver reporte general ordenado por valor")
        print("5. Salir")
        
        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "5":
            print("Saliendo del sistema...")
            break

        elif opcion == "1":
            cedula = input("Cédula: ").strip()
            nombre = input("Nombre completo: ").strip()
            telefono = input("Teléfono: ").strip()
            
            print("\nTipos: Particular, EPS, Prepagada")
            t_cliente = input("Tipo Cliente: ").strip().capitalize()
            if t_cliente == "Eps": t_cliente = "EPS"

            print("\nAtenciones: Limpieza, Calzas, Extracción, Diagnóstico")
            t_atencion = input("Tipo Atención: ").strip().capitalize()
            if "extrac" in t_atencion.lower(): t_atencion = "Extracción"

            cantidad = 1
            if t_atencion not in ["Limpieza", "Diagnóstico"]:
                cantidad_in = input(f"Cantidad de {t_atencion}: ")
                cantidad = int(cantidad_in) if cantidad_in.isdigit() else 1

            prioridad = input("Prioridad (Normal/Urgente): ").strip().capitalize()

            # --- NUEVA VALIDACIÓN DE FECHA ---
            while True:
                fecha_in = input("Fecha cita (DD/MM/AAAA): ").strip()
                try:
                    # strptime valida automáticamente que el día y mes sean reales (1-12)
                    f_valida = datetime.strptime(fecha_in, "%d/%m/%Y")
                    
                    # Validamos que el año sea 2026 en adelante
                    if f_valida.year >= 2026:
                        fecha = fecha_in
                        break
                    else:
                        print("❌ Error: El año debe ser 2026 o posterior.")
                except ValueError:
                    print("❌ Error: Formato incorrecto o fecha inexistente. Use DD/MM/AAAA (Ej: 15/08/2026)")

            p = Paciente(cedula, nombre, telefono, t_cliente, t_atencion, cantidad, prioridad, fecha)
            gestion.registrar_paciente(p)

        elif opcion == "2":
            gestion.generar_pila_contingencia()
            gestion.mostrar_pila_informe()

        elif opcion == "3":
            gestion.atender_cola_diaria()

        elif opcion == "4":
            if not gestion.lista_general:
                print("\nNo hay pacientes.")
            else:
                reporte = sorted(gestion.lista_general, key=lambda x: x.valor_total, reverse=True)
                print(f"\n{'NOMBRE':<20} | {'ATENCIÓN':<12} | {'TOTAL':<10}")
                print("-" * 45)
                for p in reporte:
                    print(f"{p.nombre[:20]:<20} | {p.tipo_atencion:<12} | ${p.valor_total:,}")

if __name__ == "__main__":
    menu()
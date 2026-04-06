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
        
        try:
            self.fecha_obj = datetime.strptime(fecha, "%d/%m/%Y")
        except ValueError:
            self.fecha_obj = datetime.now()
        
        self.valor_total = self.calcular_pago()

    def calcular_pago(self):
        # Precios basados en la tabla proporcionada
        precios_cita = {"Particular": 80000, "EPS": 5000, "Prepagada": 30000}
        precios_atencion = {
            "Particular": {"Limpieza": 60000, "Calzas": 80000, "Extracción": 100000, "Diagnóstico": 50000},
            "EPS":        {"Limpieza": 0,     "Calzas": 40000, "Extracción": 40000,  "Diagnóstico": 0},
            "Prepagada":  {"Limpieza": 0,     "Calzas": 10000, "Extracción": 10000,  "Diagnóstico": 0}
        }
        
        v_cita = precios_cita.get(self.tipo_cliente, 80000)
        v_atencion = precios_atencion.get(self.tipo_cliente, {}).get(self.tipo_atencion, 0)
        return v_cita + (v_atencion * self.cantidad)

class GestionOdontologica:
    def __init__(self):
        self.lista_general = []
        self.cola_atencion = [] 
        self.pila_urgencias = [] 

    def registrar_paciente(self, paciente):
        self.lista_general.append(paciente)
        self.cola_atencion.append(paciente)
        print(f"\n✅ Paciente {paciente.nombre} registrado en la agenda diaria.")

    def generar_pila_contingencia(self):
        filtrados = [p for p in self.lista_general 
                     if ("extrac" in p.tipo_atencion.lower()) and (p.prioridad == "Urgente")]
        filtrados.sort(key=lambda x: x.fecha_obj, reverse=True)
        self.pila_urgencias = filtrados

    def mostrar_pila_informe(self):
        print("\n" + "="*55)
        print("📋 PILA DE CONTINGENCIA (EXTRACCIONES URGENTES)")
        print("="*55)
        if not self.pila_urgencias:
            print("No hay pacientes urgentes para extracción.")
        else:
            temp_pila = list(self.pila_urgencias)
            while temp_pila:
                p = temp_pila.pop() 
                print(f"FECHA: {p.fecha_str} | ID: {p.cedula:<10} | {p.nombre}")
        print("="*55)

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
        print("4. Ver reporte detallado (Con Cédula)")
        print("5. Salir")
        
        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "5":
            print("Saliendo del sistema...")
            break

        elif opcion == "1":
            while True:
                cedula = input("Cédula (1-10 dígitos): ").strip()
                if cedula.isdigit() and 1 <= len(cedula) <= 10:
                    break
                print("❌ Error: La cédula debe ser numérica y máximo 10 dígitos.")

            while True:
                nombre = input("Nombre completo: ").strip()
                if nombre.replace(" ", "").isalpha() and len(nombre) > 0:
                    break
                print("❌ Error: Use solo letras.")

            while True:
                telefono = input("Teléfono (10 dígitos): ").strip()
                if telefono.isdigit() and len(telefono) == 10:
                    break
                print("❌ Error: El teléfono debe tener exactamente 10 números.")
            
            print("\nTipos: Particular, EPS, Prepagada")
            t_cliente = input("Tipo Cliente: ").strip().capitalize()
            if t_cliente == "Eps": t_cliente = "EPS"

            print("\nAtenciones: Limpieza, Calzas, Extracción, Diagnóstico")
            t_atencion = input("Tipo Atención: ").strip().capitalize()
            if "extrac" in t_atencion.lower(): t_atencion = "Extracción"

            cantidad = 1
            if t_atencion not in ["Limpieza", "Diagnóstico"]:
                while True:
                    cantidad_in = input(f"Cantidad de {t_atencion}: ")
                    if cantidad_in.isdigit() and int(cantidad_in) > 0:
                        cantidad = int(cantidad_in)
                        break
                    print("❌ Error: Ingrese un número válido.")

            while True:
                prioridad = input("Prioridad (Normal/Urgente): ").strip().capitalize()
                if prioridad in ["Normal", "Urgente"]:
                    break
                print("❌ Error: Elija 'Normal' o 'Urgente'.")

            while True:
                fecha_in = input("Fecha cita (DD/MM/AAAA): ").strip()
                try:
                    f_valida = datetime.strptime(fecha_in, "%d/%m/%Y")
                    if f_valida.year >= 2026:
                        fecha = fecha_in
                        break
                    else:
                        print("❌ Error: Año 2026 o posterior.")
                except ValueError:
                    print("❌ Error: Formato DD/MM/AAAA.")

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
                
                # --- DISEÑO DE CUADRO COMPACTO Y ORDENADO ---
                print("\n" + "="*105)
                print(f"{'NOMBRE':<15} | {'CÉDULA':<11} | {'ATENCIÓN':<11} | {'PRIORIDAD':<10} | {'FECHA':<11} | {'TOTAL':<8}")
                print("-" * 105)
                for p in reporte:
                    # Si el nombre es muy largo, lo corta para que no desordene la fila
                    nom_f = p.nombre[:14]
                    pri_f = f"*{p.prioridad}*" if p.prioridad == "Urgente" else p.prioridad
                    val_f = f"${p.valor_total:,}"
                    
                    print(f"{nom_f:<15} | {p.cedula:<11} | {p.tipo_atencion[:11]:<11} | {pri_f:<10} | {p.fecha_str:<11} | {val_f:<8}")
                print("="*105)

if __name__ == "__main__":
    menu()
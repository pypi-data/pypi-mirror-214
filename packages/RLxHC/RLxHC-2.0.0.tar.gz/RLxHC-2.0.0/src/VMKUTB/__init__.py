import tkinter as tk
from tkinter import messagebox

class RLCCircuitSolver1:
    def __init__(self, resistencia, inductancia, capacitancia, frecuencia):
        self.resistencia = resistencia
        self.inductancia = inductancia
        self.capacitancia = capacitancia
        self.frecuencia = frecuencia

    def resolver(self):
        try:
            admitancia = self.calcular_admitancia()
            corriente = self.calcular_corriente_total(admitancia)
            voltajes = self.calcular_voltajes(corriente)
            potencias = self.calcular_potencias(corriente)
            factores_potencia = self.calcular_factores_potencia()

            self.mostrar_resultados(voltajes, corriente, potencias, factores_potencia)
        except ZeroDivisionError:
            messagebox.showerror('Error', 'La frecuencia debe ser mayor que cero.')

    def calcular_admitancia(self):
        frecuencia_angular = 2 * 3.14159 * self.frecuencia
        conductancia_capacitiva = frecuencia_angular * self.capacitancia
        conductancia_inductiva = 1 / (frecuencia_angular * self.inductancia)
        admitancia = complex(1 / self.resistencia, conductancia_capacitiva - conductancia_inductiva)
        return admitancia

    def calcular_corriente_total(self, admitancia):
        voltaje = 1  # Asigna el valor de voltaje deseado
        corriente = voltaje * admitancia
        return corriente

    def calcular_voltajes(self, corriente):
        voltaje_r = corriente * self.resistencia
        voltaje_l = corriente / (2 * 3.14159 * self.frecuencia * self.inductancia)
        voltaje_c = corriente / (2 * 3.14159 * self.frecuencia * self.capacitancia)
        return voltaje_r, voltaje_l, voltaje_c

    def calcular_potencias(self, corriente):
        potencia_r = (corriente ** 2) * self.resistencia
        potencia_l = (corriente ** 2) / (2 * 3.14159 * self.frecuencia * self.inductancia)
        potencia_c = (corriente ** 2) / (2 * 3.14159 * self.frecuencia * self.capacitancia)
        return potencia_r, potencia_l, potencia_c

    def calcular_factores_potencia(self):
        factor_potencia_r = 1.0
        factor_potencia_l = 0.0
        factor_potencia_c = 0.0
        return factor_potencia_r, factor_potencia_l, factor_potencia_c

    def mostrar_resultados(self, voltajes, corriente, potencias, factores_potencia):
        voltaje_r, voltaje_l, voltaje_c = voltajes
        potencia_r, potencia_l, potencia_c = potencias
        factor_potencia_r, factor_potencia_l, factor_potencia_c = factores_potencia

        messagebox.showinfo('Resultados', f'Voltaje R: {voltaje_r}\n'
                                          f'Voltaje L: {voltaje_l}\n'
                                          f'Voltaje C: {voltaje_c}\n'
                                          f'Corriente Total: {corriente}\n'
                                          f'Potencia R: {potencia_r}\n'
                                          f'Potencia L: {potencia_l}\n'
                                          f'Potencia C: {potencia_c}\n'
                                          f'Factor de Potencia R: {factor_potencia_r}\n'
                                          f'Factor de Potencia L: {factor_potencia_l}\n'
                                          f'Factor de Potencia C: {factor_potencia_c}')

class App1:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Circuito RLC en Paralelo')
        self.root.geometry('400x300')

        self.label_resistencia = tk.Label(self.root, text='Resistencia (ohmios):')
        self.label_resistencia.pack()

        self.entry_resistencia = tk.Entry(self.root)
        self.entry_resistencia.pack()

        self.label_inductancia = tk.Label(self.root, text='Inductancia (henrios):')
        self.label_inductancia.pack()

        self.entry_inductancia = tk.Entry(self.root)
        self.entry_inductancia.pack()

        self.label_capacitancia = tk.Label(self.root, text='Capacitancia (faradios):')
        self.label_capacitancia.pack()

        self.entry_capacitancia = tk.Entry(self.root)
        self.entry_capacitancia.pack()

        self.label_frecuencia = tk.Label(self.root, text='Frecuencia (Hz):')
        self.label_frecuencia.pack()

        self.entry_frecuencia = tk.Entry(self.root)
        self.entry_frecuencia.pack()

        self.button_calcular = tk.Button(self.root, text='Calcular', command=self.calcular)
        self.button_calcular.pack()

        self.root.mainloop()

    def calcular(self):
        resistencia = float(self.entry_resistencia.get())
        inductancia = float(self.entry_inductancia.get())
        capacitancia = float(self.entry_capacitancia.get())
        frecuencia = float(self.entry_frecuencia.get())

        solver = RLCCircuitSolver1(resistencia, inductancia, capacitancia, frecuencia)
        solver.resolver()

class RLCCircuitSolver2:
    def __init__(self, resistencia, inductancia, capacitancia, frecuencia):
        self.resistencia = resistencia
        self.inductancia = inductancia
        self.capacitancia = capacitancia
        self.frecuencia = frecuencia

    def resolver(self):
        try:
            impedancia = self.calcular_impedancia()
            corriente = self.calcular_corriente(impedancia)
            voltaje = self.calcular_voltaje(corriente)
            potencia = self.calcular_potencia(corriente)
            factor_potencia = self.calcular_factor_potencia()

            self.mostrar_resultados(voltaje, corriente, potencia, factor_potencia)
        except ZeroDivisionError:
            messagebox.showerror('Error', 'La frecuencia debe ser mayor que cero.')

    def calcular_impedancia(self):
        frecuencia_angular = 2 * 3.14159 * self.frecuencia
        reactancia_inductiva = frecuencia_angular * self.inductancia
        reactancia_capacitiva = 1 / (frecuencia_angular * self.capacitancia)
        impedancia = complex(self.resistencia, reactancia_inductiva - reactancia_capacitiva)
        return impedancia

    def calcular_corriente(self, impedancia):
        voltaje = 1  # Asigna el valor de voltaje deseado
        corriente = voltaje / impedancia
        return corriente

    def calcular_voltaje(self, corriente):
        voltaje = corriente * self.calcular_impedancia()
        return voltaje

    def calcular_potencia(self, corriente):
        potencia = (corriente ** 2) * self.resistencia
        return potencia

    def calcular_factor_potencia(self):
        factor_potencia = self.resistencia / abs(self.calcular_impedancia())
        return factor_potencia

    def mostrar_resultados(self, voltaje, corriente, potencia, factor_potencia):
        messagebox.showinfo('Resultados', f'Voltaje: {voltaje}\n'
                                          f'Corriente: {corriente}\n'
                                          f'Potencia: {potencia}\n'
                                          f'Factor de Potencia: {factor_potencia}')

class App2:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Circuito RLC')
        self.root.geometry('400x300')

        self.label_resistencia = tk.Label(self.root, text='Resistencia (ohmios):')
        self.label_resistencia.pack()

        self.entry_resistencia = tk.Entry(self.root)
        self.entry_resistencia.pack()

        self.label_inductancia = tk.Label(self.root, text='Inductancia (henrios):')
        self.label_inductancia.pack()

        self.entry_inductancia = tk.Entry(self.root)
        self.entry_inductancia.pack()

        self.label_capacitancia = tk.Label(self.root, text='Capacitancia (faradios):')
        self.label_capacitancia.pack()

        self.entry_capacitancia = tk.Entry(self.root)
        self.entry_capacitancia.pack()

        self.label_frecuencia = tk.Label(self.root, text='Frecuencia (Hz):')
        self.label_frecuencia.pack()

        self.entry_frecuencia = tk.Entry(self.root)
        self.entry_frecuencia.pack()

        self.button_calcular = tk.Button(self.root, text='Calcular', command=self.calcular)
        self.button_calcular.pack()

        self.root.mainloop()

    def calcular(self):
        resistencia = float(self.entry_resistencia.get())
        inductancia = float(self.entry_inductancia.get())
        capacitancia = float(self.entry_capacitancia.get())
        frecuencia = float(self.entry_frecuencia.get())

        solver = RLCCircuitSolver2(resistencia, inductancia, capacitancia, frecuencia)
        solver.resolver()


def menu():
    entrada = int(input('Ingrese 1 para: Si su circuito está en serie, 2: Si su circuito está en paralelo: '))
    if entrada == 2:
        a = App1()
    elif entrada == 1:
        a = App2()

menu()







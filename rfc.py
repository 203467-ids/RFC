import tkinter as tk
from tkinter import messagebox, ttk
import re
import graphviz

class ValidadorFaseGUI:
    def __init__(self, master):
        self.master = master
        master.title("Validador FASE")

        self.label = tk.Label(master, text="Ingrese la cadena:")
        self.label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        # Agregar menú desplegable para seleccionar la expresión regular
        self.opciones_expresion = ttk.Combobox(master, values=["FA*S*E", "F(ASE)*"])
        self.opciones_expresion.set("FA*S*E")  # Establecer el valor predeterminado
        self.opciones_expresion.pack()

        self.button = tk.Button(master, text="Validar", command=self.validar)
        self.button.pack()

    def validar(self):
        cadena = self.entry.get()
        expresion_elegida = self.opciones_expresion.get()

        if expresion_elegida == "FA*S*E":
            if self.validar_cadena_original(cadena):
                messagebox.showinfo("Resultado", f"{cadena} es una cadena válida FASE.")
                self.generar_automata(cadena)
            else:
                messagebox.showwarning("Resultado", f"{cadena} no es una cadena válida FASE.")
        elif expresion_elegida == "F(ASE)*":
            if self.validar_cadena_nueva_condicion(cadena):
                messagebox.showinfo("Resultado", f"{cadena} es una cadena válida FASE con la nueva condición.")
                self.generar_automata(cadena)
            else:
                messagebox.showwarning("Resultado", f"{cadena} no es una cadena válida FASE con la nueva condición.")

    def validar_cadena_original(self, cadena):
        # Definir la expresión regular para FASE (original)
        patron_fase_original =re.compile(r'^(?i)F(?:A+(?:S+(?:E+)?)?)?$') #re.compile(r'^(f|fa|fas|fase)$', re.IGNORECASE)   
        return bool(patron_fase_original.match(cadena))

    def validar_cadena_nueva_condicion(self, cadena):
        # Definir la expresión regular para FASE con la nueva condición
        patron_fase_nueva = re.compile(r'^F[aAeEsS]{3}$', re.IGNORECASE)
        return bool(patron_fase_nueva.match(cadena))
    
    def generar_automata(self, cadena):
        # Generar el automata usando Graphviz con orientación horizontal
        dot = graphviz.Digraph(comment='Automata FASE', graph_attr={'rankdir':'LR'})

        # Crear nodo inicial
        dot.node('S', 'S', shape='circle', color='blue', style='bold')

        # Crear nodos y enlaces para cada caracter en la cadena
        for i, char in enumerate(cadena):
            dot.node(str(i), "Q"+str(i), shape='circle')
            if i == 0:
                dot.edge('S', str(i), label=char)
            else:
                dot.edge(str(i-1), str(i), label=char)

        # Marcar el último nodo como aceptador
        dot.node('A', 'A', shape='doublecircle', color='red', style='bold')
        dot.edge(str(len(cadena) - 1), 'A', label='', style='dashed')

        dot.render(f'automata_{cadena}', format='png', cleanup=True)

        messagebox.showinfo("Automata Generado", f"Se ha generado el automata para la cadena {cadena}.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ValidadorFaseGUI(root)
    root.mainloop()

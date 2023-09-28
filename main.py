# Importar las bibliotecas necesarias
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import lexer
from grammar import parser
from semantic import symbol_table, semantic_errors

# Función para analizar el texto ingresado por el usuario
def parse_input(input_str):
    lexer.lexer.input(input_str)
    parser.parse(input_str)
    return symbol_table, semantic_errors

# Función que se ejecuta al hacer clic en el botón 'Run'
def on_run_button_click():
    # Obtener el texto ingresado por el usuario
    user_input = input_text.get('1.0', tk.END).strip()
    parsed_symbol_table, errors = parse_input(user_input)
    
    # Eliminar entradas anteriores de Treeview
    for row in tree.get_children():
        tree.delete(row)

    # Poblar Treeview con datos de la tabla de símbolos
    for identifier, info in parsed_symbol_table.items():
        tree.insert('', tk.END, values=(identifier, info['type'], info['is_const']))
    
    # Mostrar errores en el área de texto
    errors_text.delete('1.0', tk.END)
    errors_text.insert(tk.END, "\n".join(errors))
    del errors[:]

# Configurar la ventana principal
root = tk.Tk()
root.title('My Language Parser')

# Crear un marco para los widgets
frame = ttk.Frame(root, padding='10')
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Área de texto para la entrada del usuario
input_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=40, height=10)
input_text.grid(row=0, column=0, sticky=(tk.W, tk.E))

# Botón 'Run' para iniciar el análisis
run_button = ttk.Button(frame, text='Run', command=on_run_button_click)
run_button.grid(row=1, column=0, sticky=tk.W)

# Treeview para mostrar la tabla de símbolos
tree = ttk.Treeview(frame, columns=('Identifier', 'Type', 'Is Const'), show='headings')
tree.heading('Identifier', text='Identifier')
tree.heading('Type', text='Type')
tree.heading('Is Const', text='Is Const')
tree.grid(row=2, column=0, sticky=(tk.W, tk.E))

# Área de texto para mostrar errores
errors_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=40, height=5)
errors_text.grid(row=3, column=0, sticky=(tk.W, tk.E))

# Iniciar el bucle principal de Tkinter
root.mainloop()

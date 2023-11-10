# Importar bibliotecas necesarias
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import lexer
from grammar import parser
from semantic import symbol_table, semantic_errors
from intermediate import intermediate_code, instruction_metrics, quad_list, triplet_list
from assembly import generate_assembly, assembly_code

# Función para analizar la entrada del usuario
def parse_input(input_str):
    lexer.lexer.input(input_str)
    parser.parse(input_str)
    return symbol_table, semantic_errors

# Función ejecutada cuando se hace clic en el botón "Run"
def on_run_button_click():
    # Obtener la entrada del usuario
    user_input = input_text.get('1.0', tk.END).strip()
    parsed_symbol_table, errors = parse_input(user_input)

    # Limpiar el árbol existente
    for row in tree.get_children():
        tree.delete(row)

    # Poblar la tabla de símbolos en la interfaz de usuario
    for identifier, info in parsed_symbol_table.items():
        tree.insert('', tk.END, values=(identifier, info['type'], info['is_const']))

    # Limpiar y actualizar el área de texto de errores
    errors_text.delete('1.0', tk.END)
    errors_text.insert(tk.END, "\n".join(errors))
    del errors[:]

    # Limpiar y actualizar el área de texto de código intermedio y métricas
    intermediate_text.delete('1.0', tk.END)
    
    # Añadir un encabezado para las métricas
    intermediate_text.insert(tk.END, "---- METRICS ----\n")
    
    # Añadir métricas de instrucción
    for metric in instruction_metrics:
        intermediate_text.insert(
            tk.END,
            f">> Instruction: {metric['instruction']}\n   - Time: {metric['time']} sec\n   - Memory: {metric['memory']} bytes\n"
        )
        
    # Limpiar las métricas de instrucción
    instruction_metrics.clear()
    
    # Separar las instrucciones de las métricas
    intermediate_text.insert(tk.END, "---- INSTRUCTIONS ----\n")

    # Añadir código intermedio
    for line in intermediate_code:
        intermediate_text.insert(tk.END, f">> {line}\n")
        
    # Limpiar el código intermedio
    intermediate_code.clear()
    
    intermediate_text.insert(tk.END, "---- QUADS ----\n")

    for quad in quad_list:
        intermediate_text.insert(tk.END, f"{quad}\n")
        generate_assembly(quad)
  
    # Añadir el código de ensamblador a la interfaz de usuario
    intermediate_text.insert(tk.END, "---- ASSEMBLY CODE ----\n")
    for line in assembly_code:
        intermediate_text.insert(tk.END, f"{line}\n")

    quad_list.clear()
    triplet_list.clear()
    assembly_code.clear()

# Configuración de la ventana principal
root = tk.Tk()
root.title('My Language Parser')
root.state('zoomed')

# Permitir al usuario salir del modo pantalla completa con la tecla Escape
def toggle_fullscreen(event=None):
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))

def end_fullscreen(event=None):
    root.attributes("-fullscreen", False)

root.bind("<F11>", toggle_fullscreen)
root.bind("<Escape>", end_fullscreen)

# Configuración del marco principal para expandirse con la ventana
main_frame = ttk.Frame(root, padding='10')
main_frame.grid(sticky='nsew')
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Configurar los widgets de entrada y botones en el marco superior
input_label = ttk.Label(main_frame, text='Input Code:', font=('Arial', 12))
input_label.grid(row=0, column=0, sticky='nw', padx=5, pady=5)
input_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=10)
input_text.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
run_button = ttk.Button(main_frame, text='Run', command=on_run_button_click)
run_button.grid(row=2, column=0, sticky='nw', padx=5, pady=5)

# Configurar los widgets de la tabla de símbolos y errores en el marco izquierdo
symbol_label = ttk.Label(main_frame, text='Symbol Table:', font=('Arial', 12))
symbol_label.grid(row=3, column=0, sticky='nw', padx=5, pady=5)
tree = ttk.Treeview(main_frame, columns=('Identifier', 'Type', 'Is Const'), show='headings')
tree.heading('Identifier', text='Identifier')
tree.heading('Type', text='Type')
tree.heading('Is Const', text='Is Const')
tree.grid(row=4, column=0, sticky='nsew', padx=5, pady=5)

errors_label = ttk.Label(main_frame, text='Errors:', font=('Arial', 12))
errors_label.grid(row=5, column=0, sticky='nw', padx=5, pady=5)
errors_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=5)
errors_text.grid(row=6, column=0, sticky='nsew', padx=5, pady=5)

# Configurar el área de texto de código intermedio y métricas para ocupar el espacio restante
metrics_label = ttk.Label(main_frame, text='Intermediate Code and Metrics:', font=('Arial', 12))
metrics_label.grid(row=0, column=1, sticky='nw', padx=5, pady=5)
intermediate_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, font=('Courier', 10))
intermediate_text.grid(row=1, column=1, rowspan=6, sticky='nsew', padx=5, pady=5)
main_frame.grid_columnconfigure(1, weight=2)  # Asigna un mayor peso a esta columna
# Iniciar el bucle de eventos de la interfaz de usuario
root.mainloop()
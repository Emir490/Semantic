import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import lexer
from grammar import parser
from semantic import symbol_table, semantic_errors

def parse_input(input_str):
    lexer.lexer.input(input_str)
    parser.parse(input_str)
    return symbol_table, semantic_errors

def on_run_button_click():
    user_input = input_text.get('1.0', tk.END).strip()
    parsed_symbol_table, errors = parse_input(user_input)
    
    # Clear previous entries from the Treeview
    for row in tree.get_children():
        tree.delete(row)

    # Populate Treeview with symbol table data
    for identifier, info in parsed_symbol_table.items():
        tree.insert('', tk.END, values=(identifier, info['type'], info['is_const']))
    
    errors_text.delete('1.0', tk.END)
    errors_text.insert(tk.END, "\n".join(errors))
    del errors[:]

root = tk.Tk()
root.title('My Language Parser')

frame = ttk.Frame(root, padding='10')
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

input_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=40, height=10)
input_text.grid(row=0, column=0, sticky=(tk.W, tk.E))

run_button = ttk.Button(frame, text='Run', command=on_run_button_click)
run_button.grid(row=1, column=0, sticky=tk.W)

# Treeview to show symbol table
tree = ttk.Treeview(frame, columns=('Identifier', 'Type', 'Is Const'), show='headings')
tree.heading('Identifier', text='Identifier')
tree.heading('Type', text='Type')
tree.heading('Is Const', text='Is Const')
tree.grid(row=2, column=0, sticky=(tk.W, tk.E))

errors_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=40, height=5)
errors_text.grid(row=3, column=0, sticky=(tk.W, tk.E))

root.mainloop()
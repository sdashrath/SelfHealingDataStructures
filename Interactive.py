import tkinter as tk
from tkinter import ttk, messagebox
import logging

# Logging setup
logging.basicConfig(filename='selfheal.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# LinkedList class for demo (replace with actual logic)
class LinkedList:
    def __init__(self):
        self.data = []
        self.backup = []

    def insert(self, value):
        self.data.insert(0, value)
        self.backup = self.data[:]
        logging.info(f"Inserted {value} into LinkedList")
        return f"Inserted {value}"

    def display(self):
        return " -> ".join(str(v) for v in self.data)

    def corrupt(self):
        if self.data:
            self.data[0] = None
            logging.warning("Corrupted first node in LinkedList")
            return "Corrupted first node"
        return "No data to corrupt"

    def break_pointer(self):
        self.data = []
        logging.warning("Pointer broken in LinkedList")
        return "Pointer broken"

    def heal(self):
        self.data = self.backup[:]
        logging.info("Healed LinkedList using backup")
        return "Healed from backup"

class BinaryTree(LinkedList):
    pass

class HashTable(LinkedList):
    pass

data_structures = {
    'Linked List': LinkedList(),
    'Binary Tree': BinaryTree(),
    'Hash Table': HashTable(),
}

def on_insert():
    value = entry.get()
    if not value:
        messagebox.showwarning("Input Error", "Please enter a value to insert.")
        return

    ds_name = structure_var.get()
    if ds_name not in data_structures:
        messagebox.showwarning("Selection Error", "Please select a valid data structure.")
        return

    ds = data_structures[ds_name]
    result = ds.insert(value)
    output.insert(tk.END, result + '\n')
    logging.info(result)
    
    entry.delete(0, tk.END)  # Clear input
    entry.focus_set()        # Refocus on input

def display_structure():
    ds_name = structure_var.get()
    if ds_name not in data_structures:
        messagebox.showwarning("Selection Error", "Please select a valid data structure.")
        return
    ds = data_structures[ds_name]
    result = ds.display()
    output.insert(tk.END, "Structure: " + result + '\n')
    logging.info(f"Displayed {ds_name}")

def simulate_corruption():
    ds = get_selected_structure()
    if ds:
        result = ds.corrupt()
        output.insert(tk.END, result + '\n')

def simulate_break():
    ds = get_selected_structure()
    if ds:
        result = ds.break_pointer()
        output.insert(tk.END, result + '\n')

def heal_structure():
    ds = get_selected_structure()
    if ds:
        result = ds.heal()
        output.insert(tk.END, result + '\n')

def get_selected_structure():
    ds_name = structure_var.get()
    if ds_name not in data_structures:
        messagebox.showwarning("Selection Error", "Please select a valid data structure.")
        return None
    return data_structures[ds_name]

# GUI setup
root = tk.Tk()
root.title("Self-Healing Data Structures")

# Configure grid to be resizable
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(5, weight=1)  # Output row

# Dropdown
tk.Label(root, text="Select Data Structure:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
structure_var = tk.StringVar()
structure_menu = ttk.Combobox(root, textvariable=structure_var)
structure_menu['values'] = ('Linked List', 'Binary Tree', 'Hash Table')
structure_menu.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

# Input entry
tk.Label(root, text="Enter Value:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry = tk.Entry(root)
entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
entry.bind("<Return>", lambda event: on_insert())  # Bind Enter key to insert

# Action buttons
tk.Button(root, text="Insert", command=on_insert).grid(row=2, column=0, padx=10, pady=5, sticky="ew")
tk.Button(root, text="Display", command=display_structure).grid(row=2, column=1, padx=10, pady=5, sticky="ew")
tk.Button(root, text="Simulate Data Corruption", command=simulate_corruption).grid(row=3, column=0, padx=10, pady=5, sticky="ew")
tk.Button(root, text="Simulate Pointer Break", command=simulate_break).grid(row=3, column=1, padx=10, pady=5, sticky="ew")
tk.Button(root, text="Self-Heal Using Backup", command=heal_structure).grid(row=4, column=0, padx=10, pady=5, sticky="ew")
tk.Button(root, text="Exit", command=root.quit).grid(row=4, column=1, padx=10, pady=5, sticky="ew")

# Output Text Area
output = tk.Text(root, height=12, wrap=tk.WORD)
output.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

root.mainloop()

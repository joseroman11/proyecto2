import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from tkcalendar import DateEntry
import csv
from datetime import datetime


# Estructuras principales: Nodo, Árbol AVL, Cola de Prioridad, y Sistema de Gestión de Turnos
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, root, key, value):
        if not root:
            return Node(key, value)

        if key < root.key:
            root.left = self.insert(root.left, key, value)
        elif key > root.key:
            root.right = self.insert(root.right, key, value)
        else:
            return root

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)

        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)

        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def get_height(self, root):
        if not root:
            return 0
        return root.height

    def get_balance(self, root):
        if not root:
            return 0
        return self.get_height(root.left) - self.get_height(root.right)

    def inorder(self, root):
        if root:
            yield from self.inorder(root.left)
            yield root
            yield from self.inorder(root.right)


class PriorityQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        self.queue.append(item)
        self.queue.sort(key=lambda x: x["urgency"], reverse=True)

    def dequeue(self):
        return self.queue.pop(0) if self.queue else None

    def get_all(self):
        return self.queue[:]


class TurnManagementSystem:
    def __init__(self):
        self.avl_tree = AVLTree()
        self.priority_queue = PriorityQueue()
        self.turns = {}

    def register_patient(self, patient_id, patient_name, urgency, appointment_date):
        patient = {"id": patient_id, "name": patient_name, "urgency": urgency}
        self.avl_tree.root = self.avl_tree.insert(self.avl_tree.root, appointment_date, patient)
        self.priority_queue.enqueue(patient)
        self.turns[appointment_date] = patient

    def delete_patient(self, appointment_date):
        del self.turns[appointment_date]

    def get_patients(self):
        return self.turns.items()


# Clase para la aplicación gráfica
class TurnManagementApp:
    def __init__(self, root):
        self.system = TurnManagementSystem()
        self.root = root
        self.root.title("Sistema de Gestión de Turnos Médicos")
        self.create_widgets()

    def create_widgets(self):
        self.root.geometry("900x700")
        self.root.resizable(False, False)

        # Título principal
        tk.Label(self.root, text="Sistema de Gestión de Turnos Médicos", font=("Arial", 18, "bold")).pack(pady=10)

        # Pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        self.tab_register = ttk.Frame(self.notebook)
        self.tab_view = ttk.Frame(self.notebook)
        self.tab_settings = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_register, text="Registrar Turnos")
        self.notebook.add(self.tab_view, text="Ver Turnos")
        self.notebook.add(self.tab_settings, text="Configuraciones")

        self.create_register_tab()
        self.create_view_tab()
        self.create_settings_tab()

    def create_register_tab(self):
        frame = tk.Frame(self.tab_register, padx=10, pady=10)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="ID del Paciente:").grid(row=0, column=0, pady=5)
        self.patient_id_entry = tk.Entry(frame)
        self.patient_id_entry.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Nombre del Paciente:").grid(row=1, column=0, pady=5)
        self.patient_name_entry = tk.Entry(frame)
        self.patient_name_entry.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="Urgencia (1-10):").grid(row=2, column=0, pady=5)
        self.urgency_entry = tk.Entry(frame)
        self.urgency_entry.grid(row=2, column=1, pady=5)

        tk.Label(frame, text="Fecha del Turno:").grid(row=3, column=0, pady=5)
        self.appointment_date_entry = DateEntry(frame, width=12, background="darkblue", foreground="white", borderwidth=2)
        self.appointment_date_entry.grid(row=3, column=1, pady=5)

        tk.Button(frame, text="Registrar Turno", command=self.register_patient).grid(row=4, column=0, columnspan=2, pady=20)

    def create_view_tab(self):
        frame = tk.Frame(self.tab_view, padx=10, pady=10)
        frame.pack(fill="both", expand=True)

        # Tabla para ver turnos
        self.turn_table = ttk.Treeview(frame, columns=("ID", "Nombre", "Urgencia", "Fecha"), show="headings")
        self.turn_table.heading("ID", text="ID")
        self.turn_table.heading("Nombre", text="Nombre")
        self.turn_table.heading("Urgencia", text="Urgencia")
        self.turn_table.heading("Fecha", text="Fecha")
        self.turn_table.pack(fill="both", expand=True, pady=10)

        btn_frame = tk.Frame(frame)
        btn_frame.pack(fill="x", pady=10)
        tk.Button(btn_frame, text="Actualizar", command=self.update_turn_list).pack(side="left", padx=5)

    def create_settings_tab(self):
        frame = tk.Frame(self.tab_settings, padx=10, pady=10)
        frame.pack(fill="both", expand=True)

        tk.Button(frame, text="Exportar Turnos a CSV", command=self.export_to_csv).pack(pady=10)

    def register_patient(self):
        try:
            patient_id = int(self.patient_id_entry.get())
            patient_name = self.patient_name_entry.get()
            urgency = int(self.urgency_entry.get())
            appointment_date = self.appointment_date_entry.get_date()

            # Verifica si la fecha es válida
            datetime.strptime(str(appointment_date), "%Y-%m-%d")
            self.system.register_patient(patient_id, patient_name, urgency, appointment_date)
            messagebox.showinfo("Éxito", "Turno registrado correctamente.")
            self.update_turn_list()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_turn_list(self):
        for row in self.turn_table.get_children():
            self.turn_table.delete(row)
        for date, patient in self.system.get_patients():
            self.turn_table.insert("", "end", values=(patient["id"], patient["name"], patient["urgency"], date))

    def export_to_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Nombre", "Urgencia", "Fecha"])
                for date, patient in self.system.get_patients():
                    writer.writerow([patient["id"], patient["name"], patient["urgency"], date])
            messagebox.showinfo("Éxito", "Turnos exportados correctamente.")


# Inicializar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = TurnManagementApp(root)
    root.mainloop()

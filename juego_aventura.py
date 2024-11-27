import tkinter as tk
from tkinter import messagebox, Menu, ttk
import json
import pygame

class JuegoAventura:
    def __init__(self, master):
        self.master = master
        master.title("Juego de Aventura Interactivo")
        master.geometry("600x400")

        # Inicializar Pygame
        pygame.mixer.init()
        self.musica_fondo = pygame.mixer.Sound("musica_fondo.wav")  # Cambia el nombre del archivo a tu música de fondo
        self.sonido_correcto = pygame.mixer.Sound("correcto.wav")
        self.sonido_incorrecto = pygame.mixer.Sound("incorrecto.wav")
        self.sonido_fin_tiempo = pygame.mixer.Sound("fin_tiempo.wav")
        self.sonido_cuenta_regresiva = pygame.mixer.Sound("cuenta_regresiva.wav")
        self.musica_fondo.play(-1)

        # Variables del juego
        self.acertijos = [
            {"tipo": "numerico", "pregunta": "Adivina un número del 1 al 15", "respuesta": 2, "tiempo": 90},
            {"tipo": "texto", "pregunta": "Soy blanco como la nieve y delicado como el algodón, pero si me tocas, te derretiré. ¿Qué soy?", "respuesta": "El hielo", "tiempo": 90},
            {"tipo": "secuencia", "pregunta": "Si me tienes, quieres compartirlo; si me compartes, ya no lo tienes. ¿Qué es?", "respuesta": "Un secreto", "tiempo": 90},
            {"tipo": "dependencia", "pregunta": "Si un tren tiene 8 vagones y cada vagón tiene 4 ruedas, ¿cuántas ruedas tiene el tren en total?", "respuesta": "32 ruedas", "tiempo": 90},
            {"tipo": "logico", "pregunta": "Si hoy es lunes, ¿qué día será en 2 días?", "respuesta": "miércoles", "tiempo": 90},
        ]
        self.indice_acertijo = 0
        self.tiempo_restante = 0
        self.temporizador_activo = False
        self.usuario = ""

        # Configurar interfaz de usuario
        self.configurar_menu()
        self.pedir_nombre_usuario()

    def configurar_menu(self):
        """Configura el menú de la aplicación."""
        self.menu_bar = Menu(self.master)
        self.master.config(menu=self.menu_bar)

        archivo_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Archivo", menu=archivo_menu)
        archivo_menu.add_command(label="Guardar Progreso", command=self.guardar_progreso)
        archivo_menu.add_command(label="Cargar Progreso", command=self.cargar_progreso)
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Salir", command=self.master.quit)

        tema_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Tema", menu=tema_menu)
        tema_menu.add_command(label="Cambiar a tema claro", command=self.cambiar_tema)

    def pedir_nombre_usuario(self):
        """Pide el nombre del usuario al inicio del juego."""
        def guardar_nombre():
            self.usuario = entry_nombre.get().strip()
            if self.usuario:
                self.mostrar_mensaje_bienvenida()
                ventana.destroy()
            else:
                messagebox.showerror("Error", "Por favor ingresa un nombre.")

        ventana = tk.Toplevel(self.master)
        ventana.title("Nombre del Usuario")
        ventana.geometry("300x150")

        label = ttk.Label(ventana, text="Ingresa tu nombre:")
        label.pack(pady=10)

        entry_nombre = ttk.Entry(ventana)
        entry_nombre.pack(pady=5)

        boton_guardar = ttk.Button(ventana, text="Guardar", command=guardar_nombre)
        boton_guardar.pack(pady=10)

        ventana.protocol("WM_DELETE_WINDOW", lambda: self.master.quit())

    def mostrar_mensaje_bienvenida(self):
        """Muestra un mensaje de bienvenida al usuario."""
        messagebox.showinfo("Bienvenido", f"¡Bienvenido, {self.usuario}! Comencemos el juego.")
        self.crear_widgets()

    def crear_widgets(self):
        """Crea los elementos de la interfaz para el juego."""
        self.frame_principal = ttk.Frame(self.master, padding=10)
        self.frame_principal.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

        # Etiqueta para la pregunta
        self.label_pregunta = ttk.Label(self.frame_principal, text="", font=("Arial", 14))
        self.label_pregunta.pack(pady=10)

        # Campo de entrada para la respuesta
        self.entry_respuesta = ttk.Entry(self.frame_principal, font=("Arial", 14))
        self.entry_respuesta.pack(pady=5)

        # Botones de interacción
        self.boton_verificar = ttk.Button(self.frame_principal, text="Verificar", command=self.verificar_respuesta)
        self.boton_verificar.pack(pady=10)

        self.boton_reiniciar = ttk.Button(self.frame_principal, text="Reiniciar Temporizador", command=self.reiniciar_temporizador)
        self.boton_reiniciar.pack(pady=10)

        # Barra de progreso
        self.label_progreso = ttk.Label(self.frame_principal, text="Progreso: 0 / {}".format(len(self.acertijos)), font=("Arial", 10))
        self.label_progreso.pack(pady=10)

        # Temporizador
        self.label_temporizador = ttk.Label(self.frame_principal, text="", font=("Arial", 12))
        self.label_temporizador.pack(pady=5)

        self.mostrar_acertijo()

    def iniciar_temporizador(self):
        """Inicia el temporizador."""
        self.tiempo_restante = self.acertijos[self.indice_acertijo]["tiempo"]
        self.temporizador_activo = True
        self.actualizar_temporizador()

    def actualizar_temporizador(self):
        """Actualiza el temporizador."""
        if self.temporizador_activo:
            if self.tiempo_restante > 0:
                self.label_temporizador.config(text=f"Tiempo restante: {self.tiempo_restante} segundos")
                self.tiempo_restante -= 1
                self.master.after(1000, self.actualizar_temporizador)  # Actualiza cada segundo
                if self.tiempo_restante <= 5:
                    self.reproducir_sonido("cuenta_regresiva")
            else:
                self.temporizador_activo = False
                self.reproducir_sonido("fin_tiempo")
                messagebox.showerror("Error", "Se acabó el tiempo para este acertijo.")
                self.reiniciar_acertijo()

    def mostrar_acertijo(self):
        """Muestra el acertijo actual y reinicia el temporizador."""
        if self.indice_acertijo < len(self.acertijos):
            acertijo = self.acertijos[self.indice_acertijo]
            self.label_pregunta.config(text=acertijo["pregunta"])
            self.entry_respuesta.delete(0, tk.END)
            self.iniciar_temporizador()
        else:
            self.mostrar_mensaje_felicidades()
            self.master.quit()  # Termina el juego

    def mostrar_mensaje_felicidades(self):
        """Muestra un mensaje de felicitaciones al completar todos los acertijos."""
        messagebox.showinfo("¡Felicidades!", "¡Completaste todos los acertijos!")

    def reiniciar_temporizador(self):
        """Reinicia el temporizador del acertijo actual."""
        if self.temporizador_activo:
            self.tiempo_restante = self.acertijos[self.indice_acertijo]["tiempo"]
            self.label_temporizador.config(text=f"Tiempo restante: {self.tiempo_restante} segundos")
            self.reproducir_sonido("cuenta_regresiva")  # Opcional: reproducir sonido al reiniciar

    def verificar_respuesta(self):
        """Verifica la respuesta ingresada."""
        respuesta_usuario = self.entry_respuesta.get().strip()
        acertijo = self.acertijos[self.indice_acertijo]

        if str(respuesta_usuario).lower() == str(acertijo["respuesta"]).lower():
            messagebox.showinfo("Correcto", "¡Respuesta correcta!")
            self.reproducir_sonido("correcto")
            self.indice_acertijo += 1
            self.mostrar_acertijo()
        else:
            messagebox.showerror("Incorrecto", "Respuesta incorrecta.")
            self.reproducir_sonido("incorrecto")

        self.label_progreso.config(text="Progreso: {} / {}".format(self.indice_acertijo, len(self.acertijos)))

    def reproducir_sonido(self, tipo):
        """Reproduce el sonido según el tipo indicado."""
        if tipo == "correcto":
            self.sonido_correcto.play()
        elif tipo == "incorrecto":
            self.sonido_incorrecto.play()
        elif tipo == "fin_tiempo":
            self.sonido_fin_tiempo.play()
        elif tipo == "cuenta_regresiva":
            self.sonido_cuenta_regresiva.play()

    def guardar_progreso(self):
        """Guarda el progreso del juego en un archivo JSON."""
        progreso = {"indice_acertijo": self.indice_acertijo}
        with open("progreso.json", "w") as archivo:
            json.dump(progreso, archivo)
        messagebox.showinfo("Guardar", "Progreso guardado.")

    def cargar_progreso(self):
        """Carga el progreso del juego desde un archivo JSON."""
        try:
            with open("progreso.json", "r") as archivo:
                progreso = json.load(archivo)
                self.indice_acertijo = progreso.get("indice_acertijo", 0)
                self.mostrar_acertijo()
                messagebox.showinfo("Cargar", "Progreso cargado.")
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró el archivo de progreso.")

    def cambiar_tema(self):
        """Cambiar el tema de la aplicación (Ejemplo básico)."""
        pass  # Implementa tu lógica para cambiar de tema aquí.

if __name__ == "__main__":
    root = tk.Tk()
    juego = JuegoAventura(root)
    root.mainloop()

from tkinter import*
from PIL import Image, ImageTk
from tkinter import messagebox
import sqlite3
import tkinter as tk
from service.resultados import progreso, resultados
from service.historial import historial
from service.rutina import ectomorfo,mesomorfo,endomorfo,alimentacion_ectomorfo,alimentacion_mesomorfo,alimentacion_endomorfo

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONO = os.path.join(BASE_DIR, "static", "icono.ico")


from service.resultados import RUTA_BD

conexion = sqlite3.connect(RUTA_BD)
cursor = conexion.cursor()

print("Base de datos utilizada:", RUTA_BD)



cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT UNIQUE NOT NULL,
    contrasena TEXT NOT NULL
)
""")

conexion.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS historial(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    porcentaje_grasa REAL,
    masa_grasa REAL,
    masa_libre REAL,
    masa_muscular REAL,
    tmb REAL,
    tdee REAL,
    FOREIGN KEY(id_usuario) REFERENCES usuarios(id)
)
""")

conexion.commit()


def seleccionar_tipo(event):

    x = event.x
    y = event.y

    if 0 <= x <= 130 and 0 <= y <= 220:
        ectomorfo()

    elif 130 < x <= 270 and 0 <= y <= 220:
        mesomorfo()

    elif 270 < x <= 400 and 0 <= y <= 220:
        endomorfo()



def validar(usuario, contrasena):


    global usuario_actual

    text_usuario = usuario.get()
    text_contrasena = contrasena.get()

    cursor.execute(
        "SELECT * FROM usuarios WHERE usuario=? AND contrasena=?",
        (text_usuario, text_contrasena)
    )

    resultado = cursor.fetchone()


    if resultado:

        usuario_actual = resultado[0]

        ventana_inicio= tk.Toplevel()
        ventana_inicio.title("BodyType Trainer")
        ventana_inicio.iconbitmap(ICONO)
        ventana_inicio.config(width=500, height=500)
        ventana_inicio.grab_set()

        FONDO_SELECCION = os.path.join(BASE_DIR, "static", "fondo_seleccion_cuerpo.jpeg")

        imagen = Image.open(FONDO_SELECCION)
        imagen = imagen.resize((500, 500), Image.Resampling.LANCZOS)


        foto_fondo_validar = ImageTk.PhotoImage(imagen)

        label_fondo = Label(ventana_inicio, image=foto_fondo_validar)
        label_fondo.image = foto_fondo_validar
        label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
        label_fondo.lower()


        frame_validar=Frame(

        ventana_inicio,
        bg="black",
        bd=2,
        relief="solid",
        padx=3,
        pady=3,
        width=400,
        height=400

        )

        frame_validar.place(relx=0.5, rely=0.5, anchor="center")


        titlo_seleccione=Label(frame_validar, text="Seleccione su tipo de cuerpo", font=("Arial", 17), bg="black", fg="white")
        titlo_seleccione.place(x=20, y=10)
        titulo_emoji=Label(frame_validar, text="💪", font=("Arial", 17), bg="black", fg="yellow")
        titulo_emoji.place(x=315, y=10)

        fondo2 = Canvas(frame_validar, width=400, height=260, bd=0, highlightthickness=0, bg="black")
        TIPOS_CUERPO = os.path.join(BASE_DIR, "static", "tipos_cuerpo.png")

        imagen_original2 = Image.open(TIPOS_CUERPO)
        imagen_redimensionada2 = imagen_original2.resize((400, 260))
        foto_ecto = ImageTk.PhotoImage(imagen_redimensionada2)
        fondo2.create_image(200, 120, image=foto_ecto)
        fondo2.image = foto_ecto  
        fondo2.place(x=-5, y=55)
        fondo2.bind("<Button-1>", seleccionar_tipo)


        boton_cerrar=Button(frame_validar, text="Cerrar sesion", font=("Arial", 13),  pady=5, bg="black",fg="#7AAC1D",activebackground="#222222",activeforeground="#A5D62A",highlightthickness=1,highlightbackground="#7AAC1D",bd=0,command=ventana_inicio.destroy)
        boton_cerrar.place(x=147, y=350)
        
        boton_historial=Button(frame_validar,text="Mi progreso",font=("Arial",13),pady=5, bg="black",fg="#7AAC1D",activebackground="#222222",activeforeground="#A5D62A",highlightthickness=1,highlightbackground="#7AAC1D",bd=0,command=lambda: historial(usuario_actual))
        boton_historial.place(x=220, y=308)



        boton_progreso=Button(frame_validar, text="Nueva evaluación", font=("Arial", 13),  pady=5, bg="black",fg="#7AAC1D",activebackground="#222222",activeforeground="#A5D62A",highlightthickness=1,highlightbackground="#7AAC1D",bd=0 ,command=lambda: progreso(usuario_actual, text_usuario))
        boton_progreso.place(x=70, y=308)

    else:

        messagebox.showinfo(message="El usuario y/o la contraseña son incorrectas", title="Error")
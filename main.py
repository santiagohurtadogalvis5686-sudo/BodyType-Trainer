
import os

def obtener_ruta_recurso(nombre_archivo):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta = os.path.join(base_dir, nombre_archivo)
    if not os.path.exists(ruta):
        ruta_static = os.path.join(base_dir, "static", nombre_archivo)
        if os.path.exists(ruta_static):
            return ruta_static
    return ruta

from service.validacion import validar

from tkinter import*

#manejo del tamaño de la imagen correctamente
from PIL import Image, ImageTk

#cajas de mensajes
from tkinter import messagebox 

#ventanas secundarias
import tkinter as tk
from tkinter import ttk

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Base de datos
RUTA_BD = os.path.join(BASE_DIR, "db", "bodytype.db")

# Icono
ICONO = os.path.join(BASE_DIR, "static", "icono.ico")

# Imágenes
FONDO_LOGIN = os.path.join(BASE_DIR, "static", "fondo_login.jpeg")
LOGO = os.path.join(BASE_DIR, "static", "login_mejor.png")


import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIR_BD = os.path.join(BASE_DIR, "db")
os.makedirs(DIR_BD, exist_ok=True)
RUTA_BD = os.path.join(DIR_BD, "bodytype.db")

conexion = sqlite3.connect(RUTA_BD)
cursor = conexion.cursor()

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



cuello_usuario = None
cintura_usuario = None
lbl_cintura=None
altura_usuario = None
peso_usuario = None
genero_usuario = None
edad_usuario=None
dias_entrenamiento_usuario=None
cadera_usuario = None
lbl_cadera = None
usuario_actual = None







def registrar_usuario():

    nombre = nombre_usuario.get()
    password = crear_contrasena.get()

    if nombre == "" or password == "":
        messagebox.showerror("Error", "Complete todos los campos")
        return

    try:

        cursor.execute(
            "INSERT INTO usuarios(usuario, contrasena) VALUES (?, ?)",
            (nombre, password)
        )

        conexion.commit()

        messagebox.showinfo(
            "Éxito",
            "Usuario registrado correctamente"
        )

    except sqlite3.IntegrityError:

        messagebox.showerror(
            "Error",
            "Ese usuario ya existe."
        )












def registro():

    global nombre_usuario
    global crear_contrasena

    ventana_registro=tk.Toplevel()
    ventana_registro.title("Registro")
<<<<<<< HEAD
    ventana_registro.iconbitmap(ICONO)
=======
    ventana_registro.iconbitmap(obtener_ruta_recurso("icono.ico"))
>>>>>>> dcf901ba8527e88828eac6e7c9bb10addb0d6902
    ventana_registro.geometry("500x500")
    ventana_registro.config(padx=0, pady=0)
    ventana_registro.grab_set()



    frame_registro=Frame(ventana_registro,  bg="#111111",
    bd=2,
    relief="solid",
    width=400,
    height=470,
    padx=0,
    pady=0
    )
    frame_registro.place(relx=0.5, rely=0.5, anchor="center", width=270, height=400)
    frame_registro.grid_propagate(False)
    frame_registro.grid_columnconfigure(0, weight=1)

<<<<<<< HEAD
    imagen = Image.open(FONDO_LOGIN)
=======
    imagen = Image.open(obtener_ruta_recurso("fondo_login.jpeg"))
>>>>>>> dcf901ba8527e88828eac6e7c9bb10addb0d6902
    imagen = imagen.resize((600, 600), Image.Resampling.LANCZOS)

    foto_fondo_validar = ImageTk.PhotoImage(imagen)


    label_fondo = Label(ventana_registro, image=foto_fondo_validar)
    label_fondo.image=foto_fondo_validar
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
    label_fondo.lower()
    

    titulo0=Label(frame_registro, text="BodyType Trainer", font=("Arial", 20), bg="#111111", fg="#7AAC05")
    titulo0.grid(column=0, row=0, sticky="ew")


    canvas_logo = Canvas(frame_registro, width=70, height=70,
                     bd=0, highlightthickness=0, bg="#111111")

<<<<<<< HEAD
    imagen_original = Image.open(LOGO)
=======
    imagen_original = Image.open(obtener_ruta_recurso("login_mejor.png"))
>>>>>>> dcf901ba8527e88828eac6e7c9bb10addb0d6902
    imagen_redimensionada = imagen_original.resize((70, 70))
    foto_logo = ImageTk.PhotoImage(imagen_redimensionada)

    canvas_logo.create_image(35, 35, image=foto_logo)
    canvas_logo.image = foto_logo   # ← ESTA LÍNEA ES LA IMPORTANTE

    canvas_logo.grid(column=0, row=1, pady=10)




    trainer=Label(frame_registro, text="Registrate", font=("Arial", 15), bg="#111111", fg="white", anchor="center", justify="center" )
    trainer.grid(column=0, row=2)


    espacio0=Label(frame_registro, text="", font=("Arial", 10), bg="#111111")
    espacio0.grid(column=0, row=3)


    titulo1=Label(frame_registro, text="Digite su nombre", font=("Arial", 10),  bg="#111111", fg="white")
    titulo1.grid(column=0, row=4)
    nombre_usuario=Entry(frame_registro, width=20, font=("Arial", 14), bg="#1E1E1E",fg="white", insertbackground="#7AAC05",relief="flat")
    nombre_usuario.grid(column=0, row=5, padx=5,pady=5)


    titulo2=Label(frame_registro, text="Crea una contraseña segura", font=("Arial", 10),  bg="#111111", fg="white")
    titulo2.grid(column=0, row=6)
    crear_contrasena=Entry(frame_registro, width=20, font=("Arial", 14), show="*", bg="#1E1E1E",fg="white", insertbackground="#7AAC05",relief="flat",)
    crear_contrasena.grid(column=0, row=7, padx=5,pady=5)

    espacio1=Label(frame_registro, text="", font=("Arial", 10), bg="#111111")
    espacio1.grid(column=0, row=8)


    boton_aceptar=Button(frame_registro, text="Aceptar", font=("Arial", 11), pady=5, bg="#111111",fg="#7AAC1D",activebackground="#222222",activeforeground="#A5D62A",highlightthickness=1,highlightbackground="#7AAC1D",bd=0 ,command=registrar_usuario)
    boton_aceptar.grid(column=0, row=9)
    

    boton_regresar=Button(frame_registro, text="Regresar",font=("Arial", 11), pady=5, bg="#111111",fg="#7AAC1D",activebackground="#222222",activeforeground="#A5D62A",highlightthickness=1,highlightbackground="#7AAC1D",bd=0, command=ventana_registro.destroy)
    boton_regresar.grid(column=0, row=10)










ventana_login= Tk()
ventana_login.title("Login")
<<<<<<< HEAD
ventana_login.iconbitmap(ICONO)
=======
ruta_icono = obtener_ruta_recurso("icono.ico")
if os.path.exists(ruta_icono):
    ventana_login.iconbitmap(ruta_icono)
>>>>>>> dcf901ba8527e88828eac6e7c9bb10addb0d6902
ventana_login.geometry("500x500")
ventana_login.config(padx=0, pady=0)
ventana_login.grid_columnconfigure(0, weight=1)

<<<<<<< HEAD
imagen = Image.open(FONDO_LOGIN)
=======
imagen = Image.open(obtener_ruta_recurso("fondo_login.jpeg"))
>>>>>>> dcf901ba8527e88828eac6e7c9bb10addb0d6902
imagen = imagen.resize((500, 500), Image.Resampling.LANCZOS)

foto_fondo = ImageTk.PhotoImage(imagen)

label_fondo = Label(ventana_login, image=foto_fondo)
label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

frame_login=Frame(

    ventana_login,
    bg="#111111",
    bd=2,
    relief="solid",
    padx=3,
    pady=3
)

frame_login.place(relx=0.5, rely=0.5, anchor="center")

label_fondo = Label(ventana_login, image=foto_fondo)
label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
label_fondo.lower()


frame_titulo = Frame(frame_login, bg="#111111")
frame_login.grid_columnconfigure(0, weight=1)
frame_login.grid_columnconfigure(1, weight=1)
frame_login.grid_columnconfigure(2, weight=1)
frame_titulo.grid(row=0, column=0, columnspan=3, pady=(0, 15))

titulo_inicio = Label(frame_titulo, text="Inicio", font=("Arial", 20, "bold"),
                      bg="#111111", fg="#7AAC05")
titulo_inicio.pack(side="left")

titulo_de = Label(frame_titulo, text=" de ", font=("Arial", 20, "bold"),
                  bg="#111111", fg="#FFFFFF")
titulo_de.pack(side="left")

titulo_sesion = Label(frame_titulo, text="sesión", font=("Arial", 20, "bold"),
                      bg="#111111", fg="#7AAC05")
titulo_sesion.pack(side="left")


canvas_logo = Canvas(frame_login, width=70, height=70, bd=0, highlightthickness=0,  bg="#111111")

<<<<<<< HEAD
imagen_original = Image.open(LOGO)
=======
imagen_original = Image.open(obtener_ruta_recurso("login_mejor.png"))
>>>>>>> dcf901ba8527e88828eac6e7c9bb10addb0d6902
imagen_redimensionada = imagen_original.resize((70, 70))
foto_logo = ImageTk.PhotoImage(imagen_redimensionada)

canvas_logo.create_image(35, 35, image=foto_logo)
canvas_logo.grid(column=0, row=2, columnspan=3, pady=10)



etiqueta1=Label(frame_login,text="Usuario", font=("Arial", 10), bg="#111111",fg="#CFCFCF")
etiqueta1.grid(column=0, row=3, columnspan=3)
usuario=Entry(frame_login,width=15, font=("Arial", 14),bg="#1E1E1E",fg="white", insertbackground="#7AAC05",relief="flat")
usuario.grid(column=0,row=4, columnspan=3, pady=5)



etiqueta2=Label(frame_login,text="Contraseña", font=("Arial", 10), bg="#111111",fg="#CFCFCF")
etiqueta2.grid(column=0, row=5, columnspan=3)
contrasena=Entry(frame_login, width=15, font=("Arial", 14), show="*", bg="#1E1E1E",fg="white", insertbackground="#7AAC05",relief="flat")
contrasena.grid(column=0, row=6, columnspan=3, pady=5)


etiqueta3=Label(frame_login,text="", font=("Arial", 10), bg="#111111")
etiqueta3.grid(column=0, row=7)


boton_enviar=Button(frame_login,text="Enviar", font=("Arial", 11), pady=5, bg="#111111",fg="#7AAC1D",activebackground="#222222",activeforeground="#A5D62A",highlightthickness=1,highlightbackground="#7AAC1D",bd=0,command=lambda:validar(usuario, contrasena))
boton_enviar.grid(column=0, row=8, columnspan=3, pady=10)



boton_registrarse=Button(frame_login,text="Registrarse", font=("Arial", 11), bg="#111111",fg="#7AAC1D",activebackground="#222222",activeforeground="#A5D62A",highlightthickness=1,highlightbackground="#7AAC1D",bd=0, command=registro)
boton_registrarse.grid(column=0, row=9, columnspan=3)




ventana_login.mainloop()
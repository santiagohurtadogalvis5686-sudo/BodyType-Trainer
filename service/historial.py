
from tkinter import*
from tkinter import ttk
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox


import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIR_BD = os.path.abspath(os.path.join(BASE_DIR, "..", "db"))
os.makedirs(DIR_BD, exist_ok=True)
RUTA_BD = os.path.join(DIR_BD, "bodytype.db")

conexion = sqlite3.connect(RUTA_BD)
cursor = conexion.cursor()





def borrar_historial(tabla, cursor, conexion, usuario_actual):

    respuesta = messagebox.askyesno(
        "Confirmar",
        "¿Desea eliminar todo su historial?"
    )

    if respuesta:

        cursor.execute(
            "DELETE FROM historial WHERE id_usuario=?",
            (usuario_actual,)
        )

        conexion.commit()

        # Vaciar la tabla en pantalla
        for item in tabla.get_children():
            tabla.delete(item)

        messagebox.showinfo(
            "Historial",
            "El historial fue eliminado correctamente."
        )







def historial(usuario_actual):

    ventana_historial=tk.Toplevel()
    ventana_historial.title("Historial")
    try:
        import os
        ruta_ico = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "icono.ico"))
        if not os.path.exists(ruta_ico):
            ruta_ico = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static", "icono.ico"))
        ventana_historial.iconbitmap(ruta_ico)
    except Exception:
        pass
    ventana_historial.geometry("700x650")
    ventana_historial.config(padx=0, pady=0)
    ventana_historial.grab_set()
    ventana_historial.grid_columnconfigure(0, weight=1)
    ventana_historial.grid_columnconfigure(1, weight=1)


    ruta_img = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "fondo_historial.png"))
    if not os.path.exists(ruta_img):
        ruta_img = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static", "fondo_historial.png"))
    imagen = Image.open(ruta_img)
    imagen = imagen.resize((700, 650), Image.Resampling.LANCZOS)

    foto_fondo_validar = ImageTk.PhotoImage(imagen)


    label_fondo = Label(ventana_historial, image=foto_fondo_validar)
    label_fondo.image=foto_fondo_validar
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
    label_fondo.lower()


    frame_historial = tk.Frame(
    ventana_historial,
    bg="#111111",
    bd=0,
    highlightthickness=0
    )

    frame_historial.place( relx=0.5,
    rely=0.50,   # Ajusta este valor si lo quieres un poco más arriba o abajo
    anchor="center",
    width=550,
    height=440)

    titulo = tk.Label(
    frame_historial,
    text="Historial de evaluaciones",
    font=("Arial", 18, "bold"),
    bg="#111111",
    fg="white"
    )

    titulo.place(relx=0.5, y=30, anchor="n")


    style = ttk.Style()

    style.theme_use("clam")   # Permite personalizar los colores
    style.layout("Treeview", [
    ("Treeview.treearea", {"sticky": "nswe"})
    ])

    style.configure(
    "Treeview",
    background="#111111",
    foreground="white",
    fieldbackground="#111111",
    rowheight=28,
    borderwidth=0,
    relief="flat"
    )

    style.configure(
    "Treeview.Heading",
    background="#111111",
    foreground="#7AAC1D",
    borderwidth=0,
    relief="flat"
    )

    style.map(
        "Treeview",
        background=[("selected", "#222222")],  # Color al seleccionar una fila
        foreground=[("selected", "white")]
    )




    tabla = ttk.Treeview(
    frame_historial,
    columns=("Fecha", "Grasa", "Masa", "Musculo", "TMB", "TDEE"),
    show="headings",
    height=12
    )

    tabla.heading("Fecha", text="Fecha", anchor="center")
    tabla.heading("Grasa", text="% Grasa")
    tabla.heading("Masa", text="Masa grasa")
    tabla.heading("Musculo", text="Músculo")
    tabla.heading("TMB", text="TMB")
    tabla.heading("TDEE", text="TDEE")

    tabla.column("Fecha", width=130)
    tabla.column("Grasa", width=70, anchor="center")
    tabla.column("Masa", width=90, anchor="center")
    tabla.column("Musculo", width=90, anchor="center")
    tabla.column("TMB", width=80, anchor="center")
    tabla.column("TDEE", width=80, anchor="center")

    for columna in ("Fecha", "Grasa", "Masa", "Musculo", "TMB", "TDEE"):
        tabla.column(columna, anchor="center")

    tabla.place(
    relx=0.5,
    y=80,
    anchor="n",
    width=540,
    height=260
    )

    cursor.execute("""
    SELECT
    fecha,
    porcentaje_grasa,
    masa_grasa,
    masa_muscular,
    tmb,
    tdee
    FROM historial
    WHERE id_usuario=?
    ORDER BY fecha DESC
    """, (usuario_actual,))

    datos = cursor.fetchall()

    for fila in datos:
        tabla.insert("", "end", values=fila)

    frame_botones = tk.Frame(
    frame_historial,
    bg="#111111"
    )

    Button(
    frame_botones,
    text="Borrar historial",bg="#111111",fg="#7AAC1D",font=("Arial", 15),activebackground="#222222",activeforeground="#A5D62A",highlightthickness=1,highlightbackground="#7AAC1D",bd=0,  command=lambda: borrar_historial(tabla,cursor,conexion,usuario_actual)
    ).pack(side="left", padx=10)

    Button(
    frame_botones,
    text="Cerrar",bg="#111111",fg="#7AAC1D",activebackground="#222222",font=("Arial", 15),activeforeground="#A5D62A",highlightthickness=1,highlightbackground="#7AAC1D",bd=0,
    command=ventana_historial.destroy,
    ).pack(side="left", padx=10)

    frame_botones.place(
    relx=0.5,
    y=380,
    anchor="n"
    )
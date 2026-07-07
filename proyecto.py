
#Verificando conexion

from tkinter import*

#Importamos Pillow para manejar el tamaño de la imagen correctamente
from PIL import Image, ImageTk

#Importacion para las cajas de mensajes
from tkinter import messagebox 

#Importacion para abrir ventanas secundarias
import tkinter as tk
from tkinter import ttk

# para el scroll
from tkinter import scrolledtext

# Para los calculos

import math

#Para la base de datos

import sqlite3


conexion = sqlite3.connect("bodytype.db")
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


def borrar_historial(tabla):

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


def historial():

    ventana_historial=tk.Toplevel()
    ventana_historial.title("Historial")
    ventana_historial.iconbitmap("icono.ico")
    ventana_historial.geometry("700x650")
    ventana_historial.config(padx=0, pady=0)
    ventana_historial.grab_set()
    ventana_historial.grid_columnconfigure(0, weight=1)
    ventana_historial.grid_columnconfigure(1, weight=1)


    imagen = Image.open("fondo_historial.png")
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
    text="Borrar historial",bg="#111111",fg="#7AAC1D",font=("Arial", 15),activebackground="#222222",activeforeground="#A5D62A",highlightthickness=1,highlightbackground="#7AAC1D",bd=0,  command=lambda: borrar_historial(tabla)
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





def resultados():


    try:
        cuello = float(cuello_usuario.get())
        cintura = float(cintura_usuario.get()) 
        altura = float(altura_usuario.get())
        peso = float(peso_usuario.get())
        genero = genero_usuario.get()
        edad = int(edad_usuario.get())
        entrenamiento = int(dias_entrenamiento_usuario.get())
    except ValueError:
        messagebox.showerror("Error", "Por favor, complete los campos numéricos con valores válidos (Cintura, Cuello, Altura, Peso, Edad).")
        return

    # 2. Separamos los cálculos matemáticos por género
    if genero == "hombre":
        porcentaje_grasa = 86.010 * math.log10(cintura - cuello) - 70.041 * math.log10(altura * 100.0) + 36.76
        porcentaje_grasa = round(porcentaje_grasa, 2)

        tmb = (10 * peso) + (6.25 * (altura * 100)) - (5 * edad) + 5
        tmb = round(tmb, 2)
        
        if porcentaje_grasa < 10:
            resultado_clasificacion = "Usted tiene un cuerpo con muy poca grasa corporal y muy definido"
        elif porcentaje_grasa < 15:
            resultado_clasificacion = "Usted tiene un cuerpo atletico y con poca grasa corporal"
        elif porcentaje_grasa < 20:
            resultado_clasificacion = "Usted tiene una buena forma fisica"
        elif porcentaje_grasa < 25:
            resultado_clasificacion = "Usted tiene un cuerpo promedio"
        else:
            resultado_clasificacion = "Usted tiene su grasa corporal alta"

    elif genero=="mujer": # Si el género es mujer
        # Intentamos leer la cadera SOLO si es mujer
        try:
            cadera = float(cadera_usuario.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un valor numérico válido para la cadera.")
            return
        
        # Ahora sí, la fórmula tiene 'cintura', 'cadera' y 'cuello' perfectamente definidos
        porcentaje_grasa = 163.205 * math.log10(cintura + cadera - cuello) - 97.684 * math.log10(altura * 100.0) - 78.387
        porcentaje_grasa = round(porcentaje_grasa, 2)

        tmb = (10 * peso) + (6.25 * (altura * 100)) - (5 * edad) - 161
        tmb = round(tmb, 2)

        if porcentaje_grasa < 15:
            resultado_clasificacion = "Usted tiene un cuerpo con muy poca grasa corporal y muy definido"
        elif porcentaje_grasa < 22:
            resultado_clasificacion = "Usted tiene un cuerpo atletico y con poca grasa corporal"
        elif porcentaje_grasa < 25:
            resultado_clasificacion = "Usted tiene una buena forma fisica"
        elif porcentaje_grasa < 32:
            resultado_clasificacion = "Usted tiene un cuerpo promedio"
        else:
            resultado_clasificacion = "Usted tiene su grasa corporal alta"

    else:

        messagebox.showerror("Error","El genero debe ser 'Hombre' o 'Mujer' ")

        return

    # 3. Cálculos de actividad y resultados finales (continúan exactamente igual que antes)
    if entrenamiento >= 1 and entrenamiento<=3:
        factor_actividad = 1.375
    elif entrenamiento >=3 and entrenamiento<=5:
        factor_actividad = 1.55
    elif entrenamiento >= 6  and entrenamiento<=7 :
        factor_actividad = 1.725
    else:
        factor_actividad = 1.2

    masa_grasa = round(peso * (porcentaje_grasa / 100), 2)
    masa_libre_grasa = round(peso - masa_grasa, 2)
    masa_muscular_estimada = round(masa_libre_grasa * 0.55, 2)
    tdee = round(tmb * factor_actividad, 2)


    cursor.execute("""
    INSERT INTO historial(
    id_usuario,
    porcentaje_grasa,
    masa_grasa,
    masa_libre,
    masa_muscular,
    tmb,
    tdee
    )
    VALUES(?,?,?,?,?,?,?)
    """,
    (
    usuario_actual,
    porcentaje_grasa,
    masa_grasa,
    masa_libre_grasa,
    masa_muscular_estimada,
    tmb,
    tdee
    ))

    conexion.commit()


    ventana_resultados=tk.Toplevel()
    ventana_resultados.title("Resultados")
    ventana_resultados.iconbitmap("icono.ico")
    ventana_resultados.geometry("700x650")
    ventana_resultados.config(padx=0, pady=0)
    ventana_resultados.grab_set()
    ventana_resultados.grid_columnconfigure(0, weight=1)
    ventana_resultados.grid_columnconfigure(1, weight=1)

    imagen = Image.open("fondo_resultado.jpeg")
    imagen = imagen.resize((700, 650), Image.Resampling.LANCZOS)

    foto_fondo_validar = ImageTk.PhotoImage(imagen)


    label_fondo = Label(ventana_resultados, image=foto_fondo_validar)
    label_fondo.image=foto_fondo_validar
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
    label_fondo.lower()


    frame_resultados=Frame(ventana_resultados, bg="#111111",bd=2,relief="solid",padx=3,pady=3,  width=600, height=560,)
    frame_resultados.place(relx=0.5, rely=0.5, anchor="center")
    frame_resultados.grid_columnconfigure(0, minsize=330)
    frame_resultados.grid_columnconfigure(1, minsize=220)
    frame_resultados.grid_columnconfigure(0, weight=3)
    frame_resultados.grid_columnconfigure(1, weight=2)

    grasa_corporal = Label(
    frame_resultados,
    bg="#111111",
    text="Porcentaje de grasa corporal:",
    fg="#7AAC05",
    font=("Arial", 15)
    )
    grasa_corporal.grid(row=1, column=0, sticky="w", padx=15, pady=8)

    resultado_grasa_corporal = Label(
    frame_resultados,
    bg="#111111",
    text=f"{porcentaje_grasa} %",
    fg="white",
    font=("Arial", 11)
    )
    resultado_grasa_corporal.grid(row=1, column=1, sticky="w", padx=15, pady=8)


    clasificacion = Label(
    frame_resultados,
    bg="#111111",
    fg="#7AAC05",
    text="Clasificación:",
    font=("Arial", 15)
    )
    clasificacion.grid(row=2, column=0, sticky="w", padx=15, pady=8)

    resultado = Label(
    frame_resultados,
    text=resultado_clasificacion,
    fg="white",
    bg="#111111",
    wraplength=300,
    justify="left",
    font=("Arial", 11),
    anchor="w"
    )
    resultado.grid(row=2, column=1, sticky="w", padx=15, pady=8)


    lb_masa_grasa = Label(
    frame_resultados,
    bg="#111111",
    fg="#7AAC05",
    text="Masa grasa:",
    font=("Arial", 15)
    )
    lb_masa_grasa.grid(row=3, column=0, sticky="w", padx=15, pady=8)

    resultado_masa_grasa = Label(
    frame_resultados,
    bg="#111111",
    fg="white",
    text=f"{masa_grasa} Kg",
    font=("Arial", 11)
    )
    resultado_masa_grasa.grid(row=3, column=1, sticky="w", padx=15, pady=8)


    lb_masa_libre_grasas = Label(
    frame_resultados,
    bg="#111111",
    fg="#7AAC05",
    text="Masa libre de grasas:",
    font=("Arial", 15)
    )
    lb_masa_libre_grasas.grid(row=4, column=0, sticky="w", padx=15, pady=8)

    resultado_masa_libre_grasas = Label(
    frame_resultados,
    bg="#111111",
    fg="white",
    text=f"{masa_libre_grasa} Kg",
   font=("Arial", 11)
    )
    resultado_masa_libre_grasas.grid(row=4, column=1, sticky="w", padx=15, pady=8)


    lb_masa_muscular_estimada = Label(
    frame_resultados,
    bg="#111111",
    fg="#7AAC05",
    text="Masa muscular estimada:",
    font=("Arial", 15)
    )
    lb_masa_muscular_estimada.grid(row=5, column=0, sticky="w", padx=15, pady=8)

    resultado_masa_muscular = Label(
    frame_resultados,
    bg="#111111",
    fg="white",
    text=f"{masa_muscular_estimada} Kg",
    font=("Arial", 11)
    )
    resultado_masa_muscular.grid(row=5, column=1, sticky="w", padx=15, pady=8)


    lb_tasa_metabolica_basal = Label(
    frame_resultados,
    bg="#111111",
    fg="#7AAC05",
    text="TMB (Tasa Metabólica Basal):",
    font=("Arial", 15)
    )
    lb_tasa_metabolica_basal.grid(row=6, column=0, sticky="w", padx=15, pady=8)

    resultado_tmb = Label(
    frame_resultados,
    bg="#111111",
    fg="white",
    text=f"{tmb} kcal/día",
    font=("Arial", 11)
    )
    resultado_tmb.grid(row=6, column=1, sticky="w", padx=15, pady=8)

    lb_tdee= Label(
        frame_resultados,
        bg="#111111",
        fg="#7AAC05",
        text="TDEE(Gasto energetico diario total):",
        font=("Arial",15)
    )
    lb_tdee.grid(column=0, row=7, sticky="w", padx=15, pady=8)

    resultado_tdee = Label(
    frame_resultados,
    bg="#111111",
    fg="white",
    text=f"{tdee} kcal/día",
    font=("Arial", 11)
    )
    resultado_tdee.grid(row=7, column=1, sticky="w", padx=15, pady=8)


    lb_mensaje = Label(
    frame_resultados,
    bg="#111111",
    fg="white",
    text=("La masa muscular es una estimación basada en el porcentaje de grasa\n"
          "corporal y no sustituye una medición realizada con equipos especializados."),
    font=("Arial", 9),
    justify="center",
    wraplength=500
    )
    lb_mensaje.grid(row=8, column=0, columnspan=2, pady=(15, 0))

    boton_regresar=Button(frame_resultados,text="Regresar",font=("Arial",15),pady=5, bg="#111111",fg="#7AAC1D",activebackground="#222222",activeforeground="#A5D62A",highlightthickness=1,highlightbackground="#7AAC1D",bd=0, command=ventana_resultados.destroy)
    boton_regresar.grid(row=9, column=0, columnspan=2, pady=20)


def mostrar_cadera(event):

    if genero_usuario.get().strip().lower() == "mujer":
        lbl_cadera.grid(column=0, row=5, sticky="w", pady=5)
        cadera_usuario.grid(column=1, row=5, padx=10)

    else:
        lbl_cadera.grid_remove()
        cadera_usuario.grid_remove()

def progreso():

    global cuello_usuario, cintura_usuario, altura_usuario
    global peso_usuario, genero_usuario, edad_usuario
    global dias_entrenamiento_usuario
    global cadera_usuario, lbl_cadera, lbl_cintura

    text_usuario = usuario.get()

    ventana_progreso = tk.Toplevel()
    ventana_progreso.title("Evaluacion corporal")
    ventana_progreso.iconbitmap("icono.ico")
    ventana_progreso.geometry("500x600")
    ventana_progreso.config(padx=0, pady=0)
    ventana_progreso.grab_set()


    imagen = Image.open("fondo_progreso.jpeg")
    imagen = imagen.resize((600, 600), Image.Resampling.LANCZOS)

    foto_fondo_validar = ImageTk.PhotoImage(imagen)


    label_fondo = Label(ventana_progreso, image=foto_fondo_validar)
    label_fondo.image=foto_fondo_validar
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
    label_fondo.lower()



    frame_progreso=Frame(ventana_progreso, bg="#111111",bd=2,relief="solid",padx=3,pady=3,  width=460, height=460,)
    frame_progreso.place(relx=0.5, rely=0.5, anchor="center")

    titulo = Label(
        frame_progreso,
        text="📈 Evaluacion",
        bg="#111111",
        fg="white",
        font=("Arial", 15, "bold")
    )
    titulo.grid(column=0, row=0, columnspan=2, pady=(0,20))

    Label(
        frame_progreso,
        text=f"👤 Bienvenido {text_usuario.title()}",
        bg="#111111",
        fg="#7AAC05",
        font=("Arial", 15)
    ).grid(column=0, row=1, columnspan=2, pady=(0,20))

    # Género
    Label(
        frame_progreso,
        text="Digite su género(Hombre/Mujer)",
        bg="#111111",
        fg="white",
    ).grid(column=0, row=2, sticky="w", pady=5)

    genero_usuario = Entry(
        frame_progreso,
        width=20,
        font=("Arial",14),
        bg="#1E1E1E",
        fg="#7AAC05",
        insertbackground="#7AAC05",
        relief="flat"
    )

    genero_usuario.grid(column=1, row=2, padx=10)
    genero_usuario.bind("<KeyRelease>", mostrar_cadera)

    # Cuello
    Label(
        frame_progreso,
        text="¿Cuánto mide su cuello?",
        bg="#111111",
        fg="white",
    ).grid(column=0, row=3, sticky="w", pady=5)

    cuello_usuario = Entry(
        frame_progreso,
        bg="#1E1E1E",
        fg="#7AAC05",
        insertbackground="#7AAC05",
        relief="flat",
        width=20,
        font=("Arial",14)
    )

    cuello_usuario.grid(column=1, row=3, padx=10)

    # Cintura
    lbl_cintura = Label(
        frame_progreso,
        bg="#111111",
        fg="white",
        text="¿Cuánto mide su cintura?"
    )

    lbl_cintura.grid(column=0, row=4, sticky="w", pady=5)

    cintura_usuario = Entry(
        frame_progreso,
        bg="#1E1E1E",
        fg="#7AAC05",
        insertbackground="#7AAC05",
        relief="flat",
        width=20,
        font=("Arial",14)
    )

    cintura_usuario.grid(column=1, row=4, padx=10)

    # Cadera (oculta inicialmente)
    lbl_cadera = Label(
        frame_progreso,
        bg="#111111",
        fg="white",
        text="¿Cuánto mide su cadera?"
    )

    cadera_usuario = Entry(
        frame_progreso,
        width=20,
        bg="#1E1E1E",
        fg="#7AAC05",
        insertbackground="#7AAC05",
        relief="flat",
        font=("Arial",14)
    )

    # Altura
    Label(
        frame_progreso,
        text="¿Cuánto mide?",
        bg="#111111",
        fg="white",
    ).grid(column=0, row=6, sticky="w", pady=5)

    altura_usuario = Entry(
        frame_progreso,
        width=20,
        bg="#1E1E1E",
        fg="#7AAC05",
        insertbackground="#7AAC05",
        relief="flat",
        font=("Arial",14)
    )

    altura_usuario.grid(column=1, row=6, padx=10)

    # Peso
    Label(
        frame_progreso,
        text="¿Cuál es su peso?",
        bg="#111111",
        fg="white",
    ).grid(column=0, row=7, sticky="w", pady=5)

    peso_usuario = Entry(
        frame_progreso,
        width=20,
        bg="#1E1E1E",
        fg="#7AAC05",
        insertbackground="#7AAC05",
        relief="flat",
        font=("Arial",14)
    )

    peso_usuario.grid(column=1, row=7, padx=10)

    # Edad
    Label(
        frame_progreso,
        text="Digite su edad",
        bg="#111111",
        fg="white",
    ).grid(column=0, row=8, sticky="w", pady=5)

    edad_usuario = Entry(
        frame_progreso,
        width=20,
        font=("Arial",14),
        bg="#1E1E1E",
        fg="#7AAC05",
        insertbackground="#7AAC05",
        relief="flat"
    )

    edad_usuario.grid(column=1, row=8, padx=10)

    # Días de entrenamiento
    Label(
        frame_progreso,
        text="¿Cuántos días a la semana entrena?",
        bg="#111111",
        fg="white",
    ).grid(column=0, row=9, sticky="w", pady=5)


    dias_entrenamiento_usuario = Entry(
        frame_progreso,
        width=20,
        font=("Arial",14),
        bg="#1E1E1E",
        fg="#7AAC05",
        insertbackground="#7AAC05",
        relief="flat"
    )

    dias_entrenamiento_usuario.grid(column=1, row=9, padx=10)

    # Botones
    Button(
        frame_progreso,
        text="Calcular",
        font=("Arial",15),
       pady=5, bg="#111111",fg="#7AAC1D",activebackground="#222222",activeforeground="#A5D62A",highlightthickness=1,highlightbackground="#7AAC1D",bd=0,
        command=resultados
    ).grid(column=0, row=10, pady=10)



    Button(
        frame_progreso,
        text="Regresar",
        font=("Arial",15),
        pady=5, bg="#111111",fg="#7AAC1D",activebackground="#222222",activeforeground="#A5D62A",highlightthickness=1,highlightbackground="#7AAC1D",bd=0,
        command=ventana_progreso.destroy
    ).grid(column=1, row=10, pady=20)






def registro():

    global nombre_usuario
    global crear_contrasena

    ventana_registro=tk.Toplevel()
    ventana_registro.title("Registro")
    ventana_registro.iconbitmap("icono.ico")
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

    imagen = Image.open("fondo_login.jpeg")
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

    imagen_original = Image.open("login_mejor.png")
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


def alimentacion_endomorfo():

    ventana_alimentacion=tk.Toplevel()
    ventana_alimentacion.title("Guia para endomorfos")
    ventana_alimentacion.iconbitmap("icono.ico")
    ventana_alimentacion.config(width=550, height=550)
    ventana_alimentacion.grab_set()


    imagen = Image.open("fondo_entrenamiento.PNG")
    imagen = imagen.resize((600, 600), Image.Resampling.LANCZOS)

    foto_fondo_validar = ImageTk.PhotoImage(imagen)


    label_fondo = Label(ventana_alimentacion, image=foto_fondo_validar)
    label_fondo.image=foto_fondo_validar
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
    label_fondo.lower()


    frame_alimentacion=Frame(ventana_alimentacion, width=500, height=500, bg="black", bd=2,relief="solid",padx=3, pady=3)
    frame_alimentacion.place(relx=0.5, rely=0.5, anchor="center")



    alimentacion_ectomorfo=Label(frame_alimentacion, text="Alimentacion", font=("Arial", 14), bg="black", fg="White")
    alimentacion_ectomorfo.place(x=200, y=10)
    emoji=Label(frame_alimentacion, text="🍽", font=("Arial", 14), bg="black", fg="sky blue")
    emoji.place(x=310, y=10)


    tipo_dieta="""

   Distribución aproximada de macronutrientes

    • Carbohidratos: 30-40%
    • Proteínas: 30-35%
    • Grasas: 25-30%

    PROTEÍNAS

    • Pollo
    • Pavo
    • Pescado
    • Claras de huevo
    • Carne magra

    CARBOHIDRATOS DE ABSORCIÓN LENTA

    • Avena
    • Arroz integral
    • Quinoa
    • Legumbres
    • Batata

    VERDURAS

    • Brócoli
    • Espinaca
    • Lechuga
    • Pepino
    • Coliflor

    GRASAS SALUDABLES

    • Aguacate
    • Aceite de oliva
    • Nueces
    """

    borde = Frame(
    frame_alimentacion,
    bg="#7AAC05"
    )

    borde.place(
    relx=0.5,
    y=60,
    width=480,
    height=380,
    anchor="n"
)

    contenido = Frame(
    borde,
    bg="#7AAC05"
    )

    contenido.place(x=2, y=2, width=70, height=20)

    frame_texto = Frame(borde, bg="black")
    frame_texto.place(x=3, y=3, width=474, height=374)

    scroll = tk.Scrollbar(
        frame_texto,
        bg="#111111",
        activebackground="#7AAC05",
        troughcolor="#222222",
        width=20
    )
    scroll.pack(side="right", fill="y")
    
    scroll.place(
    x=454,
    y=0,
    width=20,
    height=374
)

    canvas_scroll = tk.Canvas(
    frame_texto,
    width=12,
    bg="#111111",
    highlightthickness=0
    )

    contenido_scroll = tk.Text(
    frame_texto,
    font=("Arial", 10),
    bg="black",
    fg="white",
    insertbackground="#7AAC05",
    wrap="word"
    )

    contenido_scroll.pack(side="left", fill="both", expand=True)

    contenido_scroll.insert("1.0", tipo_dieta)
    contenido_scroll.config(state="disabled")

    contenido_scroll.config(yscrollcommand=scroll.set)
    scroll.config(command=contenido_scroll.yview)

    canvas_scroll.create_rectangle(
        2, 2, 10, 370,
        fill="#222222",
        outline=""
    )

    thumb = canvas_scroll.create_rectangle(
    2, 40, 10, 120,
    fill="#7AAC05",
    outline=""
    )

    def mover(event):
        canvas_scroll.coords(
            thumb,
            2,
            event.y-40,
            10,
            event.y+40
        )

    canvas_scroll.tag_bind(thumb, "<B1-Motion>", mover)
    canvas_scroll.pack(side="right", fill="y")




    boton_regresar=Button(frame_alimentacion, text="Regresar", font=("Arial", 15), pady=5, bg="black",fg="#7AAC1D",activebackground="#222222",activeforeground="#A5D62A",highlightthickness=1,highlightbackground="#7AAC1D",bd=0 ,command=ventana_alimentacion.destroy)
    boton_regresar.place(x=220, y=450)



def endomorfo():

    ventana_endomorfo=tk.Toplevel()
    ventana_endomorfo.title("Guia para endomorfos")
    ventana_endomorfo.iconbitmap("icono.ico")
    ventana_endomorfo.config(width=600, height=600)
    ventana_endomorfo.grab_set()

    
    imagen = Image.open("fondo_entrenamiento.PNG")
    imagen = imagen.resize((600, 600), Image.Resampling.LANCZOS)

    foto_fondo_validar = ImageTk.PhotoImage(imagen)


    label_fondo = Label(ventana_endomorfo, image=foto_fondo_validar)
    label_fondo.image=foto_fondo_validar
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
    label_fondo.lower()


    frame_endomorfo=Frame(ventana_endomorfo, width=550, height=550,   bg="black",bd=2,relief="solid",padx=3, pady=3)
    frame_endomorfo.place(relx=0.5, rely=0.5, anchor="center")


    titulo=Label(frame_endomorfo, text="BodyType", font=("Arial", 14), bg="black", fg="#7AAC05")
    titulo.place(x=200, y=10)

    titulo_trainer=Label(frame_endomorfo, text="Trainer", font=("Arial", 14), bg="black", fg="white")
    titulo_trainer.place(x=290, y=10)

    emoji=Label(frame_endomorfo, text="💪", font=("Arial", 14), bg="black", fg="yellow")
    emoji.place(x=355, y=10)

    seleccion_cuerpo=Label(frame_endomorfo, text="Entrenamiento", font=("Arial", 11), bg="black", fg="white")
    seleccion_cuerpo.place(x=250, y=40)



    fondo = Canvas(frame_endomorfo, width=500, height=400, bd=0, highlightthickness=0)
    imagen_original = Image.open("entrenamiento_endo.png")
    imagen_redimensionada = imagen_original.resize((500, 400))
    foto_logo = ImageTk.PhotoImage(imagen_redimensionada)
    fondo.image = foto_logo 
    fondo.create_image(250, 200, image=foto_logo)
    fondo.place(x=25, y=70)
    

    boton_alimentacion=Button(frame_endomorfo, text="Alimentacion", font=("Arial", 11), pady=5, bg="black",fg="#7AAC1D",activebackground="#222222",activeforeground="#A5D62A",highlightthickness=1,highlightbackground="#7AAC1D",bd=0, command=alimentacion_endomorfo)
    boton_alimentacion.place(x=220, y=480)

    boton_regresar=Button(frame_endomorfo, text="Regresar", font=("Arial", 11),  pady=5, bg="black",fg="#7AAC1D",activebackground="#222222",activeforeground="#A5D62A",highlightthickness=1,highlightbackground="#7AAC1D",bd=0 ,command=ventana_endomorfo.destroy)
    boton_regresar.place(x=230, y=510)







def alimentacion_mesomorfo():

    ventana_alimentacion=tk.Toplevel()
    ventana_alimentacion.title("Guia para mesomorfos")
    ventana_alimentacion.iconbitmap("icono.ico")
    ventana_alimentacion.config(width=550, height=550)
    ventana_alimentacion.grab_set()

    imagen = Image.open("fondo_entrenamiento.PNG")
    imagen = imagen.resize((600, 600), Image.Resampling.LANCZOS)

    foto_fondo_validar = ImageTk.PhotoImage(imagen)


    label_fondo = Label(ventana_alimentacion, image=foto_fondo_validar)
    label_fondo.image=foto_fondo_validar
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
    label_fondo.lower()


    frame_alimentacion=Frame(ventana_alimentacion, width=500, height=500, bg="black", bd=2,relief="solid",padx=3, pady=3)
    frame_alimentacion.place(relx=0.5, rely=0.5, anchor="center")



    alimentacion_ectomorfo=Label(frame_alimentacion, text="Alimentacion", font=("Arial", 14), bg="black", fg="White")
    alimentacion_ectomorfo.place(x=200, y=10)
    emoji=Label(frame_alimentacion, text="🍽", font=("Arial", 14), bg="black", fg="sky blue")
    emoji.place(x=310, y=10)


    tipo_dieta="""

   Distribución aproximada de macronutrientes

    • Carbohidratos: 40-50%
    • Proteínas: 25-30%
    • Grasas: 25-30%

    PROTEÍNAS

    • Pollo
    • Pavo
    • Carne magra
    • Huevos
    • Pescados

    CARBOHIDRATOS

    • Arroz integral
    • Avena
    • Quinoa
    • Frutas
    • Verduras

    GRASAS SALUDABLES

    • Aguacate
    • Almendras
    • Aceite de oliva

    """

    borde = Frame(
    frame_alimentacion,
    bg="#7AAC05"
    )

    borde.place(
    relx=0.5,
    y=60,
    width=480,
    height=380,
    anchor="n"
)

    contenido = Frame(
    borde,
    bg="#7AAC05"
    )

    contenido.place(x=2, y=2, width=70, height=20)

    frame_texto = Frame(borde, bg="black")
    frame_texto.place(x=3, y=3, width=474, height=374)

    scroll = tk.Scrollbar(
        frame_texto,
        bg="#111111",
        activebackground="#7AAC05",
        troughcolor="#222222",
        width=20
    )
    scroll.pack(side="right", fill="y")
    
    scroll.place(
    x=454,
    y=0,
    width=20,
    height=374
)

    canvas_scroll = tk.Canvas(
    frame_texto,
    width=12,
    bg="#111111",
    highlightthickness=0
    )

    contenido_scroll = tk.Text(
    frame_texto,
    font=("Arial", 10),
    bg="black",
    fg="white",
    insertbackground="#7AAC05",
    wrap="word"
    )

    contenido_scroll.pack(side="left", fill="both", expand=True)

    contenido_scroll.insert("1.0", tipo_dieta)
    contenido_scroll.config(state="disabled")

    contenido_scroll.config(yscrollcommand=scroll.set)
    scroll.config(command=contenido_scroll.yview)

    canvas_scroll.create_rectangle(
        2, 2, 10, 370,
        fill="#222222",
        outline=""
    )

    thumb = canvas_scroll.create_rectangle(
    2, 40, 10, 120,
    fill="#7AAC05",
    outline=""
    )

    def mover(event):
        canvas_scroll.coords(
            thumb,
            2,
            event.y-40,
            10,
            event.y+40
        )

    canvas_scroll.tag_bind(thumb, "<B1-Motion>", mover)
    canvas_scroll.pack(side="right", fill="y")




    boton_regresar=Button(frame_alimentacion, text="Regresar", font=("Arial", 15), pady=5, bg="black",fg="#7AAC1D",activebackground="#222222",activeforeground="#A5D62A",highlightthickness=1,highlightbackground="#7AAC1D",bd=0 ,command=ventana_alimentacion.destroy)
    boton_regresar.place(x=220, y=450)



def mesomorfo():

    ventana_mesomorfo=tk.Toplevel()
    ventana_mesomorfo.title("Guia para mesomorfos")
    ventana_mesomorfo.iconbitmap("icono.ico")
    ventana_mesomorfo.config(width=600, height=600)
    ventana_mesomorfo.grab_set()

    imagen = Image.open("fondo_entrenamiento.PNG")
    imagen = imagen.resize((600, 600), Image.Resampling.LANCZOS)

    foto_fondo_validar = ImageTk.PhotoImage(imagen)


    label_fondo = Label(ventana_mesomorfo, image=foto_fondo_validar)
    label_fondo.image=foto_fondo_validar
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
    label_fondo.lower()


    frame_mesomorfo=Frame(ventana_mesomorfo, width=550, height=550,   bg="black",bd=2,relief="solid",padx=3, pady=3)
    frame_mesomorfo.place(relx=0.5, rely=0.5, anchor="center")


    titulo=Label(frame_mesomorfo, text="BodyType", font=("Arial", 14), bg="black", fg="#7AAC05")
    titulo.place(x=200, y=10)

    titulo_trainer=Label(frame_mesomorfo, text="Trainer", font=("Arial", 14), bg="black", fg="white")
    titulo_trainer.place(x=290, y=10)

    emoji=Label(frame_mesomorfo, text="💪", font=("Arial", 14), bg="black", fg="yellow")
    emoji.place(x=355, y=10)

    seleccion_cuerpo=Label(frame_mesomorfo, text="Entrenamiento", font=("Arial", 11), bg="black", fg="white")
    seleccion_cuerpo.place(x=250, y=40)



    fondo = Canvas(frame_mesomorfo, width=500, height=400, bd=0, highlightthickness=0)
    imagen_original = Image.open("entrenamiento_meso.png")
    imagen_redimensionada = imagen_original.resize((500, 400))
    foto_logo = ImageTk.PhotoImage(imagen_redimensionada)
    fondo.image = foto_logo 
    fondo.create_image(250, 200, image=foto_logo)
    fondo.place(x=25, y=70)
    

    boton_alimentacion=Button(frame_mesomorfo, text="Alimentacion", font=("Arial", 11), pady=5, bg="black",fg="#7AAC1D",activebackground="#222222",activeforeground="#A5D62A",highlightthickness=1,highlightbackground="#7AAC1D",bd=0, command=alimentacion_mesomorfo)
    boton_alimentacion.place(x=220, y=480)

    boton_regresar=Button(frame_mesomorfo, text="Regresar", font=("Arial", 11),  pady=5, bg="black",fg="#7AAC1D",activebackground="#222222",activeforeground="#A5D62A",highlightthickness=1,highlightbackground="#7AAC1D",bd=0 ,command=ventana_mesomorfo.destroy)
    boton_regresar.place(x=230, y=510)




def alimentacion_ectomorfo():

    ventana_alimentacion=tk.Toplevel()
    ventana_alimentacion.title("Guia para ectomorfos")
    ventana_alimentacion.iconbitmap("icono.ico")
    ventana_alimentacion.config(width=600, height=600)
    ventana_alimentacion.grab_set()

    imagen = Image.open("fondo_entrenamiento.PNG")
    imagen = imagen.resize((600, 600), Image.Resampling.LANCZOS)

    foto_fondo_validar = ImageTk.PhotoImage(imagen)


    label_fondo = Label(ventana_alimentacion, image=foto_fondo_validar)
    label_fondo.image=foto_fondo_validar
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
    label_fondo.lower()


    frame_alimentacion=Frame(ventana_alimentacion, width=500, height=500, bg="black", bd=2,relief="solid",padx=3, pady=3)
    frame_alimentacion.place(relx=0.5, rely=0.5, anchor="center")



    alimentacion_ectomorfo=Label(frame_alimentacion, text="Alimentacion", font=("Arial", 14), bg="black", fg="White")
    alimentacion_ectomorfo.place(x=200, y=10)
    emoji=Label(frame_alimentacion, text="🍽", font=("Arial", 14), bg="black", fg="sky blue")
    emoji.place(x=310, y=10)

    tipo_dieta="""

   Distribución aproximada de macronutrientes

    • Carbohidratos: 50-60%
    • Proteínas: 20-25%
    • Grasas: 20-25%

    PROTEÍNAS

    • Pechuga de pollo
    • Carne magra
    • Huevos
    • Atún
    • Salmón

    CARBOHIDRATOS

    • Arroz
    • Pasta
    • Avena
    • Papa
    • Batata

    GRASAS SALUDABLES

    • Aguacate
    • Frutos secos
    • Aceite de oliva

    """

    borde = Frame(
    frame_alimentacion,
    bg="#7AAC05"
    )

    borde.place(
    relx=0.5,
    y=60,
    width=480,
    height=380,
    anchor="n"
)

    contenido = Frame(
    borde,
    bg="#7AAC05"
    )

    contenido.place(x=2, y=2, width=70, height=20)

    frame_texto = Frame(borde, bg="black")
    frame_texto.place(x=3, y=3, width=474, height=374)

    scroll = tk.Scrollbar(
        frame_texto,
        bg="#111111",
        activebackground="#7AAC05",
        troughcolor="#222222",
        width=20
    )
    scroll.pack(side="right", fill="y")
    
    scroll.place(
    x=454,
    y=0,
    width=20,
    height=374
)

    canvas_scroll = tk.Canvas(
    frame_texto,
    width=12,
    bg="#111111",
    highlightthickness=0
    )

    contenido_scroll = tk.Text(
    frame_texto,
    font=("Arial", 10),
    bg="black",
    fg="white",
    insertbackground="#7AAC05",
    wrap="word"
    )

    contenido_scroll.pack(side="left", fill="both", expand=True)

    contenido_scroll.insert("1.0", tipo_dieta)
    contenido_scroll.config(state="disabled")

    contenido_scroll.config(yscrollcommand=scroll.set)
    scroll.config(command=contenido_scroll.yview)

    canvas_scroll.create_rectangle(
        2, 2, 10, 370,
        fill="#222222",
        outline=""
    )

    thumb = canvas_scroll.create_rectangle(
    2, 40, 10, 120,
    fill="#7AAC05",
    outline=""
    )

    def mover(event):
        canvas_scroll.coords(
            thumb,
            2,
            event.y-40,
            10,
            event.y+40
        )

    canvas_scroll.tag_bind(thumb, "<B1-Motion>", mover)
    canvas_scroll.pack(side="right", fill="y")




    boton_regresar=Button(frame_alimentacion, text="Regresar", font=("Arial", 15), pady=5, bg="black",fg="#7AAC1D",activebackground="#222222",activeforeground="#A5D62A",highlightthickness=1,highlightbackground="#7AAC1D",bd=0 ,command=ventana_alimentacion.destroy)
    boton_regresar.place(x=220, y=450)




def ectomorfo():

    ventana_ectomorfo=tk.Toplevel()
    ventana_ectomorfo.title("Guia para ectomorfos")
    ventana_ectomorfo.iconbitmap("icono.ico")
    ventana_ectomorfo.config(width=600, height=600)
    ventana_ectomorfo.grab_set()

    imagen = Image.open("fondo_entrenamiento.PNG")
    imagen = imagen.resize((600, 600), Image.Resampling.LANCZOS)

    foto_fondo_validar = ImageTk.PhotoImage(imagen)


    label_fondo = Label(ventana_ectomorfo, image=foto_fondo_validar)
    label_fondo.image=foto_fondo_validar
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
    label_fondo.lower()

    frame_ectomorfo=Frame(ventana_ectomorfo, width=550, height=550,   bg="black",bd=2,relief="solid",padx=3, pady=3)
    frame_ectomorfo.place(relx=0.5, rely=0.5, anchor="center")

    titulo=Label(frame_ectomorfo, text="BodyType", font=("Arial", 14), bg="black", fg="#7AAC05")
    titulo.place(x=200, y=10)

    titulo_trainer=Label(frame_ectomorfo, text="Trainer", font=("Arial", 14), bg="black", fg="white")
    titulo_trainer.place(x=290, y=10)

    emoji=Label(frame_ectomorfo, text="💪", font=("Arial", 14), bg="black", fg="yellow")
    emoji.place(x=355, y=10)

    seleccion_cuerpo=Label(frame_ectomorfo, text="Entrenamiento", font=("Arial", 11), bg="black", fg="white")
    seleccion_cuerpo.place(x=250, y=40)

    fondo = Canvas(frame_ectomorfo, width=500, height=400, bd=0, highlightthickness=0)
    imagen_original = Image.open("entrenamiento_ecto.png")
    imagen_redimensionada = imagen_original.resize((500, 400))
    foto_logo = ImageTk.PhotoImage(imagen_redimensionada)
    fondo.image = foto_logo 
    fondo.create_image(250, 200, image=foto_logo)
    fondo.place(x=25, y=70)

    boton_alimentacion=Button(frame_ectomorfo, text="Alimentacion", font=("Arial", 11), pady=5, bg="black",fg="#7AAC1D",activebackground="#222222",activeforeground="#A5D62A",highlightthickness=1,highlightbackground="#7AAC1D",bd=0, command=alimentacion_ectomorfo)
    boton_alimentacion.place(x=220, y=480)

    boton_regresar=Button(frame_ectomorfo, text="Regresar", font=("Arial", 11),  pady=5, bg="black",fg="#7AAC1D",activebackground="#222222",activeforeground="#A5D62A",highlightthickness=1,highlightbackground="#7AAC1D",bd=0 ,command=ventana_ectomorfo.destroy)
    boton_regresar.place(x=230, y=510)

def seleccionar_tipo(event):

    x = event.x
    y = event.y

    if 0 <= x <= 130 and 0 <= y <= 220:
        ectomorfo()

    elif 130 < x <= 270 and 0 <= y <= 220:
        mesomorfo()

    elif 270 < x <= 400 and 0 <= y <= 220:
        endomorfo()



def validar():


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
        ventana_inicio.iconbitmap("icono.ico")
        ventana_inicio.config(width=500, height=500)
        ventana_inicio.grab_set()

        imagen = Image.open("fondo_seleccion_cuerpo.jpeg")
        imagen = imagen.resize((500, 500), Image.Resampling.LANCZOS)

        foto_fondo_validar = ImageTk.PhotoImage(imagen)


        label_fondo = Label(ventana_inicio, image=foto_fondo_validar)
        label_fondo.image=foto_fondo_validar
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
        imagen_original2 = Image.open("tipos_cuerpo.png")
        imagen_redimensionada2 = imagen_original2.resize((400, 260))
        foto_ecto = ImageTk.PhotoImage(imagen_redimensionada2)
        fondo2.create_image(200, 120, image=foto_ecto)
        fondo2.image = foto_ecto  
        fondo2.place(x=-5, y=55)
        fondo2.bind("<Button-1>", seleccionar_tipo)


        boton_cerrar=Button(frame_validar, text="Cerrar sesion", font=("Arial", 13),  pady=5, bg="black",fg="#7AAC1D",activebackground="#222222",activeforeground="#A5D62A",highlightthickness=1,highlightbackground="#7AAC1D",bd=0,command=ventana_inicio.destroy)
        boton_cerrar.place(x=147, y=350)
        
        boton_historial=Button(frame_validar,text="Mi progreso",font=("Arial",13),pady=5, bg="black",fg="#7AAC1D",activebackground="#222222",activeforeground="#A5D62A",highlightthickness=1,highlightbackground="#7AAC1D",bd=0,command=historial)
        boton_historial.place(x=220, y=308)



        boton_progreso=Button(frame_validar, text="Nueva evaluación", font=("Arial", 13),  pady=5, bg="black",fg="#7AAC1D",activebackground="#222222",activeforeground="#A5D62A",highlightthickness=1,highlightbackground="#7AAC1D",bd=0 ,command=progreso)
        boton_progreso.place(x=70, y=308)

    else:

        messagebox.showinfo(message="El usuario y/o la contraseña son incorrectas", title="Error")



ventana_login= Tk()
ventana_login.title("Login")
ventana_login.iconbitmap("icono.ico")
ventana_login.geometry("500x500")
ventana_login.config(padx=0, pady=0)
ventana_login.grid_columnconfigure(0, weight=1)

imagen = Image.open("fondo_login.jpeg")
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

imagen_original = Image.open("login_mejor.png")
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


boton_enviar=Button(frame_login,text="Enviar", font=("Arial", 11), pady=5, bg="#111111",fg="#7AAC1D",activebackground="#222222",activeforeground="#A5D62A",highlightthickness=1,highlightbackground="#7AAC1D",bd=0,command=validar)
boton_enviar.grid(column=0, row=8, columnspan=3, pady=10)



boton_registrarse=Button(frame_login,text="Registrarse", font=("Arial", 11), bg="#111111",fg="#7AAC1D",activebackground="#222222",activeforeground="#A5D62A",highlightthickness=1,highlightbackground="#7AAC1D",bd=0, command=registro)
boton_registrarse.grid(column=0, row=9, columnspan=3)




ventana_login.mainloop()
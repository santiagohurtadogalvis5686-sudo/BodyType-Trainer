from tkinter import*
from tkinter import messagebox 
import math
import tkinter as tk
from PIL import Image, ImageTk


import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIR_BD = os.path.abspath(os.path.join(BASE_DIR, "..", "db"))
os.makedirs(DIR_BD, exist_ok=True)
RUTA_BD = os.path.join(DIR_BD, "bodytype.db")

conexion = sqlite3.connect(RUTA_BD)
cursor = conexion.cursor()










def resultados(usuario_actual):


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
    try:
        ruta_ico = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "icono.ico"))
        if not os.path.exists(ruta_ico):
            ruta_ico = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static", "icono.ico"))
        ventana_resultados.iconbitmap(ruta_ico)
    except Exception:
        pass
    ventana_resultados.geometry("700x650")
    ventana_resultados.config(padx=0, pady=0)
    ventana_resultados.grab_set()
    ventana_resultados.grid_columnconfigure(0, weight=1)
    ventana_resultados.grid_columnconfigure(1, weight=1)

    ruta_img = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "fondo_resultado.jpeg"))
    if not os.path.exists(ruta_img):
        ruta_img = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static", "fondo_resultado.jpeg"))
    imagen = Image.open(ruta_img)
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

def progreso(usuario_actual, nombre_usuario):

    global cuello_usuario, cintura_usuario, altura_usuario
    global peso_usuario, genero_usuario, edad_usuario
    global dias_entrenamiento_usuario
    global cadera_usuario, lbl_cadera, lbl_cintura

    text_usuario = nombre_usuario.get() if hasattr(nombre_usuario, 'get') else nombre_usuario

    ventana_progreso = tk.Toplevel()
    ventana_progreso.title("Evaluacion corporal")
    try:
        import os
        ruta_ico = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "icono.ico"))
        if not os.path.exists(ruta_ico):
            ruta_ico = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static", "icono.ico"))
        ventana_progreso.iconbitmap(ruta_ico)
    except Exception:
        pass
    ventana_progreso.geometry("500x600")
    ventana_progreso.config(padx=0, pady=0)
    ventana_progreso.grab_set()


    ruta_img = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "fondo_progreso.jpeg"))
    if not os.path.exists(ruta_img):
        ruta_img = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static", "fondo_progreso.jpeg"))
    imagen = Image.open(ruta_img)
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
        command=lambda: resultados(usuario_actual)
    ).grid(column=0, row=10, pady=10)



    Button(
        frame_progreso,
        text="Regresar",
        font=("Arial",15),
        pady=5, bg="#111111",fg="#7AAC1D",activebackground="#222222",activeforeground="#A5D62A",highlightthickness=1,highlightbackground="#7AAC1D",bd=0,
        command=ventana_progreso.destroy
    ).grid(column=1, row=10, pady=20)
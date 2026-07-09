from tkinter import*
from PIL import Image, ImageTk
import tkinter as tk

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ICONO = os.path.join(BASE_DIR, "static", "icono.ico")
FONDO_ENTRENAMIENTO = os.path.join(BASE_DIR, "static", "fondo_entrenamiento.PNG")

ENTRENAMIENTO_ECTO = os.path.join(BASE_DIR, "static", "entrenamiento_ecto.png")
ENTRENAMIENTO_MESO = os.path.join(BASE_DIR, "static", "entrenamiento_meso.png")
ENTRENAMIENTO_ENDO = os.path.join(BASE_DIR, "static", "entrenamiento_endo.png")


def alimentacion_endomorfo():

    ventana_alimentacion=tk.Toplevel()
    ventana_alimentacion.title("Guia para endomorfos")
    ventana_alimentacion.iconbitmap(ICONO)
    ventana_alimentacion.config(width=550, height=550)
    ventana_alimentacion.grab_set()


    imagen = Image.open(FONDO_ENTRENAMIENTO)
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
    ventana_endomorfo.iconbitmap(ICONO)
    ventana_endomorfo.config(width=600, height=600)
    ventana_endomorfo.grab_set()

    
    imagen = Image.open(FONDO_ENTRENAMIENTO)
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

    imagen_original = Image.open(ENTRENAMIENTO_ENDO)
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
    ventana_alimentacion.iconbitmap(ICONO)
    ventana_alimentacion.config(width=550, height=550)
    ventana_alimentacion.grab_set()

    imagen = Image.open(FONDO_ENTRENAMIENTO)
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
    ventana_mesomorfo.iconbitmap(ICONO)
    ventana_mesomorfo.config(width=600, height=600)
    ventana_mesomorfo.grab_set()

    imagen = Image.open(FONDO_ENTRENAMIENTO)
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

    imagen_original = Image.open(ENTRENAMIENTO_MESO)
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
    ventana_alimentacion.iconbitmap(ICONO)
    ventana_alimentacion.config(width=600, height=600)
    ventana_alimentacion.grab_set()

    imagen = Image.open(FONDO_ENTRENAMIENTO)
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
    ventana_ectomorfo.iconbitmap(ICONO)
    ventana_ectomorfo.config(width=600, height=600)
    ventana_ectomorfo.grab_set()

    imagen = Image.open(FONDO_ENTRENAMIENTO)
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

    imagen_original=Image.open(ENTRENAMIENTO_ECTO)
    imagen_redimensionada = imagen_original.resize((500, 400))
    
    foto_logo = ImageTk.PhotoImage(imagen_redimensionada)
    fondo.image = foto_logo 
    fondo.create_image(250, 200, image=foto_logo)
    fondo.place(x=25, y=70)

    boton_alimentacion=Button(frame_ectomorfo, text="Alimentacion", font=("Arial", 11), pady=5, bg="black",fg="#7AAC1D",activebackground="#222222",activeforeground="#A5D62A",highlightthickness=1,highlightbackground="#7AAC1D",bd=0, command=alimentacion_ectomorfo)
    boton_alimentacion.place(x=220, y=480)

    boton_regresar=Button(frame_ectomorfo, text="Regresar", font=("Arial", 11),  pady=5, bg="black",fg="#7AAC1D",activebackground="#222222",activeforeground="#A5D62A",highlightthickness=1,highlightbackground="#7AAC1D",bd=0 ,command=ventana_ectomorfo.destroy)
    boton_regresar.place(x=230, y=510)
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

# ==========================
# CONFIGURACIÓN DE FLASK
# ==========================

app = Flask(__name__)
CORS(app)

# Ruta de la base de datos
RUTA_BD = "db/bodytype.db"


# ==========================
# FUNCIÓN PARA CONECTARSE A LA BD
# ==========================

def obtener_conexion():
    conexion = sqlite3.connect(RUTA_BD)
    conexion.row_factory = sqlite3.Row
    return conexion


# ==========================
# LOGIN
# ==========================

@app.route("/login", methods=["POST"])
def login():

    datos = request.get_json()

    if not datos:
        return jsonify({
            "ok": False,
            "mensaje": "No se recibieron datos."
        }), 400

    usuario = datos.get("usuario")
    contrasena = datos.get("contrasena")

    if not usuario or not contrasena:
        return jsonify({
            "ok": False,
            "mensaje": "Complete todos los campos."
        }), 400

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT *
        FROM usuarios
        WHERE usuario = ? AND contrasena = ?
        """,
        (usuario, contrasena)
    )

    resultado = cursor.fetchone()

    conexion.close()

    if resultado:
        return jsonify({
            "ok": True,
            "mensaje": "Inicio de sesión exitoso."
        })

    return jsonify({
        "ok": False,
        "mensaje": "Usuario o contraseña incorrectos."
    })


# ==========================
# REGISTRO DE USUARIO
# ==========================

@app.route("/registro", methods=["POST"])
def registro():

    datos = request.get_json()

    if not datos:
        return jsonify({
            "ok": False,
            "mensaje": "No se recibieron datos."
        }), 400

    usuario = datos.get("usuario")
    contrasena = datos.get("contrasena")

    if not usuario or not contrasena:
        return jsonify({
            "ok": False,
            "mensaje": "Complete todos los campos."
        }), 400

    try:

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            INSERT INTO usuarios(usuario, contrasena)
            VALUES (?, ?)
            """,
            (usuario, contrasena)
        )

        conexion.commit()
        conexion.close()

        return jsonify({
            "ok": True,
            "mensaje": "Usuario registrado correctamente."
        })

    except sqlite3.IntegrityError:

        return jsonify({
            "ok": False,
            "mensaje": "Ese usuario ya existe."
        })


# ==========================
# EJECUTAR SERVIDOR
# ==========================

if __name__ == "__main__":
    app.run(debug=True)
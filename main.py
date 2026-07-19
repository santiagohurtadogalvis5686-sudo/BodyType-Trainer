from fastapi import FastAPI, HTTPException, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
import sqlite3
import os

app = FastAPI()

# Definimos la raíz del proyecto de forma segura (la carpeta donde vive este archivo)
BASE_DIR = Path(__file__).resolve().parent

# Ruta de la base de datos (dentro de la carpeta db)
RUTA_BD = BASE_DIR / "db" / "bodytype.db"

# ==========================================
# CONEXIÓN A LA BASE DE DATOS (MIGRADO DE FLASK)
# ==========================================
def obtener_conexion():
    conexion = sqlite3.connect(str(RUTA_BD))
    conexion.row_factory = sqlite3.Row
    return conexion

# Modelos de datos para las peticiones de FastAPI
class LoginRequest(BaseModel):
    usuario: str
    contrasena: str

class RegistroRequest(BaseModel):
    usuario: str
    contrasena: str

# Middleware personalizado para registrar peticiones
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"--> [PETICIÓN] {request.method} {request.url.path}")
    response = await call_next(request)
    print(f"<-- [RESPUESTA] Código de estado: {response.status_code}")
    return response

# ==========================================
# RUTA DE LOGIN REAL (MIGRADO DE FLASK)
# ==========================================
@app.post("/login")
async def login(data: LoginRequest):
    print(f"\n[LOGIN INTENTO] Usuario recibido: '{data.usuario}'")
    
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    cursor.execute(
        "SELECT * FROM usuarios WHERE usuario = ? AND contrasena = ?",
        (data.usuario, data.contrasena)
    )
    resultado = cursor.fetchone()
    conexion.close()
    
    if resultado:
        print("[LOGIN ÉXITO] Credenciales correctas encontradas en la BD.\n")
        return {"ok": True, "mensaje": "Inicio de sesión exitoso."}
    
    print("[LOGIN FALLIDO] Credenciales inválidas.\n")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Usuario o contraseña incorrectos."
    )

# ==========================================
# RUTA DE REGISTRO REAL (MIGRADO DE FLASK)
# ==========================================
@app.post("/registro")
async def registro(data: RegistroRequest):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        cursor.execute(
            "INSERT INTO usuarios(usuario, contrasena) VALUES (?, ?)",
            (data.usuario, data.contrasena)
        )
        conexion.commit()
        conexion.close()
        
        print(f"[REGISTRO ÉXITO] Usuario '{data.usuario}' creado con éxito.")
        return {"ok": True, "mensaje": "Usuario registrado correctamente."}
        
    except sqlite3.IntegrityError:
        print(f"[REGISTRO FALLIDO] El usuario '{data.usuario}' ya existe.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ese usuario ya existe."
        )

# ==========================================
# --- CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS ---
# ==========================================
# Apunta a la carpeta 'src' para exponer de forma segura 'img', 'js' y 'styles'
src_path = BASE_DIR / "src"
app.mount("/static", StaticFiles(directory=str(src_path)), name="static")

# ==========================================
# --- VISTAS / RUTAS DE LAS PÁGINAS HTML ---
# ==========================================

# Ruta para servir tu index.html principal (Vive directamente en 'src')
@app.get("/")
async def read_index():
    ruta_index = src_path / "index.html"
    if ruta_index.exists():
        return FileResponse(ruta_index)
    raise HTTPException(status_code=404, detail="index.html no encontrado")

# Ruta dinámica para servir las demás páginas HTML (Viven dentro de 'src/pages/')
@app.get("/pages/{page_name}.html")
async def get_html_page(page_name: str):
    file_path = src_path / "pages" / f"{page_name}.html"
    if file_path.exists():
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail=f"La página '{page_name}.html' no fue encontrada")

# ==========================================
# ARRANQUE ÚNICO EN EL PUERTO 8080
# ==========================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os

app = FastAPI()

# Modelo de datos para el Login
class LoginRequest(BaseModel):
    usuario: str
    contrasena: str

# Middleware personalizado para ver en consola TODAS las peticiones que entran
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"--> [PETICIÓN] {request.method} {request.url.path}")
    response = await call_next(request)
    print(f"<-- [RESPUESTA] Código de estado: {response.status_code}")
    return response

@app.post("/login")
async def login(data: LoginRequest):
    print(f"\n[LOGIN INTENTO] Usuario recibido: '{data.usuario}' | Contraseña recibida: '{data.contrasena}'")
    
    # Simulación de validación
    if data.usuario == "admin" and data.contrasena == "1234":
        print("[LOGIN ÉXITO] Credenciales correctas. ID generado: 1\n")
        return {"success": True, "id": 1}
    
    print("[LOGIN FALLIDO] Credenciales inválidas.\n")
    return {"success": False, "message": "Usuario o contraseña incorrectos."}

# --- CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS ---
print("[INFO] Verificando rutas de archivos estáticos...")
if os.path.exists("./src/static"):
    print("[OK] Carpeta './src/static' encontrada exitosamente.")
    app.mount("/static", StaticFiles(directory="./src/static"), name="static")
else:
    print("[ERROR CRÍTICO] No se encontró la carpeta './src/static'. Revisa la estructura.")

# Ruta para servir tu index.html principal
@app.get("/")
async def read_index():
    ruta_index = "./pages/index.html"
    if os.path.exists(ruta_index):
        print(f"[Carga HTML] Sirviendo la página principal: {ruta_index}")
        return FileResponse(ruta_index)
    print(f"[ERROR] No se encontró el archivo HTML en: {ruta_index}")
    raise HTTPException(status_code=404, detail="index.html no encontrado")

# Ruta dinámica para servir las demás páginas HTML (.html)
@app.get("/{page_name}.html")
async def get_html_page(page_name: str):
    file_path = f"./pages/{page_name}.html"
    if os.path.exists(file_path):
        print(f"[Carga HTML] Sirviendo página secundaria: {file_path}")
        return FileResponse(file_path)
    print(f"[ERROR 404] El cliente solicitó una página inexistente: {file_path}")
    raise HTTPException(status_code=404, detail="Página no encontrada")
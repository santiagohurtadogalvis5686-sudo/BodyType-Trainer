# BodyType Trainer 💪

BodyType Trainer es una aplicación web diseñada para ayudar a los usuarios a identificar su tipo de cuerpo (ectomorfo, mesomorfo o endomorfo), calcular indicadores de composición corporal, visualizar resultados de forma intuitiva y almacenar un historial personalizado.

Anteriormente concebida como una aplicación de escritorio, esta versión ha sido migrada a una arquitectura web moderna, rápida y ligera.

---

## 🚀 Características Principales

*   **Autenticación de Usuarios:** Sistema seguro de inicio de sesión y registro integrado con base de datos.
*   **Evaluación de Somatotipo:** Interfaz interactiva para la selección e información de tipos de cuerpo.
*   **Módulo de Progreso y Nutrición:** Seguimiento de rutinas, alimentación y evolución física.
*   **Historial Personalizado:** Almacenamiento persistente de los datos de cada usuario.

---

## 🛠️ Tecnologías Utilizadas

*   **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (Python 3) - Para la gestión de rutas, API endpoints y lógica de negocio.
*   **Base de Datos:** [SQLite3](https://www.sqlite.org/) - Almacenamiento local ligero y eficiente.
*   **Frontend:** HTML5, CSS3 (Diseño responsivo) y JavaScript (Vanilla JS).
*   **Servidor ASGI:** [Uvicorn](https://www.uvicorn.org/) - Para un despliegue rápido en desarrollo.

---

## 📂 Estructura del Proyecto

El proyecto mantiene una organización limpia separando la lógica del servidor de los archivos del cliente:

```text
├── db/
│   └── bodytype.db          # Base de datos SQLite
├── src/
│   ├── img/                 # Recursos gráficos e imágenes
│   ├── js/                  # Scripts de JavaScript (index.js, progreso.js, etc.)
│   ├── pages/               # Vistas secundarias en HTML
│   ├── styles/              # Hojas de estilo CSS
│   └── index.html           # Pantalla principal de la aplicación
├── main.py                  # Servidor principal en FastAPI
├── README.md                  
└── settings.json

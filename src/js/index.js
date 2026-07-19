// ===============================
// VARIABLES (Se recupera el usuario si ya inició sesión)
// ===============================
let usuarioActual = localStorage.getItem("usuarioActual") || null;

// Si ya estaba logueado al recargar la página, saltamos el login directamente
if (usuarioActual) {
    document.getElementById("login").hidden = true;
    document.getElementById("seleccionCuerpo").hidden = false;
}

// ===============================
// LOGIN
// ===============================
const loginForm = document.getElementById("loginForm");
const btnRegistro = document.getElementById("btnRegistro");

loginForm.addEventListener("submit", validarUsuario);
btnRegistro.addEventListener("click", () => {
    window.location.href = "registro.html";
});

async function validarUsuario(e) {
    e.preventDefault();

    const usuario = document.getElementById("usuario").value.trim();
    const contrasena = document.getElementById("contrasena").value.trim();
    const mensaje = document.getElementById("mensaje");

    if (usuario === "" || contrasena === "") {
        mensaje.textContent = "Complete todos los campos.";
        return;
    }

    try {
        // CONEXIÓN CON FASTAPI: Cambiamos la ruta al endpoint de Python
        // Si tu backend corre en el mismo puerto que el servidor de estáticos, basta con "/login"
        // Si corre en otro puerto (ej: http://127.0.0.1:8000), pon la URL completa.
        const respuesta = await fetch("http://127.0.0.1:8080/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                usuario,
                contrasena
            })
        });

        const datos = await respuesta.json();

        if (datos.ok) {
            usuarioActual = usuario;

            localStorage.setItem("usuarioActual", usuario);

            document.getElementById("login").hidden = true;
            document.getElementById("seleccionCuerpo").hidden = false;
        } else {
            mensaje.textContent = datos.message || "Usuario o contraseña incorrectos.";
        }

    } catch (error) {
        console.error(error);
        mensaje.textContent = "No fue posible conectar con el servidor.";
    }
}

// ===============================
// SELECCIONAR TIPO DE CUERPO
// ===============================
document.getElementById("ectomorfo").addEventListener("click", () => { seleccionarTipo("ectomorfo"); });
document.getElementById("mesomorfo").addEventListener("click", () => { seleccionarTipo("mesomorfo"); });
document.getElementById("endomorfo").addEventListener("click", () => { seleccionarTipo("endomorfo"); });

function seleccionarTipo(tipo){
    switch(tipo){
        case "ectomorfo":
            window.location.href = "ectomorfo.html";
            break;
        case "mesomorfo":
            window.location.href = "mesomorfo.html";
            break;
        case "endomorfo":
            window.location.href = "endomorfo.html";
            break;
    }
}

// ===============================
// NUEVA EVALUACIÓN
// ===============================
document.getElementById("btnNuevaEvaluacion").addEventListener("click", () => {

    window.location.href = "progreso.html";

});

// ===============================
// MI PROGRESO
// ===============================
document.getElementById("btnProgreso").addEventListener("click", () => {
    if(usuarioActual != null){
        window.location.href = "historial.html?id=" + usuarioActual;
    }
});

// ===============================
// CERRAR SESIÓN
// ===============================
document.getElementById("btnCerrarSesion").addEventListener("click", cerrarSesion);

function cerrarSesion(){

    usuarioActual = null;

    localStorage.removeItem("usuarioActual");
    localStorage.removeItem("datosProgreso");

    document.getElementById("usuario").value="";
    document.getElementById("contrasena").value="";
    document.getElementById("mensaje").textContent="";

    document.getElementById("seleccionCuerpo").hidden=true;
    document.getElementById("login").hidden=false;

}
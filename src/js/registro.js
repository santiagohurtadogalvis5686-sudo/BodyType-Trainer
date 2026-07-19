// ===============================
// ELEMENTOS DEL DOM
// ===============================

const registroForm = document.getElementById("registroForm");
const btnVolver = document.getElementById("btnVolver");
const mensaje = document.getElementById("mensajeRegistro");

// ===============================
// REGISTRAR USUARIO
// ===============================

registroForm.addEventListener("submit", registrarUsuario);

async function registrarUsuario(e) {

    e.preventDefault();

    const usuario = document.getElementById("nuevoUsuario").value.trim();
    const contrasena = document.getElementById("nuevaContrasena").value.trim();

    mensaje.style.color = "#ff5f5f";
    mensaje.textContent = "";

    if (usuario === "" || contrasena === "") {

        mensaje.textContent = "Complete todos los campos.";
        return;

    }

    try {

        const respuesta = await fetch("http://127.0.0.1:8080/registro", {

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

            mensaje.style.color = "#7AAC1D";
            mensaje.textContent = datos.mensaje;

            registroForm.reset();

            setTimeout(() => {

                window.location.href = "/pages/index.html";

            }, 1500);

        } else {

            mensaje.style.color = "#ff5f5f";
            mensaje.textContent = datos.mensaje;

        }

    } catch (error) {

        console.error(error);

        mensaje.style.color = "#ff5f5f";
        mensaje.textContent = "No fue posible conectar con el servidor.";

    }

}

// ===============================
// VOLVER AL LOGIN
// ===============================

btnVolver.addEventListener("click", () => {

    window.location.href = "/";

});
// ==========================
// CAMPO CADERA
// ==========================
const genero = document.getElementById("genero");
const campoCadera = document.getElementById("campoCadera");

genero.addEventListener("input", () => {
    if(genero.value.trim().toLowerCase() === "mujer"){
        campoCadera.style.display="flex";
    }
    else{
        campoCadera.style.display="none";
    }
});

// ==========================
// BIENVENIDA
// ==========================
const nombre = localStorage.getItem("usuarioActual");

if(nombre){
    document.getElementById("bienvenida").textContent =
    "👤 Bienvenido " + nombre;
}

// ==========================
// ENVÍO DEL FORMULARIO
// ==========================
document.getElementById("formProgreso").addEventListener("submit",(e)=>{
    e.preventDefault(); // Detiene el envío automático

    // 1. Lanzamos la pregunta emergente al usuario
    const respuesta = confirm("¿Los datos ingresados son correctos?");

    // 2. Si el usuario presiona "Aceptar", se ejecuta el código interno
    if (respuesta) {
        const datos={
            genero:document.getElementById("genero").value,
            cuello:document.getElementById("cuello").value,
            cintura:document.getElementById("cintura").value,
            cadera:document.getElementById("cadera").value,
            altura:document.getElementById("altura").value,
            peso:document.getElementById("peso").value,
            edad:document.getElementById("edad").value,
            entrenamiento:document.getElementById("entrenamiento").value
        };

        localStorage.setItem(
            "datosProgreso",
            JSON.stringify(datos)
        );

        // Redirige solo si todo está confirmado
        window.location.href="resultados.html"; 
    } 
    // Si presiona "Cancelar", el flujo se detiene y se queda en la misma página
});
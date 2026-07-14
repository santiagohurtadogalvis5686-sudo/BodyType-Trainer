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

// SOLUCIÓN: Asigna el valor a la variable 'nombre'
const nombre = localStorage.getItem("usuarioActual");

if(nombre){
    document.getElementById("bienvenida").textContent =
    "👤 Bienvenido " + nombre;
}

// ==========================
// ENVÍO DEL FORMULARIO
// ==========================

document.getElementById("formProgreso").addEventListener("submit",(e)=>{

    e.preventDefault();

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

    window.location.href="resultados.html";

});
// ==============================
// REFERENCIAS
// ==============================

const tabla = document.querySelector("#tablaHistorial tbody");

const btnEliminar = document.getElementById("btnEliminar");

const btnBorrarHistorial = document.getElementById("btnBorrarHistorial");

const btnCerrar = document.getElementById("btnCerrar");

let filaSeleccionada = null;

// ==============================
// CARGAR HISTORIAL
// ==============================

window.addEventListener("load", cargarHistorial);

function cargarHistorial(){

    const historial = JSON.parse(localStorage.getItem("historial")) || [];

    tabla.innerHTML = "";

    historial.forEach((registro, indice)=>{

        const fila = document.createElement("tr");

        fila.innerHTML = `

            <td>${registro.fecha}</td>

            <td>${registro.grasa}</td>

            <td>${registro.masaGrasa}</td>

            <td>${registro.masaMuscular}</td>

            <td>${registro.tmb}</td>

            <td>${registro.tdee}</td>

        `;

        fila.addEventListener("click",()=>{

            document.querySelectorAll("#tablaHistorial tbody tr")
            .forEach(f=>f.classList.remove("seleccionado"));

            fila.classList.add("seleccionado");

            filaSeleccionada = indice;

        });

        tabla.appendChild(fila);

    });

}

// ==============================
// ELIMINAR UNA EVALUACIÓN
// ==============================

btnEliminar.addEventListener("click",()=>{

    if(filaSeleccionada===null){

        alert("Seleccione una evaluación.");

        return;

    }

    const historial = JSON.parse(localStorage.getItem("historial")) || [];

    historial.splice(filaSeleccionada,1);

    localStorage.setItem(

        "historial",

        JSON.stringify(historial)

    );

    filaSeleccionada = null;

    cargarHistorial();

});

// ==============================
// BORRAR HISTORIAL
// ==============================

btnBorrarHistorial.addEventListener("click",()=>{

    if(!confirm("¿Desea borrar todo el historial?")){

        return;

    }

    localStorage.removeItem("historial");

    filaSeleccionada = null;

    cargarHistorial();

});

// ==============================
// CERRAR
// ==============================

btnCerrar.addEventListener("click",()=>{

    history.back();

});
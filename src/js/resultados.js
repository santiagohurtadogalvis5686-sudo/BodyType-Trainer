// ==========================
// OBTENER DATOS
// ==========================

const datos = JSON.parse(localStorage.getItem("datosProgreso"));

if (!datos) {

    alert("No hay datos para mostrar.");

    window.location.href = "/pages/progreso.html";

}

// ==========================
// VARIABLES
// ==========================

const genero = datos.genero.trim().toLowerCase();

const cuello = parseFloat(datos.cuello);
const cintura = parseFloat(datos.cintura);
const cadera = parseFloat(datos.cadera || 0);

const altura = parseFloat(datos.altura);

const peso = parseFloat(datos.peso);

const edad = parseInt(datos.edad);

const entrenamiento = parseInt(datos.entrenamiento);

// ==========================
// VALIDACIONES
// ==========================

if(

    isNaN(cuello) ||
    isNaN(cintura) ||
    isNaN(altura) ||
    isNaN(peso) ||
    isNaN(edad)

){

    alert("Complete correctamente todos los campos.");

    history.back();

}

// ==========================
// PORCENTAJE DE GRASA
// ==========================

let porcentajeGrasa;

let clasificacion;

let tmb;

if(genero==="hombre"){

    porcentajeGrasa =
    86.010*Math.log10(cintura-cuello)
    -
    70.041*Math.log10(altura*100)
    +
    36.76;

    tmb=
    (10*peso)
    +
    (6.25*(altura*100))
    -
    (5*edad)
    +
    5;

    if(porcentajeGrasa<10){

        clasificacion="Usted tiene un cuerpo con muy poca grasa corporal y muy definido";

    }

    else if(porcentajeGrasa<15){

        clasificacion="Usted tiene un cuerpo atlético y con poca grasa corporal";

    }

    else if(porcentajeGrasa<20){

        clasificacion="Usted tiene una buena forma física";

    }

    else if(porcentajeGrasa<25){

        clasificacion="Usted tiene un cuerpo promedio";

    }

    else{

        clasificacion="Usted tiene su grasa corporal alta";

    }

}

else if(genero==="mujer"){

    porcentajeGrasa=

    163.205*Math.log10(cintura+cadera-cuello)

    -

    97.684*Math.log10(altura*100)

    -

    78.387;

    tmb=

    (10*peso)

    +

    (6.25*(altura*100))

    -

    (5*edad)

    -

    161;

    if(porcentajeGrasa<15){

        clasificacion="Usted tiene un cuerpo con muy poca grasa corporal y muy definido";

    }

    else if(porcentajeGrasa<22){

        clasificacion="Usted tiene un cuerpo atlético y con poca grasa corporal";

    }

    else if(porcentajeGrasa<25){

        clasificacion="Usted tiene una buena forma física";

    }

    else if(porcentajeGrasa<32){

        clasificacion="Usted tiene un cuerpo promedio";

    }

    else{

        clasificacion="Usted tiene su grasa corporal alta";

    }

}

else{

    alert("El género debe ser Hombre o Mujer.");

    history.back();

}

// ==========================
// FACTOR DE ACTIVIDAD
// ==========================

let factorActividad=1.2;

if(entrenamiento>=1 && entrenamiento<=3){

    factorActividad=1.375;

}

else if(entrenamiento>=3 && entrenamiento<=5){

    factorActividad=1.55;

}

else if(entrenamiento>=6 && entrenamiento<=7){

    factorActividad=1.725;

}

// ==========================
// CÁLCULOS
// ==========================

porcentajeGrasa=porcentajeGrasa.toFixed(2);

tmb=tmb.toFixed(2);

const masaGrasa=

(peso*(porcentajeGrasa/100)).toFixed(2);

const masaLibre=

(peso-masaGrasa).toFixed(2);

const masaMuscular=

(masaLibre*0.55).toFixed(2);

const tdee=

(tmb*factorActividad).toFixed(2);

// ==========================
// MOSTRAR RESULTADOS
// ==========================

document.getElementById("porcentajeGrasa").textContent=

porcentajeGrasa+" %";

document.getElementById("clasificacion").textContent=

clasificacion;

document.getElementById("masaGrasa").textContent=

masaGrasa+" Kg";

document.getElementById("masaLibre").textContent=

masaLibre+" Kg";

document.getElementById("masaMuscular").textContent=

masaMuscular+" Kg";

document.getElementById("tmb").textContent=

tmb+" kcal/día";

document.getElementById("tdee").textContent=

tdee+" kcal/día";

// ==========================
// MOSTRAR RESULTADOS
// ==========================

document.getElementById("porcentajeGrasa").textContent=
porcentajeGrasa+" %";

document.getElementById("clasificacion").textContent=
clasificacion;

document.getElementById("masaGrasa").textContent=
masaGrasa+" Kg";

document.getElementById("masaLibre").textContent=
masaLibre+" Kg";

document.getElementById("masaMuscular").textContent=
masaMuscular+" Kg";

document.getElementById("tmb").textContent=
tmb+" kcal/día";

document.getElementById("tdee").textContent=
tdee+" kcal/día";


// ============================================================
// NUEVO: GUARDAR LA EVALUACIÓN EN EL HISTORIAL (Añadir aquí)
// ============================================================

// 1. Obtener el historial existente del localStorage o crear uno vacío si no existe
const historial = JSON.parse(localStorage.getItem("historial")) || [];

// 2. Crear la fecha del día de hoy formateada (AAAA-MM-DD)
const hoy = new Date();
const fechaFormateada = hoy.toISOString().split('T')[0];

// 3. Crear el nuevo objeto de registro con la estructura exacta que pide tu historial
const nuevoRegistro = {
    fecha: fechaFormateada,
    grasa: porcentajeGrasa + " %",
    masaGrasa: masaGrasa + " Kg",
    masaMuscular: masaMuscular + " Kg",
    tmb: tmb + " kcal/día",
    tdee: tdee + " kcal/día"
};

// 4. Agregar la nueva evaluación al arreglo de historial
historial.push(nuevoRegistro);

// 5. Guardar el arreglo actualizado en el localStorage
localStorage.setItem("historial", JSON.stringify(historial));
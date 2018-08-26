var USUARIO_A = "";
var DIA = "";

/*----Obiene el csrf_token del formulario----*/
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/*----Muestra la fecha en la pagina----*/
function showDate() {
    nuevaFecha = new Date();
    y = nuevaFecha.getFullYear();
    m = nuevaFecha.getMonth() + 1;
    d = nuevaFecha.getDate();
    document.getElementById("fecha").innerHTML = m + "/" + d + "/" + y;
}

/*----Cambia el contenido segun la opcion seleccionada---*/
function showActiveContainer(active_container, no1, no2, no3, no4) {
    $(active_container).show();
    $(no1).hide();
    $(no2).hide();
    $(no3).hide();
    $(no3).hide();

}

function submitListar() {
    $("#listar_familias").submit();
}

function submitSolicitud() {
    $("#listar_solicitudes").submit();
}

function submitMatches() {
    $("#listar_matches").submit();
}

function solicitarPool(usuario) {
    USUARIO_A = usuario.id.replace('-yes', '');
    $("#solicitar").submit();
}

function aceptarPool(usuario) {
    USUARIO_A = usuario.id.replace('-si', '');
    alert(USUARIO_A);
    $("#aceptar").submit();
}


function registrarDia(dia){
    DIA = dia.id;
    $("#registrar_dia").submit();
}
/*----Crea el contenedor principal----*/
function newContainerPrincipalSize() {
    var $containerPrincipal = $(".container-principal");
    var width_nav = parseInt($("#nav").width());
    var widthContainerPrincipal = parseInt($(window).width()) - width_nav - 20;
    $containerPrincipal.css({"max-width": widthContainerPrincipal + "px"});
    $containerPrincipal.css({"width": widthContainerPrincipal + "px"});
    $containerPrincipal.css({"margin-left": width_nav + 10 + "px"});

    var heightContainerPrincipal = parseInt($(window).height()) - 80; //-60 de fixed menubar y 10 de paddings de cada lado
    $containerPrincipal.css({"height": heightContainerPrincipal + "px"});
    $containerPrincipal.css({"max-height": heightContainerPrincipal + "px"});
}

$(document).ready(function () {
    showDate();
    showActiveContainer("#container-1", "#container-2", "#container-3", "#container-4", '#container-5');
    newContainerPrincipalSize();


    /*----Ejecucion de funciones al hacer resize de pantalla---*/
    $(window).resize(function () {
        newContainerPrincipalSize();
    });

    /*----Busqueda articulos en la base de datos sin refresh----*/
    $("#listar_familias").submit(function (e) {
        e.preventDefault();

        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: $(this).serialize(),
            dataType: 'html',
            success: function (respuesta) {
                console.log(respuesta);
                $("#lista").html(respuesta);

            },
            error: function (error_respuesta) {
                console.log(error_respuesta);
            }
        })
    });
    $("#listar_solicitudes").submit(function (e) {
        e.preventDefault();

        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: {
                'usuario_sol': $("#usuariot").val()
            },
            dataType: 'html',
            success: function (respuesta) {
                console.log(respuesta);
                $("#lista2").html(respuesta);

            },
            error: function (error_respuesta) {
                console.log(error_respuesta);

            }
        })
    });
    $("#solicitar").submit(function (e) {
        e.preventDefault();
        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: {
                'usuario': USUARIO_A,
                'usuario_sol': $("#usuariot").val()
            },
            dataType: 'html',
            success: function (respuesta) {
                console.log(respuesta);

            },
            error: function (error_respuesta) {
                console.log(error_respuesta);
            }
        })
    });
    $("#aceptar").submit(function (e) {
        e.preventDefault();
        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: {
                'usuario_acomodado': USUARIO_A,
                'usuario_auto': $("#usuariot").val()
            },
            dataType: 'html',
            success: function (respuesta) {
                console.log(respuesta);

            },
            error: function (error_respuesta) {
                console.log(error_respuesta);
            }
        })
    });
    $("#listar_matches").submit(function (e) {
        e.preventDefault();
        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: {
                'usuario': $("#usuariot").val()
            },
            dataType: 'html',
            success: function (respuesta) {
                console.log(respuesta);
                $("#lista3").html(respuesta);

            },
            error: function (error_respuesta) {
                console.log(error_respuesta);
            }
        })
    });
     $("#registrar_dia").submit(function (e) {
        e.preventDefault();
        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: {
                'dia': DIA,
                'usuario': $("#usuariot").val()
            },
            dataType: 'html',
            success: function (respuesta) {
                console.log(respuesta);
            },
            error: function (error_respuesta) {
                console.log(error_respuesta);
            }
        })
    });
});
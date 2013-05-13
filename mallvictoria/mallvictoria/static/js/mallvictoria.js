/* Cookie para post */
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = $.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

$(document).ready(function() {  
	$("#categorias").load("/categorias/");  
    $("#categorias_footer").load("/categorias/");  
	if (typeof(localStorage) != 'undefined' ) {
		if(localStorage.length>0){
			entrarSession();	
		}else{
			cerrarSession();
		}	
	}else{
		cerrarSession();
	}	
});


/* Busqueda de Articulos */
$('#frmBusqueda').submit(function() {
	$("input[name=csrfmiddlewaretoken]").val(csrftoken);
    $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: $(this).serialize(),
    });   
}); 
/* Fin Busqueda de Articulos */

/* Funciones de Login */

$("#m_correo").keypress(function(event) {
    var keycode = (event.keyCode ? event.keyCode : event.which);
    if(keycode == '13') {
        $("#frmLogin").submit();
    }
});

$("#m_password").keypress(function(event) {
    var keycode = (event.keyCode ? event.keyCode : event.which);
    if(keycode == '13') {
        $("#frmLogin").submit();
    }
});

/* Boton Cerrar Session */
$("#btnCerrarSession").click(function(){
	cerrarSession();
    window.location='/cerrar'
});

/* Boton Entrar */
$("#button-bar").click(function(){
	$("#msgLogin").html("");
	$("#m_correo").val("");
	$("#m_password").val("");
	$("#registro").reveal({"animation":"fade","opened":function(){$("#m_correo").focus();}});
});

$("#modal").click(function(){
    $("#msgLogin").html("");
    $("#m_correo").val("");
    $("#m_password").val("");
    $("#registro").reveal({"animation":"fade","opened":function(){$("#m_correo").focus();}});
});

function cerrarSession(){
    $("#button-bar").css("display","inline");           
    $("#menu_login").css("display","none");   
    $("#btn_registro").css("display","inline");
    localStorage.clear();
}

function entrarSession(){
    $("#button-bar").css("display","none");           
    $("#menu_login").css("display","inline");
    $("#btn_registro").css("display","none");
    $("#datos_correo").text(localStorage.getItem("correo"));   
}

$("#btnLogin").click(function() {
	$('#frmLogin').submit();
});

$('#frmLogin').submit(function() {
	$("input[name=csrfmiddlewaretoken]").val(csrftoken);
    $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: $(this).serialize(),
        success: function(data) { 
        	if(data!="0"){
	        	var obj = $.parseJSON(data);
				localStorage.setItem("correo", obj.correo);    
                localStorage.setItem("nombre", obj.nombre);      
				entrarSession();
	        	$('#registro').trigger('reveal:close');  
                window.location='/administracion/'           
	        }else{
	        	$("#msgLogin").html('<div class="alert-box alert">Verifique los datos.</div>');
	        }

        }
    });   
    return false;
}); 
/* Fin Funciones de Login */

$("#id_estado").change(function(){
    //$("#id_estado option:[value=" + $(this).val()+"]").attr("selected", "selected"); 
    $.post("ciudades",{idestado:$(this).val(),csrfmiddlewaretoken:getCookie('csrftoken')},function(data){
        $("#id_ciudad").html(data);
    });
});

/*$("#btn_registro").click(function(){
    $("#div_registro_usuario").load("registro",function(){
        $.post("ciudades",{idestado:$("#id_estado option:selected").val(),csrfmiddlewaretoken:getCookie('csrftoken')},function(data){
            $("#id_ciudad").html(data);
        });    
    });
     $("#registro_usuario").reveal();
});*/
/* Funcione Volver al Top */
$("#regresar_top").click(function(){volver_top();});

function volver_top(){
   $("html, body").animate({
         scrollTop: $("header").position().top
       }, "slow");
}

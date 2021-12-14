async function msjSinRegistros(argument) { document.getElementById('msj-sin-registro').style.display = "block";  }
async function msjExito(msj) {
    var edo = document.getElementById('msj-estado');
       edo.innerHTML = 'Éxito';
        edo.style.backgroundColor = '#4CAF50'
      document.getElementById('msj-mensaje').innerHTML = msj;      
      document.getElementById('msj').style.display = "block";  }
async function msjError(msj) {
      var edo = document.getElementById('msj-estado');
       edo.innerHTML = 'Error';
       edo.style.backgroundColor = '#f44336'
      document.getElementById('msj-mensaje').innerHTML = msj;      
      document.getElementById('msj').style.display = "block";  }  
async function msjAdvertencia(msj) {
      var edo = document.getElementById('msj-estado');
       edo.innerHTML = 'Advertencia';
       edo.style.backgroundColor = '#FAB30F'
      document.getElementById('msj-mensaje').innerHTML = msj;      
      document.getElementById('msj').style.display = "block";  }  
async function procesoInicio(elemento) {
  btnHtml = elemento.textContent;//contenido actual del elemento    
   const div = document.createElement('div'); //seá el nuevo contenido  
   div.className = 'right mini-spin-white';
   const span = document.createElement('span');
   span.className = 'left';
   span.textContent =  `Procesando`;
   span.appendChild(div);
  elemento.appendChild (span)
  elemento.disabled=true;
}   
async function procesoFin(elemento) { elemento.textContent = btnHtml;   elemento.disabled= false;}
function getElement(element){return document.getElementById(element);}
function getValue(element){  return document.getElementById(element).value.trim();}
function setValue(element, valor){  document.getElementById(element).value = valor;}
function cleanValue(element){  document.getElementById(element).value = "";}
async  function procesando() { addClass('procesador', 'cargando');  }
async function completo(argument) { removeClass('procesador', 'cargando');}
async function addClass(elemento, clas){ var element, name, arr; element = document.getElementById(elemento);  name = clas; arr = element.className.split(" "); if (arr.indexOf(name) == -1) {element.className += " " + name;}}
async function removeClass(elemento, clas) {var element = document.getElementById(elemento); element.className = element.className.replace(clas, "");}
async function verModal(modal) {document.getElementById(modal).style.display = 'block'}
async function ocultarModal(modal) {document.getElementById(modal).style.display = 'none'}
function verCargador(argument) {document.getElementById('cargador').style.display = "block";  cargando = true;}
function ocultarCargador(argument) {document.getElementById('cargador').style.display = "none";  cargando = false;}


async function getFetch(url, config) {try{ var response = await fetch(url, config); if(response.ok  &&  response.status == 200){console.log('response', response); return response; }else{throw "Error en la llamada Ajax"; } }catch(error){console.warn(error); msjError('¡Ocurrión un error! <br/> No se pudo consultar los datos'); return false;} }
async function getJSON(url, config) {var response = await getFetch(url,config); if(await response){  return await response.json(); } else{return false;}  }

async function getDatos(form) {var tipo = document.getElementById("tipo").value;
console.log('tipo', tipo);
 return await getJSON("http://localhost:5000/api/proabilidad/ditribuciones?tipo="+tipo+"" ,{method: 'post',mode:'same-origin',body: form });}

//var form ;

async function getDistribucion() {try{
  //init_vars(c);//inicializa variables
   var res = await getDatos(await getForm() );
 }catch(error){    console.warn(error);  }
}

function ocultarForm(){
	addClass('form', 'oculto');
	addClass('l_div', 'oculto');
	addClass('n_div', 'oculto');
	addClass('p_div', 'oculto');
	addClass('loc_div', 'oculto');
	addClass('scale_div', 'oculto');	
}

function cleanValues(){ cleanValue('l'); cleanValue('n'); cleanValue('p'); cleanValue('loc'); cleanValue('scale'); cleanValue('cardinality');}

function getValues(){

	var form = new FormData();  

	var tipo = document.getElementById("tipo").value;
	form.append('tipo', tipo);
	form.append('cardinality', document.getElementById("cardinality").value);

 	switch (tipo) {
	  case 'Poisson':
	  	if(getValue('l') != null && getValue('l') != ""){ form.append('l',getValue('l')); }
	    else{ form = null; }
	    break;
	  case 'Binomial':
		  if(getValue('n') != null && getValue('p') != null && getValue('n') != "" && getValue('p') != ""){
		 	 form.append('n',getValue('n')); form.append('p',getValue('p'));
		  	}else{ form = null; }
	    break;
	  case 'BinomialNegativa':
		  if(getValue('n') != null && getValue('p') != null && getValue('n') != "" && getValue('p') != ""){
		  	  form.append('n',getValue('n')); form.append('p',getValue('p'));
		   	}else{ form = null;}
	    break;
	  case 'Normal':
	  	if(getValue('loc') != null && getValue('scale') != null && getValue('loc') != "" && getValue('scale') != ""){	  
			  form.append('loc',getValue('loc')); form.append('scale',getValue('scale'));
			}else{form = null;}
	    break;
	  case 'Exponencial':
		  if(getValue('scale') != null && getValue('scale') != ""){	  
		     form.append('scale',getValue('scale'));
		 }else{form = null;}
		    break;
	  default:
		form = null;	   
	}
	return form;
}

function verForm(){
 	ocultarForm(); 	 
 	var tipo = document.getElementById("tipo").value;
 	document.getElementById("titulo-distribucion").textContent=tipo+" - Ingresar Parámetros";
 	cleanValues(); removeClass('form', 'oculto');

 	switch (tipo) {
	  case 'Poisson':
	    removeClass('l_div', 'oculto');
	    break;
	  case 'Binomial':
	    removeClass('n_div', 'oculto');
	    removeClass('p_div', 'oculto');
	    break;
	  case 'BinomialNegativa':
	    removeClass('n_div', 'oculto');
	    removeClass('p_div', 'oculto');
	    break;
	  case 'Normal':
	    removeClass('loc_div', 'oculto');
	    removeClass('scale_div', 'oculto');
	    break;
	  case 'Exponencial':
	    removeClass('scale_div', 'oculto');
	    break;
	  default:
	    //console.log('Lo lamentamos, por el momento no disponemos de ' + expr + '.');
	}

 }

 async function calcular(event){
 	event.preventDefault()
 	var formu
 	if(formu = getValues()){
 		console.log('values', formu);
 		var res = await getDatos(formu);
 		console.log('res', await res);

 		getElement('numeros').textContent=res;
 		removeClass('resultados', 'oculto');
 	}else{
 		console.log('values nulos' , formu);
 	}
 }
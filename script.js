//////////////////game//////////////////
var napr1 = 1
var cord1 = 1
var KEY_W = 87; 
var KEY_A = 65;
var KEY_S = 83;
var KEY_D = 68;
var KEY_E = 69
var speed = true
var statfire1 = false
var statfire1cord = -1
var statfire1col = 0
var statfire1napr

function fire() {

	if (statfire1) {
		if (statfire1napr == "d" && ((statfire1cord + statfire1col) % 40) != 0) {
			document.getElementById('game' + (statfire1cord + statfire1col)).innerHTML=''
			statfire1col = statfire1col + 1
			document.getElementById('game' + (statfire1cord + statfire1col)).innerHTML='→'
		}
		if ((((statfire1cord + statfire1col) % 40) != 0) == false) {statfire1 = false; statfire1col = 0; statfire1napr = "none";  document.getElementById('game' + (statfire1cord + statfire1col)).innerHTML=''}
		if (statfire1napr == "w" && (statfire1cord + statfire1col) > 40) {
			document.getElementById('game' + (statfire1cord + statfire1col)).innerHTML=''
			statfire1col = statfire1col - 40
			document.getElementById('game' + (statfire1cord + statfire1col)).innerHTML='↑'
		}
		if ((((statfire1cord + statfire1col) > 40)) == false) {statfire1 = false; statfire1col = 0; statfire1napr = "none"; document.getElementById('game' + (statfire1cord + statfire1col)).innerHTML=''}
		if (statfire1napr == "a" && ((statfire1cord + statfire1col) % 40) != 1) {
			document.getElementById('game' + (statfire1cord + statfire1col)).innerHTML=''
			statfire1col = statfire1col - 1
			document.getElementById('game' + (statfire1cord + statfire1col)).innerHTML='←'
		}
		if ((((statfire1cord + statfire1col) % 40) != 1) == false) {statfire1 = false; statfire1col = 0; statfire1napr = "none"; document.getElementById('game' + (statfire1cord + statfire1col)).innerHTML=''}
		if (statfire1napr == "s" && ((statfire1cord + statfire1col) + 40) < 1040) {
			document.getElementById('game' + (statfire1cord + statfire1col)).innerHTML=''
			statfire1col = statfire1col + 40
			document.getElementById('game' + (statfire1cord + statfire1col)).innerHTML='↓'
		}
		if ((((statfire1cord + statfire1col) + 40) < 1040) == false) {statfire1 = false; statfire1col = 0; statfire1napr = "none"; document.getElementById('game' + (statfire1cord + statfire1col )).innerHTML=''}
	}
	if (statfire2) {
		if (statfire1napr == "d" && ((statfire1cord + statfire1col) % 40) != 0) {
			document.getElementById('game' + (statfire1cord + statfire1col)).innerHTML=''
			statfire1col = statfire1col + 1
			document.getElementById('game' + (statfire1cord + statfire1col)).innerHTML='→'
		}
		if ((((statfire1cord + statfire1col) % 40) != 0) == false) {statfire1 = false; statfire1col = 0; statfire1napr = "none";  document.getElementById('game' + (statfire1cord + statfire1col)).innerHTML=''}
		if (statfire1napr == "w" && (statfire1cord + statfire1col) > 40) {
			document.getElementById('game' + (statfire1cord + statfire1col)).innerHTML=''
			statfire1col = statfire1col - 40
			document.getElementById('game' + (statfire1cord + statfire1col)).innerHTML='↑'
		}
		if ((((statfire1cord + statfire1col) > 40)) == false) {statfire1 = false; statfire1col = 0; statfire1napr = "none"; document.getElementById('game' + (statfire1cord + statfire1col)).innerHTML=''}
		if (statfire1napr == "a" && ((statfire1cord + statfire1col) % 40) != 1) {
			document.getElementById('game' + (statfire1cord + statfire1col)).innerHTML=''
			statfire1col = statfire1col - 1
			document.getElementById('game' + (statfire1cord + statfire1col)).innerHTML='←'
		}
		if ((((statfire1cord + statfire1col) % 40) != 1) == false) {statfire1 = false; statfire1col = 0; statfire1napr = "none"; document.getElementById('game' + (statfire1cord + statfire1col)).innerHTML=''}
		if (statfire1napr == "s" && ((statfire1cord + statfire1col) + 40) < 1040) {
			document.getElementById('game' + (statfire1cord + statfire1col)).innerHTML=''
			statfire1col = statfire1col + 40
			document.getElementById('game' + (statfire1cord + statfire1col)).innerHTML='↓'
		}
		if ((((statfire1cord + statfire1col) + 40) < 1040) == false) {statfire1 = false; statfire1col = 0; statfire1napr = "none"; document.getElementById('game' + (statfire1cord + statfire1col )).innerHTML=''}
	}
	if (cord1 == statfire1cord + statfire1col) {alert("Game Over"); location.reload()}
}



document.onkeydown = function(e) 
{
	if (speed) {
	    if (e.keyCode == KEY_W) 
		    {
		    	if (cord1 > 40) 
		    	{	
		    		napr1 = 'w'
		    		document.getElementById('game' + cord1).style.backgroundColor = 'white';
		    		document.getElementById('game' + cord1).style.backgroundImage = 'url("")'; 
		    		cord1 = cord1 - 40
		    		document.getElementById('game' + cord1).style.backgroundImage = 'url("tank.png")'; 
		    		speed = false
		    	}
		    }
	     if (e.keyCode == KEY_A)
		    {
		    	if ((cord1 % 40) != 1)
		    	{
		    		napr1 = 'a'
		    		document.getElementById('game' + cord1).style.backgroundColor = 'white';
		    		document.getElementById('game' + cord1).style.backgroundImage = 'url("")'; 
		    		
		    		cord1 = cord1 - 1
		    		document.getElementById('game' + cord1).style.backgroundImage = 'url("tank3.png")'; 
		    		speed = false

		    	}
		    }
	    if (e.keyCode == KEY_S) 
		    {
		    	if (cord1 + 40 < 1040) 
		    	{
		    		napr1 = 's'
		    		//socket.send(parseInt(rand1) + 12)
		    		document.getElementById('game' + cord1).style.backgroundColor = 'white';
		    		document.getElementById('game' + cord1).style.backgroundImage = 'url("")'; 
		    		cord1 = cord1 + 40
		    		document.getElementById('game' + cord1).style.backgroundImage = 'url("tank2.png")'; 
		    		speed = false
		    	}
		    }
	    if (e.keyCode == KEY_D) 
		    {
		    	if ((cord1 % 40) != 0)
			    	{
			    		napr1 = 'd'
			    		document.getElementById('game' + cord1).style.backgroundColor = 'white';
			    		document.getElementById('game' + cord1).style.backgroundImage = 'url("")'; 
			    		cord1 = cord1 + 1
			    		document.getElementById('game' + cord1).style.backgroundImage = 'url("tank1.png")';
			    		speed = false 
			    	}
		    }
		 if (e.keyCode == KEY_E && statfire1 == false) 
		    {
		    	statfire1cord = cord1
		    	statfire1 = true
		    	statfire1napr = napr1
		    	fire()
		    }
	}
}
function speedsett() {
	speed = true
}
setInterval(fire, 75);
setInterval(speedsett, 300)

//////////////////socket//////////////////
var counter = false
var nap = 5
var cord2 = 9
var socket = new WebSocket("ws://0.tcp.ngrok.io:10817");
socket.onopen = function() {
  alert("Соединение установлено.");
};

socket.onclose = function(event) {
  if (event.wasClean) {
    alert('Соединение закрыто чисто');
  } else {
    alert('Обрыв соединения'); // например, "убит" процесс сервера
  }
  alert('Код: ' + event.code + ' причина: ' + event.reason);
};

socket.onmessage = function(event) {
	if (counter == false) {game = event.data; counter = true}
	if (counter) {
		try {document.getElementById('game' + cord2).style.backgroundImage = 'url("")'; }
		catch(err){}
		console.log(JSON.parse(event.data));
		// cord = JSON.parse(event.data)["cord"]
		// console.log(cord)

		cord2 = JSON.parse(event.data)["cord"]
		napr2 = JSON.parse(event.data)["napr"]
		console.log(napr2)
		if (napr2 == 1) {
			try {document.getElementById('game' + cord2).style.backgroundImage = 'url("tank.png")';}  catch (err){}
		}
		if (napr2 == 2) {
			try {document.getElementById('game' + cord2).style.backgroundImage = 'url("tank3.png")';}  catch (err){}
		}
		if (napr2 == 3) {
			try {document.getElementById('game' + cord2).style.backgroundImage = 'url("tank2.png")';}  catch (err){}
		}
		if (napr2 == 4) {
			try {
				document.getElementById('game' + cord2).style.backgroundImage = 'url("tank1.png")';
			}  
			catch (err){}
		}
		// try {document.getElementById('game' + cord2).style.backgroundImage = 'url("tank1.png")';}
		
		// catch (err){}
		if (napr1 == "w") {nap = 1}
		if (napr1 == "a") {nap = 2}
		if (napr1 == "s") {nap = 3}
		if (napr1 == "d") {nap = 4}
		var send = '{"napr":' + nap.toString() + ',"game":' + game.toString() + ',"cord":' + cord1.toString() + ',"status":' + statfire1.toString()+'}'
		socket.send(send)
	}
};

socket.onerror = function(error) {
  alert("Ошибка " + error.message);
};
// socket.send("Привет");

// function socketsend(argument) {
// 	var send = {
// 		"game": game,
// 		"cord": cord1,
// 		"firestat": var statfire1 = false
// 	}
// 	socket.send()
// }


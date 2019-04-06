//////////////////socket//////////////////

// var socket = new WebSocket("ws://127.0.0.1:9001");
// socket.onopen = function() {
//   alert("Соединение установлено.");
// };

// socket.onclose = function(event) {
//   if (event.wasClean) {
//     alert('Соединение закрыто чисто');
//   } else {
//     alert('Обрыв соединения'); // например, "убит" процесс сервера
//   }
//   alert('Код: ' + event.code + ' причина: ' + event.reason);
// };

// socket.onmessage = function(event) {
//   alert("Получены данные " + event.data);
// };

// socket.onerror = function(error) {
//   alert("Ошибка " + error.message);
// };
// socket.send("Привет");

//////////////////game//////////////////
var cord1 = 1
var KEY_W = 87; 
var KEY_A = 65;
var KEY_S = 83;
var KEY_D = 68;
document.onkeydown = function(e) 
{
    if (e.keyCode == KEY_W) 
	    {
	    	if (cord1 > 41) 
	    	{
	    		document.getElementById('game' + cord1).style.backgroundColor = 'white';
	    		document.getElementById('game' + cord1).style.backgroundImage = 'url("")'; 
	    		cord1 = cord1 - 41
	    		document.getElementById('game' + cord1).style.backgroundImage = 'url("tank.png")'; 
	    	}
	    }
     if (e.keyCode == KEY_A)
	    {
	    	if ((cord1 % 41) != 1)
	    	{
	    		document.getElementById('game' + cord1).style.backgroundColor = 'white';
	    		document.getElementById('game' + cord1).style.backgroundImage = 'url("")'; 
	    		
	    		cord1 = cord1 - 1
	    		document.getElementById('game' + cord1).style.backgroundImage = 'url("tank3.png")'; 

	    	}
	    }
    if (e.keyCode == KEY_S) 
	    {
	    	if (cord1 + 41 < 1066) 
	    	{
	    		//socket.send(parseInt(rand1) + 12)
	    		document.getElementById('game' + cord1).style.backgroundColor = 'white';
	    		document.getElementById('game' + cord1).style.backgroundImage = 'url("")'; 
	    		cord1 = cord1 + 41
	    		document.getElementById('game' + cord1).style.backgroundImage = 'url("tank2.png")'; 
	    	}
	    }
    if (e.keyCode == KEY_D) 
	    {
	    	if ((cord1 % 41) != 0)
		    	{
		    		document.getElementById('game' + cord1).style.backgroundColor = 'white';
		    		document.getElementById('game' + cord1).style.backgroundImage = 'url("")'; 
		    		cord1 = cord1 + 1
		    		document.getElementById('game' + cord1).style.backgroundImage = 'url("tank1.png")'; 
		    	}
	    }
}
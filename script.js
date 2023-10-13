function Fart(){
 var audio = document.getElementById("Fart");
        audio.play();
}

function Scream(){
 var audio = document.getElementById("Scream");
        audio.play();
}

function LoadTime(){
	document.getElementById("date").innerHTML = new Date().toLocaleDateString("en-US")
}
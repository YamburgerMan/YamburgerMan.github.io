function Fart(){
 var audio = document.getElementById("audio");
        audio.play();
}

function LoadTime(){
	document.getElementById("date").innerHTML = new Date().toLocaleDateString("en-US")
}
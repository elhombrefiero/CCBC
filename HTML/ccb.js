//Comment syntax
function init(){
    // Do some stuff
    updateCanvas();
}

function updateCanvas(){
    // Create the drawing
    // Create the background. Change either of these to fixed values if desired
    var width = window.innerWidth;
    var height = window.innerHeight;
    var myCanvas = document.getElementById("brewery");
        myCanvas.width = width;
        myCanvas.height = height;
        
    var context = myCanvas.getContext("2d");
        context.fillStyle = "blue";
        context.fillRect(0,0,width,height);
}
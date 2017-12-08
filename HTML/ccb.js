//Comment syntax
function drawBrewery(){
    // Change either of these to fixed values if a smaller size is desired
    var width = window.innerWidth;
    var height = window.innerHeight;
    var side_margin = 50; // 50 seems like a good offset
    
    // Sets a canvas (which we use to "draw" on). Size set using the height and width defined above
    var myCanvas = document.getElementById("brewery");
        myCanvas.width = width;
        myCanvas.height = height;
    
    // Water Tank Constants, Everything is function of these constants, do not alter unless you know what you're doing
    var length_of_tank = 150;
    var height_of_tank = length_of_tank * 2;
    var highest_height_of_tank = 100;
    var padding_between_tanks = 50;
    var x_pos_tank1 = padding_between_tanks;
    var x_pos_cwtank = x_pos_tank1 + length_of_tank + padding_between_tanks;
    var x_pos_tank2 = x_pos_cwtank + length_of_tank + padding_between_tanks;
    var x_pos_tank4 = x_pos_tank2 + (0.5 * length_of_tank) + padding_between_tanks;
    var x_pos_tank5 = x_pos_tank4 + length_of_tank + padding_between_tanks;
   
    // TODO: Make the drawing of the tanks more object oriented
    // Hot Water Tank, T1
    var tank1 = myCanvas.getContext("2d");
        tank1.fillStyle = "#0033cc"; // 0033cc - dark blue
        tank1.fillRect(x_pos_tank1,highest_height_of_tank,length_of_tank,height_of_tank); // (x, y, length, height) x and y are positions as measured from top left of page
        tank1.font = "30px Helvetica";
        tank1.fillStyle = "#ffffff"; // #ffffff - white
        tank1.textAlign = "center";
        tank1.fillText("T1", x_pos_tank1 + 0.5 * length_of_tank, highest_height_of_tank + 0.5 * height_of_tank);
    
    // Cold Water Tank
    var cwtank = myCanvas.getContext("2d");
        cwtank.fillStyle = "#66b3ff"; // 66b3ff - lighter blue
        cwtank.fillRect(x_pos_cwtank,highest_height_of_tank,length_of_tank,height_of_tank);
    
    // Mash Heater Tank, T2    
    var tank2 = myCanvas.getContext("2d");
        tank2.fillStyle = "#0033cc"; // 0033cc - dark blue
        tank2.fillRect(x_pos_tank2,highest_height_of_tank + 0.25 * height_of_tank, length_of_tank * 0.5, height_of_tank * 0.75);
        tank2.font = "30px Helvetica";
        tank2.fillStyle = "#ffffff";
        tank2.textAlign = "center";
        tank2.fillText("T2", x_pos_tank2 + 0.25 * length_of_tank, highest_height_of_tank + 0.5 * height_of_tank); // The text is higher to make room for heater
        
    // Boil Tank, T4
    var tank4 = myCanvas.getContext("2d");
        tank4.fillStyle = "#0033cc";
        tank4.fillRect(x_pos_tank4,highest_height_of_tank,length_of_tank,height_of_tank);
        tank4.font = "30px Helvetica";
        tank4.fillStyle = "#ffffff";
        tank4.textAlign = "center";
        tank4.fillText("T4", x_pos_tank4 + 0.5 * length_of_tank, highest_height_of_tank + 0.5 * height_of_tank);     
        
    // Exit Tank, T5
    var tank5 = myCanvas.getContext("2d");
        tank5.fillStyle = "#ffff00"; // #ffff00 - Yellow
        tank5.fillRect(x_pos_tank5,highest_height_of_tank + 0.25 * height_of_tank,length_of_tank,height_of_tank * 0.75);
        
    // Heater Constants
    var length_of_heater = 0.75 * length_of_tank;
    var height_of_heater = 0.1 * height_of_tank;
    
    // Heater 1, on Hot Water Tank
    var heater1 = myCanvas.getContext("2d");
        heater1.fillStyle = "#ff0000" // #ff0000 - red
        heater1.fillRect(x_pos_tank1, highest_height_of_tank + (0.8 * height_of_tank), length_of_heater, height_of_heater);
        heater1.font = "20px Helvetica";
        heater1.fillStyle = "#ffffff";
        heater1.textAlign = "center";
        heater1.fillText("H1", x_pos_tank1 + 0.5 * length_of_heater, highest_height_of_tank + (0.8 * height_of_tank) + (0.75 * height_of_heater));
        
    // Heater 2, on Mash Heater Tank
    var heater2 = myCanvas.getContext("2d");
        heater2.fillStyle = "#ff0000" // #ff0000 - red
        heater2.fillRect(x_pos_tank2 + (0.25 * length_of_tank) - (0.5 * height_of_heater), highest_height_of_tank + height_of_tank - length_of_heater, height_of_heater, length_of_heater);
        heater2.font = "20px Helvetica";
        heater2.fillStyle = "#ffffff";
        heater2.textAlign = "center";
        heater2.fillText("H2", x_pos_tank2 + (0.25 * length_of_tank), highest_height_of_tank + (0.8 * height_of_tank) + (0.75 * height_of_heater));
}

function makeTank(x_pos, y_pos, length, height){
    
    
}

function init(){
    // Do some stuff
    drawBrewery();
}
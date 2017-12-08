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
    
    var tankProperties = {
        font: "30px Helvetica",
        text_color: "#ffffff",
        text_alignment: "center",
    };
  
    // TODO: Make the drawing of the tanks more object oriented
    // Hot Water Tank, T1
    var tank1 = myCanvas.getContext("2d");
        tank1.fillStyle = "#0033cc"; // 0033cc - dark blue
        tank1.fillRect(x_pos_tank1,highest_height_of_tank,length_of_tank,height_of_tank); // (x, y, length, height) x and y are positions as measured from top left of page
        tank1.font = tankProperties.font;
        tank1.fillStyle = tankProperties.text_color;
        tank1.textAlign = tankProperties.text_alignment;
        tank1.fillText("T1", x_pos_tank1 + 0.5 * length_of_tank, highest_height_of_tank + 0.5 * height_of_tank);
    
    // Cold Water Tank
    var cwtank = myCanvas.getContext("2d");
        cwtank.fillStyle = "#66b3ff"; // 66b3ff - lighter blue
        cwtank.fillRect(x_pos_cwtank,highest_height_of_tank,length_of_tank,height_of_tank);
    
    // Mash Heater Tank, T2    
    var tank2 = myCanvas.getContext("2d");
        tank2.fillStyle = "#0033cc"; // 0033cc - dark blue
        tank2.fillRect(x_pos_tank2,highest_height_of_tank + 0.25 * height_of_tank, length_of_tank * 0.5, height_of_tank * 0.75);
        tank2.font = tankProperties.font;
        tank2.fillStyle = tankProperties.text_color;
        tank2.textAlign = tankProperties.text_alignment;
        tank2.fillText("T2", x_pos_tank2 + 0.25 * length_of_tank, highest_height_of_tank + 0.5 * height_of_tank); // The text is higher to make room for heater
        
    // Boil Tank, T4
    var tank4 = myCanvas.getContext("2d");
        tank4.fillStyle = "#0033cc";
        tank4.fillRect(x_pos_tank4,highest_height_of_tank,length_of_tank,height_of_tank);
        tank4.font = tankProperties.font;
        tank4.fillStyle = tankProperties.text_color;
        tank4.textAlign = tankProperties.text_alignment;
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
        heater1.fillStyle = "#ff0000"; // #ff0000 - red
        heater1.fillRect(x_pos_tank1, highest_height_of_tank + (0.8 * height_of_tank), length_of_heater, height_of_heater);
        heater1.font = "20px Helvetica";
        heater1.fillStyle = "#ffffff";
        heater1.textAlign = "center";
        heater1.fillText("H1", x_pos_tank1 + 0.5 * length_of_heater, highest_height_of_tank + (0.8 * height_of_tank) + (0.75 * height_of_heater));
        
    // Heater 2, on Mash Heater Tank
    var heater2 = myCanvas.getContext("2d");
        heater2.fillStyle = "#ff0000"; // #ff0000 - red
        heater2.fillRect(x_pos_tank2 + (0.25 * length_of_tank) - (0.5 * height_of_heater), highest_height_of_tank + height_of_tank - length_of_heater, height_of_heater, length_of_heater);
        heater2.font = "20px Helvetica";
        heater2.fillStyle = "#ffffff";
        heater2.textAlign = "center";
        heater2.fillText("H2", x_pos_tank2 + (0.25 * length_of_tank), highest_height_of_tank + (0.8 * height_of_tank) + (0.75 * height_of_heater));
        
    // Pumps consist of a rectangle, overlayed by a circle. It's in that order so it looks like a pump on a pump diagram
    
    // Pump Constants
    var pump_radius = length_of_tank * 0.25;
    var pump_center_y_axis = highest_height_of_tank + height_of_tank + padding_between_tanks + pump_radius;
    var pump_properties = {
      font: "30px Helvetica",
      shape_color: "#008000", // #008000 - green
      text_color: "#ffffff",
      text_alignment: "center",
    };
    
    // Pump 1
    var pump1 = myCanvas.getContext("2d");
        pump1.fillStyle = pump_properties.shape_color; // #008000 - green
        pump1.fillRect(x_pos_tank1 + 0.5 * length_of_tank, pump_center_y_axis - pump_radius, pump_radius * 1.5, pump_radius);
        pump1.beginPath();
        pump1.arc(x_pos_tank1 + 0.5 * length_of_tank,pump_center_y_axis,pump_radius,0,2*Math.PI);
        pump1.fill();
        pump1.font = pump_properties.font;
        pump1.fillStyle = pump_properties.text_color;
        pump1.textAlign = pump_properties.text_alignment;
        pump1.fillText("P1", x_pos_tank1 + (0.5 * length_of_tank), pump_center_y_axis);
        
    // Pump 2
    var pump2 = myCanvas.getContext("2d");
        pump2.fillStyle = pump_properties.shape_color; // #008000 - green
        pump2.fillRect(x_pos_cwtank + 0.5 * length_of_tank, pump_center_y_axis - pump_radius, pump_radius * 1.5, pump_radius);
        pump2.beginPath();
        pump2.arc(x_pos_cwtank + 0.5 * length_of_tank,pump_center_y_axis,pump_radius,0,2*Math.PI);
        pump2.fill();
        pump2.font = pump_properties.font;
        pump2.fillStyle = pump_properties.text_color;
        pump2.textAlign = pump_properties.text_alignment;
        pump2.fillText("P2", x_pos_cwtank + (0.5 * length_of_tank), pump_center_y_axis);
        
    // Pump 3
    var pump3 = myCanvas.getContext("2d");
        pump3.fillStyle = pump_properties.shape_color; // #008000 - green
        pump3.fillRect(x_pos_tank4 + 0.5 * length_of_tank, pump_center_y_axis - pump_radius, pump_radius * 1.5, pump_radius);
        pump3.beginPath();
        pump3.arc(x_pos_tank4 + 0.5 * length_of_tank,pump_center_y_axis,pump_radius,0,2*Math.PI);
        pump3.fill();
        pump3.font = pump_properties.font;
        pump3.fillStyle = pump_properties.text_color;
        pump3.textAlign = pump_properties.text_alignment;
        pump3.fillText("P3", x_pos_tank4 + (0.5 * length_of_tank), pump_center_y_axis);        
}

function makeTank(x_pos, y_pos, length, height){
    
    
}

function getBreweryConditions(){
    var request = null;
    if (window.XMLHttpRequest) {
        request = new XMLHttpRequest();
    } else if (window.ActiveXObject) {
        request = new ActiveXObject("Microsoft.XMLHTTP");
    }
    if (request){
        request.open("GET", "ccbc.xml");
        request.onreadystatechange = function() {
            if (request.readyState == 4) {
                alert("Download complete! ");
            }
        }
    }
}
    

function init(){
    // Do some stuff
    drawBrewery();
    setInterval(getBreweryConditions, 1000);
}
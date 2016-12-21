var canvas = document.getElementById("canvas");
var c = canvas.getContext("2d");

function drawClock() {
    // clear the background
    c.fillStyle = 'white';
    c.fillRect(0, 0, canvas.width, canvas.height);
    
    // Get the current time
    var now = new Date(),
        h = now.getHours(),
        m = now.getMinutes(),
        s = now.getSeconds(),
   
    // Make values like '5' into '05'
    h = addLeadingZeroWhenNecessary(h);
    m = addLeadingZeroWhenNecessary(m);
    s = addLeadingZeroWhenNecessary(s);
    
    // Assemble the text
    var clockText = h + ':' + m + ':' + s,
        x = 7,
        y = 15;
    
    // This green color was picked
    // using http://jscolor.com/
    c.fillStyle = 'black';
    
    // Draw the text
    c.font = '9pt Arial';
    c.fillText(clockText, x, y);
   
}

function addLeadingZeroWhenNecessary(s){
    return (s < 10 ? '0' : '') + s;
}

// Draw the clock right away
drawClock();

// Then draw the clock every subsequent second
setInterval(drawClock, 1000);
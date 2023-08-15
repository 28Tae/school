"Add to onclick attribute, but pass in proper parameters."

function calcProcess(n) {
    // Convert inputs to numerics
    let x = +document.querySelector("#num1").value;
    let y = +document.querySelector("#num2").value;
    let answer = 0;

    // Defaulting numbers to 0
    if (x == "") {
        x = 0;
    }
    if (y == "") {
        y = 0;
    }
    // FOOD FOR THOUGHT: What if you did <else if (y == "")> instead?
    
    // Calculate based on parameter n
    // rmbr convert RAD (radians) to DEG (degrees) !!
    if (n == 0) {
        answer = x**y;
    } else if (n==1) {
        answer = x**(1/y);
    } else if (n==2) {
        answer = Math.hypot(x, y);
    } else if (n==3) {
        answer = Math.atan(y/x) * 180/Math.PI;
    }

    // Update resultant input box
    document.querySelector("#result").value = answer;
}

"Add to onkeyup (releasing a key) attribute to both inputs"

function calc() {
    // Extracting both inputs
    // + tries convert to int
    let x = +document.querySelector("#num1").value;
	  let y = +document.querySelector("#num2").value;

    // Calculating and plug answer into HTML text content
	  document.querySelector("#sum").innerText = x + y;
	  document.querySelector("#difference").innerText = Math.abs(x - y);
	  document.querySelector("#product").innerText = x * y;
}

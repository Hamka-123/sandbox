const checkInput = (inputElement) => {

    let inputValue = inputElement.value;
    console.log(`Input value = ${inputValue}`);

    if (inputValue.includes(" ")) {
        // Display ERROR
        // STEP 1: display error:
        document.getElementById("err").style.color = "red";
        inputElement.style.color = "red";
        document.getElementById("err").innerHTML = "ERROR: space not allowed";

        // STEP 2: remove input text
        inputElement.value = "";
        return;
    }
    else {
        document.getElementById("err").style.color = "green";
        inputElement.style.color = "green";

        document.getElementById("err").innerText = inputValue;
    }
    const dateInput = document.querySelector('input[type="date"]')
    // Проверяем, что значение не пустое
    if (dateInput.value) {
        const dateDisplay = document.getElementById("date");
        const colorInput = document.querySelector('input[type="color"]');
        if (dateDisplay) {
            dateDisplay.innerHTML = `Detected Date: ${dateInput.value}`;
            if (colorInput){
                 dateDisplay.style.color = `${colorInput.value}`;
            }
            else {
                dateDisplay.style.color = `black`;
            }
           
        }
        
        
    }

};
const colorMixer = () => {
    let redColor = document.getElementById("redColor").value
    let greenColor = document.getElementById("greenColor").value
    let blueColor = document.getElementById("blueColor").value

   
    console.log(`red: ${redColor}, green: ${greenColor}, blue: ${blueColor}`)

    document.getElementById("palette").style.backgroundColor = `rgb(${redColor},${greenColor},${blueColor}`


}
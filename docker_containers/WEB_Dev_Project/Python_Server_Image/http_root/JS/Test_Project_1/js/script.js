const chH1Color = (color = "red") => {
    // STEP 1: get element (get DOM element by ID)
    const FIRST_H1 = document.getElementById("firstH1");
    console.log(FIRST_H1);

    // STEP 2: change property (color -> RED)
    FIRST_H1.style.color = color;

}

/*
Mouse Events
Event	        Description
click	        User clicks an element
dblclick	    Double click
mousedown	    Mouse button pressed
mouseup	        Mouse button released
mousemove	    Mouse moves
mouseover	    Mouse enters element
mouseout	    Mouse leaves element


Element properties:
element.style
element.innerText
element.textContent
element.innerHTML

*/

const div1 = () => {
    document
        .getElementById("test1")
        .innerText = "Text DIV1"
        ;
    document.getElementById("date").innerText = `Curent date: ${new Date().toTimeString()}`
}

console.log(`Curent date: ${new Date().toDateString()}`);
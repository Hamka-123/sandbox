const showDescription = (elem) => {
    let el = elem
        .parentElement
        .querySelector(".description")
    
    let allElem = document.querySelectorAll("a")
    allElem.forEach(element => {
        element.style.color = "grey"
    });

    el.style
        .visibility = "visible"
    elem.style.color = "red"


}

const hideDescription = (elem) => {
    let el = elem
        .parentElement
        .querySelector(".description")
        
    el.style
        .visibility = "hidden"
    
    let allElem = document.querySelectorAll("a")
    allElem.forEach(element => {
        element.style.color = "black"
    });
}
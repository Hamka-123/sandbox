/*
HTML_ELEMENT.style.fontSize = "30px"


fontSize = "30px"
'30px'
parseInt(fontSize)
30
Get HTML element
document.documentElement
window.getComputedStyle(document.documentElement).fontSize

const STEP = 2  // 2 PX
*/
// const STEP = 2 
// const htmlTag = document.documentElement
// const startFontSize = parseFloat(window.getComputedStyle(htmlTag).fontSize)
// let currentFontSize = startFontSize

// console.log(currentFontSize)
// const increase_fontsize = () => {
// console.log("increase")
// currentFontSize = currentFontSize+STEP
// htmlTag.style.fontSize = `${currentFontSize}px`
// }

// const decrease_fontsize = () => {
// console.log("decrease")
// currentFontSize = currentFontSize-STEP
// htmlTag.style.fontSize = `${currentFontSize}px`
// }

// const reset_fontsize = () => {
// console.log("reset")
// console.log(currentFontSize)
// currentFontSize = startFontSize
// htmlTag.style.fontSize = `${currentFontSize}px`
// }
// const html = document.documentElement;
// const STEP = 2;
// const DEFAULT_SIZE = parseFloat(window.getComputedStyle(html).fontSize);

// // Текущее состояние храним в одном месте
// let currentSize = DEFAULT_SIZE;

// // Единая точка правды для обновления интерфейса
// const setFontSize = (newSize) => {
//     currentSize = Math.max(newSize, 8); // Ограничиваем минимум 8px
//     html.style.fontSize = `${currentSize}px`;
//     console.log(`Current size: ${currentSize}px`);
// };

// // Компактные стрелочные функции
// const increase_fontsize = () => setFontSize(currentSize + STEP);
// const decrease_fontsize = () => setFontSize(currentSize - STEP);
// const reset_fontsize    = () => setFontSize(DEFAULT_SIZE);

const fontSizeController = (() => {
    const html = document.documentElement;
    const STEP = 2;
    const DEFAULT_SIZE = parseFloat(window.getComputedStyle(html).fontSize);
    
    // Эта переменная "заперта" внутри области видимости этой функции (замыкание)
    let currentSize = DEFAULT_SIZE;

    const setSize = (size) => {
        currentSize = Math.max(size, 8);
        html.style.fontSize = `${currentSize}px`;
        return currentSize;
    };

    return {
        increase: () => setSize(currentSize + STEP),
        decrease: () => setSize(currentSize - STEP),
        reset:    () => setSize(DEFAULT_SIZE),
        getCurrent: () => currentSize
    };
})();
// fontSizeController.increase()

const changeFontSize = (elemId) => {

    switch(elemId){
        case "inc":
            break
        case "dec":
            break
        case "res":
            break
    }
}
/*
document.getElementById() -> Single element
document.getElementsByTagName() -> collection
document.getElementsByClassName() -> collection
document.querySelector(CSS_SELECTOR) -> single element
document.querySelectorAll(CSS_SELECTOR) -> collection

document.body.parentElement
document.body.childNodes -> NodeList collection (all node types)
document.body.children -> HTMLCollection (element nodes)
document.body.previousElementSibling -> leftSibling
document.body.nextElementSibling -> rightSibling

В DOM есть два способа достучаться до самого главного тега <html>:

document.documentElement — это и есть официальный путь к тегу <html>.

document.querySelector('html') — более медленный, но тоже рабочий вариант.
*/
console.log(document.documentElement.children)
console.log(document.documentElement.nextElementSibling)

let timeout1;


const displayMsg = () => {

    timeout1 = setTimeout(
        () => {
            document.getElementById("msg").innerText += "New message text";
        },2000);
}

const cancelMsg = () => {

    clearTimeout(timeout1);

}
delay = 5500
document.addEventListener("DOMContentLoaded",()=>{
    setTimeout(
        () => {
            const c = document.getElementById("chat")
            c.innerHTML += `<br/><span>Появился через ${delay / 1000} секунд после загрузки DOM</span>`
            c.style.display = "block"
        }, delay
    )
})

let counter = 1;
let counterInterval;
const startCounter = () =>{
    counterInterval = setInterval(()=>{
        document.getElementById("counter").innerText = counter++;
    }, 1000)
}
const stopCounter = () =>{
    clearInterval(counterInterval)
}


const images = [
    "image1.webp", 
    "image2.webp", 
    "image3.webp", 
    "image4.webp"
];

let currentImg = 0; 
const img = document.querySelector("#slider img");

const changeImg = () => { 
    currentImg = (currentImg + 1) % images.length;
    img.src = images[currentImg];
    console.log(`Текущее изображение ${images[currentImg]}`)
};
let sliderInterval;
const startSlider = ()=>{
    sliderInterval = setInterval(changeImg, 1000)
    console.log("Слайдер запущен")
}
const stopSlider = ()=>{
    clearInterval(sliderInterval)
    console.log("Слайдер остановлен")
}
document.addEventListener('DOMContentLoaded', startSlider)
img.addEventListener('mouseenter', stopSlider)
img.addEventListener('mouseleave', startSlider)

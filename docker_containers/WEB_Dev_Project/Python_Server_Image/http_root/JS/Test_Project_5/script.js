const Init = (e) => {
console.log(e)
console.log(e.currentTarget)
}

// const button1 = (e) => {
//     document.body.innerHTML = "Hello!"
// };

// const resize_fun = () => {
//     document.addEventListener('mousemove', button1)
//     document.addEventListener('click', () => {
//         document.removeEventListener('mousemove', button1)
//         document.body.innerHTML = "All Clean!"
//     })
// };

// document.addEventListener('DOMContentLoaded', Init)
// window.addEventListener('resize',resize_fun)

document.addEventListener('DOMContentLoaded',(e)=>{
    document.getElementById('symbol').addEventListener('keyup',(KeyboardEvent)=>{
        console.log( KeyboardEvent.currentTarget.nextElementSibling)
        KeyboardEvent.currentTarget.nextElementSibling.innerHTML = `${KeyboardEvent.keyCode}`
    })
})

// Function declaration:
function f1(p1){
    // Function body
    console.log("f1 called");
    console.log(`Parameters: ${p1}`)
}

// Function call
f1();

const f2 = (par1) => {
    // Function body
    console.log("f2 called");
    console.log(`Parameters: ${par1}`)    
}; // Arrow function

console.log(typeof f2) // function

// const f3 = () => {
//     // Task1
//     console.log("Task1");
// }

// f3 = () => {
//     // Task2
//     console.log("Task2");
// }
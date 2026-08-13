// Task 1
function toggleDisplay() {
  // TODO: find password input
  let inp = document.querySelector("#pwd input");
  console.log("Текущий элемент:", inp);
  // // TODO: check input type
  if (inp.type === "password") {
    // // TODO: change type to text or password
    inp.type = "text";
  } else {
    inp.type = "password";
  }
}

// Task 2
function enableForm(el) {
  // TODO: get checkbox element
  let checkBox = el;
  //     // TODO: get fieldset
  let fieldSet = checkBox.nextElementSibling;
  console.log(fieldSet);
  //     // TODO: if checkbox checked -> show form
  if (checkBox.checked == true) {
    fieldSet.style.display = "block";
  }
  //   // TODO: else hide form
  else {
    fieldSet.style.display = "none";
  }
}

// Task 3
let day;
let dayNumber = new Date().getDay();
switch (dayNumber) {
  // TODO cases
  case 0:
    day = "Sunday";
    break;
  case 1:
    day = "Monday";
    break;
  case 2:
    day = "Tuesday";
    break;
  case 3:
    day = "Wednesday";
    break;
  case 4:
    day = "Thursday";
    break;
  case 5:
    day = "Friday";
    break;
  case 6:
    day = "Saturday";
    break;
  default:
    day = "Unknown day";
    console.error("Invalid day number!");
    break;
}
console.log(day);
document.querySelectorAll('h2').forEach(header => {
    if (header.textContent.includes("Task 3")) {
        let span = header.querySelector('span');
        span.style.color = "green"
        if (span) span.innerText = day;
    }
});


// Task 4
function myContact() {
  // TODO get selected radio value
  let selectedAction = document.querySelector(
    'input[name="action"]:checked',
  ).value;
  //  TODO switch action
  switch (selectedAction) {
    case "mail":
      console.log("Вы выбрали e-mail. Отправляем письмо...");
      // Здесь можно добавить код, например, показать поле для ввода почты
      break;

    case "phone":
      console.log("Вы выбрали телефон. Готовим звонок...");
      break;

    case "sms":
      console.log("Вы выбрали SMS. Пишем сообщение...");
      break;

    default:
      console.log("Ничего не выбрано");
  }
}

// Task 5
function showDescr() {
  // TODO display div
  document.getElementById("div1").style.display = "inline-block";
}
function hideDescr() {
  // TODO hide div
  document.getElementById("div1").style.display = "none";
}

// Task 6
let img = document.querySelector("#myImages");
// TODO add mouse events
// // mouseover
img.addEventListener("mouseover", () => {
  img.style.backgroundImage = "url('image1.webp')";
});
// // mouseout
img.addEventListener("mouseout", () => {
  img.style.backgroundImage = "url('image2.webp')";
});
// // mousedown
img.addEventListener("mousedown", () => {
  img.style.backgroundImage = "url('image3.webp')";
});
// // mouseup
img.addEventListener("mouseup", () => {
  img.style.backgroundImage = "url('image4.webp')";
});

// Task 7
const Menu = {
  show: function (id) {
    // TODO show description
    document.getElementById(id).style.display = "block";
  },
  hide: function (id) {
    // TODO hide description
    document.getElementById(id).style.display = "none";
  },
};

// Task 8
// Находим один раз и используем везде
const page = document.documentElement;
const step = 2;

function changeSize(delta) {
    let currentSize = parseFloat(window.getComputedStyle(page).fontSize);
    page.style.fontSize = (currentSize + delta) + "px";
}

// Функции-обертки для кнопок
const increaseFont = () => changeSize(step);
const decreaseFont = () => changeSize(-step);

// ui vars
const ui_OK = document.getElementById("OK");
const ui_Cancel = document.getElementById("Cancel");
const ui_Quit = document.getElementById("Quit");
const ui_matches = document.getElementById("matches")

const ui_rows = [];
for (let i=0; i<5; i++) {
  ui_rows.push(document.getElementById("row"+String(i)));
}

// load all event listeners
loadEventListeners();

function loadEventListeners() {
  document.addEventListener('DOMContentLoaded', init);
  ui_matches.addEventListener('click', matches)
  ui_OK.addEventListener('click', ok);
  ui_Cancel.addEventListener('click', cancel);
  ui_Quit.addEventListener('click', quit);
}

// event listeners
function init(e) {
  console.log(e)
  // actions
  rows = [1,2,3,4,5];
  rows_previous = [];
  for (let i = 0; i < 5; i++) {
    let s = 'I';
    for (let k = 1; k <= i; k++) {
      s = s + ' I';
    }
    ui_rows[i].firstElementChild.innerHTML = s;
  }
  ui_OK.innerText = 'Start';
  ui_OK.disabled = false;
  ui_Cancel.disabled = true;
  ui_Quit.disabled = true;
  // new state
  gameState = gameBegin;
}

function matches(e) {
  const t = e.target;
  //console.log(`${t} clicked`);
  //console.log(t.nodeName);
  if (t.nodeName === 'SPAN') {
    //console.log("juhu");
    const p = t.parentElement;
    //console.log(p);
    //console.log(p.id);
    let i = p.id[3];
    //console.log(i)
    i = Number(i);
    //console.log(ui_rows[i]);
    rows[i] -= 1;
    //...
    ui_rows[i].firstElementChild.innerHTML = '...';
  }
}

function ok(e) {
  console.log("ok clicked")
}

function cancel(e) {
  console.log("cancel clicked")
}

function quit(e) {
  console.log("quit clicked")
}

// model
// -----

let rows = [1,2,3,4,5];
let rows_previous = [];

// game states
const gameBegin = 0, userSelecting = 1, compiSelecting = 2, gameGoing = 3, gameOver = 4;
let gameState;
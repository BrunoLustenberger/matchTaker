// model
// -----

// rows containing the matches
let rows;
let rows_previous;

let selectedRowIndex; //todo: set to undefined or null, when not in use
let nMatchesTaken; //todo: analog

// game states
const gameBegin = 0, userSelecting = 1, compiSelecting = 2, gameGoing = 3/*, gameOver = 4*/;
let gameState;

// rules
let firstMoveByUser = false;

function resetRows() {
  rows = [1,2,3,4,5];
  rows_previous = Array.from(rows);
}

function nMatches() {
  return rows.reduce((total,num) => total + num,0);
}

function setGameState(newState) {
  switch (newState) {
    case gameBegin:
      resetRows();
      showRows();
      ui_message.innerText = 'Click Start to begin the game';
      break;
    case gameGoing:
      nMatchesTaken = 0;
      selectedRowIndex = -1; //undef
      rows_previous = Array.from(rows);
      break;
    case userSelecting:
      break;
    case compiSelecting:
      //simulate response
      console.log('fire response begin')
      setTimeout(() => document.dispatchEvent(simulatedResponseEvent), 2000);
      console.log('fire response end');
      break;
    default:
      console.assert(false);
  }
  gameState = newState;
}

// UI
// --

// ui vars
const ui_OK = document.getElementById("OK");
const ui_Cancel = document.getElementById("Cancel");
const ui_Quit = document.getElementById("Quit");
const ui_matches = document.getElementById("matches");
const ui_message = document.getElementById("message");

const ui_rows = [];
for (let i=0; i<5; i++) {
  ui_rows.push(document.getElementById("row"+String(i)));
}

// helper functions
function showRow(rowIndex) {
  let n = rows[rowIndex];
  let s = '';
  if (n > 0) {
    s = 'I';
    for (let k = 1; k < n; k++) {
      s = s + ' I';
    }
  }
  ui_rows[rowIndex].firstElementChild.innerHTML = s;
}

function showRows() {
  for (let i = 0; i < 5; i++) {
    showRow(i);
  }
}

function setButtons() {
  switch (gameState) {
    case gameBegin:
      ui_OK.innerText = 'Start';
      ui_OK.disabled = false;
      ui_Cancel.disabled = true;
      ui_Quit.disabled = true;
      break;
    case gameGoing:
      ui_OK.innerText = 'OK';
      ui_OK.disabled = true;
      ui_Cancel.disabled = true;
      ui_Quit.disabled = false;
      break;
    case userSelecting:
      ui_OK.innerText = 'OK';
      ui_OK.disabled = false;
      ui_Cancel.disabled = false;
      ui_Quit.disabled = false;
      break;
    default:
      ui_OK.innerText = 'OK';
      ui_OK.disabled = true;
      ui_Cancel.disabled = true;
      ui_Quit.disabled = true;
  }
}

// load all event listeners
loadEventListeners();

const simulatedResponseEvent = new Event('simulatedResponse');

function loadEventListeners() {
  document.addEventListener('DOMContentLoaded', init);
  document.addEventListener('simulatedResponse', response, true);
  ui_matches.addEventListener('click', matches);
  ui_OK.addEventListener('click', ok);
  ui_Cancel.addEventListener('click', cancel);
  ui_Quit.addEventListener('click', quit);
}

// event listeners
function init(e) {
  console.log(e)
  setGameState(gameBegin);
  setButtons();
}

function matches(e) {
  const t = e.target;
  console.log(`${t} clicked`);
  //console.log(t.nodeName);
  if (gameState === userSelecting || gameState === gameGoing) {
    if (t.nodeName === 'SPAN') {
      const p = t.parentElement;
      let i = p.id[3];
      //console.log(i)
      i = Number(i);
      //console.log(ui_rows[i]);
      if (gameState === gameGoing) {
        selectedRowIndex = i;
      }
      if (i === selectedRowIndex) {
        if (nMatchesTaken < 3) {
          rows[i] -= 1;
          nMatchesTaken += 1;
          showRow(i);
        } else {
          console.log('already 3 matches taken');
        }
      } else {
        console.log('clicked other row')
      }
      // new state, buttons
      setGameState(userSelecting);
      setButtons();
    }
  } else {
    console.log("row click has no effect")
  }
}

function response(e) {
  console.log('response begin');
  if (nMatches() > 1) {
    // new state, buttons
    setGameState(gameGoing);
    setButtons();
  } else {
    let s = (nMatches() === 1) ? "You won!" : "You lost!";
    alert(s);
    setGameState(gameBegin);
    setButtons();
  }
  console.log('response end');
}

function ok(e) {
  console.log("ok clicked");
  if (gameState === gameBegin) {
    if (firstMoveByUser) {
      setGameState(gameGoing);
    } else {
      setGameState(compiSelecting);
    }
    setButtons();
  } else if (gameState === userSelecting) {
      setGameState(compiSelecting);
      setButtons();
  } else {
    console.log("ok has no effect")
  }
}

function cancel(e) {
  console.log("cancel clicked")
  if (gameState === userSelecting) {
    // reset selected row
    rows[selectedRowIndex] = rows_previous[selectedRowIndex];
    showRow(selectedRowIndex);
    // new state, buttons
    setGameState(gameGoing);
    setButtons();
  } else {
    console.log("cancel has no effect")
  }
}

function quit(e) {
  console.log("quit clicked")
  if (gameState === userSelecting || gameState === gameGoing) {
    if (confirm("Quitting means you lost the game!")) {
      setGameState(gameBegin);
      setButtons();
    }
  } else {
    console.log("quit has no effect")
  }
}


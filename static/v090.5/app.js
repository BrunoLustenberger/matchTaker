// utils
const tempVersion = 'x';

function wait(milliseconds) {
  console.log('wait ' + String(milliseconds));
  return new Promise(resolve => {
      setTimeout(() => {
          resolve()
      }, milliseconds)
  })
}

function scrollToMiddle(element) {
  let box = element.getBoundingClientRect();
  let x = box.x + window.pageXOffset;
  let y = box.y + window.pageYOffset - window.innerHeight / 2;
  window.scrollTo(x,y);
}

// model
// -----

// rows containing the matches
let rows;
let rows_previous;

let selectedRowIndex; //todo: set to undefined or null, when not in use
let nMatchesTaken; //todo: analog

// game states
const gameBegin = 0, userSelecting = 1, appSelecting = 2, gameGoing = 3, gameOver = 4;
let gameState;
let userWon;

// rules
let firstMoveByUser = true;

//..
let simulateResponse = false;
let appLevel = 0; // smartness of the app as a player

// baseUrl
const baseUrl = "https://matchtaker.herokuapp.com";
//const baseUrl = "http://localhost:5000";

function resetRows() {
  rows = [1,2,3,4,5];
  rows_previous = Array.from(rows);
}

function nMatches() {
  return rows.reduce((total,num) => total + num, 0);
}

/**
 * Computes the parameter for the next_move route
 * @returns {String} - the parameters, with leading slash
 * @example rows == [1,0,3,2,3], appLevel == 1 --> '/10323/1'
 */
function getNextMoveParams() {
  let result = "/";
  for (let i = 0; i < 5; i++) {
    result += String(rows[i]);
  }
  result += "/" + String(appLevel);
  return result;
}

/**
 * Takes some matches to simulate the move by the computer.
 * @returns {number} - index of row, from which matches were taken
 */
function takeMatches() {
  console.assert(nMatches() > 0);
  for (let i = 4; i >= 0; i--) {
    if (rows[i] > 0) {
      let n = Math.min(3, rows[i]);
      if (n === nMatches()) {
        n -= 1; //must not take all matches
      }
      rows[i] -= n;
      return i;
    }
  }
}

/**
 * Perform all state-transition actions that do not depend on the previous gameState.
 */
function enterGameState(newState) {
  switch (newState) {
    case gameBegin:
      resetRows();
      showRows();
      ui_message.value = 'Click Start to begin the game.';
      break;
    case gameGoing:
      nMatchesTaken = 0;
      selectedRowIndex = -1; //undef
      rows_previous = Array.from(rows);
      ui_message.value = 'Take matches by clicking on them.';
      break;
    case userSelecting:
      let nMoreMatches = Math.min(3-nMatchesTaken, rows[selectedRowIndex]);
      if (nMoreMatches > 0) {
        ui_message.value = `You can take ${nMoreMatches} more match`
            + (nMoreMatches > 1 ? 'es' : '') + ' from this row.';
      } else if (rows[selectedRowIndex] > 0) {
        ui_message.value = 'You can take no more matches from this row.';
      } else {
        ui_message.value = 'You took the last match from this row.';
      }
      break;
    case appSelecting:
      ui_message.value = 'Wait for the app to take matches';
      if (simulateResponse) {
        //simulate response
        console.log('fire simulated response begin')
        setTimeout(() => document.dispatchEvent(simulatedResponseEvent), 1000);
        console.log('fire simulated response end');
      } else {
        // send request
        console.log('send request begin');
        //alert('send request begin');
        const xmlHttp = new XMLHttpRequest();
        xmlHttp.onreadystatechange = function () {
          console.log('handle response begin');
          console.log(`${this.readyState}, ${this.status}`);
          //alert('handle response begin');
          //alert(`${this.readyState}, ${this.status}`);
          //if (this.readyState === 4 && this.status === 200) {
          if (this.readyState === 4) {
            console.log(`responseText ${this.responseText}`);
            //alert(`responseText ${this.responseText}`);
            if (this.status === 200) {
              processResponse(this.responseText);
            }
          }
          console.log('handle response end');
          //alert('handle response end');
        };
        const url = baseUrl + "/next_move" + getNextMoveParams();
        xmlHttp.open("GET", url, true);
        //xmlHttp.open("GET", url, false);
        xmlHttp.send();
        console.log('send request end');
        //alert('send request end');
      }
      break;
    case gameOver:
      ui_message.value = userWon ? 'You won! :-)' : 'You lost :-(';
      break;
    default:
      console.assert(false);
  }
  gameState = newState;
  setButtons();
}

// UI
// --

// ui vars
const ui_OK = document.getElementById("OK");
const ui_Cancel = document.getElementById("Cancel");
const ui_Quit = document.getElementById("Quit");
const ui_QuitYes = document.getElementById("QuitYes");
const ui_matches = document.getElementById("matches");
const ui_message = document.getElementById("message");
const ui_body = document.querySelector('body');
const uiNavbar = document.querySelector('.navbar');
const uiButtons = document.getElementById("buttons");
const uiAlert = document.getElementById("modalAlert");
const uiAlertTitle = document.getElementById("modalAlertTitle");
const uiAlertDetail = document.getElementById("modalAlertDetail");

const ui_rows = [];
for (let i=0; i<5; i++) {
  ui_rows.push(document.getElementById("row"+String(i)));
}

const buttonClasses = {
  "OK" : {"enabled": "btn-success", "disabled": "btn-outline-success"},
  "Cancel" : {"enabled": "btn-dark", "disabled": "btn-outline-dark"},
  "Quit" : {"enabled": "btn-danger", "disabled": "btn-outline-danger"}
};

/**
 * Set css properties with runtime information
 */
function dynamicCss() {
  //ui_body.css({'padding_top' : '80px'}); -- doesn't work
  //console.log(uiNavbar.clientHeight);
  //console.log(uiNavbar.style.height); --> empty
  //console.log(uiNavbar.getBoundingClientRect().height);
  //ui_body.style.paddingTop = uiNavbar.height(); -- no such function
  ui_body.style.paddingTop = `${uiNavbar.getBoundingClientRect().height}px`;
  //todo: use a css class
  //ui_body.style.paddingBottom = `${ui_OK.getBoundingClientRect().height * 3}px`;
  ui_body.style.paddingBottom = `${uiButtons.getBoundingClientRect().height}px`;
}

// helper functions


/**
 * Shows a modal alert dialog
 * @param {String} title - title resp. short message.
 * @param {String} detail - detailed or additional message.
 */
function showAlert(title, detail) {
  //uiAlert.modal(); -- doesn't work
  uiAlertTitle.innerText = title;
  uiAlertDetail.innerText = detail;
  $("#modalAlert").modal(); //this works
}

/**
 * Shows a row.
 * @param {Number} rowIndex - index of row.
 */
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

/**
 * Shows all rows.
 */
function showRows() {
  for (let i = 0; i < 5; i++) {
    showRow(i);
  }
}

/**
 * Enables or disables a button, uses improved appearance.
 * @param {String} id - html id of button.
 * @param {Boolean} enable - true/false for enable/disable
 */
function enableButton(id, enable) {
  console.assert(["OK", "Cancel", "Quit"].includes(id));
  const btn = document.getElementById(id);
  btn.disabled = ! enable;
  if (enable) {
    btn.classList.remove(buttonClasses[id]["disabled"]);
    btn.classList.add(buttonClasses[id]["enabled"]);
  } else {
    btn.classList.remove(buttonClasses[id]["enabled"]);
    btn.classList.add(buttonClasses[id]["disabled"]);
  }
}

/**
 * Sets the buttons depending on gameState
 */
function setButtons() {
  switch (gameState) {
    case gameBegin:
      ui_OK.innerText = 'Start';
      enableButton("OK", true);
      enableButton("Cancel", false);
      enableButton("Quit", false);
      break;
    case gameGoing:
      ui_OK.innerText = 'OK';
      enableButton("OK", false);
      enableButton("Cancel", false);
      enableButton("Quit", true);
      break;
    case userSelecting:
      ui_OK.innerText = 'OK';
      enableButton("OK", true);
      enableButton("Cancel", true);
      enableButton("Quit", true);
      break;
    case gameOver:
      ui_OK.innerText = 'OK';
      enableButton("OK", true);
      enableButton("Cancel", false);
      enableButton("Quit", false);
      break;
    case appSelecting:
      ui_OK.innerText = 'OK';
      enableButton("OK", false);
      enableButton("Cancel", false);
      enableButton("Quit", false);
      break;
    default:
      console.assert(false);
  }
}

// load all event listeners

const simulatedResponseEvent = new Event('simulatedResponse');

function loadEventListeners() {
  document.addEventListener('DOMContentLoaded', init);
  document.addEventListener('simulatedResponse', simResponse, true);
  ui_matches.addEventListener('click', matches);
  ui_OK.addEventListener('click', ok);
  ui_Cancel.addEventListener('click', cancel);
  ui_Quit.addEventListener('click', quit);
  ui_QuitYes.addEventListener('click', quitYes);
}

loadEventListeners();

/**
 * event listeners
 * @param e {Event} - the event
 */

/**
 * Handle page-load event.
 */
function init(e) {
  console.log(tempVersion);
  console.log(e);
  dynamicCss();
  enterGameState(gameBegin);
}

/**
 * Handle the event when user clicks on a row.
 */
function matches(e) {
  const t = e.target;
  console.log(`${t} clicked`);
  // the event only has an effect for the following 2 states
  if (gameState === userSelecting || gameState === gameGoing) {
    // additionally: the user must click on or near a symbol representing a match.
    if (t.nodeName === 'SPAN') {
      const p = t.parentElement;
      let i = p.id[3]; // the char at this index gives the row-index
      //console.log(i)
      i = Number(i);
      //console.log(ui_rows[i]);
      if (gameState === gameGoing) { // first click of this move
        selectedRowIndex = i;
      }
      if (i === selectedRowIndex) { // the same row as before was clicked, or first click
        if (nMatchesTaken < 3) { // max not yet done
          rows[i] -= 1;
          nMatchesTaken += 1;
          showRow(i);
        } else {
          showAlert('No more matches', 'You cannot take more than 3 matches. Click OK or Cancel!');
        }
      } else { // another row than the one before was clicked
        showAlert('Other row', 'To take matches from another row, click Cancel first!');
      }
      // remain in state userSelecting or enter it
      enterGameState(userSelecting);
    } else {
      console.log("clicked outside of matches");
    }
  } else {
    console.log("row click has no effect");
  }
}

/**
 * Handle the response of the app, simulated.
 */
async function simResponse(e) {
  console.log('simulate response begin');
  if (nMatches() > 1) {
    let i = takeMatches();
    ui_rows[i].classList.remove('btn-black');
    ui_rows[i].classList.add('btn-warning');
    scrollToMiddle(ui_rows[i]);
    await wait(1000);
    showRow(i);
    await wait(1000);
    ui_rows[i].classList.remove('btn-warning');
    ui_rows[i].classList.add('btn-black');
    if (nMatches() > 1) {
      enterGameState(gameGoing);
    } else {
      console.assert(nMatches() === 1);
      userWon = false;
      enterGameState(gameOver);
    }
  } else {
    userWon = true;
    enterGameState(gameOver);
  }
  console.log('simulate response end');
}

/**
 * Handle the response of the app.
 */
async function processResponse(text) {
  const textJson = JSON.parse(text);
  if ('gameContinues' in textJson) {
    let c = textJson.gameContinues;
    if (c === -1) {
      userWon = true;
      enterGameState(gameOver);
    } else {
      let i = textJson.rowIndex;
      let n = textJson.numberOfMatches;
      console.log(`c:${c}, i:${i}, n:${n}`);
      ui_rows[i].classList.remove('btn-black');
      ui_rows[i].classList.add('btn-warning');
      scrollToMiddle(ui_rows[i]);
      await wait(1000);
      rows[i] -= n;
      showRow(i);
      await wait(1000);
      ui_rows[i].classList.remove('btn-warning');
      ui_rows[i].classList.add('btn-black');
      if (c === 0) {
        userWon = false;
        enterGameState(gameOver);
        //alert shows before row is updated, use setTimeout as workaround
        /*
        setTimeout(function(){
          userWon = false;
          enterGameState(gameOver);
          }, 1000);
         */
      } else {
        enterGameState(gameGoing);
      }
    }
  } else {
    console.assert('error' in textJson);
    showAlert("Error", textJson.error);
    userWon = true;
    enterGameState(gameOver);
  }
}

/**
 * Handle click on OK resp. Start.
 */
function ok(e) {
  console.log("ok clicked");
  if (gameState === gameBegin) {
    if (firstMoveByUser) {
      enterGameState(gameGoing);
    } else {
      enterGameState(appSelecting);
    }
  } else if (gameState === userSelecting) {
    enterGameState(appSelecting);
  } else if (gameState === gameOver) {
    enterGameState(gameBegin);
  } else {
    console.log("ok has no effect")
  }
}

/**
 * Handle click on Cancel.
 */
function cancel(e) {
  console.log("cancel clicked")
  if (gameState === userSelecting) {
    // reset selected row
    rows[selectedRowIndex] = rows_previous[selectedRowIndex];
    showRow(selectedRowIndex);
    // new state
    enterGameState(gameGoing);
  } else {
    console.log("cancel has no effect")
  }
}

/**
 * Handle Click on Quit.
 */
function quit(e) {
  console.log("quit clicked")
  if (gameState === userSelecting || gameState === gameGoing) {
    /*
    if (confirm("Quitting means you lost the game!")) {
      enterGameState(gameBegin);
    }
    */
    $("#modalQuitConfirm").modal('show');
  } else {
    console.log("quit has no effect")
  }
}

/**
 * Handle Quit Confirm.
 */
function quitYes(e) {
  console.log("quitYes clicked");
  $("#modalQuitConfirm").modal('hide');
  enterGameState(gameBegin);
}

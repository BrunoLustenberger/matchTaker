console.log("init module home begin");
import {ui_body, showAlert} from "./base.js";
import {wait, scrollToMiddle} from "./utils.js";
import * as state from "./state.js";
import * as settings_ from "./settings_.js"

const tempVersion = 'a';

//the server
const simulateResponse = false;
//const baseUrl = "https://matchtaker.herokuapp.com";
const baseUrl = "http://localhost:5000";

/**
 * Computes the parameter for the next_move route
 * @returns {String} - the parameters, with leading slash
 * @example state.rows == [1,0,3,2,3], appLevel == 1 --> '/10323/1'
 */
function getNextMoveParams() {
  let result = "/";
  for (let i = 0; i < 5; i++) {
    result += String(state.getRow(i));
  }
  result += "/" + String(state.appLevel);
  return result;
}

/**
 * Takes some matches to simulate the move by the computer.
 * @returns {number} - index of row, from which matches were taken
 */
function takeMatches() {
  console.assert(state.totalNrOfMatches() > 0);
  for (let i = 4; i >= 0; i--) {
    if (state.getRow(i) > 0) {
      let n = Math.min(3, state.getRow(i));
      if (n === state.totalNrOfMatches()) {
        n -= 1; //must not take all matches
      }
      state.decrRow(i,n);
      return i;
    }
  }
}

/**
 * Perform all state-transition actions that do not depend on the previous gameState.
 */
function enterGameState(newState) {
  switch (newState) {
    case state.gameBegin:
      state.initRows();
      showRows();
      ui_message.value = 'Click Start to begin the game.';
      break;
    case state.usersTurn:
      state.zeroNrOfMatchesTaken();
      state.selectRowIndex(-1);
      state.backupRows();
      ui_message.value = 'Take matches by clicking on them.';
      break;
    case state.userSelecting:
      let nMoreMatches = Math.min(3-state.getNrOfMatchesTaken(), state.getRow(state.getSelectedRowIndex()));
      if (nMoreMatches > 0) {
        ui_message.value = `You can take ${nMoreMatches} more match`
            + (nMoreMatches > 1 ? 'es' : '') + ' from this row.';
      } else if (state.getRow(state.getSelectedRowIndex()) > 0) {
        ui_message.value = 'You can take no more matches from this row.';
      } else {
        ui_message.value = 'You took the last match from this row.';
      }
      break;
    case state.appSelecting:
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
    case state.gameOver:
      ui_message.value = state.getUserWon() ? 'You won! :-)' : 'You lost :-(';
      break;
    default:
      console.assert(false);
  }
  state.setGameState(newState);
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
const uiButtons = document.getElementById("buttons");

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
  //ui_body.style.paddingTop = `${uiNavbar.getBoundingClientRect().height}px`; --> base
  //todo: use a css class
  //ui_body.style.paddingBottom = `${ui_OK.getBoundingClientRect().height * 3}px`;
  ui_body.style.paddingBottom = `${uiButtons.getBoundingClientRect().height}px`;
}

// helper functions

/**
 * Shows a row.
 * @param {Number} rowIndex - index of row.
 */
function showRow(rowIndex) {
  let n = state.getRow(rowIndex);
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
  switch (state.getGameState()) {
    case state.gameBegin:
      ui_OK.innerText = 'Start';
      enableButton("OK", true);
      enableButton("Cancel", false);
      enableButton("Quit", false);
      break;
    case state.usersTurn:
      ui_OK.innerText = 'OK';
      enableButton("OK", false);
      enableButton("Cancel", false);
      enableButton("Quit", true);
      break;
    case state.userSelecting:
      ui_OK.innerText = 'OK';
      enableButton("OK", true);
      enableButton("Cancel", true);
      enableButton("Quit", true);
      break;
    case state.gameOver:
      ui_OK.innerText = 'OK';
      enableButton("OK", true);
      enableButton("Cancel", false);
      enableButton("Quit", false);
      break;
    case state.appSelecting:
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
  console.log('home loadPage');
  console.log(tempVersion);
  //console.log(e);
  dynamicCss();
  // Restart the game, but only if a new browser session is starting.
  // Otherwise: recreate the display of the current state
  if (! state.getGameState()) {
    enterGameState(state.gameBegin);
  } else {
    enterGameState(state.getGameState());
    showRows();
  }
}

/**
 * Handle the event when user clicks on a row.
 */
function matches(e) {
  const t = e.target;
  console.log(`${t} clicked`);
  // the event only has an effect for the following 2 states
  if (state.getGameState() === state.userSelecting || state.getGameState() === state.usersTurn) {
    // additionally: the user must click on or near a symbol representing a match.
    if (t.nodeName === 'SPAN') {
      const p = t.parentElement;
      let i = p.id[3]; // the char at this index gives the row-index
      //console.log(i)
      i = Number(i);
      //console.log(ui_rows[i]);
      if (state.getGameState() === state.usersTurn) { // first click of this move
        state.selectRowIndex(i);
      }
      if (i === state.getSelectedRowIndex()) { // the same row as before was clicked, or first click
        if (state.getNrOfMatchesTaken() < 3) { // max not yet done
          state.decrRow(i,1);
          state.incrNrOfMatchesTaken(1);
          showRow(i);
        } else {
          showAlert('No more matches', 'You cannot take more than 3 matches. Click OK or Cancel!');
        }
      } else { // another row than the one before was clicked
        showAlert('Other row', 'To take matches from another row, click Cancel first!');
      }
      // remain in state state.userSelecting or enter it
      enterGameState(state.userSelecting);
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
  if (state.totalNrOfMatches() > 1) {
    let i = takeMatches();
    ui_rows[i].classList.remove('btn-black');
    ui_rows[i].classList.add('btn-warning');
    scrollToMiddle(ui_rows[i]);
    await wait(1000);
    showRow(i);
    await wait(1000);
    ui_rows[i].classList.remove('btn-warning');
    ui_rows[i].classList.add('btn-black');
    if (state.totalNrOfMatches() > 1) {
      enterGameState(state.usersTurn);
    } else {
      console.assert(state.totalNrOfMatches() === 1);
      state.setUserWon(false);
      enterGameState(state.gameOver);
    }
  } else {
    state.setUserWon(true);
    enterGameState(state.gameOver);
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
      state.setUserWon(true);
      enterGameState(state.gameOver);
    } else {
      let i = textJson.rowIndex;
      let n = textJson.numberOfMatches;
      console.log(`c:${c}, i:${i}, n:${n}`);
      ui_rows[i].classList.remove('btn-black');
      ui_rows[i].classList.add('btn-warning');
      scrollToMiddle(ui_rows[i]);
      await wait(1000);
      state.decrRow(i,n);
      showRow(i);
      await wait(1000);
      ui_rows[i].classList.remove('btn-warning');
      ui_rows[i].classList.add('btn-black');
      if (c === 0) {
        state.setUserWon(false);
        enterGameState(state.gameOver);
        //alert shows before row is updated, use setTimeout as workaround
        /*
        setTimeout(function(){
          state.setUserWon(false);
          enterGameState(state.gameOver);
          }, 1000);
         */
      } else {
        enterGameState(state.usersTurn);
      }
    }
  } else {
    console.assert('error' in textJson);
    showAlert("Error", textJson.error);
    state.setUserWon(true);
    enterGameState(state.gameOver);
  }
}

/**
 * Handle click on OK resp. Start.
 */
function ok(e) {
  console.log("ok clicked");
  if (state.getGameState() === state.gameBegin) {
    if (settings_.userBegins()) {
      enterGameState(state.usersTurn);
    } else {
      enterGameState(state.appSelecting);
    }
  } else if (state.getGameState() === state.userSelecting) {
    enterGameState(state.appSelecting);
  } else if (state.getGameState() === state.gameOver) {
    enterGameState(state.gameBegin);
  } else {
    console.log("ok has no effect")
  }
}

/**
 * Handle click on Cancel.
 */
function cancel(e) {
  console.log("cancel clicked")
  if (state.getGameState() === state.userSelecting) {
    // restore selected row
    state.restoreRow(state.getSelectedRowIndex());
    showRow(state.getSelectedRowIndex());
    // new state
    enterGameState(state.usersTurn);
  } else {
    console.log("cancel has no effect")
  }
}

/**
 * Handle Click on Quit.
 */
function quit(e) {
  console.log("quit clicked")
  if (state.getGameState() === state.userSelecting || state.getGameState() === state.usersTurn) {
    /*
    if (confirm("Quitting means you lost the game!")) {
      enterGameState(state.gameBegin);
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
  enterGameState(state.gameBegin);
}

console.log("init module home end");
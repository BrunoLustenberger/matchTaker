console.log("init module state begin"); //--use import.meta.url

// rows containing the matches
let rows;
let rows_previous;

export function initRows() {
  rows = [1,2,3,4,5];
  saveRows();
}

export function saveRows() {
  rows_previous = Array.from(rows);
}

export function nMatches() {
  return rows.reduce((total,num) => total + num, 0);
}

export function restoreRow(i) {
  rows[i] = rows_previous[i];
}

export function getRow(i) {
  return rows[i];
}

function setRow(i, n) {
  rows[i] = n;
}

export function decrRow(i, n) {
  rows[i] -= n;
}

//selected row
let selectedRowIndex; //todo: set to undefined or null, when not in use

export function selectRowIndex(i) {
  selectedRowIndex = i;
}

export function getSelectedRowIndex() {
  return selectedRowIndex;
}

//matches taken so far in user's move
let nMatchesTaken;

export function getNrOfMatchesTaken() {
  return nMatchesTaken;
}

export function zeroNrOfMatchesTaken() {
  nMatchesTaken = 0;
}

export function incrNrOfMatchesTaken(n) {
  nMatchesTaken += n;
}

// game states
export const gameBegin = 0, userSelecting = 1, appSelecting = 2, usersTurn = 3, gameOver = 4;
let gameState;

export function getGameState() {
  return gameState;
}

export function setGameState(gs) {
  gameState = gs;
}

// user won

let userWon;

export function getUserWon() {
  return userWon;
}

export function setUserWon(b) {
  userWon = b;
}

// later to settings
export const firstMoveByUser = true;
export const appLevel = 0; // smartness of the app as a player

console.log("init module state end");

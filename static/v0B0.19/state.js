console.log("init module state begin"); //--use import.meta.url

// game states

export const gameBegin = 0, usersTurn = 1, userSelecting = 2, appSelecting = 3, gameOver = 4;

export function getGameState() {
  return JSON.parse(sessionStorage.getItem('gameState'));
}

export function setGameState(gameState) {
  sessionStorage.setItem('gameState', JSON.stringify(gameState));
}

// rows containing the matches

export function initRows() {
  let rows = [1,2,3,4,5];
  sessionStorage.setItem('rows', JSON.stringify(rows));
  sessionStorage.setItem('rowsBackup', JSON.stringify(rows));
}

export function totalNrOfMatches() {
  let rows = JSON.parse(sessionStorage.getItem('rows'));
  return rows.reduce((total,num) => total + num, 0);
}

export function backupRows() {
  let rows = JSON.parse(sessionStorage.getItem('rows'));
  sessionStorage.setItem('rowsBackup', JSON.stringify(rows));
}

export function restoreRow(i) {
  let rows = JSON.parse(sessionStorage.getItem('rows'));
  let rowsBackup = JSON.parse(sessionStorage.getItem('rowsBackup'));
  rows[i] = rowsBackup[i];
  sessionStorage.setItem('rows', JSON.stringify(rows));
}

export function getRow(i) {
  let rows = JSON.parse(sessionStorage.getItem('rows'));
  return rows[i];
}

function setRow(i, n) {
  let rows = JSON.parse(sessionStorage.getItem('rows'));
  rows[i] = n;
  sessionStorage.setItem('rows', JSON.stringify(rows));
}

export function decrRow(i, n) {
  let rows = JSON.parse(sessionStorage.getItem('rows'));
  rows[i] -= n;
  sessionStorage.setItem('rows', JSON.stringify(rows));
}

//selected row

export function selectRowIndex(i) {
  sessionStorage.setItem('selectedRowIndex', JSON.stringify(i));
}

export function getSelectedRowIndex() {
  return JSON.parse(sessionStorage.getItem('selectedRowIndex'));
}

//matches taken so far in user's move

export function getNrOfMatchesTaken() {
  return JSON.parse(sessionStorage.getItem('nrOfMatchesTaken'));
}

export function zeroNrOfMatchesTaken() {
  sessionStorage.setItem('nrOfMatchesTaken', JSON.stringify(0))
}

export function incrNrOfMatchesTaken(n) {
  let nr = JSON.parse(sessionStorage.getItem('nrOfMatchesTaken'));
  nr += n;
  sessionStorage.setItem('nrOfMatchesTaken', JSON.stringify(nr));
}

// user won

export function getUserWon() {
  return JSON.parse(sessionStorage.getItem('userWon'));
}

export function setUserWon(b) {
  sessionStorage.setItem('userWon', JSON.stringify(b));
}

// todo: later to settings

export const appLevel = 0; // smartness of the app as a player

console.log("init module state end");

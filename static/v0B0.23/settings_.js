console.log('init module settings_');

// who begins

export const youBegin = 0, appBegins = 1;

export function setWhoBegins(beginner) {
  sessionStorage.setItem('whoBegins', JSON.stringify(beginner));
}

export function getWhoBegins() {
  let whoBegins = sessionStorage.getItem('whoBegins');
  if (!whoBegins) { // new session
    setWhoBegins(youBegin);
    whoBegins = sessionStorage.getItem('whoBegins');
  }
  return JSON.parse(whoBegins);
}

export function userBegins() {
  return getWhoBegins() === youBegin;
}

// howSmart

export const beDumb = 0, beMediocre = 1, beSmart = 2;

export function setHowSmart(level) {
  sessionStorage.setItem('howSmart', JSON.stringify(level));
}

export function getHowSmart() {
  let howSmart = sessionStorage.getItem('howSmart');
  if (!howSmart) { // new session
    setHowSmart(beMediocre);
    howSmart = sessionStorage.getItem('howSmart');
  }
  return JSON.parse(howSmart);
}

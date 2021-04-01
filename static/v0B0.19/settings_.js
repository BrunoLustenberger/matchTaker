console.log('init module settings_');

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

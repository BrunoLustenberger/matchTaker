console.log("init module settings begin"); //--use import.meta.url
//import {ui_body, showAlert} from "./base.js";
import * as ss from "./settings_.js"

// who begins

const uiWhoBegins = document.getElementById('whoBegins');
const uiWhoBeginsRadios = []; //indices defined in settings_
uiWhoBeginsRadios.push(document.getElementById('radioYou'));
uiWhoBeginsRadios.push(document.getElementById('radioApp'));

console.log(`uiWhoBegins ${uiWhoBegins}`);

uiWhoBegins.addEventListener('click', handleWhoBegins);

function handleWhoBegins(e) {
  console.log('who begins..');
  const t = e.target;
  console.log(`${t} clicked`);
  if (t.id === "radioYou") {
    console.log("you....");
    ss.setWhoBegins(ss.youBegin);
  } else if (t.id === "radioApp") {
    console.log("app....");
    ss.setWhoBegins(ss.appBegins);
  }
}

// page load handler

function handlePageLoad() {
  console.log("page loaded");
  uiWhoBeginsRadios[ss.getWhoBegins()].checked = true;
}

document.addEventListener('DOMContentLoaded', handlePageLoad);


console.log("init module settings end");

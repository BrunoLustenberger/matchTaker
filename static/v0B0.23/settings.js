console.log("init module settings begin"); //--use import.meta.url
//import {ui_body, showAlert} from "./base.js";
import * as ss from "./settings_.js"

// who begins

const uiWhoBegins = document.getElementById('whoBegins');
const uiWhoBeginsRadios = []; //indices defined in settings_
uiWhoBeginsRadios.push(document.getElementById('radioYou'));
uiWhoBeginsRadios.push(document.getElementById('radioApp'));

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

// how smart

const uiHowSmart = document.getElementById('howSmart');
const uiHowSmartRadios = []; //indices defined in settings_
uiHowSmartRadios.push(document.getElementById('radioDumb'));
uiHowSmartRadios.push(document.getElementById('radioMediocre'));
uiHowSmartRadios.push(document.getElementById('radioSmart'));

uiHowSmart.addEventListener('click', handleHowSmart);

function handleHowSmart(e) {
  console.log('how smart..');
  const t = e.target;
  console.log(`${t} clicked`);
  if (t.id === "radioDumb") {
    ss.setHowSmart(ss.beDumb);
  } else if (t.id === "radioMediocre") {
    ss.setHowSmart(ss.beMediocre);
  } else if (t.id === "radioSmart") {
    ss.setHowSmart(ss.beSmart);
  }
}

// page load handler

function handlePageLoad() {
  console.log("page loaded");
  uiWhoBeginsRadios[ss.getWhoBegins()].checked = true;
  uiHowSmartRadios[ss.getHowSmart()].checked = true;
}

document.addEventListener('DOMContentLoaded', handlePageLoad);

console.log("init module settings end");

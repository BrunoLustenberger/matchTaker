console.log("init module base");
// ui vars
export const ui_body = document.querySelector('body');
const uiNavbar = document.querySelector('.navbar');
const uiAlert = document.getElementById("modalAlert");
const uiAlertTitle = document.getElementById("modalAlertTitle");
const uiAlertDetail = document.getElementById("modalAlertDetail");

ui_body.style.paddingTop = `${uiNavbar.getBoundingClientRect().height}px`;

/**
 * Shows a modal alert dialog
 * @param {String} title - title resp. short message.
 * @param {String} detail - detailed or additional message.
 */
export function showAlert(title, detail) {
  //uiAlert.modal(); -- doesn't work
  uiAlertTitle.innerText = title;
  uiAlertDetail.innerText = detail;
  $("#modalAlert").modal(); //this works
}

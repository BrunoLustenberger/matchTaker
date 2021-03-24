console.log("init module utils");

export function wait(milliseconds) {
  console.log('wait ' + String(milliseconds));
  return new Promise(resolve => {
      setTimeout(() => {
          resolve()
      }, milliseconds)
  })
}

export function scrollToMiddle(element) {
  let box = element.getBoundingClientRect();
  let x = box.x + window.pageXOffset;
  let y = box.y + window.pageYOffset - window.innerHeight / 2;
  window.scrollTo(x,y);
}

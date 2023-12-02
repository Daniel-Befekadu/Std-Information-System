function disappearAfterSeconds(elementSelector, seconds) {
    const element = document.querySelector(elementSelector);
    if (!element) {
      console.error("Element with selector '" + elementSelector + "' not found.");
      return;
    }
  
    setTimeout(function() {
      element.style.display = "none";
    }, seconds * 1000);
  }
  
  disappearAfterSeconds(".message", 2);
  
  
// app/static/js/history.js

// tracks which 'month-button' has the date input. Value is name of month.
var dateInputTracker = "";

// if a 'month-button' is clicked, move the date input to the clicked 'month-button'
document.body.addEventListener('click', function (evt) {
    if (evt.target.classList.contains('month-button')) {
      dateInputTracker = target.innerHTML;
      moveDateInput(target);
    }
}, false);


// clears the date input from the document and appends it under element
function moveDateInput(element) {
  // // remove current date input
  // var dateInputElement = document.getElementById("dateInput");
  // dateInputElement.parentNode.removeChild(dateInputElement);

  // create date input under element


  // move the date input under element
  var dateInputElement = document.getElementById("dateInput");

}

<input type="date" name="date" id="dateInput" oninput="myFunction()">

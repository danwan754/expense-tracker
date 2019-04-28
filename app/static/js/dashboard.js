// Get the modal
var modal = document.getElementById('expense-modal');

// Get the button that opens the modal
var btn = document.getElementById("add-expense-button");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// // When the user clicks anywhere outside of the modal, close it
// window.onclick = function(event) {
//   if (event.target == modal) {
//     modal.style.display = "none";
//   }
// }



// submit new expense

// add-expense-submit-button



document.getElementById("add-expense-submit-button").addEventListener("click", function(event) {
  event.preventDefault();
  var addExpenseForm = document.getElementById("add-expense-form");

  // post new expense
  var data = new FormData(addExpenseForm);
  axios.post('/add-expense', data)

  /* display posted expense to today's expense table */
  .then(function (response) {
    if (response.status_code = 201) {
      var expenseTable = document.getElementsByClassName("today-expense-table")[0];
      var newRow = expenseTable.insertRow(2);
      var newCell = newRow.insertCell(0);
      newCell.innerHTML = response.data.item;
      newCell = newRow.insertCell(1);
      newCell.innerHTML = response.data.cost;
    }
    else {
      console.log(response.status_code);

    }
  })
  .catch(function (error) {
    console.log(error);
  })
  .then(function () {
    modal.style.display = "none";
  });
});

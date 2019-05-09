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



// post new expense for today and display new expense on today's expense table
document.getElementById("add-expense-submit-button").addEventListener("click", function(event) {
  event.preventDefault();
  var addExpenseError = document.getElementById("add-expense-error");
  var addExpenseForm = document.getElementById("add-expense-form");

  // post new expense
  var data = new FormData(addExpenseForm);
  axios.post('/add-expense', data)
  .then(function(response) {

    // display posted expense to today's expense table
    if (response.data.success) {
      var expenseTable = document.getElementsByClassName("today-expense-table")[0];
      var newRow = expenseTable.insertRow(2);
      var newCell = newRow.insertCell(0);
      newCell.innerHTML = response.data.item;
      newCell = newRow.insertCell(1);
      newCell.innerHTML = response.data.cost;
      modal.style.display = "none";
      addExpenseError.style.display = "none";
    }
    else {
      var errors = "";
      for (prop in response.data.errors) {
        for (item of response.data.errors[prop]) {
          errors += item + "\n";
        }
      }
      addExpenseError.innerHTML = errors;
      addExpenseError.style.display = "block";
    }
  })
  .catch(function(error) {
    console.log(error);
    addExpenseError.innerHTML = error;
    addExpenseError.style.display = "block";
  });
});


// post budgets
document.getElementById('edit-budget-button').addEvenListener('click', function(event) {
  event.preventDefault();
  var budgetError = document.getElementById('budget-error');
  var budgetForm = document.getElementById("edit-budget-form");
  var data = new FormData(budgetForm);
  axios.post('/edit-budget', data)
  .then(function(response) {

    // display the budgets
    if (response.data.success) {
      document.getElementById('budget-daily').innerHTML = 
    }
  })
})

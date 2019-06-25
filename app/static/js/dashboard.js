// app/static/js/dashboard.js


var addExpenseModal = document.getElementById('add-expense-modal');
var editBudgetModal = document.getElementById('edit-budget-modal');

// buttons that opens the add-expense and edit-budget modals
var addExpenseBtn = document.getElementById("add-expense-button");
var editBudgetBtn = document.getElementById("edit-budget-button");

// <span> elements that closes the modals
var closeAddExpense = document.getElementById("close-add-expense");
var closeEditBudget = document.getElementById("close-edit-budget");

// budget input fields
var dailyBudgetField = document.getElementById("dailyBudgetField");
var weeklyBudgetField = document.getElementById("weeklyBudgetField");
var monthlyBudgetField = document.getElementById("monthlyBudgetField");
var yearlyBudgetField = document.getElementById("yearlyBudgetField");

var dateAddExpenseField = document.getElementById('date');

var dateComponentsArr = new Date().toLocaleDateString().split('/');
var todayDate = dateComponentsArr[2] + "-" + dateComponentsArr[1] + "-" + dateComponentsArr[0];

// onclick listeners to open the modals
addExpenseBtn.onclick = function() {
  addExpenseModal.style.display = "block";
  // document.getElementById('date').value = new Date().toISOString().slice(0, 10);
  dateAddExpenseField.value = todayDate;

}
editBudgetBtn.onclick = function() {
  editBudgetModal.style.display = "block";
}

// onclick listeners to close the modals
closeAddExpense.onclick = function() {
  addExpenseModal.style.display = "none";
}
closeEditBudget.onclick = function() {
  editBudgetModal.style.display = "none";
}


// input listeners to update all the budget input fields when any field recieves input
dailyBudgetField.addEventListener("input", function() {
  var value = dailyBudgetField.value;
  weeklyBudgetField.value = (value * 7.0).toFixed(2);
  monthlyBudgetField.value = (value * 30.0).toFixed(2);
  yearlyBudgetField.value = (value * 365).toFixed(2);
});
weeklyBudgetField.addEventListener("input", function() {
  var value = weeklyBudgetField.value;
  var dailyValue = value / 7.0;
  dailyBudgetField.value = dailyValue.toFixed(2);
  monthlyBudgetField.value = (dailyValue * 30.0).toFixed(2);
  yearlyBudgetField.value = (dailyValue * 365).toFixed(2);
});
monthlyBudgetField.addEventListener("input", function() {
  var value = monthlyBudgetField.value;
  var dailyValue = value / 30.0;
  dailyBudgetField.value = dailyValue.toFixed(2);
  weeklyBudgetField.value = (dailyValue * 7.0).toFixed(2);
  yearlyBudgetField.value = (dailyValue * 365).toFixed(2);
});
yearlyBudgetField.addEventListener("input", function() {
  var value = yearlyBudgetField.value;
  var dailyValue = value / 365.0;
  dailyBudgetField.value = dailyValue.toFixed(2);
  weeklyBudgetField.value = (dailyValue * 7.0).toFixed(2);
  monthlyBudgetField.value = (dailyValue * 30.0).toFixed(2);
});

// post new expense for today and display new expense on today's expense table
document.getElementById("add-expense-submit-button").addEventListener("click", function(event) {
  event.preventDefault();
  var addExpenseError = document.getElementById("add-expense-error");
  var addExpenseForm = document.getElementById("add-expense-form");

  // post new expense
  var data = new FormData(addExpenseForm);
  axios.post('/api/users/1/expenses', data)
  .then(function(response) {

    // display posted expense to today's expense table
    if (response.status == 201) {
      var expenseTable = document.getElementsByClassName("today-expense-table")[0];
      var newRow = expenseTable.insertRow(2);
      var newCell = newRow.insertCell(0);
      newCell.innerHTML = response.data.item;
      newCell = newRow.insertCell(1);
      newCell.innerHTML = response.data.cost;
      addExpenseModal.style.display = "none";
      addExpenseError.style.display = "none";

      // update budget display
      var todayBudgetRemain = parseFloat(document.getElementById('budget-daily').innerHTML)
      var weekBudgetRemain = parseFloat(document.getElementById('budget-weekly').innerHTML)
      var monthBudgetRemain = parseFloat(document.getElementById('budget-monthly').innerHTML)
      document.getElementById('budget-daily').innerHTML = (todayBudgetRemain - response.data.cost).toFixed(2);
      document.getElementById('budget-weekly').innerHTML = (weekBudgetRemain - response.data.cost).toFixed(2);
      document.getElementById('budget-monthly').innerHTML = (monthBudgetRemain - response.data.cost).toFixed(2);
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
document.getElementById('edit-budget-submit-button').addEventListener('click', function(event) {
  event.preventDefault();
  var budgetError = document.getElementById('edit-budget-error');
  var budgetForm = document.getElementById("edit-budget-form");
  // var data = new FormData();
  // data.append('csrf_token', csrf_token);
  // data.append('dailyBudgetField', '1.0');
  var data = new FormData(budgetForm);
  axios.post('/edit-budget', data)
  .then(function(response) {

    // display the budgets
    if (response.status_code == 200) {
      document.getElementById('budget-daily').innerHTML = response.data.budget.today.toFixed(2);
      document.getElementById('budget-weekly').innerHTML = response.data.budget.week.toFixed(2);
      document.getElementById('budget-monthly').innerHTML = response.data.budget.month.toFixed(2);
      // document.getElementById('budget-yearly').innerHTML = response.data.budget.yearly;
      editBudgetModal.style.display = "none";
      editBudgetModal.style.display = "none";
    }
    else {
      var errors = "";
      for (prop in response.data.errors) {
        for (item of response.data.errors[prop]) {
          errors += item + "\n";
        }
      }
      budgetError.innerHTML = errors;
      budgetError.style.display = "block";
    }
  })
  .catch(function(error) {
    console.log(error);
    budgetError.innerHTML = error;
    budgetError.style.display = "block";
  });
});

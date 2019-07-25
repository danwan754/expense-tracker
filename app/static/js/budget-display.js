// app/static/js/budget-display.js

var editBudgetModal = document.getElementById('edit-budget-modal');

// buttons that opens the edit-budget modals
var editBudgetBtn = document.getElementById("edit-budget-button");

// <span> element that close the modal
var closeEditBudget = document.getElementById("close-edit-budget");

var addExpenseForm = document.getElementById("add-expense-form");

// budget input fields
var dailyBudgetField = document.getElementById("dailyBudgetField");
var weeklyBudgetField = document.getElementById("weeklyBudgetField");
var monthlyBudgetField = document.getElementById("monthlyBudgetField");
var yearlyBudgetField = document.getElementById("yearlyBudgetField");

editBudgetBtn.onclick = function() {
  editBudgetModal.style.display = "block";
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


// post budgets
document.getElementById('edit-budget-submit-button').addEventListener('click', function(event) {
  event.preventDefault();
  var budgetError = document.getElementById('edit-budget-error');
  var budgetForm = document.getElementById("edit-budget-form");
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


// update budgets display by subtracting a new cost
function subtractFromBudget(cost) {

  // update budget display
  var todayBudgetRemain = parseFloat(document.getElementById('budget-daily').innerHTML)
  var weekBudgetRemain = parseFloat(document.getElementById('budget-weekly').innerHTML)
  var monthBudgetRemain = parseFloat(document.getElementById('budget-monthly').innerHTML)
  document.getElementById('budget-daily').innerHTML = (todayBudgetRemain - cost).toFixed(2);
  document.getElementById('budget-weekly').innerHTML = (weekBudgetRemain - cost).toFixed(2);
  document.getElementById('budget-monthly').innerHTML = (monthBudgetRemain - cost).toFixed(2);
}

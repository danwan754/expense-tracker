// app/static/js/dashboard.js


var addExpenseModal = document.getElementById('add-expense-modal');
var editBudgetModal = document.getElementById('edit-budget-modal');

// buttons that opens the add-expense and edit-budget modals
var addExpenseBtn = document.getElementById("add-expense-button");
var editBudgetBtn = document.getElementById("edit-budget-button");

// <span> elements that closes the modals
var closeAddExpense = document.getElementById("close-add-expense");
var closeEditBudget = document.getElementById("close-edit-budget");

var addExpenseError = document.getElementById("add-expense-error");
var addExpenseForm = document.getElementById("add-expense-form");

// budget input fields
var dailyBudgetField = document.getElementById("dailyBudgetField");
var weeklyBudgetField = document.getElementById("weeklyBudgetField");
var monthlyBudgetField = document.getElementById("monthlyBudgetField");
var yearlyBudgetField = document.getElementById("yearlyBudgetField");

var dateAddExpenseField = document.getElementById('date');
var itemAddExpenseField = document.getElementById('item');
var costAddExpenseField = document.getElementById('cost');
var categoryExpenseField = document.getElementById('category');
var submitExpenseButton = document.getElementById("add-expense-submit-button");
var modalHeader = addExpenseModal.querySelector("h2");

// // get all the delete buttons in the today-expense table
// var deleteButtons = document.getElementsByClassName('delete-expense');

// get all the edit expense buttons in the today-expense table
var editButtons = document.getElementsByClassName('edit-expense');

var dateComponentsArr = new Date().toLocaleDateString().split('/');
var todayDate = dateComponentsArr[2] + "-" + dateComponentsArr[1] + "-" + dateComponentsArr[0];

// currently selected expense id
var currentExpenseID = null;

// onclick listeners to open the modals
addExpenseBtn.onclick = function() {
  submitExpenseButton.value = "Add";
  modalHeader.innerHTML = "Add Expense";
  addExpenseForm.reset();
  categoryExpenseField.value = null;
  addExpenseModal.style.display = "block";
  dateAddExpenseField.value = todayDate;
}
editBudgetBtn.onclick = function() {
  editBudgetModal.style.display = "block";
}

// onclick listeners to close the modals
closeAddExpense.onclick = function() {
  addExpenseError.style.display = "none";
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


// event listener to delete row on today-expense table
function addListenerToDeleteRow(element){
  element.addEventListener('click', function() {

    var row = element.parentNode.parentNode;

    // delete expense from server
    axios.delete('/api/users/expenses', {
      data: {
        id: row.id
      }
    })
    .then(response => {
      // delete the row
      row.remove();
    })
    .catch(error => {
      console.log(error)
    });

  });
}

// create a delete button component
function createDeleteButton() {
  var divEle = document.createElement('div');
  divEle.className = 'delete-expense';
  divEle.innerHTML = 'x';
  addListenerToDeleteRow(divEle);
  return divEle;
}

// create a edit button component for expense
function createEditButton() {
  var divEle = document.createElement('div');
  divEle.className = 'edit-expense';
  divEle.innerHTML = '<i class="fa fa-edit"></i>';
  addListenerToEditExpense(divEle);
  return divEle;
}


function openEditModal(id = 0) {
  addExpenseModal.style.display = "block";

  if (id) {
    modalHeader.innerHTML = "Edit Expense";
    var row = document.getElementById(id);
    itemAddExpenseField.value = row.cells[0].innerHTML;
    costAddExpenseField.value = row.cells[1].innerHTML;
    categoryExpenseField.value = row.getAttribute("data-category");
    submitExpenseButton.value = "Confirm Changes";
    console.log(row.getAttribute("data-category"));
  }
  else {
    modalHeader.innerHTML = "Add Expense";
  }

  dateAddExpenseField.value = todayDate;
}


// event listener to edit row on today-expense table
function addListenerToEditExpense(element){
  element.addEventListener('click', function() {

    var row = element.parentNode.parentNode;
    var id = row.id;
    currentExpenseID = id;
    openEditModal(id);
  });
}

// // fetch all of today's expenses
// function getTodayExpenses() {
//
//   axios.get('/api/users/expenses', {
//     params: {
//       date: todayDate
//     }
//   })
//   .then(response => {
//     todayExpenseArr = response.data.expenses;
//   })
// }


// // add event listener to every delete button in today-expense table
// for (var i=0; i<deleteButtons.length; i++) {
//   addListenerToDeleteRow(deleteButtons[i]);
// }

// add event listener to every edit button in today-expense table
for (var i=0; i<editButtons.length; i++) {
  addListenerToEditExpense(editButtons[i]);
}

// var expenseTable = document.getElementsByClassName("today-expense-table")[0];
// for (var i=0; i<expenseTable.rows.length; i++) {
//   console.log(expenseTable.rows[i].id + " : " + expenseTable.rows[i].getAttribute("data-category"));
// }

// post new expense for today and display on today's expense table
submitExpenseButton.addEventListener("click", function(event) {
  event.preventDefault();

  // post new expense
  var data = new FormData(addExpenseForm);


  // create new expense
  if (submitExpenseButton.value == "Add") {
    axios.post('/api/users/expenses', data)
    .then(function(response) {

      // display posted expense to today's expense table
      if (response.status == 201) {
        var expenseTable = document.getElementsByClassName("today-expense-table")[0];
        var newRow = expenseTable.insertRow(2);
        newRow.id = response.data.id;
        newRow.setAttribute("data-category", response.data.category);
        var newCell = newRow.insertCell(0);
        newCell.innerHTML = response.data.item;
        newCell = newRow.insertCell(1);
        newCell.innerHTML = response.data.cost;
        newCell = newRow.insertCell(2);
        var newEditButton = createEditButton();
        // var newDeleteButton = createDeleteButton();
        newCell.appendChild(newEditButton);

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
  }
  // modify existing expense
  else if (submitExpenseButton.value == "Confirm Changes") {
    axios.put('/api/users/expenses', data, {
      params:
      {
        id: currentExpenseID
      }
    })
    .then(response => {
      if (response.status == 200) {
        var row = document.getElementById(response.data.id);
        row.cells[0].innerHTML = response.data.item;
        row.cells[1].innerHTML = response.data.cost;
        row.setAttribute("data-category", response.data.category);

        addExpenseModal.style.display = "none";
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
  }
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

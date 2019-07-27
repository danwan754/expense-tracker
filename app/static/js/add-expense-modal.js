// app/static/js/add-expense-modal.js

var addExpenseModal = document.getElementById('add-expense-modal');
var addExpenseForm = document.getElementById("add-expense-form");

// button that opens the modal
var addExpenseBtn = document.getElementById("add-expense-button");

// <span> elements that closes the modal
var closeAddExpense = document.getElementById("close-add-expense");

var addExpenseError = document.getElementById("add-expense-error");

var dateAddExpenseField = document.getElementById('date');
var itemAddExpenseField = document.getElementById('item');
var costAddExpenseField = document.getElementById('cost');
var categoryExpenseField = document.getElementById('category');
var submitExpenseButton = document.getElementById("add-expense-submit-button");
var modalHeader = addExpenseModal.querySelector("h2");
var deleteExpenseBtn = document.getElementById("delete-expense-button");

// get all the edit expense buttons in the today-expense table
var editButtons = document.getElementsByClassName('edit-expense');

var dateComponentsArr = new Date().toLocaleDateString().split('/');

// chosenDate is today by default
var chosenDate = dateComponentsArr[2] + "-" + dateComponentsArr[1] + "-" + dateComponentsArr[0];

// currently selected expense id
var currentExpenseID = null;

// delete row on today-expense table
function deleteExpense() {
  var row = document.getElementById(currentExpenseID);

  // delete expense from server
  axios.delete('/api/users/expense', {
    data: {
      id: currentExpenseID
    }
  })
  .then(response => {
    // delete the row
    row.remove();
    addExpenseModal.style.display = "none";
  })
  .catch(error => {
    console.log(error)
  });
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
    deleteExpenseBtn.style.display = "block";
  }
  else {
    modalHeader.innerHTML = "Add Expense";
  }

  dateAddExpenseField.value = chosenDate;
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


// get expenses for provided date
function getDateExpenses(date) {
  return axios.get('/api/users/expenses', {
    params: {
      date: date
    }
  })
  .then(response => {
    return response.data;
  })
}


// add expense to table display
function appendExpenseToTable(tbody, obj) {
  var newRow = tbody.insertRow(0);
  newRow.id = obj.id;
  newRow.setAttribute("data-category", obj.category);
  var newCell = newRow.insertCell(0);
  newCell.innerHTML = obj.item;
  newCell = newRow.insertCell(1);
  newCell.innerHTML = obj.cost;
  newCell = newRow.insertCell(2);
  var newEditButton = createEditButton();
  newCell.appendChild(newEditButton);

  addExpenseModal.style.display = "none";
  addExpenseError.style.display = "none";
}

// post new expense for today and display on today's expense table
function addDateExpense(method) {

  // post new expense
  var data = new FormData(addExpenseForm);


  // create new expense
  if (method == 'post') {
    return axios.post('/api/users/expenses', data)
      .then(function(response) {

        // display posted expense to today's expense table
        if (response.status == 201) {
          var expenseTbody = document.getElementById("expense-table-tbody");
          appendExpenseToTable(expenseTbody, response.data);
          return response.data.cost;
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
  else if (method == 'put') {
    return axios.put('/api/users/expenses', data, {
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
          return response.data.cost;
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
}


// // serves as a proxy target object to signal an expense is deleted and to update the budget display
// var deleteExpenseTrigger = {};

// onclick listener to open the modal
addExpenseBtn.onclick = function() {
  submitExpenseButton.value = "Add";
  modalHeader.innerHTML = "Add Expense";
  addExpenseForm.reset();
  categoryExpenseField.value = null;
  addExpenseModal.style.display = "block";
  console.log(chosenDate);
  dateAddExpenseField.value = chosenDate;
  deleteExpenseBtn.style.display = "none";
}

// onclick listener to close the modal
closeAddExpense.onclick = function() {
  addExpenseError.style.display = "none";
  addExpenseModal.style.display = "none";
  console.log('close');
}

// add event listener to every edit button in today-expense table
for (var i=0; i<editButtons.length; i++) {
  addListenerToEditExpense(editButtons[i]);
}

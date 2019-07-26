// app/static/js/dashboard.js

// var deleteExpenseTriggerProxy = new Proxy(deleteExpenseTrigger, {
//   set: function(target, key, value) {
//     target[key] = value;
//     return;
//   }
// });

// listen for deleteExpenseBtn onclick
document.getElementById("delete-expense-button").addEventListener("click", () => {
  var cost = document.getElementById(currentExpenseID).cells[1].innerHTML;
  console.log("cost: " + cost);

  // delete expense row in today-expense-table
  deleteExpense();

  // add the cost of the removed expense back to the displayed budgets
  subtractFromBudget(-1 * cost);
})



// post new expense for today and display on today's expense table
submitExpenseButton.addEventListener("click", async function(event) {
  event.preventDefault();

  // post new expense
  var data = new FormData(addExpenseForm);

  // create new expense
  if (submitExpenseButton.value == "Add") {
    var cost = await getDateExpenses('get');
    if (cost) {
      subtractFromBudget(cost);
    }
  }
  // modify existing expense
  else if (submitExpenseButton.value == "Confirm Changes") {
    var oldCost = document.getElementById(currentExpenseID).cells[1].innerHTML;
    var cost = await getDateExpenses('put');
    if (cost) {
      cost = cost - oldCost;
      subtractFromBudget(cost);
    }
  }
});

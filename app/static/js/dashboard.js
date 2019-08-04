// app/static/js/dashboard.js


// listen for deleteExpenseBtn onclick
document.getElementById("delete-expense-button").addEventListener("click", async () => {
  var cost = document.getElementById(currentExpenseID).cells[1].innerHTML;

  // delete expense row in today-expense-table
  await deleteExpense();

  // add the cost of the removed expense back to the displayed budgets
  subtractFromBudget(-1 * cost);

  // setTimeout(fetchAndDisplaySavings(), 4000);
  // update savings display
  subtractFromSavings(-1 * cost);
  // fetchAndDisplaySavings();
})



// post new expense for today and display on today's expense table
submitExpenseButton.addEventListener("click", async function(event) {
  event.preventDefault();

  // post new expense
  var data = new FormData(addExpenseForm);

  // create new expense
  if (submitExpenseButton.value == "Add") {
    var cost = await addDateExpense('post');
    if (typeof cost == "number") {
      subtractFromBudget(cost);
      fetchAndDisplaySavings();
    }
  }
  // modify existing expense
  else if (submitExpenseButton.value == "Confirm Changes") {
    var oldCost = document.getElementById(currentExpenseID).cells[1].innerHTML;
    var cost = await addDateExpense('put');
    if (typeof cost == "number") {
      cost = cost - oldCost;
      subtractFromBudget(cost);
      fetchAndDisplaySavings();
    }
  }
});

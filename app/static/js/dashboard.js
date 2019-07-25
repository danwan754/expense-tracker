




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

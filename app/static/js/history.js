// app/static/js/history.js

var toggleDateRange = document.getElementById("toggle-range");
var toggleSingleDate = document.getElementById("toggle-single");
var toggleExpenseSavingModeBtns = document.getElementsByClassName("mode-button");

var expenseSummaryContainers = document.getElementsByClassName("savings-expense-container");
var chartSummaryContainers = document.getElementsByClassName("chart-value");

document.getElementById('expense-table-title').innerHTML = "Expenses";

// set the background-color of the Savings button as active
toggleExpenseSavingModeBtns[0].style.backgroundColor = "#008ae6";

// default toggle is single date selection mode
toggleSingleDate.style.backgroundColor = "#99cfff";

// months in a year
monthArr = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
  'August', 'September', 'October', 'November', 'December'];

var todayDate = new Date();
var yearChart = null;
var monthChart = null;
var dayChart = null;


const mode = {
  SAVINGS: "Savings",
  EXPENSES: "Expenses",
  ANALYTICS: "Analytics"
}

var currentMode = mode.SAVINGS;



google.charts.load('current', {packages: ['corechart', 'bar']});
google.charts.setOnLoadCallback(() => {
  yearChart = new google.visualization.BarChart(document.getElementById('year-chart'));
  monthChart = new google.visualization.BarChart(document.getElementById('month-chart'));
  dayChart = new google.visualization.BarChart(document.getElementById('date-chart'));
});

function drawChart(date, data, period) {

  var initialChart = [['Category', 'Percentage of Total Expense']];
  chartData = google.visualization.arrayToDataTable(initialChart.concat(data));

  var options = {
    title: date,
    chartArea: {
      left: 100,
      width: '80%',
    },
    hAxis: {
      title: '% of Expenses',
      minValue: 0,
      maxValue: 100
    },
    vAxis: {
      title: 'Category'
    },
    legend: {
      position: 'none'
    }
  };

  if (period == 'day') {
    dayChart.draw(chartData, options);
  }
  else if (period == 'month') {
    monthChart.draw(chartData, options);
  }
  else {
    yearChart.draw(chartData, options);
  }
}

// hide either the expense/savings or analytics <div>, and show the other
function hidePrevMode() {
  if (currentMode == mode.ANALYTICS) {
    for (var i=0; i<expenseSummaryContainers.length; i++) {
      expenseSummaryContainers[i].style.display = 'none';
    }
    for (var i=0; i<chartSummaryContainers.length; i++) {
      chartSummaryContainers[i].style.display = 'block';
    }
  }
  else {
    for (var i=0; i<expenseSummaryContainers.length; i++) {
      expenseSummaryContainers[i].style.display = 'block';
    }
    for (var i=0; i<chartSummaryContainers.length; i++) {
      chartSummaryContainers[i].style.display = 'none';
    }
  }
}

function updateMonthSavingsDisplay(heading, value) {
  document.getElementById("month-savings-header").innerHTML = heading;
  document.getElementById("month-savings-value").innerHTML = value;
}

function updateDateSavingsDisplay(heading, value) {

  document.getElementById("date-savings-header").innerHTML = heading;
  document.getElementById("date-savings-value").innerHTML = value.toLocaleString();
}

function updateYearSavingsDisplay(heading, value) {
  document.getElementById("year-savings").innerHTML = heading;
  document.getElementById("year-savings-value").innerHTML = value;
}


// fetch chart data
function getChartData(date) {

  return axios.get('/day-expense-chart', {
    params: {
      date: date
    }
  })
  .then((response) => {
    if (response.status == 200) {
      var chartData = response.data.chartData;
      return chartData;
    }
  });
}

// fetch chart data for selected date and display
async function getAndDisplayChartForDate(year, month, day) {

  var dataArr = await getChartData(chosenDate);
  date = monthArr[month] + " " + day + ", " + year;
  console.log(date);
  drawChart(date, dataArr, 'day');
}

// fetch data for savings or expenses depending on endpoint provided
function fetchDateData(year, month, day, endpoint) {

  return axios.get(endpoint, {
    params: {
      year: year,
      month: month + 1,
      day: day,
    }
  })
  .then(function(response) {
    var heading = monthArr[month] + " " + day + ", " + year;
    var value = response.data.savings;
    return [heading, value];
  });
}

// wrapper to fetch and display the selected mode data for given date
async function getModeDateDataAndDisplay(year, month, day) {

  var endpoint = '';
  if (currentMode == mode.SAVINGS) {
    endpoint = '/day-savings';
  }
  else if (currentMode == mode.EXPENSES) {
    endpoint = '/day-expenses';
  }

  var headAndValue = await fetchDateData(year, month, day, endpoint);
  updateDateSavingsDisplay(headAndValue[0], headAndValue[1]);
}


// fetch and display savings for date range
function fetchDateRangeData(year1, year2, month1, month2, day1, day2, endpoint) {
  return axios.get(endpoint, {
    params: {
      year1: year1,
      year2: year2,
      month1: month1 + 1,
      month2: month2 + 1,
      day1: day1,
      day2: day2,
    }
  })
  .then(function(response) {
    var heading = monthArr[month1] + " " + day1 + ", " + year1 + "  -  " + monthArr[month2] + " " + day2 + ", " + year2;
    var value = response.data.savings.toLocaleString();
    return [heading, value];
  });
}


// fetch and display chart data for date range
async function getModeDateRangeChartDataAndDisplay(date1, date2) {

  var data = await axios.get('/date-range-chart', {
    params: {
      start: date1,
      end: date2
    }
  })
  .then((response) => {
    return response.data.chartData;
  });

  var date = date1 + " to " + date2;
  drawChart(date, data, 'day');
}

// wrapper to fetch and display the selected mode data for given date range
async function getModeDateRangeDataAndDisplay(year1, year2, month1, month2, day1, day2) {
  var endpoint = '';
  if (currentMode == mode.SAVINGS) {
    endpoint = '/date-range-savings';
  }
  else if (currentMode == mode.EXPENSES) {
    endpoint = '/date-range-expenses';
  }

  var headAndValue = await fetchDateRangeData(year1, year2, month1, month2, day1, day2, endpoint);
  updateDateSavingsDisplay(headAndValue[0], headAndValue[1]);
}


function fetchMonthData(month, year, endpoint) {
  return axios.get(endpoint, {
    params: {
      month: month,
      year: year
    }
  })
  .then(function(response) {
    var heading = monthArr[month - 1] + " " + year;
    var value = response.data.savings.toLocaleString();
    return [heading, value];
  });
}


// wrapper to fetch and display the selected mode data for given month and year
async function getModeMonthDataAndDisplay(month, year) {

  var endpoint = '';
  if (currentMode == mode.SAVINGS) {
    endpoint = '/month-savings';
  }
  else if (currentMode == mode.EXPENSES) {
    endpoint = '/month-expenses';
  }
  var headingAndValue = await fetchMonthData(month, year, endpoint);
  updateMonthSavingsDisplay(headingAndValue[0], headingAndValue[1]);
}

async function getChartMonthDataAndDisplay(month, year) {
   var data = await axios.get('/month-chart', {
     params: {
       month: month,
       year: year
     }
   })
   .then((res) => {
     return res.data.chartData;
   });

   var date = monthArr[month - 1];
   drawChart(date, data, 'month');
}

async function getChartYearDataAndDisplay(year) {
   var data = await axios.get('/year-chart', {
     params: {
       year: year
     }
   })
   .then((res) => {
     return res.data.chartData;
   });

   var date = year;
   drawChart(date, data, 'year');
}


// wrapper to fetch and display the selected mode data for given year
async function getModeYearDataAndDisplay(year) {

  var endpoint = '';
  if (currentMode == mode.SAVINGS) {
    endpoint = '/year-savings';
  }
  else if (currentMode == mode.EXPENSES) {
    endpoint = '/year-expenses';
  }
  var headingAndValue = await fetchYearData(year, endpoint);
  updateYearSavingsDisplay(headingAndValue[0], headingAndValue[1]);
}


function fetchYearData(year, endpoint) {
  return axios.get(endpoint, {
    params: {
      year: year
    }
  })
  .then(function(response) {
    thisYear = new Date().getFullYear();
    heading = year;

    if (thisYear == year) {
      heading = year + " Year-To-Date";
    }
    var value = response.data.savings.toLocaleString();
    return [heading, value];
  });
}


// fetch expenses for selected date and display on expense table
async function getAndDisplayExpensesForDate() {
  if (currentMode == mode.EXPENSES && calendar.config.mode == 'single') {
    document.getElementById("history-bottom-expense-container").style.display = "block";
  }
  var expenseTbody = document.getElementById("expense-table-tbody");

  // clear the table of all expenses
  expenseTbody.innerHTML = '';

  var expenseObjArr = await getDateExpenses(chosenDate);

  for (var i=0; i<expenseObjArr.length; i++) {
    appendExpenseToTable(expenseTbody, expenseObjArr[i]);
  }
}


// change the background colors of active mode button (element) and the other 2 modes
function setModeActive(element) {
  for (var i=0; i<toggleExpenseSavingModeBtns.length; i++) {
    toggleExpenseSavingModeBtns[i].style.backgroundColor = "#99d6ff";
  }
  element.style.backgroundColor = "#008ae6";
}

// change the display to data for active mode
function updateModeDisplay(element, calendar) {

  switch (element.innerHTML) {
    case mode.EXPENSES:
      currentMode = mode.EXPENSES;
      displayExpenseMode(calendar);
      break;

    case mode.SAVINGS:
      currentMode = mode.SAVINGS;
      displaySavingsMode(calendar);
      break;

    default:
      currentMode = mode.ANALYTICS;
      displayAnalyticsMode(calendar);
  }
}


// invoke calendar functions to update data for mode display
function invokeCalendarUpdate(calendar) {
  calendar.config.onMonthChange[0](calendar.selectedDates, calendar.dateStr, calendar);
  calendar.config.onYearChange[0](calendar.selectedDates, calendar.dateStr, calendar);
  calendar.config.onChange[0](calendar.selectedDates, calendar.dateStr, calendar);
}

// set display to analytics mode
function displayAnalyticsMode(calendar) {

  document.getElementById("summary-header").innerHTML = 'Total Expenditure in Categories';

  hidePrevMode();
  document.getElementById("history-bottom-expense-container").style.display = "none";

  invokeCalendarUpdate(calendar);
}



// set display to expense mode
function displayExpenseMode(calendar) {

  hidePrevMode();
  document.getElementById("summary-header").innerHTML = "Expenses";

  if (!calendar.selectedDates[0]) {
    calendar.selectedDates[0] = todayDate;
  }
  invokeCalendarUpdate(calendar);
}

// set display to savings mode
function displaySavingsMode(calendar) {

  hidePrevMode();
  document.getElementById("summary-header").innerHTML = "Savings";

  if (!calendar.selectedDates[0]) {
    calendar.selectedDates[0] = todayDate;
  }
  invokeCalendarUpdate(calendar);

  document.getElementById("history-bottom-expense-container").style.display = "none";
}


// subtract the cost from expense summary display
function subtractFromExpenseSummary(cost) {
  if (typeof cost == "number") {
    var yearSummary = parseFloat(document.getElementById('year-savings-value').innerHTML);
    var monthSummary = parseFloat(document.getElementById('month-savings-value').innerHTML);
    var dateSummary = parseFloat(document.getElementById('date-savings-value').innerHTML);
    document.getElementById("year-savings-value").innerHTML = (yearSummary + cost).toFixed(2);
    document.getElementById('month-savings-value').innerHTML = (monthSummary + cost).toFixed(2);
    document.getElementById('date-savings-value').innerHTML = (dateSummary + cost).toFixed(2);
  }
}


// listen for click on button to delete expense from table
document.getElementById("delete-expense-button").addEventListener("click", () => {
  var cost = document.getElementById(currentExpenseID).cells[1].innerHTML;

  // delete expense row in today-expense-table
  deleteExpense();

  // add the cost of the removed expense back to the displayed budgets
  subtractFromExpenseSummary(-1 * cost);
});

// post new expense for date and display on today's expense table
submitExpenseButton.addEventListener("click", async function(event) {
  event.preventDefault();

  // post new expense
  var data = new FormData(addExpenseForm);

  // create new expense
  if (submitExpenseButton.value == "Add") {
    var cost = await addDateExpense('post');
    if (typeof cost == "number") {
      subtractFromExpenseSummary(cost);
    }
  }
  // modify existing expense
  else if (submitExpenseButton.value == "Confirm Changes") {
    var oldCost = document.getElementById(currentExpenseID).cells[1].innerHTML;
    var cost = await addDateExpense('put');
    if (typeof cost == "number") {
      cost = cost - oldCost;
      subtractFromExpenseSummary(cost);
    }
  }
});



calendarOptions = {
  minDate: minDate, // minDate declared in history.html
  maxDate: todayDate,
  // maxDate: new Date(2020, 3, 1), // for testing
  defaultDate: todayDate,
  altInput: true,
  altFormat: "F j, Y",
  dateFormat: "Y-m-d",
  inline: true, // keep calendar open

  onMonthChange: function(selectedDates, dateStr, instance) {
    selectedMonth = instance.currentMonth + 1;
    selectedYear = instance.currentYear;
    if (currentMode == mode.ANALYTICS) {
      getChartMonthDataAndDisplay(selectedMonth, selectedYear);
    }
    else {
      getModeMonthDataAndDisplay(selectedMonth, selectedYear);
    }
  },

  onYearChange: function(selectedDates, dateStr, instance) {
    selectedMonth = instance.currentMonth + 1;
    selectedYear = instance.currentYear;
    if (currentMode == mode.ANALYTICS) {
      getChartYearDataAndDisplay(selectedYear);
      getChartMonthDataAndDisplay(selectedMonth, selectedYear);
    }
    else {
      getModeYearDataAndDisplay(selectedYear);
      getModeMonthDataAndDisplay(selectedMonth, selectedYear);
    }
  },

  onChange: function(selectedDates, dateStr, instance) {

    // wait for two selected dates if calendar is in range mode
    if (instance.config.mode == "range") {
      chosenDate = null;
      if (selectedDates.length < 2) {
        return;
      }
      year2 = selectedDates[1].getFullYear();
      month2 = selectedDates[1].getMonth();
      day2 = selectedDates[1].getDate();
      var date2 = year2.toString() + "-" + (month2 + 1).toString() + "-" + day2.toString();
    }

    if (selectedDates[0]) {
      year = selectedDates[0].getFullYear();
      month = selectedDates[0].getMonth();
      day = selectedDates[0].getDate();
    }
    else {
      year = todayDate.getFullYear();
      month = todayDate.getMonth();
      day = todayDate.getDate();
    }
    var date1 = year.toString() + "-" + (month + 1).toString() + "-" + day.toString();

    if (instance.config.mode == "single") {
      chosenDate = date1;
      if (currentMode == mode.ANALYTICS) {
        getAndDisplayChartForDate(year, month, day);
        return;
      }

      getModeDateDataAndDisplay(year, month, day);

      if (currentMode == mode.EXPENSES) {
        getAndDisplayExpensesForDate();
      }
    }
    else if (currentMode == mode.ANALYTICS) {
      getModeDateRangeChartDataAndDisplay(date1, date2);
    }
    else {
      getModeDateRangeDataAndDisplay(year, year2, month, month2, day, day2);
    }
  }

}

// initializes the calendar
var calendar = flatpickr("#date-input", calendarOptions);

// highlights the date range button if it is active
toggleDateRange.addEventListener("click", function() {
  toggleDateRange.style.backgroundColor = "#99cfff";
  toggleSingleDate.style.backgroundColor = "#FFFFFF";
  calendar.config.mode = "range";
  calendar.clear();

  // do not show the expense table when in range mode
  document.getElementById("history-bottom-expense-container").style.display = "none";
});

// highlight the single date selection button if it is active
toggleSingleDate.addEventListener("click", function() {
  toggleDateRange.style.backgroundColor = "#FFFFFF";
  toggleSingleDate.style.backgroundColor = "#99cfff";
  calendar.config.mode = "single";
});

// add listeners to detect what mode is active
for (var i=0; i<toggleExpenseSavingModeBtns.length; i++) {
  toggleExpenseSavingModeBtns[i].addEventListener("click", function() {
    setModeActive(this);
    updateModeDisplay(this, calendar);
  });
}

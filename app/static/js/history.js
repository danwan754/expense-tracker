// app/static/js/history.js

var toggleDateRange = document.getElementById("toggle-range");
var toggleSingleDate = document.getElementById("toggle-single");
var toggleExpenseSavingModeBtns = document.getElementsByClassName("mode-button");

// default toggle is single date selection mode
toggleSingleDate.style.backgroundColor = "#99cfff";

// months in a year
monthArr = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
  'August', 'September', 'October', 'November', 'December'];

var todayDate = new Date();


const mode = {
  SAVINGS: "Savings",
  EXPENSES: "Expenses",
  DUAL: "Dual"
}

var currentMode = mode.SAVINGS;


function updateMonthSavingsDisplay(heading, value) {
  document.getElementById("month-savings-header").innerHTML = heading;
  document.getElementById("month-savings-value").innerHTML = value;
}


function updateDateSavingsDisplay(heading, value) {
  document.getElementById("date-savings-header").innerHTML = heading;
  document.getElementById("date-savings-value").innerHTML = value;
}

function updateYearSavingsDisplay(heading, value) {
  document.getElementById("year-savings").innerHTML = heading;
  document.getElementById("year-savings-value").innerHTML = value;
}

// // fetch and display savings for date
// function getDateSavingsAndUpdateDisplay(year, month, day) {
//   axios.get('/day-savings', {
//     params: {
//       year: year,
//       month: month + 1,
//       day: day,
//     }
//   })
//   .then(function(response) {
//     var heading = monthArr[month] + " " + day + ", " + year;
//     var value = response.data.savings.toLocaleString();
//     updateDateSavingsDisplay(heading, value);
//   });
// }

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
    var value = response.data.savings.toLocaleString();
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
  console.log(headAndValue);
  updateDateSavingsDisplay(headAndValue[0], headAndValue[1]);

}


// fetch and display savings for date range
function getDateRangeSavingsAndUpdateDisplay(year1, year2, month1, month2, day1, day2) {
  axios.get('/date-range-savings', {
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
    updateDateSavingsDisplay(heading, value);
  });
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



// change the background colors of active mode button (element) and the other 2 modes
function setModeActive(element) {
  for (var i=0; i<toggleExpenseSavingModeBtns.length; i++) {
    toggleExpenseSavingModeBtns[i].style.backgroundColor = "#99d6ff";
  }
  element.style.backgroundColor = "#008ae6";
}

// change the display to data for active mode
function updateModeDisplay(element, calendar) {
  currentMode = element.innerHTML;

  switch (currentMode) {
    case mode.EXPENSES:
      displayExpenseMode(calendar);
      break;

    case mode.DUAL:
      displayDualMode(calendar);
      break;

    default:
      displaySavingsMode(calendar);
  }
}

// set display to expense mode
function displayExpenseMode(calendar) {

  document.getElementById("summary-header").innerHTML = "Expenses";
  calendar.config.onMonthChange[0](calendar.selectedDates, calendar.dateStr, calendar);
  calendar.config.onYearChange[0](calendar.selectedDates, calendar.dateStr, calendar);
  calendar.config.onChange[0](calendar.selectedDates, calendar.dateStr, calendar);
}

// set display to savings mode
function displaySavingsMode(calendar) {
  document.getElementById("summary-header").innerHTML = "Savings";
  calendar.config.onMonthChange[0](calendar.selectedDates, calendar.dateStr, calendar);
  calendar.config.onYearChange[0](calendar.selectedDates, calendar.dateStr, calendar);
  calendar.config.onChange[0](calendar.selectedDates, calendar.dateStr, calendar);
}


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
    getModeMonthDataAndDisplay(selectedMonth, selectedYear);
  },

  onYearChange: function(selectedDates, dateStr, instance) {
    selectedMonth = instance.currentMonth + 1;
    selectedYear = instance.currentYear;
    getModeYearDataAndDisplay(selectedYear);
    getModeMonthDataAndDisplay(selectedMonth, selectedYear);
  },

  onChange: function(selectedDates, dateStr, instance) {

    // wait for two selected dates if calendar is in range mode
    if (instance.config.mode == "range") {
      if (selectedDates.length < 2) {
        return;
      }
      year2 = selectedDates[1].getFullYear();
      month2 = selectedDates[1].getMonth();
      day2 = selectedDates[1].getDate();
    }

    year = selectedDates[0].getFullYear();
    month = selectedDates[0].getMonth();
    day = selectedDates[0].getDate();

    if (instance.config.mode == "single") {
      getModeDateDataAndDisplay(year, month, day);
    }
    else {
      getDateRangeSavingsAndUpdateDisplay(year, year2, month, month2, day, day2);
    }
  },

}

// initializes the calendar
var calendar = flatpickr("#date-input", calendarOptions);

// highlights the date range button if it is active
toggleDateRange.addEventListener("click", function() {
  toggleDateRange.style.backgroundColor = "#99cfff";
  toggleSingleDate.style.backgroundColor = "#FFFFFF";
  calendar.config.mode = "range";
  calendar.clear();
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

// app/static/js/history.js

var toggleDateRange = document.getElementById("toggle-range");
var toggleSingleDate = document.getElementById("toggle-single");

// default toggle is single date selection mode
toggleSingleDate.style.backgroundColor = "#99cfff";

// months in a year
monthArr = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
  'August', 'September', 'October', 'November', 'December'];

var todayDate = new Date();


function updateMonthSavingsDisplay(heading, value) {
  // document.getElementById("month-summary-div").style.visibility = "visible";
  document.getElementById("month-savings-header").innerHTML = heading + " Savings";
  document.getElementById("month-savings-value").innerHTML = value;
}


function updateDateSavingsDisplay(heading, value) {
  // document.getElementById("date-summary-div").style.visibility = "visible";
  document.getElementById("date-savings-header").innerHTML = heading + " Savings";
  document.getElementById("date-savings-value").innerHTML = value;
}


// fetch and display savings for date
function getDateSavings(year, month, day) {
  axios.get('/day-savings', {
    params: {
      year: year,
      month: month,
      day: day,
    }
  })
  .then(function(response) {
    var heading = monthArr[month] + " " + day + ", " + year;
    var value = response.data.savings;
    updateDateSavingsDisplay(heading, value);
  });
}

// fetch and display month savings
function getMonthSavings(month, year) {
  axios.get('/month-savings', {
    params: {
      month: month,
      year: year,
    }
  })
  .then(function(response) {
    var heading = monthArr[month - 1] + " " + year;
    var value = response.data.savings;
    updateMonthSavingsDisplay(heading, value);
  });
}

// fetch and display year savings
function getYearSavings(year) {
  axios.get('/year-savings', {
    params: {
      year: year,
    }
  })
  .then(function(response) {
    thisYear = new Date().getFullYear();
    heading = year + " Savings";

    if (thisYear == year) {
      heading = year + " Year-To-Date Savings";
    }
    document.getElementById("year-savings").innHTML = heading;
    document.getElementById("year-savings-value").innerHTML = response.data.savings;
  });
}

calendarOptions = {
  minDate: minDate, // minDate declared in history.html
  maxDate: todayDate,
  // maxDate: new Date(2020, 3, 1),
  defaultDate: todayDate,
  altInput: true,
  altFormat: "F j, Y",
  dateFormat: "Y-m-d",
  inline: true, // keep calendar open

  onMonthChange: function(selectedDates, dateStr, instance) {
    selectedMonth = instance.currentMonth + 1;
    selectedYear = instance.currentYear;
    getMonthSavings(selectedMonth, selectedYear);
  },

  onYearChange: function(selectedDates, dateStr, instance) {
    selectedMonth = instance.currentMonth + 1;
    selectedYear = instance.currentYear;
    getYearSavings(selectedYear);
    getMonthSavings(selectedMonth, selectedYear);
  },

  onChange: function(selectedDates, dateStr, instance) {
    year = selectedDates[0].getFullYear();
    month = selectedDates[0].getMonth();
    day = selectedDates[0].getDate();
    savings = getDateSavings(year, month, day);
  },

}

var calendar = flatpickr("#date-input", calendarOptions);


toggleDateRange.addEventListener("click", function() {
  toggleDateRange.style.backgroundColor = "#99cfff";
  toggleSingleDate.style.backgroundColor = "#FFFFFF";
  calendar.config.mode = "range";
});

toggleSingleDate.addEventListener("click", function() {
  toggleDateRange.style.backgroundColor = "#FFFFFF";
  toggleSingleDate.style.backgroundColor = "#99cfff";
  calendar.config.mode = "single";
});

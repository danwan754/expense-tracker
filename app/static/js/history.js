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
function getDateSavingsAndUpdateDisplay(year, month, day) {
  axios.get('/day-savings', {
    params: {
      year: year,
      month: month + 1,
      day: day,
    }
  })
  .then(function(response) {
    var heading = monthArr[month] + " " + day + ", " + year;
    var value = response.data.savings;
    updateDateSavingsDisplay(heading, value);
  });
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
    var value = response.data.savings;
    updateDateSavingsDisplay(heading, value);
  });
}


// fetch and display month savings
function getMonthSavingsAndUpdateDisplay(month, year) {
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
function getYearSavingsAndUpdateDisplay(year) {
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
    getMonthSavingsAndUpdateDisplay(selectedMonth, selectedYear);
  },

  onYearChange: function(selectedDates, dateStr, instance) {
    selectedMonth = instance.currentMonth + 1;
    selectedYear = instance.currentYear;
    getYearSavingsAndUpdateDisplay(selectedYear);
    getMonthSavingsAndUpdateDisplay(selectedMonth, selectedYear);
  },

  onChange: function(selectedDates, dateStr, instance) {

    // wait for two selected dates if calendar is in range mode
    if (instance.config.mode == "range") {
      if (selectedDates.length < 2) {
        console.log("1");
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
      getDateSavingsAndUpdateDisplay(year, month, day);
    }
    else {
      getDateRangeSavingsAndUpdateDisplay(year, year2, month, month2, day, day2);
    }

    // for (var i=0; i<selectedDates.length; i++) {
    //   console.log(selectedDates[i]);
    // }
  },

}

var calendar = flatpickr("#date-input", calendarOptions);


toggleDateRange.addEventListener("click", function() {
  toggleDateRange.style.backgroundColor = "#99cfff";
  toggleSingleDate.style.backgroundColor = "#FFFFFF";
  calendar.config.mode = "range";
  calendar.clear();
});

toggleSingleDate.addEventListener("click", function() {
  toggleDateRange.style.backgroundColor = "#FFFFFF";
  toggleSingleDate.style.backgroundColor = "#99cfff";
  calendar.config.mode = "single";
});

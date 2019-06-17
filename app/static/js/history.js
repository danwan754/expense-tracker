// app/static/js/history.js

// // track if date values were changed
// var dateChangeDic = {
//   'isChangeDay': false,
//   'isChangeMonth': false,
//   'isChangeYear': false
// }

// months in a year
monthArr = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
  'August', 'September', 'October', 'November', 'December'];

var todayDate = new Date();

function createSummaryContainer(heading, value) {
  var savingsDiv = document.createElement("DIV");
  savingsDiv.className = "summary-sub-container";
  savingsDiv.innerHTML = "<p id='month-savings'>" + heading + " Savings</p><p id='month-savings-value' class='savings-value'>" + value + "</p>";
  document.getElementById("history-right-side-container").appendChild(savingsDiv);
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
    createSummaryContainer(heading, value);
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
    createSummaryContainer(heading, value);
  });
  // console.log('month fetched');
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
  // console.log('year changed');
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
    console.log("month: " + selectedMonth);
    console.log("year: " + selectedYear);
  },

  onYearChange: function(selectedDates, dateStr, instance) {
    selectedMonth = instance.currentMonth + 1;
    selectedYear = instance.currentYear;
    getYearSavings(selectedYear);
    getMonthSavings(selectedMonth, selectedYear);
    console.log("year only: " + selectedYear);
  },

  onChange: function(selectedDates, dateStr, instance) {
    year = selectedDates[0].getFullYear();
    month = selectedDates[0].getMonth();
    day = selectedDates[0].getDate();
    savings = getDateSavings(year, month, day);
    console.log('date changed');
  },

}

var calendar = flatpickr("#dateInput", calendarOptions);


// if a 'month-button' is clicked, move the date input to the clicked 'month-button'
document.body.addEventListener('click', function (evt) {
    if (evt.target.classList.contains('month-button')) {
      dateInputTracker = target.innerHTML;
    }
}, false);

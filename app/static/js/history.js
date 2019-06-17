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

// // fetch savings for day, month, or year
// function getSavings(endpoint, selectedDate) {
//   var options = {
//     params: {
//       date: selectedDate
//     }
//   }
//   return axios.get(endpoint, options)
// }

// fetch and display month savings
function getMonthSavings(month, year) {
  axios.get('/month-savings', {
    params: {
      month: month,
      year: year,
    }
  })
  .then(function(response) {
    var monthSavingsDiv = document.createElement("DIV");
    monthSavingsDiv.className = "summary-sub-container";
    monthSavingsDiv.innerHTML = "<p id='month-savings'>" + monthArr[selectedMonth - 1] + " " + selectedYear + " Savings</p><p id='month-savings-value' class='savings-value'>" + response.data.savings + "</p>";
    document.getElementById("history-right-side-container").appendChild(monthSavingsDiv);
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
    // selectedMonth = selectedDates[0].getMonth() + 1;
    // selectedYear = selectedDates[0].getFullYear();
    selectedMonth = instance.currentMonth + 1;
    selectedYear = instance.currentYear;
    getYearSavings(selectedYear);
    getMonthSavings(selectedMonth, selectedYear);
    console.log("year only: " + selectedYear);
  },

  onChange: function(selectedDates, dateStr, instance) {

    // // when month date change, fetch savings for mmonth
    // if (dateChangeDic['isChangeMonth']) {
    //   savings = getSavings('/month-savings', selectedDates[0])
    //   console.log('month fetched')
    //   dateChangeDic['isChangeMonth'] = false;
    // }

    // // when day date change, fetch savings for new date
    // if (dateChangeDic['isChangeDay']) {
    //   savings = getSavings('/day-savings', selectedDates[0])
    //   console.log('day fetched')
    // }

    // // when year date change
    // if (dateChangeDic['isChangeYear']) {
    //   savings = getSavings('/year-savings', selectedDates[0])
    //   console.log('year fetched')
    //   dateChangeDic['isChangeYear'] = false;
    // }

    savings = getSavings('/day-savings', selectedDates[0])
    console.log('date changed');
    console.log('day fetched');

  },

}

var calendar = flatpickr("#dateInput", calendarOptions);


// if a 'month-button' is clicked, move the date input to the clicked 'month-button'
document.body.addEventListener('click', function (evt) {
    if (evt.target.classList.contains('month-button')) {
      dateInputTracker = target.innerHTML;
    }
}, false);

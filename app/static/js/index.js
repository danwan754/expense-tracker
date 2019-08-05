// app/static/js/index.js


var currentIndex = 0;
var numOfSlides = 4;
var pause = false;

// slide dot elements
var slideDots = document.getElementsByClassName('slide-dot');

// slide image elements
var slideImages = document.getElementsByClassName('slide-image');

// click listeners for highlighting the active slide dot
for (var i=0; i<slideDots.length; i++) {
  slideDots[i].addEventListener('click', function() {
    currentIndex = this.dataset.index;
    clearDotColor();
    displayDotColor();
    clearSlideImages();
    displaySlide();
    pause = true;
  });
}

autoSlides();

// auto rotate slides
function autoSlides() {
  if (pause) {
    setTimeout(function(){
      return 0;
    }, 4000);
    pause = false;
  }
  clearDotColor();
  displayDotColor();
  clearSlideImages();
  displaySlide();
  setTimeout(autoSlides, 4000);

  if (currentIndex == numOfSlides - 1) {
    currentIndex = 0;
  }
  else {
    currentIndex++;
  }
}


// clear the background color of all slide dots
function clearDotColor() {
  for (var i=0; i<slideDots.length; i++) {
    slideDots[i].style.backgroundColor = '';
  }
}

// change active dot color
function displayDotColor() {
    slideDots[currentIndex].style.backgroundColor = '#bbb';
}

// change slide show image
function displaySlide() {
  slideImages[currentIndex].style.display = "block";
}

// hide all slide images
function clearSlideImages() {
  for (var i=0; i<slideImages.length; i++) {
    slideImages[i].style.display = "none";
  }
}

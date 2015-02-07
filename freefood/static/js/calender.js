
DATES = {0: "Sunday", 1: "Monday", 2: "Tuesday",
         3: "Wednesday", 4: "Thursday", 5: "Friday",
         6: "Saturday"}

function resize_heights() {
  var w_size = $(window).height();
  $(".sidebar").css("height", w_size);
  $(".main-calender").css("height", w_size);
}

function click_handlers() {
  $(".sidebar-toggler").click(function() {
    if ($(this).hasClass("clicked")) {
      $(this).removeClass("clicked");
      $(".sidebar-col").hide();
      $(".main-col").removeClass("col-md-10").removeClass("col-sm-9").addClass("col-md-12").addClass("collapsed");
    } else {
      $(this).addClass("clicked");
      $(".sidebar-col").show();
      $(".main-col").addClass("col-md-10").addClass("col-sm-9").removeClass("col-md-12").removeClass("collapsed");
    }
  });
}

function get_nearest_prev_sunday() {
  var sunday = new Date();
  var day = today.getDay();
  sunday.setDate(sunday.getDate() - day)
  return sunday
}

$(document).ready(function() {
  resize_heights();
  click_handlers();
  var today = new Date();
  console.log(today);
})
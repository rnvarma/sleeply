WEEKDIFF = 0;

HOURSIZE = 70;
CAL_SIZE = 24 * HOURSIZE;

EVENTDICT = {};

function formatted_time(mil_num) {
  if (mil_num < 12) return mil_num.toString() + " AM";
  else if (mil_num == 12) return mil_num.toString() + " PM";
  else return (mil_num % 12).toString() + " PM";
}

function place_event(event) {
  var day = moment(event.start_date.full).day();
  var eventdiv = $(document.createElement("div"));
  var top = -(CAL_SIZE - event.start_date.scaledT * HOURSIZE) + 2;
  var left = day * $(".caltop-date").width();
  var width = $(".caltop-date").width();
  var height = (event.end_date.scaledT - event.start_date.scaledT) * HOURSIZE - 4;
  eventdiv.addClass("calender-event");
  eventdiv.css("width", width);
  eventdiv.css("height", height);
  eventdiv.css("margin-top", top);
  eventdiv.css("margin-left", left);
  eventdiv.text(event.name);
  var time = event.start_date.time;
  var timeDiv = $(document.createElement("div"));
  timeDiv.addClass("eventTimeText");
  timeDiv.text(time);
  eventdiv.append(timeDiv);
  $(".body-stuff").append(eventdiv);
}

function resize_heights() {
  var w_size = $(window).height();
  $(".sidebar").css("height", w_size - 50);
  $(".main-calender").css("height", w_size - 51);

  var cal_w = $(".main-calender").width();
  console.log(cal_w);
  $(".topdates").css("width", cal_w - 75);
  $(".body-times").css("height", CAL_SIZE);
  $(".body-stuff").css("height", CAL_SIZE);
  $(".hourtime").css("height", HOURSIZE);
  $(".hourtime").css("padding-top", 59);
  $(".hourbox").css("height", HOURSIZE);
  $(".body-stuff").css("width", cal_w - 75);
  $(".body-calender").css("height", w_size - 100)
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
    resize_heights();
  });

  $(".prev-week-button").click(function() {
    var sunday = new Date();
    WEEKDIFF -= 1
    var date = get_short_date(get_x_days_away(WEEKDIFF * 7));
    populate_top_dates(get_x_days_away(WEEKDIFF * 7));
    $(".calender-event").remove();
    console.log(date, EVENTDICT[date])
    place_event_list(EVENTDICT[date]);
  });

  $(".next-week-button").click(function() {
    var sunday = new Date();
    WEEKDIFF += 1
    var date = get_short_date(get_x_days_away(WEEKDIFF * 7));
    populate_top_dates(get_x_days_away(WEEKDIFF * 7));
    $(".calender-event").remove();
    console.log(date, EVENTDICT[date])
    place_event_list(EVENTDICT[date]);
  });

  $(".today-button-div").click(function() {
    populate_top_dates(get_nearest_prev_sunday());
  });

  $(".calender-event").click(function() {
    console.log("got into here");
    $(".clickedEvent").removeClass("clickedEvent");
    $(this).addClass("clickedEvent");
  });
}

function get_short_date(sunday) {
  return (sunday.month()+1).toString() + "/" + sunday.date().toString();
}

function get_prev_day(day) {
  var next_day = moment(day)
  next_day.subtract(1, "days");
  return next_day;
}

function get_next_day(day) {
  var next_day = moment(day)
  next_day.add(1, "days");
  return next_day;
}

function get_x_days_away(x) {
  var sunday = get_nearest_prev_sunday();
  for (var i = 0; i < Math.abs(x); i++) {
    if (x < 0) {
      sunday = get_prev_day(sunday);
    } else {
      sunday = get_next_day(sunday);
    }
  }
  return sunday;  
}

function get_nearest_prev_sunday() {
  var today = new Date();
  var sunday = new moment();
  var day = today.getDay();
  sunday.subtract(day, "days");
  return sunday
}

function get_nearest_sunday_to_date(date) {
  var distance = date.day();
  date.subtract(distance, "days");
  var month = (date.month()+1).toString();
  var day = date.date().toString();
  return month + "/" + day
}

function get_days_of_week(sunday) {
  var nextday;
  nextday = moment(sunday);
  days = [sunday];
  for(var i = 1; i < 7; i++) {
    nextday = get_next_day(nextday)
    days.push(nextday)
  }
  return days;
}

function populate_top_dates(sunday) {
  var today = moment().format("dddd").slice(0,3) + " " + moment().format("MM/DD");
  var days = get_days_of_week(sunday);
  $(".isToday").removeClass("isToday")
  for (var i = 0; i < days.length; i++) {
    var date = days[i];
    var finaldate = date.format("dddd").slice(0,3) + " " + date.format("MM/DD");
    $("#topdate" + i.toString()).text(finaldate);
    if (today == finaldate) {
      $("#topdate" + i.toString()).addClass("isToday");
    }
  }
}

function load_days() {
  var sunday = get_nearest_prev_sunday();
  populate_top_dates(sunday);
}

function process_events(raw_events) {
  for (var i = 0; i < raw_events.length; i++) {
    var eventData = raw_events[i]
    var bin = get_nearest_sunday_to_date(moment(eventData.start_date.full))
    if (EVENTDICT[bin]) {
      EVENTDICT[bin].push(eventData)
    } else {
      EVENTDICT[bin] = [eventData]
    }
  }
}

function place_event_list(event_list) {
  for (var i = 0; i < event_list.length; i++) {
    place_event(event_list[i])
  }
}

function get_backend_events() {
  var username = $(".username-button").text();
  var url = "/1/get_events?username=" + username;
  $.ajax({
    type: 'GET',
    url: url,
    contentType: 'application/json',
    success: function (data) {
      console.log(data);
      process_events(data)
      console.log(EVENTDICT);
      var sunday = get_nearest_prev_sunday()
      var stringsunday = (sunday.month()+1).toString() + "/" + sunday.date().toString();
      console.log(stringsunday);
      var currevents = EVENTDICT[stringsunday];
      place_event_list(currevents);
    },
    error: function(a , b, c){
    },
    async: true
  });
}

$(document).ready(function() {
  get_backend_events()
  resize_heights();
  click_handlers();
  load_days();
  // place_event(events[0]);
  // place_event(events[1]);
  // place_event(events[2]);

  $( window ).resize(function() {
    resize_heights();
  });
})



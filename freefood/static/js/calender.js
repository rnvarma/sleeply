WEEKDIFF = 0;

HOURSIZE = 70;
CAL_SIZE = 24 * HOURSIZE;

EVENTDICT = {};

IMG_DICT = {
  "Excercise": "fa fa-heartbeat",
  "Caffeine": "fa fa-coffee",
  "PowerNap": "fa fa-power-off",
  "Productivity": "fa fa-bolt",
  "Relaxation": "fa fa-thumbs-up"
}

function load_spinner() {
  var opts = {
    lines: 13, // The number of lines to draw
    length: 20, // The length of each line
    width: 10, // The line thickness
    radius: 30, // The radius of the inner circle
    corners: 1, // Corner roundness (0..1)
    rotate: 0, // The rotation offset
    direction: 1, // 1: clockwise, -1: counterclockwise
    color: '#000', // #rgb or #rrggbb or array of colors
    speed: 1, // Rounds per second
    trail: 60, // Afterglow percentage
    shadow: false, // Whether to render a shadow
    hwaccel: false, // Whether to use hardware acceleration
    className: 'spinner', // The CSS class to assign to the spinner
    zIndex: 2e9, // The z-index (defaults to 2000000000)
    top: '50%', // Top position relative to parent
    left: '50%' // Left position relative to parent
  };
  $(".shaded-region-loading").show();
  var target = document.getElementsByClassName("higher-level-div")[0]
  var spinner = new Spinner(opts).spin(target);
}

function formatted_time(mil_num) {
  if (mil_num < 12) return mil_num.toString() + " AM";
  else if (mil_num == 12) return mil_num.toString() + " PM";
  else return (mil_num % 12).toString() + " PM";
}

function get_icon_div(name) {
  var classname = "fa fa-moon-o";
  if(IMG_DICT.hasOwnProperty(name)) {
    classname = IMG_DICT[name]
  }
  var icon = $(document.createElement("i"))
  icon.addClass(classname + " suggestion-icon");
  return icon;
}

function place_event(event) {
  var day = moment(event.start_date.month + "/" + event.start_date.date + "/" + event.start_date.year).day();
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
  if (event.is_suggestion) {
    icon_div = get_icon_div(event.name);
    eventdiv.append(icon_div);
    if (icon_div.hasClass("fa-moon-o")) {
      eventdiv.addClass("NapThing");
    } else {
      icon_div.addClass(event.name);
      eventdiv.addClass(event.name + "-background");
    }
  } else {
    eventdiv.text(event.name);
    var time = event.start_date.time;
    var timeDiv = $(document.createElement("div"));
    timeDiv.addClass("eventTimeText");
    timeDiv.text(time);
    eventdiv.append(timeDiv);
  }
  $(".body-stuff").append(eventdiv);
}

function resize_heights() {
  var w_size = $(window).height();
  $(".sidebar").css("height", w_size - 50);
  $(".main-calender").css("height", w_size - 51);

  var cal_w = $(".main-calender").width();
  $(".topdates").css("width", cal_w - 75);
  $(".body-times").css("height", CAL_SIZE);
  $(".body-stuff").css("height", CAL_SIZE);
  $(".hourtime").css("height", HOURSIZE);
  $(".hourtime").css("padding-top", 59);
  $(".hourbox").css("height", HOURSIZE);
  $(".body-stuff").css("width", cal_w - 75);
  $(".body-calender").css("height", w_size - 100)
  $(".verticalcol").css("height", CAL_SIZE);
  var col_width = $(".caltop-date").width()
  $(".verticalcol").css("width", col_width);
  $(".verticalcol").css("margin-top", -CAL_SIZE);
  $(".verticalcol").each(function(i) {
    $(this).css("margin-left", col_width * i);
  })
}

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) == (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

function allNighterClickHandler($elem) {
  var post_data = {}
  var text = $elem.text().split(" ")[1];
  var date = text.split("/");
  post_data.month = parseInt(date[0])
  post_data.day = parseInt(date[1])
  post_data.year = parseInt($elem.attr("data-year"));
  post_data.username = $(".username-button").text();
  var csrftoken = getCookie('csrftoken');
  $.ajax({
    type: 'POST',
    data: JSON.stringify(post_data),
    url: "/1/setallnighter",
    contentType: 'application/json',
    beforeSend: function (xhr) {
        xhr.withCredentials = true;
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    },
    success: function (data) {
      console.log(data);
      window.location.href = "/"
    },
    error: function(a , b, c){
      console.log("there was an error setting an all nighter");
    },
    async: true
  });
  $(".selectable").removeClass("selectable");
  $(".allnighter-button").prop("disabled", true);
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
    var date = get_short_date(get_x_days_away(WEEKDIFF * 7));
    $(".calender-event").remove();
    place_event_list(EVENTDICT[date]);
  });

  $(".prev-week-button").click(function() {
    var sunday = new Date();
    WEEKDIFF -= 1
    var date = get_short_date(get_x_days_away(WEEKDIFF * 7));
    populate_top_dates(get_x_days_away(WEEKDIFF * 7));
    $(".calender-event").remove();
    place_event_list(EVENTDICT[date]);
  });

  $(".next-week-button").click(function() {
    var sunday = new Date();
    WEEKDIFF += 1
    var date = get_short_date(get_x_days_away(WEEKDIFF * 7));
    populate_top_dates(get_x_days_away(WEEKDIFF * 7));
    $(".calender-event").remove();
    place_event_list(EVENTDICT[date]);
  });

  $(".today-button-div").click(function() {
    WEEKDIFF = 0;
    $(".calender-event").remove();
    populate_top_dates(get_nearest_prev_sunday());
    place_event_list(EVENTDICT[get_short_date(get_nearest_prev_sunday())]);
  });

  $(".calender-event").click(function() {
    $(".clickedEvent").removeClass("clickedEvent");
    $(this).addClass("clickedEvent");
  });

  $(".allnighter-button").click(function() {
    $(".caltop-date").toggleClass("selectable");
  });

  $(".caltop-date.selectable").click();

  $(window).click(function(e) {
    if (e.target.id.slice(0,7) == "topdate") {
      if (e.target.className == "caltop-date selectable") {
        allNighterClickHandler($("#" + e.target.id));
        load_spinner();
      }
    };
  });

  $(".mood-button").click(function() {
    var username = $(".username-button").text();
    $.ajax({
      type: 'GET',
      url: '/1/mood?username=' + username,
      contentType: 'application/json',
      success: function (data) {
        window.location.href = "/"
      },
      error: function(a , b, c){
      },
      async: true
    });
    load_spinner();
  });

  $(".weekplan-button").click(function() {
    post_data = {};
    var sunday = get_x_days_away(WEEKDIFF * 7)
    post_data.month = sunday.month() + 1
    post_data.day = sunday.date()
    post_data.year = sunday.year()
    post_data.username = $(".username-button").text();
    var csrftoken = getCookie('csrftoken');
    $.ajax({
      type: 'POST',
      data: JSON.stringify(post_data),
      url: "/1/regular",
      contentType: 'application/json',
      beforeSend: function (xhr) {
          xhr.withCredentials = true;
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
      },
      success: function (data) {
        console.log(data);
        window.location.href = "/"
      },
      error: function(a , b, c){
        console.log("there was an error setting an all nighter");
      },
      async: true
    });
    load_spinner();
  })
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
    $("#topdate" + i.toString()).attr("data-year", date.year());
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
      process_events(data)
      var sunday = get_nearest_prev_sunday()
      var stringsunday = (sunday.month()+1).toString() + "/" + sunday.date().toString();
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

  $( window ).resize(function() {
    resize_heights();
  });
})



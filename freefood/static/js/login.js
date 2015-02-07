

$(document).ready(function() {
  $("#signin-btn").click(function() {
    window.location.href = "/signup";
  })

  $("#login-btn").click(function() {
    $(".sign-up-option").hide();
    $(".login-option").hide();
    $(".form-signin").show(500);
  })
})
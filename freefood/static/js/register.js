function render() {
    gapi.signin.render('customBtn', {
    'callback': function(authResult) {
        console.log(authResult);
        var g_token = authResult.access_token;
        var u_token = $(".up_code").attr("data-code");
        console.log(g_token);
        if (g_token) {
            $("#gSignInWrapper").hide();
            $("#signup-wrapper").show();
            $(".g-key-hidden").attr("value", g_token);
            $(".u-key-hidden").attr("value", u_token);
        }
    },
    'clientid': '196405873859-d2tuulj4imr0r5olf32mbdlcjat4hihm.apps.googleusercontent.com',
    'cookiepolicy': 'single_host_origin',
    'requestvisibleactions': 'http://schema.org/AddAction',
    'scope': 'https://www.googleapis.com/auth/plus.login'
    });
}

function signinCallback(authResult) {
    if (authResult['status']['signed_in']) {
    // Update the app to reflect a signed in user
    // Hide the sign-in button now that the user is authorized, for example:
    document.getElementById('signinButton').setAttribute('style', 'display: none');
  } else {
    // Update the app to reflect a signed out user
    // Possible error values:
    //   "user_signed_out" - User is signed-out
    //   "access_denied" - User denied access to your app
    //   "immediate_failed" - Could not automatically log in the user
    console.log('Sign-in state: ' + authResult['error']);
  }
}
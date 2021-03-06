function loginForConfirmation() {
  FB.getLoginStatus(function(response) {
    if (response.status === 'connected') {
      var data = {
        'access_token': response.authResponse.accessToken,
        'user_id': response.authResponse.userID,
      };
      $.post('.', data)
        .success(function (response) {
          window.location = '/';
        });
    } else if (response.status === 'not_authorized') {
    } else {
    }
  });
}

function checkLoginState() {
  FB.getLoginStatus(function(response) {
    if (response.status === 'connected') {
      var data = {
        'access_token': response.authResponse.accessToken,
        'user_id': response.authResponse.userID,
      };
      $.post('/login/', data)
        .success(function (response) {
          window.location = '/';
        });
    } else if (response.status === 'not_authorized') {
    } else {
    }
  });
}

window.fbAsyncInit = function() {
  FB.init({
    appId      : APP_ID,
    cookie     : true,  // enable cookies to allow the server to access
                        // the session
    xfbml      : true,  // parse social plugins on this page
    version    : 'v2.0' // use version 2.0
  });
};

(function(d, s, id) {
  var js, fjs = d.getElementsByTagName(s)[0];
  if (d.getElementById(id)) return;
  js = d.createElement(s); js.id = id;
  js.src = "//connect.facebook.net/en_US/sdk.js";
  fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));
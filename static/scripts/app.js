var CognitoUserPool = AmazonCognitoIdentity.CognitoUserPool;
var CognitoUser = AmazonCognitoIdentity.CognitoUser;
var AuthenticationDetails = AmazonCognitoIdentity.AuthenticationDetails;
var poolData = {
  UserPoolId : 'us-east-2_aHB9PBvtQ', // User pool ID here
  ClientId : 'o1i9rlj9rvjva8c1eemrlstih'  // Client ID here
};


function signIn(){
  var username = $('#sign_in_username').val();
  var password = $('#sign_in_password').val();

  var authenticationData = {
    Username : username,
    Password : password
  };
  console.log(username);
  console.log(password);

  var authenticationDetails = new AuthenticationDetails(authenticationData);
  var userPool = new AWSCognito.CognitoIdentityServiceProvider.CognitoUserPool(poolData);
  var userData = {
    Username : username,
    Pool : userPool
  };

  var cognitoUser = new AWSCognito.CognitoIdentityServiceProvider.CognitoUser(userData);
  cognitoUser.authenticateUser(authenticationDetails, {
    onSuccess: function(result){
      console.log('access token + ' + result.getAccessToken().getJwtToken());
      window.location.href = "/select"; // The user will be redirected to this page after logging in.
    },

    onFailure: function(err) {
      alert(err);
    }
  });


}

function register(){
  var username = $('#sign_up_username').val();
  var password = $('#sign_up_password').val();
  var email = $('#sign_up_email').val();

  var userPool = new CognitoUserPool(poolData);

  var attributeList = [];

  var dataEmail = {
    Name : 'email',
    Value : email
  };

  var attributeEmail = new AWSCognito.CognitoIdentityServiceProvider.CognitoUserAttribute(dataEmail);

  attributeList.push(attributeEmail);

  userPool.signUp( username, password, attributeList, null, function(err, result){
    if (err) {
      alert(err);
      return;
    }
    cognitoUser = result.user;
    console.log('user name is ' + cognitoUser.getUsername());
    window.location.href = "/login";
  });

  console.log(username);
  console.log(password);
  console.log(email);
}

function validate(){
  var username = $('#code_username').val();
  var code = $('#code_code').val();

  var userPool = new CognitoUserPool(poolData);

  var userData = {
    username : username,
    Pool : userPool
  };

  var cognitoUser = new CognitoUserPool(poolData);
  cognitoUser.comfirmRegistration( code, true, function(err,result) {
    if (err) {
      alert(err);
      return;
    }
    console.log('call result: ' + result);
  });

  console.log(username);
  console.log(code);
}

function signOut() {
  var userPool = new CognitoUserPool(poolData);
  var cognitoUser = userPool.getCurrentUser();

  if(cognitoUser != null){
    cognitoUser.signOut();
  }
  window.location.href = "/";
}

function setSignedIn() {
  var userPool = new CognitoUserPool(poolData);
  var cognitoUser = userPool.getCurrentUser();

  if(cognitoUser != null){
    cognitoUser.getSession(function(err, session){
      if (err){
        alert(err);
        return;
      }
      console.log('session validity: ' + session.isValid());
      console.log('Username logged in: ' + cognitoUser.username);
      $('#username').html(cognitoUser.username);
    });
  }
}

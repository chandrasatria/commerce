import {gapi} from './platform.js';

$(document).ready(function (){
    var auth2 = gapi.auth2.getAuthInstance();
    alert('signout')
    auth2.signOut().then(function () {
      console.log('User signed out.');
      alert('signout')
    });
})

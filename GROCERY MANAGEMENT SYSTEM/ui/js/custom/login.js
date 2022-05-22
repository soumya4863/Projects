var attempt = 3; // Variable to count number of attempts.
// Below function Executes on click of login button.
function validate(){
var username = document.getElementById("username").value;
var password = document.getElementById("password").value;
if ( username == "ksstore" && password == "ks#123"){
alert ("Login successfully");
window.location = "file:///C:/Users/SOUMYA/Desktop/vscodes/GROCERY%20MANAGEMENT%20SYSTEM/ui/home.html"; // Redirecting to other page.
}
else if ( username == "" || password == ""){
alert(" Enter the requested credentials")
}
else{
attempt --;// Decrementing by one.
alert("You have left "+attempt+" attempt;");
// Disabling fields after 3 attempts.
if( attempt == 0){
alert("you lost all your attempts! Please try later")
window.close()
}
}
}
function changePass(){

}
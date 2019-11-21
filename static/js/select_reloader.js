function event() {
  var list = document.getElementsByTagName("select");
  var temp = "";

  for (var i = 0; i < list.length; i++) {
    var item = list[i];
    if (item.options[item.selectedIndex].value == "new") {
      console.log(item)
      temp += '&' + item.name + '=1';
    }
  }

  if (temp != "") {
    window.location.search += temp
  }
}


var body = document.getElementsByTagName("body")[0]; // get body and attach lost of events
console.log(body);
body.addEventListener("load", event, false);
body.addEventListener("keyup", event, false);
body.addEventListener("mousedown", event, false);
body.addEventListener("change", event, false);
body.addEventListener("blur", event, false);
console.log(body);
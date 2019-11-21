// This file is part of Track In Time Server.
//
// Track In Time Server is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// Track In Time Server is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with Track In Time Server.  If not, see <https://www.gnu.org/licenses/>.

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
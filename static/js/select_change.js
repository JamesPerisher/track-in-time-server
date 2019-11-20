function myfunction(id) {
   item = document.getElementById(id);
   console.log(item);
   if (item.options[item.selectedIndex].value == "other") {
     console.log("other")
     item.parentElement.style.display = "none";
   }
}

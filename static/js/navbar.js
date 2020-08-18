var mobile_icon = document.getElementById("MenuItems");
mobile_icon.style.maxHeight = "0px";
function menutoggle() {
  if (mobile_icon.style.maxHeight == "0px") {
    mobile_icon.style.maxHeight = "150px";
  } else {
    mobile_icon.style.maxHeight = "0px";
  }
}

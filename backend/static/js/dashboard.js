const date = document.getElementById("date");
date.addEventListener("click", function (e) {
	window.location.href += "?date=" + document.getElementById("date_picker").value;
});
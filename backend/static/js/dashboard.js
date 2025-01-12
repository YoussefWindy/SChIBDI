const date = document.getElementById("date");
date.addEventListener("click", function (e) {
	window.location.href += "?date=" + document.getElementById("date_picker").value;
});

const breakfast = document.getElementById("break-submit");
breakfast.addEventListener("click", function (e) {
	// Insert fetch function to database
});

const lunch = document.getElementById("lunch-submit");
lunch.addEventListener("click", function (e) {
	// Insert fetch function to database
});

const dinner = document.getElementById("dinner-submit");
dinner.addEventListener("click", function (e) {
	// Insert fetch function to database
});

const snack = document.getElementById("snack-submit");
snack.addEventListener("click", function (e) {
	// Insert fetch function to database
});
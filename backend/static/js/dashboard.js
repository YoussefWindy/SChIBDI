const date = document.getElementById("date");
date.addEventListener("click", function (e) {
	window.location.href += "?date=" + document.getElementById("date_picker").value;
});

const breakfast = document.getElementById("break-add");
breakfast.addEventListener("click", function (e) {
	
});

const lunch = document.getElementById("lunch-add");
lunch.addEventListener("click", function (e) {
	// Insert fetch function to database
});

const dinner = document.getElementById("dinner-add");
dinner.addEventListener("click", function (e) {
	// Insert fetch function to database
});

const snack = document.getElementById("snack-add");
snack.addEventListener("click", function (e) {
	// Insert fetch function to database
});

const symptoms = document.getElementById("sym-add");
symptoms.addEventListener("click", function (e) {
	const symptom_inputs = document.getElementById("sym-inputs");
	console.log(symptom_inputs)
	const new_input = document.createElement("input");
	new_input.type = "text";
	new_input.classList.add("sympts");
	new_input.name = "syms";
	new_input.list = "symps";
	new_input.placeholder = "Add a symptom";
	symptom_inputs.appendChild(document.createElement("br"));
	symptom_inputs.appendChild(new_input);
});
const pick_date = document.getElementById("date");
pick_date.addEventListener("click", function (e) {
	let date = document.getElementById("date_picker").value;
	while (date.indexOf("-") !== -1) {
		date = date.slice(0, date.indexOf("-")) + date.slice(date.indexOf("-") + 1);
	}
	window.location.href += "?date=" + date;
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
	const symptom_inputs = document.getElementById("dinner-inputs");
	console.log(symptom_inputs)
	const new_input = document.createElement("input");
	new_input.type = "text";
	new_input.classList.add("dinner");
	new_input.name = "dinner";
	new_input.placeholder = "Dinner";
	symptom_inputs.appendChild(document.createElement("br"));
	symptom_inputs.appendChild(new_input);
});

const snack = document.getElementById("snack-add");
snack.addEventListener("click", function (e) {
	const symptom_inputs = document.getElementById("snack-inputs");
	console.log(symptom_inputs)
	const new_input = document.createElement("input");
	new_input.type = "text";
	new_input.classList.add("snack");
	new_input.name = "snack";
	new_input.placeholder = "Yummy snack 😋";
	symptom_inputs.appendChild(document.createElement("br"));
	symptom_inputs.appendChild(new_input);
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
document.body.onload = (e) => {
	if (window.location.href.indexOf("?") !== -1) {
		document.getElementById("date_picker").value = window.location.href;
	}
}

const pick_date = document.getElementById("date");
pick_date.addEventListener("click", function (e) {
	const url = window.location.href;
	const date = document.getElementById("date_picker").value;
	let new_date;
	if (!date.startsWith("yyy")) {
		if (url.indexOf("?") !== -1) {
			window.location.href = url.slice(0, url.indexOf("=") + 1) + new_date;
		} else {
			window.location.href = url + "?date=" + new_date;
		}
	}
});

const breakfast = document.getElementById("break-add");
breakfast.addEventListener("click", function (e) {
	const breakfast_inputs = document.getElementById("breakfast-inputs");
	const new_input = document.createElement("input");
	new_input.type = "text";
	new_input.classList.add("breakfast");
	new_input.name = "breakfast";
	new_input.placeholder = "Breakfast";

	const newOne = breakfast_inputs.children[breakfast_inputs.length-1];
	const removeButton = document.createElement("button");
	removeButton.classList.add("item-remove");
	newOne.appendChild(removeButton);
	removeButton.addEventListener("click", removeItem);
	
	const newDiv = document.createElement("div");
	newDiv.classList.add("meal");
	newDiv.appendChild(new_input)
	breakfast_inputs.appendChild(document.createElement("br"));
	breakfast_inputs.appendChild(newDiv);
	
});

const lunch = document.getElementById("lunch-add");
lunch.addEventListener("click", function (e) {
	const lunch_inputs = document.getElementById("lunch-inputs");
	const new_input = document.createElement("input");
	new_input.type = "text";
	new_input.classList.add("lunch");
	new_input.name = "lunch";
	new_input.placeholder = "Lunch";

	const newOne = lunch_inputs.children[lunch_inputs.length-1];
	const removeButton = document.createElement("button");
	removeButton.classList.add("item-remove");
	newOne.appendChild(removeButton);
	removeButton.addEventListener("click", removeItem);

	const newDiv = document.createElement("div");
	newDiv.classList.add("meal");
	newDiv.appendChild(new_input)
	lunch_inputs.appendChild(document.createElement("br"));
	lunch_inputs.appendChild(newDiv);
});

const dinner = document.getElementById("dinner-add");
dinner.addEventListener("click", function (e) {
	const dinner_inputs = document.getElementById("dinner-inputs");
	const new_input = document.createElement("input");
	new_input.type = "text";
	new_input.classList.add("dinner");
	new_input.name = "dinner";
	new_input.placeholder = "Dinner";

	const newOne = dinner_inputs.children[breakfast_inputs.length-1];
	const removeButton = document.createElement("button");
	removeButton.classList.add("item-remove");
	newOne.appendChild(removeButton);
	removeButton.addEventListener("click", removeItem);

	const newDiv = document.createElement("div");
	newDiv.classList.add("meal");
	newDiv.appendChild(new_input)
	dinner_inputs.appendChild(document.createElement("br"));
	dinner_inputs.appendChild(newDiv);
});

const snack = document.getElementById("snack-add");
snack.addEventListener("click", function (e) {
	const snack_inputs = document.getElementById("snack-inputs");
	const new_input = document.createElement("input");
	new_input.type = "text";
	new_input.classList.add("snack");
	new_input.name = "snack";
	new_input.placeholder = "Yummy snack 😋";

	const newOne = snack_inputs.children[snack_inputs.length-1];
	const removeButton = document.createElement("button");
	removeButton.classList.add("item-remove");
	newOne.appendChild(removeButton);
	removeButton.addEventListener("click", removeItem);

	const newDiv = document.createElement("div");
	newDiv.classList.add("meal");
	newDiv.appendChild(new_input)
	snack_inputs.appendChild(document.createElement("br"));
	snack_inputs.appendChild(newDiv);
});

const symptoms = document.getElementById("sym-add");
symptoms.addEventListener("click", function (e) {
	const symptom_inputs = document.getElementById("sym-inputs");
	const new_input = document.createElement("input");
	new_input.type = "text";
	new_input.classList.add("sympts");
	new_input.name = "syms";
	new_input.list = "symps";
	new_input.placeholder = "Add a symptom";

	const newOne = symptom_inputs.children[symptom_inputs.length-1];
	const removeButton = document.createElement("button");
	removeButton.classList.add("item-remove");
	newOne.appendChild(removeButton);
	removeButton.addEventListener("click", removeItem);

	const newDiv = document.createElement("div");
	newDiv.classList.add("symmies");
	newDiv.appendChild(new_input)
	symptom_inputs.appendChild(document.createElement("br"));
	symptom_inputs.appendChild(newDiv);
});

const save_button = document.getElementById("save-changes");
save_button.addEventListener("click", function(e) {
	const breakfast = [];
	for (let meal of document.getElementById("breakfast-inputs").children) {
		meal.value.strip().toLowerCase() != '' ? breakfast.push(meal.value.strip().toLowerCase()) : console.log("empty");
	}
	const lunch = [];
	for (let meal of document.getElementById("lunch-inputs").children) {
		meal.value.strip().toLowerCase() != '' ? lunch.push(meal.value.strip().toLowerCase()) : console.log("empty");
	}
	const dinner = [];
	for (let meal of document.getElementById("dinner-inputs").children) {
		meal.value.strip().toLowerCase() != '' ? dinner.push(meal.value.strip().toLowerCase()) : console.log("empty");
	}
	const snack = [];
	for (let meal of document.getElementById("snack-inputs").children) {
		meal.value.strip().toLowerCase() != '' ? snack.push(meal.value.strip().toLowerCase()) : console.log("empty");
	}

	const meds = [];
	for (let med of document.getElementById("morning").children) {
		meds.push(med.value, med.isChecked, 0);
	}
	for (let med of document.getElementById("afternoon").children) {
		meds.push(med.value, med.isChecked, 1);
	}
	for (let med of document.getElementById("evening").children) {
		meds.push(med.value, med.isChecked, 2);
	}
	for (let med of document.getElementById("night").children) {
		meds.push(med.value, med.isChecked, 3);
	}

	const symptoms = [];
	for (let symptom of document.getElementById("sym-inputs").children) {
		symptom.value.strip().toLowerCase() != '' ? symptoms.push(symptom.value.strip().toLowerCase()) : console.log("empty");
	}

	const data = {
		date: window.location.href.slice(window.location.href.indexOf("+") + 1),
		meals: {
			breakfast: breakfast,
			lunch: lunch,
			dinner: dinner,
			snack: snack
		},
		meds: meds,
		symptoms: symptoms
	};

	fetch("/dashboard", {
		method: "POST",
		body: JSON.stringify(data),
		headers: {"Content-Type" : "application/json"}
	}).then((res) => {
		if (res.ok && res.status == 200) {
			return res.json();
		} else {
			console.error(res);
		}
	}).then((json) => console.log(json))
	.catch((error) => console.error(error));
});


const closePopup = document.getElementById("closePopup");
closePopup.addEventListener("click", function () {
	medPopup.style.display = "none"; // Close pop-up
});

const itemRemovers = document.getElementsByClassName("item-remove");
for (let item of itemRemovers) {
	item.addEventListener("click", removeItem);
} 
function removeItem(remove_button) {
	this.parent.remove();
}

const saveMeds = document.getElementById("save");
saveMeds.addEventListener("click", function (e) {
	const medList = document.getElementById("med-list");
	const medData = [];
	for (let med of medList.children) {
		const name = med.children[0].children[0].innerHTML;
		const time = med.children[0].children[1].innerHTML;
		let taken = false;
		for (let otherMed of document.getElementById(time.toLowerCase()).children) {
			if (otherMed.type == "text"){
				if (otherMed.value == name) {
					taken = otherMed.isChecked;
				}
			}
		}
		medData.push([name, take, time]);
	}
	fetch("/dashboard", {
		method: "POST",
		body: JSON.stringify({
			medicine: true,
			meds: medData
		}),
		headers: {
			"Content-Type": "application/json"
		}
	}).then((res) => {
		if (res.ok && res.status == 200) {
			return res.json();
		} else {
			console.error(res);
		}
	}).then((json) => console.log(json))
	.catch((error) => console.error(error));
	medPopup.style.display = "none";

});

document.getElementById("configure").addEventListener("click", function (e) {
    const medPopup = document.getElementById("medPopup");
	console.log(medPopup)
    medPopup.style.display = "flex"; // Show pop-up
	const removes = document.getElementsByClassName("med-remove");
	for (let remove of removes) {
		console.log(remove)
		remove.addEventListener("click", removeMed);
	}
});

function removeMed() {
	const parent = this.parentElement;
	parent.remove();
}

// Update your JavaScript code
const medList = document.querySelector('.med-list');
const addMedButton = document.getElementById('med-add');

function createMedicationItem(medication, time) {
	const medItem = document.createElement('div');
	medItem.className = 'med-item';

	const medItemContent = document.createElement('div');
	medItemContent.className = 'med-item-content';
	
	const medName = document.createElement('span');
	medName.className = 'med-name';
	medName.textContent = medication;
	
	const medTime = document.createElement("span");
	medTime.className = 'med-name';
	switch (time) {
		case 0:
			time = "Morning";
			break;
		case 1:
			time = "Afternoon";
			break;
		case 2:
			time = "Evening";
			break;
		case 3:
			time = "Night";
			break;
	}
	medTime.textContent = time;

	const removeButton = document.createElement('button');
	removeButton.className = 'med-remove';
	removeButton.innerHTML = '&minus;';
	
	removeButton.addEventListener("click", removeMed);
	
	medItemContent.appendChild(medName);
	medItemContent.appendChild(medTime);
	medItem.appendChild(medItemContent);
	medItem.appendChild(removeButton);
	
	return medItem;
}

addMedButton.addEventListener('click', function() {
	const medInput = document.getElementById('add_med');
	const medication = medInput.value.trim();
	let medTime = document.getElementById('time').value;
	medTime = medTime[0].toUpperCase() + medTime.slice(1);
	switch (medTime) {
		case "Morning":
			medTime = 0;
			break;
		case "Afternoon":
			medTime = 1;
			break;
		case "Evening":
			medTime = 2;
			break;
		case "Night":
			medTime = 3;
			break;
		default:
			console.log("regex test failed")
			return;
	}
	const medList = document.getElementById("med-list");

	if (medication) {
		const medItem = createMedicationItem(medication, medTime);
		medList.appendChild(medItem);
		medInput.value = '';


		/*fetch('/add_medication', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({ medication: medication })
		})
		.then(response => response.json())
		.then(data => {
			if (data.success) {
				
			}
		}).catch(error => console.error('Error adding medication:', error));*/
	}
});

// Initialize existing medications
const existingMeds = document.querySelectorAll('#medications');
existingMeds.forEach(med => {
	const medication = med.value;
	const isChecked = med.checked;
	const medItem = createMedicationItem(medication, isChecked);
	medList.appendChild(medItem);
	med.closest('.med-item')?.remove();
});
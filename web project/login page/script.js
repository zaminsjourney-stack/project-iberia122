document.getElementById("loginForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
const response = await fetch("https://velocity-submitter-squeeze.ngrok-free.dev/api/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "ngrok-skip-browser-warning": "69420"
        },
        body: JSON.stringify({ username, password })
    });
        const data = await response.json();

        if (response.ok) {
            localStorage.setItem("loggedInUser", username);
            window.location.href = "../index.html";
        } else {
            alert(data.message || "Invalid username or password");
        }
    } catch (error) {
        console.error("Connection error:", error);
        alert("Unable to connect to the authentication server.");
    }
});
(function () {
    var USER_KEY = "loggedInUser";

    function getUser() {
        try { return localStorage.getItem(USER_KEY); } catch (e) { return null; }
    }

    // Only allow redirects to local pages like "courses.html"
    function safeNext(value) {
        return /^[\w-]+\.html$/.test(value || "") ? value : "";
    }

    var params = new URLSearchParams(window.location.search);
    var next = safeNext(params.get("next"));

    // ---------- Login page ----------
    var form = document.getElementById("loginForm");
    if (form) {
        var notice = document.getElementById("loginNotice");
        if (notice && next) {
            notice.textContent = "Please log in to watch the courses.";
            notice.hidden = false;
        }

        form.addEventListener("submit", async function (e) {
            e.preventDefault();

            var username = document.getElementById("username").value;
            var password = document.getElementById("password").value;

            try {
                var response = await fetch("https://velocity-submitter-squeeze.ngrok-free.dev/api/login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "ngrok-skip-browser-warning": "69420"
                    },
                    body: JSON.stringify({ username: username, password: password })
                });

                var data = await response.json();

                if (response.ok) {
                    localStorage.setItem(USER_KEY, username);
                    // Go back to the page they wanted (e.g. courses), otherwise home
                    window.location.href = next || "index.html";
                } else {
                    alert(data.message || "Invalid username or password");
                }
            } catch (error) {
                console.error("Connection error:", error);
                alert("Unable to connect to the authentication server.");
            }
        });
    }

    // ---------- Other pages: show a Logout link when logged in ----------
    var navList = document.querySelector("nav ul");
    if (navList && getUser()) {
        var li = document.createElement("li");
        var a = document.createElement("a");
        a.href = "#";
        a.textContent = "Logout";
        a.addEventListener("click", function (e) {
            e.preventDefault();
            try { localStorage.removeItem(USER_KEY); } catch (err) {}
            window.location.href = "index.html";
        });
        li.appendChild(a);
        navList.appendChild(li);
    }
})();

document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".topnav a").forEach((link) => {
        if (
            link.href === window.location.href ||
            (link.getAttribute("href") !== "/" &&
                window.location.pathname.startsWith(
                    link.getAttribute("href")
                ))
        ) {
            link.classList.add("active");
        }
    });

    const darkModeToggle = document.getElementById("darkModeToggle");
    
    if (!darkModeToggle) {
        console.error("Dark mode toggle button not found");
        return;
    }

    const savedTheme = localStorage.getItem("theme");

    if (savedTheme === "dark") {
        document.documentElement.classList.add("dark-mode");
        darkModeToggle.textContent = "☀️ Light Mode";
    }

    darkModeToggle.addEventListener("click", () => {
        document.documentElement.classList.toggle("dark-mode");
        const isDark = document.documentElement.classList.contains("dark-mode");
        
        if (isDark) {
            darkModeToggle.textContent = "☀️ Light Mode";
            localStorage.setItem("theme", "dark");
            console.log("Theme DARK");
        } else {
            darkModeToggle.textContent = "🌙 Dark Mode";
            localStorage.setItem("theme", "light");
            console.log("Theme LIGHT");
        }
    });
});

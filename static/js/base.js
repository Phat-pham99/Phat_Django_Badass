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

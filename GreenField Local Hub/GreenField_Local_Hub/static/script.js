// Placeholder: mark active nav link based on current URL path
document.addEventListener("DOMContentLoaded", () => {
    const links = document.querySelectorAll(".main-nav .nav-link");
    const path = window.location.pathname;

    links.forEach(link => {
        if (link.getAttribute("href") === path) {
            link.classList.add("nav-link-active");
        }
    });
});

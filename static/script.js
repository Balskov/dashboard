document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("toggleSidebar");
    const body = document.body;

    // 🌙 Mørkt tema
    const savedMode = localStorage.getItem("darkMode");
    if (savedMode === "true") {
        body.classList.add("dark-mode");
    }

    const darkToggle = document.getElementById("darkModeToggle");
    if (darkToggle) {
        darkToggle.addEventListener("click", function () {
            body.classList.toggle("dark-mode");
            localStorage.setItem("darkMode", body.classList.contains("dark-mode"));
        });
    }

    // ☰ Sidebar toggle
    if (toggleBtn) {
        toggleBtn.addEventListener("click", function () {
            if (window.innerWidth <= 768) {
                body.classList.toggle("sidebar-visible");  // mobilvisning
            } else {
                body.classList.toggle("sidebar-hidden");   // desktopvisning
            }
        });
    }

    // 📱 Luk sidebar automatisk når man klikker på et link (på mobil)
    const sidebarLinks = document.querySelectorAll(".sidebar a");
    sidebarLinks.forEach(link => {
        link.addEventListener("click", () => {
            if (window.innerWidth <= 768) {
                body.classList.remove("sidebar-visible");
            }
        });
    });
});
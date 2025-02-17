document.addEventListener("DOMContentLoaded", function() {
    const toggler = document.querySelector(".navbar-toggler");
    const collapse = document.querySelector("#navbarToggle");
    const closeBtn = document.querySelector("#closeSidebar");


    toggler.addEventListener("click", function() {
        collapse.classList.toggle("show");
    });

    closeBtn.addEventListener("click", function () {
        collapse.classList.remove("show");
        collapse.style.width = '0';
        collapse.style.display = 'none';
    });

    // Close sidebar when clicking outside of it
    document.addEventListener("click", function (event) {
        if (!collapse.contains(event.target) && !toggler.contains(event.target)) {
            collapse.classList.remove("show");
        }
    });
});
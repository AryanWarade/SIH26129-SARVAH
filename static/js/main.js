document.addEventListener("DOMContentLoaded", function () {

    // Automatically hide Bootstrap alerts after 5 seconds.
    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(function (alert) {

        setTimeout(function () {

            const closeButton = alert.querySelector(".btn-close");

            if (closeButton) {
                closeButton.click();
            }

        }, 5000);

    });

});
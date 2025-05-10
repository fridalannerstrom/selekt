/* jslint esversion: 6 */

// Wait until the entire DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {

    // Initialize the upload script
    initUploadScript();

    setTimeout(() => {
        // Find the first element with the class "alert" (if any)
        const alert = document.querySelector('.alert');

        // If an alert exists, remove the "show" class to hide it
        if (alert) alert.classList.remove('show');
    }, 3000);
});

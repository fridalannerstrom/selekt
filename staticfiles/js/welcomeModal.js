// Run this once the entire DOM is fully loaded
document.addEventListener('DOMContentLoaded', function () {
  const modalEl = document.getElementById('welcomeModal');
  if (!modalEl) return; // Exit early if the modal is not present

  // Initialize the Bootstrap modal instance
  const welcomeModal = new bootstrap.Modal(modalEl);

  // Track if the modal has already been dismissed
  let hasDismissed = false;

  // Optional: URL to redirect to after modal is dismissed
  let redirectAfterDismiss = null;

  // Get dismiss URL and CSRF token from data attributes
  const dismissUrl = modalEl.dataset.dismissUrl;
  const csrfToken = modalEl.dataset.csrfToken;

  // Show the modal immediately on page load
  welcomeModal.show();

  // Dismiss function: sends POST to backend to mark welcome as "seen"
  function dismissWelcome() {
    if (hasDismissed) return; // Prevent multiple triggers
    hasDismissed = true;

    // Send request to backend to mark the modal as dismissed
    fetch(dismissUrl, {
      method: "POST",
      headers: {
        'X-CSRFToken': csrfToken,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({})
    }).then(() => {
      welcomeModal.hide(); // Hide the modal
    }).catch(err => {
      console.error("Failed to dismiss welcome modal:", err);
    });
  }

  // Handle click on "Upload First Candidate" button
  document.getElementById('uploadFirstCandidateBtn')?.addEventListener('click', function () {
    redirectAfterDismiss = this.dataset.redirectUrl; // Set redirect path
    dismissWelcome(); // Trigger dismissal logic
  });

  // Handle click on "Do Later" button
  document.getElementById('doLaterBtn')?.addEventListener('click', dismissWelcome);

  // Also dismiss when user clicks outside modal or uses the close (X) button
  modalEl.addEventListener('hide.bs.modal', dismissWelcome);

  // After modal is fully hidden, perform redirect if needed
  modalEl.addEventListener('hidden.bs.modal', function () {
    if (redirectAfterDismiss) {
      window.location.href = redirectAfterDismiss;
    }
  });
});
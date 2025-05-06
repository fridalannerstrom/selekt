document.addEventListener('DOMContentLoaded', function () {
    const modalEl = document.getElementById('welcomeModal');
    if (!modalEl) return;
  
    const welcomeModal = new bootstrap.Modal(modalEl);
    let hasDismissed = false;
    let redirectAfterDismiss = null;
  
    const dismissUrl = modalEl.dataset.dismissUrl;
    const csrfToken = modalEl.dataset.csrfToken;
  
    welcomeModal.show();
  
    function dismissWelcome() {
      if (hasDismissed) return;
      hasDismissed = true;
  
      fetch(dismissUrl, {
        method: "POST",
        headers: {
          'X-CSRFToken': csrfToken,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
      }).then(() => {
        welcomeModal.hide();
      }).catch(err => {
        console.error("Failed to dismiss welcome modal:", err);
      });
    }
  
    // Om användaren klickar på "Upload First Candidate"
    document.getElementById('uploadFirstCandidateBtn')?.addEventListener('click', function () {
      redirectAfterDismiss = this.dataset.redirectUrl;
      dismissWelcome();
    });
  
    // Om användaren klickar på "Do Later"
    document.getElementById('doLaterBtn')?.addEventListener('click', dismissWelcome);
  
    // När modalen håller på att stängas (klick på X eller overlay)
    modalEl.addEventListener('hide.bs.modal', dismissWelcome);
  
    // När modalen har stängts – gör redirect om det är satt
    modalEl.addEventListener('hidden.bs.modal', function () {
      if (redirectAfterDismiss) {
        window.location.href = redirectAfterDismiss;
      }
    });
  });
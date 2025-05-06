document.addEventListener('DOMContentLoaded', () => {
    initUploadScript();
  
    setTimeout(() => {
      const alert = document.querySelector('.alert');
      if (alert) alert.classList.remove('show');
    }, 3000);
  });
  
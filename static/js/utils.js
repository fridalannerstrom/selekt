document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.dot-menu').forEach(menu => {
      menu.addEventListener('click', function (e) {
        e.stopPropagation();
        const dropdown = this.querySelector('.dot-menu-dropdown');
        dropdown.classList.toggle('d-none');
        document.querySelectorAll('.dot-menu-dropdown').forEach(d => {
          if (d !== dropdown) d.classList.add('d-none');
        });
      });
    });
  
    document.addEventListener('click', () => {
      document.querySelectorAll('.dot-menu-dropdown').forEach(d => d.classList.add('d-none'));
    });
  });
  
  document.addEventListener('input', function (event) {
    if (event.target.closest('#linkInputs')) {
      updateHiddenLinks();
    }
  });
  
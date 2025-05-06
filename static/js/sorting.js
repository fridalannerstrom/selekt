document.addEventListener('DOMContentLoaded', function () {
    const sortSelect = document.getElementById('sortSelect');
    if (sortSelect) {
      sortSelect.addEventListener('change', function () {
        const url = new URL(window.location.href);
        const params = url.searchParams;
        const selectedSort = this.value;
        selectedSort ? params.set('sort', selectedSort) : params.delete('sort');
        window.location.href = url.pathname + '?' + params.toString();
      });
    }
  
    const searchInput = document.getElementById('searchInput');
    const clearBtn = document.getElementById('clearSearchBtn');
    if (searchInput && clearBtn) {
      const updateClearButtonVisibility = () => {
        clearBtn.classList.toggle('d-none', searchInput.value.length === 0);
      };
      searchInput.addEventListener('input', updateClearButtonVisibility);
      clearBtn.addEventListener('click', () => {
        searchInput.value = '';
        updateClearButtonVisibility();
        window.location.href = window.location.href.split('?')[0];
      });
      updateClearButtonVisibility();
    }
  });
  
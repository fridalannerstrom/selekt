/* jslint esversion: 6 */

// Run this once the entire DOM is fully loaded
document.addEventListener('DOMContentLoaded', function () {

    // SORTING FUNCTIONALITY
    const sortSelect = document.getElementById('sortSelect');
  
    if (sortSelect) {
      sortSelect.addEventListener('change', function () {
        const url = new URL(window.location.href);
        const params = url.searchParams; 
        const selectedSort = this.value; 
  
        // If a sort option is selected, set it in URL; otherwise, remove the param
        selectedSort ? params.set('sort', selectedSort) : params.delete('sort');
  
        // Redirect to updated URL (this causes a page reload)
        window.location.href = url.pathname + '?' + params.toString();
      });
    }
  
    // SEARCH INPUT + CLEAR BUTTON
    const searchInput = document.getElementById('searchInput');
    const clearBtn = document.getElementById('clearSearchBtn');
  
    if (searchInput && clearBtn) {
      // Toggle visibility of clear button depending on input value
      const updateClearButtonVisibility = () => {
        clearBtn.classList.toggle('d-none', searchInput.value.length === 0);
      };
  
      // Update clear button visibility as user types
      searchInput.addEventListener('input', updateClearButtonVisibility);
  
      // Clear search input and reload page without query params
      clearBtn.addEventListener('click', () => {
        searchInput.value = '';
        updateClearButtonVisibility();
        window.location.href = window.location.href.split('?')[0]; // reload without search query
      });
  
      // Set initial button visibility on page load
      updateClearButtonVisibility();
    }
  
  });
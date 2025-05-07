// Run this once the entire DOM is fully loaded
document.addEventListener('DOMContentLoaded', function () {
    const favoritesToggle = document.getElementById('favoritesToggle');
  
    if (favoritesToggle) {
      // Handle click on "Show Favorites / Show All" toggle
      favoritesToggle.addEventListener('click', function () {
        const url = new URL(window.location.href);
        const params = url.searchParams;
  
        // Toggle the "favorites" parameter in the URL
        if (params.get('favorites') === 'on') {
          params.delete('favorites');
        } else {
          params.set('favorites', 'on');
        }
  
        // Reload the page with updated URL parameters
        window.location.href = url.pathname + '?' + params.toString();
      });
  
      // Set button state on initial load based on URL parameter
      const url = new URL(window.location.href);
      const params = url.searchParams;
  
      if (params.get('favorites') === 'on') {
        // Update toggle button to reflect "Favorites active"
        favoritesToggle.innerHTML = '<i class="fas fa-heart"></i> Show All';
        favoritesToggle.classList.remove('btn-outline-dark');
        favoritesToggle.classList.add('btn-dark');
      } else {
        // Update toggle button to reflect "Show favorites"
        favoritesToggle.innerHTML = '<i class="fa-regular fa-heart"></i> Show Favorites';
        favoritesToggle.classList.add('btn-outline-dark');
        favoritesToggle.classList.remove('btn-dark');
      }
    }
  });
  
  /**
   * Toggle favorite status for a candidate (called when clicking heart icon)
   * Updates both card view and modal view with correct icon and styling
   * @param {string|number} candidateId - The ID of the candidate to toggle
   */
  function toggleFavorite(candidateId) {
    fetch(`/toggle-favorite/${candidateId}/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': '{{ csrf_token }}', // Replace with dynamic CSRF token if needed
      }
    })
      .then(response => response.json())
      .then(data => {
        // Update heart icon in candidate card
        const cardHeart = document.getElementById(`heart-card-${candidateId}`);
        if (cardHeart) {
          cardHeart.classList.toggle('fa-solid', data.is_favorite);
          cardHeart.classList.toggle('fa-regular', !data.is_favorite);
        }
  
        // Update heart icon in modal (if open)
        const modalHeart = document.getElementById(`heart-modal-${candidateId}`);
        if (modalHeart) {
          modalHeart.classList.toggle('fa-solid', data.is_favorite);
          modalHeart.classList.toggle('fa-regular', !data.is_favorite);
        }
  
        // Update modal favorite button styling and text
        const favoriteButtonModal = document.getElementById(`favoriteButtonModal-${candidateId}`);
        if (favoriteButtonModal) {
          favoriteButtonModal.classList.toggle('btn-dark', data.is_favorite);
          favoriteButtonModal.classList.toggle('btn-outline-dark', !data.is_favorite);
  
          favoriteButtonModal.innerHTML = data.is_favorite
            ? `<i class="fas fa-heart" id="heart-modal-${candidateId}"></i> <span class="label-desktop">Remove from favorites</span>`
            : `<i class="far fa-heart" id="heart-modal-${candidateId}"></i> <span class="label-desktop">Add to favorites</span>`;
        }
      })
      .catch(error => {
        console.error('Error toggling favorite:', error);
      });
  }
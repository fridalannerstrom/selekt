document.addEventListener('DOMContentLoaded', function () {
    const favoritesToggle = document.getElementById('favoritesToggle');
    if (favoritesToggle) {
      favoritesToggle.addEventListener('click', function () {
        const url = new URL(window.location.href);
        const params = url.searchParams;
        if (params.get('favorites') === 'on') {
          params.delete('favorites');
        } else {
          params.set('favorites', 'on');
        }
        window.location.href = url.pathname + '?' + params.toString();
      });
  
      const url = new URL(window.location.href);
      const params = url.searchParams;
      if (params.get('favorites') === 'on') {
        favoritesToggle.innerHTML = '<i class="fas fa-heart"></i> Show All';
        favoritesToggle.classList.remove('btn-outline-dark');
        favoritesToggle.classList.add('btn-dark');
      } else {
        favoritesToggle.innerHTML = '<i class="fa-regular fa-heart"></i> Show Favorites';
        favoritesToggle.classList.add('btn-outline-dark');
        favoritesToggle.classList.remove('btn-dark');
      }
    }
  });
  
  function toggleFavorite(candidateId) {
    fetch(`/toggle-favorite/${candidateId}/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': '{{ csrf_token }}',
      }
    })
      .then(response => response.json())
      .then(data => {
        const cardHeart = document.getElementById(`heart-card-${candidateId}`);
        const modalHeart = document.getElementById(`heart-modal-${candidateId}`);
        const favoriteButtonModal = document.getElementById(`favoriteButtonModal-${candidateId}`);
  
        if (cardHeart) {
          cardHeart.classList.toggle('fa-solid', data.is_favorite);
          cardHeart.classList.toggle('fa-regular', !data.is_favorite);
        }
        if (modalHeart) {
          modalHeart.classList.toggle('fa-solid', data.is_favorite);
          modalHeart.classList.toggle('fa-regular', !data.is_favorite);
        }
        if (favoriteButtonModal) {
          favoriteButtonModal.classList.toggle('btn-dark', data.is_favorite);
          favoriteButtonModal.classList.toggle('btn-outline-dark', !data.is_favorite);
          favoriteButtonModal.innerHTML = data.is_favorite
            ? `<i class="fas fa-heart" id="heart-modal-${candidateId}"></i> <span class="label-desktop">Remove from favorites</span>`
            : `<i class="far fa-heart" id="heart-modal-${candidateId}"></i> <span class="label-desktop">Add to favorites</span>`;
        }
      })
      .catch(error => console.error('Error toggling favorite:', error));
  }
  
/* jslint esversion: 6 */

// Run this once the entire DOM is fully loaded
document.addEventListener('DOMContentLoaded', function () {

    document.querySelectorAll('.dot-menu').forEach(menu => {
        menu.addEventListener('click', function (e) {
            e.stopPropagation();
            const dropdown = this.querySelector('.dot-menu-dropdown');
            dropdown.classList.toggle('d-none');

            // Hide all other open dot-menus
            document.querySelectorAll('.dot-menu-dropdown').forEach(d => {
                if (d !== dropdown) d.classList.add('d-none');
            });
        });
    });

    // Close all dropdowns if user clicks outside
    document.addEventListener('click', () => {
        document.querySelectorAll('.dot-menu-dropdown').forEach(d => d.classList.add('d-none'));
    });

    // SKILL BADGE OVERFLOW HANDLING (e.g. +3 if not enough space)
    const containers = document.querySelectorAll('.skill-container');

    containers.forEach(container => {
        const badges = Array.from(container.querySelectorAll('.skill-badge:not(.skill-badge-extra)'));
        const plusBadge = container.querySelector('.skill-badge-extra');

        let totalWidth = 0;
        const containerWidth = container.clientWidth;
        let visibleCount = 0;

        badges.forEach(badge => {
            badge.style.display = 'inline-block';
            const width = badge.offsetWidth + 8; // approx. 8px gap

            if (totalWidth + width < containerWidth - 40) { // reserve ~40px for +X badge
                totalWidth += width;
                visibleCount++;
            } else {
                badge.style.display = 'none';
            }
        });

        const hiddenCount = badges.length - visibleCount;
        if (hiddenCount > 0) {
            plusBadge.textContent = `+${hiddenCount}`;
            plusBadge.style.display = 'inline-block';
        }
    });
});

// LIVE LINK FIELD UPDATE HANDLING (for hidden link string input)
document.addEventListener('input', function (event) {
    if (event.target.closest('#linkInputs')) {
        updateHiddenLinks(); // This function should be defined globally (e.g. in editor.js)
    }
});

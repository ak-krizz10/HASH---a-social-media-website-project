document.addEventListener('DOMContentLoaded', function () {
    const meButton = document.querySelector('.header__me-btn');
    const meMenu = document.querySelector('.header__me-menu');

    let isMeMenuOpen = false;

    meButton.addEventListener('click', function (event) {
        isMeMenuOpen = !isMeMenuOpen;

        if (isMeMenuOpen) {
            meMenu.style.display = 'block';
            meMenu.classList.add('show'); // Add 'show' class for fade-in effect
        } else {
            meMenu.classList.remove('show'); // Remove 'show' class for fade-out effect
            setTimeout(() => {
                meMenu.style.display = 'none';
            }, 300); // Adjust the timeout to match the transition duration
        }
    });

    // Close the menu if clicking outside of it
    document.addEventListener('click', function (event) {
        if (!meButton.contains(event.target) && !meMenu.contains(event.target)) {
            meMenu.classList.remove('show'); // Remove 'show' class for fade-out effect
            setTimeout(() => {
                meMenu.style.display = 'none';
            }, 300); // Adjust the timeout to match the transition duration
            isMeMenuOpen = false;
        }
    });

    // Hide the menu on initial load
    meMenu.style.display = 'none';
});
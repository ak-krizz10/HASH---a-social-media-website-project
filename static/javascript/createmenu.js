document.addEventListener('DOMContentLoaded', function () {
    const createButton = document.querySelector('.dropbtn');
    const createMenu = document.querySelector('.dropdown-content');

    let isCreateMenuOpen = false;

    createButton.addEventListener('click', function (event) {
        isCreateMenuOpen = !isCreateMenuOpen;

        if (isCreateMenuOpen) {
            createMenu.style.display = 'block';
            createMenu.classList.add('show'); // Add 'show' class for fade-in effect
        } else {
            createMenu.classList.remove('show'); // Remove 'show' class for fade-out effect
            setTimeout(() => {
                createMenu.style.display = 'none';
            }, 300); // Adjust the timeout to match the transition duration
        }
    });

    // Close the menu if clicking outside of it
    document.addEventListener('click', function (event) {
        if (!createButton.contains(event.target) && !createMenu.contains(event.target)) {
            createMenu.classList.remove('show'); // Remove 'show' class for fade-out effect
            setTimeout(() => {
                createMenu.style.display = 'none';
            }, 300); // Adjust the timeout to match the transition duration
            isCreateMenuOpen = false;
        }
    });

    // Hide the menu on initial load
    createMenu.style.display = 'none';
});

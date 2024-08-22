// Lazy loading function
function lazyLoad() {
  // Get all post containers
  const postContainers = document.querySelectorAll('.post-container');

  // IntersectionObserver configuration
  const options = {
      root: null, // Use the viewport as the root
      rootMargin: '0px', // No margin
      threshold: 0.001 // 10% of the post needs to be visible for lazy loading to trigger
  };

  // IntersectionObserver callback function
  const callback = (entries, observer) => {
      entries.forEach(entry => {
          if (entry.isIntersecting) {
              // Add a CSS class to trigger loading of content
              entry.target.classList.add('load-content');
              observer.unobserve(entry.target); // Stop observing this post container once it's loaded
          }
      });
  };

  // Create the IntersectionObserver instance
  const observer = new IntersectionObserver(callback, options);

  // Start observing each post container
  postContainers.forEach(postContainer => {
      observer.observe(postContainer);
  });
}

// Call the lazyLoad function when the page loads
window.addEventListener('load', lazyLoad);
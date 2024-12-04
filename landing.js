document.addEventListener('DOMContentLoaded', () => {
    const startButton = document.getElementById('start-button');
    const animatedElements = document.querySelectorAll('.fade-in, .slide-in, .zoom-in');

    // Smooth scrolling to "start" section
    startButton.addEventListener('click', (event) => {
        event.preventDefault();
        document.querySelector('#start').scrollIntoView({ behavior: 'smooth' });
    });

    // Intersection Observer for animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target); // Stop observing once animation is triggered
            }
        });
    }, {
        threshold: 0.1, // Trigger animation when 10% of the element is visible
    });

    // Apply observer to all animated elements
    animatedElements.forEach((element) => {
        observer.observe(element);
    });
});

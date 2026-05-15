// Back to Top Button Functionality
window.addEventListener('DOMContentLoaded', function() {
    const backToTopButton = document.getElementById('backToTop');
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            backToTopButton.classList.add('show');
        } else {
            backToTopButton.classList.remove('show');
        }
    });
    
    backToTopButton.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // Initialize Vanta.js for hero header
    setVanta();
});

// Parallel scrolling effect with reduced intensity
window.addEventListener('scroll', function() {
    const scrollPosition = window.scrollY;
    const elements = document.querySelectorAll('.parallax-element');
    
    elements.forEach(function(element) {
        const speed = element.dataset.speed || 0.1; // Reduced from 0.5 to 0.1
        const yPos = -(scrollPosition * speed);
        element.style.transform = `translateY(${yPos}px)`;
    });
});
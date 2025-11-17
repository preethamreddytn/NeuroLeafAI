// Theme Toggle Functionality
function initThemeToggle() {
    const toggleButton = document.getElementById('theme-toggle-btn');
    
    // Add active class if in dark mode
    const currentTheme = document.documentElement.getAttribute('data-theme');
    if (currentTheme === 'dark') {
        toggleButton.classList.add('active');
    }
    
    // Toggle theme on button click
    toggleButton.addEventListener('click', function() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        
        // Update active class
        if (newTheme === 'dark') {
            toggleButton.classList.add('active');
        } else {
            toggleButton.classList.remove('active');
        }
    });
}

// Initialize theme toggle when DOM is loaded
document.addEventListener('DOMContentLoaded', initThemeToggle);
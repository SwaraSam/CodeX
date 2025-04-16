// Main JavaScript file

// Handle automatic flash message dismissal
document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash-message');
    
    if (flashMessages.length > 0) {
        setTimeout(() => {
            flashMessages.forEach(message => {
                message.style.opacity = '0';
                message.style.transition = 'opacity 0.5s ease';
                
                // Remove from DOM after fade out
                setTimeout(() => {
                    message.remove();
                }, 500);
            });
        }, 5000);
    }
});

// Custom date filter for templates
// This is used in Jinja2 templates with the now function
// e.g., {% now 'Y' %} to get the current year
function getCurrentYear() {
    return new Date().getFullYear();
}

// Implement a confirmation dialog for critical actions if needed
function confirmAction(message) {
    return confirm(message);
}

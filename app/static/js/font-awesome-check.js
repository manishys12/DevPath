// Check if Font Awesome is loaded properly
document.addEventListener('DOMContentLoaded', function() {
    // Function to check if an icon is rendered properly
    function isFontAwesomeLoaded() {
        // Create a test icon
        var testIcon = document.createElement('i');
        testIcon.className = 'fas fa-check';
        testIcon.style.visibility = 'hidden';
        document.body.appendChild(testIcon);

        // Get the computed width and content
        var style = window.getComputedStyle(testIcon);
        var width = style.width;
        var content = style.content;

        // Remove the test icon
        document.body.removeChild(testIcon);

        // If the width is "0px" or "auto", or content is empty/none, Font Awesome is not loaded
        return width !== '0px' && width !== 'auto' && content !== 'none' && content !== '';
    }

    // Check if Font Awesome is loaded
    if (!isFontAwesomeLoaded()) {
        console.warn('Font Awesome not loaded properly. Using fallback.');

        // Remove any existing Font Awesome CDN link to avoid conflicts
        var existingLinks = document.querySelectorAll('link[href*="font-awesome"]');
        existingLinks.forEach(function(link) {
            if (link.href.includes('cdnjs.cloudflare.com')) {
                link.remove();
            }
        });

        // Force reload the fallback CSS with cache busting
        var link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = '/static/css/fontawesome-fallback.css?v=' + new Date().getTime();
        document.head.appendChild(link);

        // Add a class to the body to indicate we're using fallback
        document.body.classList.add('using-fa-fallback');

        // Log for debugging
        console.info('Font Awesome fallback loaded');
    }
});

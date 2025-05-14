// Apply gradient borders to all containers
document.addEventListener('DOMContentLoaded', function() {
    // List of selectors to apply the gradient effect to
    const containerSelectors = [
        // Cards
        '.card',

        // Alerts
        '.alert',

        // List groups
        '.list-group',

        // Modals
        '.modal-content',

        // Navs and tabs
        '.nav-pills',
        '.tab-content',

        // Jumbotron/hero sections
        '.jumbotron',
        '.hero',

        // Accordions
        '.accordion',
        '.accordion-item',

        // Toasts
        '.toast',

        // Pagination
        '.pagination',

        // Breadcrumbs
        '.breadcrumb',

        // Progress bars container
        '.progress',

        // Input groups
        '.input-group',

        // Custom containers
        '.container-custom',
        '.box',
        '.panel'
    ];

    // Elements to explicitly exclude from gradient effect
    const excludeSelectors = [
        '.dropdown-menu',
        '.dropdown',
        '.dropdown-toggle',
        '.navbar-nav .dropdown'
    ];

    // Function to apply the gradient border class
    window.applyGradientBorders = function(selector) {
        // If a specific selector is provided, use it, otherwise use the containerSelectors list
        const selectorsToUse = selector ? [selector] : containerSelectors;

        selectorsToUse.forEach(selector => {
            const elements = document.querySelectorAll(selector);

            elements.forEach(element => {
                // Skip elements that already have the class
                if (!element.classList.contains('roadmap-gradient-container')) {
                    // Skip elements that are children of elements with the gradient class
                    let parent = element.parentElement;
                    let skipElement = false;

                    // Skip elements with the no-gradient class
                    if (element.classList.contains('no-gradient')) {
                        skipElement = true;
                    }

                    while (parent) {
                        if (parent.classList && parent.classList.contains('roadmap-gradient-container')) {
                            skipElement = true;
                            break;
                        }
                        parent = parent.parentElement;
                    }

                    // Check if element matches any exclude selectors
                    let isExcluded = false;
                    for (const selector of excludeSelectors) {
                        if (element.matches(selector)) {
                            isExcluded = true;
                            break;
                        }
                    }

                    // Skip certain elements based on their context or classes
                    if (isExcluded ||
                        element.classList.contains('card-header') ||
                        element.classList.contains('card-body') ||
                        element.classList.contains('card-footer') ||
                        element.classList.contains('list-group-item') ||
                        element.classList.contains('dropdown-item') ||
                        element.classList.contains('dropdown-menu') ||
                        element.classList.contains('dropdown-toggle') ||
                        element.classList.contains('dropdown') ||
                        element.classList.contains('page-item') ||
                        element.classList.contains('breadcrumb-item') ||
                        element.classList.contains('progress-bar') ||
                        element.classList.contains('nav-item') ||
                        element.classList.contains('nav-link') ||
                        element.classList.contains('btn') ||
                        element.classList.contains('badge') ||
                        element.classList.contains('form-control') ||
                        element.classList.contains('form-select') ||
                        element.classList.contains('form-check') ||
                        element.classList.contains('form-check-input') ||
                        element.classList.contains('form-check-label') ||
                        element.classList.contains('input-group-text') ||
                        element.classList.contains('navbar') ||
                        element.classList.contains('navbar-brand') ||
                        element.classList.contains('navbar-nav') ||
                        element.classList.contains('navbar-toggler') ||
                        element.classList.contains('collapse') ||
                        element.classList.contains('container') ||
                        element.classList.contains('container-fluid') ||
                        element.classList.contains('row') ||
                        element.classList.contains('col') ||
                        element.tagName === 'BUTTON' ||
                        element.tagName === 'INPUT' ||
                        element.tagName === 'SELECT' ||
                        element.tagName === 'TEXTAREA' ||
                        element.tagName === 'LABEL' ||
                        element.tagName === 'A' ||
                        // Check if element is a dropdown or has dropdown parent
                        element.closest('.dropdown') !== null ||
                        element.querySelector('.dropdown-menu') !== null) {
                        skipElement = true;
                    }

                    // Apply the class if not skipped
                    if (!skipElement) {
                        element.classList.add('roadmap-gradient-container');
                    }
                }
            });
        });
    }

    // Apply gradient borders initially
    window.applyGradientBorders();

    // Remove gradient effect from dropdown menus
    function fixDropdowns() {
        // Remove gradient from dropdown menus
        document.querySelectorAll('.dropdown-menu').forEach(menu => {
            menu.classList.remove('roadmap-gradient-container');
        });

        // Remove gradient from dropdown parents
        document.querySelectorAll('.dropdown').forEach(dropdown => {
            dropdown.classList.remove('roadmap-gradient-container');
        });

        // Remove gradient from dropdown toggles
        document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
            toggle.classList.remove('roadmap-gradient-container');
        });
    }

    // Fix dropdowns initially
    fixDropdowns();

    // Fix dropdowns when Bootstrap's dropdown is shown
    document.addEventListener('shown.bs.dropdown', fixDropdowns);
    document.addEventListener('hidden.bs.dropdown', fixDropdowns);

    // Set up a MutationObserver to apply gradient borders to new elements
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length) {
                applyGradientBorders();
                fixDropdowns();
            }
        });
    });

    // Start observing the document with the configured parameters
    observer.observe(document.body, { childList: true, subtree: true });

    // Log for debugging
    console.info('Gradient borders applied to all containers');

    // Function to toggle gradient borders on/off
    window.toggleGradientBorders = function(enabled) {
        if (enabled === false) {
            // Remove gradient borders from all elements
            document.querySelectorAll('.roadmap-gradient-container').forEach(element => {
                // We don't need to get computed styles anymore since we're using CSS classes

                // Remove gradient container class and add disabled class
                element.classList.remove('roadmap-gradient-container');
                element.classList.add('gradient-disabled');

                // Add a thin border to replace the gradient
                element.style.borderRadius = '10px';
            });

            // Update the gradient toggle icon
            const gradientToggle = document.getElementById('gradient-toggle');
            if (gradientToggle) {
                gradientToggle.style.opacity = '0.5';
                gradientToggle.title = 'Enable Gradient Borders';
            }

            localStorage.setItem('gradientBordersEnabled', 'false');
        } else {
            // Re-apply gradient borders to elements that had them before
            document.querySelectorAll('.gradient-disabled').forEach(element => {
                element.classList.add('roadmap-gradient-container');
                element.classList.remove('gradient-disabled');

                // Remove the border style
                element.style.border = '';
            });

            // Also apply to any new elements
            applyGradientBorders();

            // Update the gradient toggle icon
            const gradientToggle = document.getElementById('gradient-toggle');
            if (gradientToggle) {
                gradientToggle.style.opacity = '1';
                gradientToggle.title = 'Disable Gradient Borders';
            }

            localStorage.setItem('gradientBordersEnabled', 'true');
        }

        // Fix dropdowns after toggling
        fixDropdowns();
    };

    // Check if gradient borders should be disabled based on user preference
    if (localStorage.getItem('gradientBordersEnabled') === 'false') {
        window.toggleGradientBorders(false);
    } else {
        // Make sure the gradient toggle button is properly styled
        const gradientToggle = document.getElementById('gradient-toggle');
        if (gradientToggle) {
            gradientToggle.style.opacity = '1';
            gradientToggle.title = 'Disable Gradient Borders';
        }
    }
});

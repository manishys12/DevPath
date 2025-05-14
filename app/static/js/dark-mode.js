// Dark Mode Toggle Functionality
document.addEventListener('DOMContentLoaded', function() {
    // Get the theme toggle button
    const themeToggle = document.getElementById('theme-toggle');

    if (!themeToggle) {
        console.error('Theme toggle button not found');
        return;
    }

    // Check for saved theme preference or use the system preference
    const savedTheme = localStorage.getItem('theme') || 'light';

    // Apply the saved theme
    applyTheme(savedTheme);
    updateThemeIcon(savedTheme);

    // Toggle theme when button is clicked
    themeToggle.addEventListener('click', function() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

        // Update theme
        applyTheme(newTheme);
        localStorage.setItem('theme', newTheme);

        // Update icon
        updateThemeIcon(newTheme);
    });

    // Function to apply theme to document
    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        document.body.setAttribute('data-theme', theme);

        // Add theme class to body
        if (theme === 'dark') {
            document.body.classList.add('dark-mode');
            document.body.classList.remove('light-mode');
        } else {
            document.body.classList.add('light-mode');
            document.body.classList.remove('dark-mode');
        }

        // Update any theme-specific elements
        const bgLightElements = document.querySelectorAll('.bg-light');
        bgLightElements.forEach(el => {
            el.classList.toggle('bg-dark', theme === 'dark');
            el.classList.toggle('text-white', theme === 'dark');
        });

        // Update filter elements
        const filterGroups = document.querySelectorAll('.filter-group');
        if (filterGroups.length > 0) {
            // If we have filter groups, make sure they get the theme
            filterGroups.forEach(el => {
                const inputs = el.querySelectorAll('input, select');
                inputs.forEach(input => {
                    if (theme === 'dark') {
                        input.style.backgroundColor = 'var(--input-bg)';
                        input.style.color = 'var(--text-color)';
                        input.style.borderColor = 'var(--input-border)';
                    } else {
                        input.style.backgroundColor = '';
                        input.style.color = '';
                        input.style.borderColor = '';
                    }
                });
            });

            // Update clear filters button
            const clearFiltersBtn = document.getElementById('clearFilters');
            if (clearFiltersBtn) {
                if (theme === 'dark') {
                    if (clearFiltersBtn.classList.contains('btn-primary')) {
                        clearFiltersBtn.style.backgroundColor = 'var(--primary-color)';
                        clearFiltersBtn.style.borderColor = 'var(--primary-color)';
                    } else if (clearFiltersBtn.classList.contains('btn-danger')) {
                        clearFiltersBtn.style.backgroundColor = 'var(--danger-color)';
                        clearFiltersBtn.style.borderColor = 'var(--danger-color)';
                    }
                } else {
                    clearFiltersBtn.style.backgroundColor = '';
                    clearFiltersBtn.style.borderColor = '';
                }
            }
        }

        // Apply gradient borders after theme change
        setTimeout(function() {
            if (typeof window.applyGradientBorders === 'function') {
                window.applyGradientBorders('.roadmap-gradient-container');
            }
        }, 100);
    }

    // Function to update the theme toggle icon
    function updateThemeIcon(theme) {
        if (theme === 'dark') {
            themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
            themeToggle.setAttribute('title', 'Switch to Light Mode');
        } else {
            themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
            themeToggle.setAttribute('title', 'Switch to Dark Mode');
        }
    }
});

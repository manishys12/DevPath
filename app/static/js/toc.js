/**
 * Enhanced Table of Contents functionality for EdgeRoute
 */

class TableOfContents {
    constructor(options = {}) {
        // Default options
        this.options = {
            containerId: 'toc-container',
            tocId: 'toc',
            nodeSelector: '.roadmap-node',
            linkClass: 'toc-link',
            activeClass: 'active',
            completedClass: 'completed',
            progressBarId: 'toc-progress-bar-inner',
            progressTextId: 'toc-progress-text',
            searchId: 'toc-search',
            filterAllId: 'toc-filter-all',
            filterCompletedId: 'toc-filter-completed',
            filterRemainingId: 'toc-filter-remaining',
            offset: 70, // Offset for scrolling (header height)
            ...options
        };

        // State
        this.nodes = [];
        this.totalNodes = 0;
        this.completedNodes = 0;
        this.userProgress = {};
        this.currentFilter = 'all';
        this.searchTerm = '';

        // DOM Elements
        this.container = document.getElementById(this.options.containerId);
        this.toc = document.getElementById(this.options.tocId);
        this.progressBar = document.getElementById(this.options.progressBarId);
        this.progressText = document.getElementById(this.options.progressTextId);
        this.searchInput = document.getElementById(this.options.searchId);
        this.filterAll = document.getElementById(this.options.filterAllId);
        this.filterCompleted = document.getElementById(this.options.filterCompletedId);
        this.filterRemaining = document.getElementById(this.options.filterRemainingId);

        // Initialize
        this.init();
    }

    init() {
        console.log('Initializing TableOfContents');

        // Get all nodes
        this.nodes = document.querySelectorAll(this.options.nodeSelector);
        console.log(`Found ${this.nodes.length} nodes in the DOM`);

        // Initialize user progress by checking which TOC links have the completed class
        const completedLinks = document.querySelectorAll(`.${this.options.linkClass}.${this.options.completedClass}`);
        console.log(`Found ${completedLinks.length} completed links`);

        completedLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (href && href.startsWith('#node-')) {
                const nodeId = href.substring(6); // Remove '#node-' prefix
                this.userProgress[nodeId] = true;
            }
        });

        // Set up event listeners
        this.setupEventListeners();

        // Initial update of active item
        this.updateActiveItem();

        // Note: updateProgress() will be called separately with the correct values
        // from the template after initialization
    }

    setupEventListeners() {
        // Smooth scrolling for TOC links
        const tocLinks = document.querySelectorAll(`.${this.options.linkClass}`);
        tocLinks.forEach(link => {
            link.addEventListener('click', (e) => this.handleLinkClick(e, link));
        });

        // Update active item on scroll
        window.addEventListener('scroll', () => this.updateActiveItem());

        // Search functionality
        if (this.searchInput) {
            this.searchInput.addEventListener('input', (e) => this.handleSearch(e));
        }

        // Filter functionality
        if (this.filterAll) {
            this.filterAll.addEventListener('click', () => this.setFilter('all'));
        }
        if (this.filterCompleted) {
            this.filterCompleted.addEventListener('click', () => this.setFilter('completed'));
        }
        if (this.filterRemaining) {
            this.filterRemaining.addEventListener('click', () => this.setFilter('remaining'));
        }
    }

    handleLinkClick(e, link) {
        e.preventDefault();

        const targetId = link.getAttribute('href');
        const targetElement = document.querySelector(targetId);

        if (targetElement) {
            // Scroll the main window to the target element
            window.scrollTo({
                top: targetElement.offsetTop - this.options.offset,
                behavior: 'smooth'
            });

            // Highlight the active TOC item
            this.setActiveItem(link);
        }
    }

    setActiveItem(activeLink) {
        // Remove active class from all links
        const tocLinks = document.querySelectorAll(`.${this.options.linkClass}`);
        tocLinks.forEach(link => {
            link.classList.remove(this.options.activeClass);
        });

        // Add active class to the current link
        if (activeLink) {
            activeLink.classList.add(this.options.activeClass);
        }
    }

    updateActiveItem() {
        const scrollPosition = window.scrollY;

        // Find the current node in view
        let currentNodeId = null;
        this.nodes.forEach(node => {
            const nodeTop = node.offsetTop;
            const nodeHeight = node.offsetHeight;

            if (scrollPosition >= nodeTop - this.options.offset - 50 &&
                scrollPosition < nodeTop + nodeHeight - this.options.offset) {
                currentNodeId = node.id;
            }
        });

        // Update active TOC item
        if (currentNodeId) {
            const activeLink = document.querySelector(`.${this.options.linkClass}[href="#${currentNodeId}"]`);
            this.setActiveItem(activeLink);
        }
    }

    updateProgress(completedCount = null, totalCount = null) {
        console.log('updateProgress called with:', { completedCount, totalCount });
        console.log('Current state:', { completedNodes: this.completedNodes, totalNodes: this.totalNodes });

        // Update counts if provided
        if (completedCount !== null) {
            this.completedNodes = parseInt(completedCount, 10);
        }

        if (totalCount !== null) {
            this.totalNodes = parseInt(totalCount, 10);
        }

        // Ensure we have valid numbers
        if (isNaN(this.completedNodes)) this.completedNodes = 0;
        if (isNaN(this.totalNodes)) this.totalNodes = 0;

        console.log('Updated state:', { completedNodes: this.completedNodes, totalNodes: this.totalNodes });

        // Check if progress elements exist
        if (!this.progressBar || !this.progressText) {
            console.error('Progress bar elements not found:', {
                progressBar: this.progressBar,
                progressText: this.progressText
            });
            return;
        }

        // Calculate progress percentage
        const progressPercentage = this.totalNodes > 0
            ? Math.round((this.completedNodes / this.totalNodes) * 100)
            : 0;

        console.log('Progress percentage:', progressPercentage);

        // Update the progress bar
        this.progressBar.style.width = `${progressPercentage}%`;

        // Update the progress text
        this.progressText.textContent = `${this.completedNodes} of ${this.totalNodes} completed (${progressPercentage}%)`;
    }

    setNodeCompleted(nodeId, completed) {
        console.log(`Setting node ${nodeId} completed: ${completed}`);

        // Check if the node's state is already what we want to set it to
        const wasAlreadyCompleted = this.userProgress[nodeId] === true;

        if (completed === wasAlreadyCompleted) {
            console.log(`Node ${nodeId} was already ${completed ? 'completed' : 'not completed'}`);
            return; // No change needed
        }

        // Update user progress
        if (completed) {
            this.userProgress[nodeId] = true;
            this.completedNodes++;
            console.log(`Incremented completedNodes to ${this.completedNodes}`);
        } else {
            delete this.userProgress[nodeId];
            this.completedNodes--;
            console.log(`Decremented completedNodes to ${this.completedNodes}`);
        }

        // Update TOC item
        const tocLink = document.querySelector(`.${this.options.linkClass}[href="#node-${nodeId}"]`);
        if (tocLink) {
            console.log(`Updating TOC link for node ${nodeId}`);
            if (completed) {
                tocLink.classList.add(this.options.completedClass);
                const icon = tocLink.querySelector('i');
                if (icon) {
                    icon.className = 'fas fa-check-circle';
                }
            } else {
                tocLink.classList.remove(this.options.completedClass);
                const icon = tocLink.querySelector('i');
                if (icon) {
                    icon.className = 'far fa-circle';
                }
            }
        } else {
            console.warn(`TOC link for node ${nodeId} not found`);
        }

        // Update node
        const node = document.getElementById(`node-${nodeId}`);
        if (node) {
            console.log(`Updating node element for node ${nodeId}`);
            if (completed) {
                node.classList.add('node-completed');
            } else {
                node.classList.remove('node-completed');
            }
        } else {
            console.warn(`Node element for node ${nodeId} not found`);
        }

        // Update progress
        console.log('Updating progress after node completion change');
        this.updateProgress();

        // Apply current filter
        this.applyFilter();
    }

    handleSearch(e) {
        this.searchTerm = e.target.value.toLowerCase();
        this.applyFilter();
    }

    setFilter(filter) {
        this.currentFilter = filter;

        // Update filter buttons
        if (this.filterAll) {
            this.filterAll.classList.toggle('active', filter === 'all');
        }
        if (this.filterCompleted) {
            this.filterCompleted.classList.toggle('active', filter === 'completed');
        }
        if (this.filterRemaining) {
            this.filterRemaining.classList.toggle('active', filter === 'remaining');
        }

        this.applyFilter();
    }

    applyFilter() {
        const tocItems = document.querySelectorAll('.toc-item');

        tocItems.forEach(item => {
            const link = item.querySelector(`.${this.options.linkClass}`);
            if (!link) return;

            const href = link.getAttribute('href');
            if (!href) return;

            const nodeId = href.substring(6); // Remove '#node-' prefix
            const isCompleted = link.classList.contains(this.options.completedClass);
            const title = link.textContent.toLowerCase();

            // Apply search filter
            const matchesSearch = this.searchTerm === '' || title.includes(this.searchTerm);

            // Apply completion filter
            let matchesFilter = true;
            if (this.currentFilter === 'completed') {
                matchesFilter = isCompleted;
            } else if (this.currentFilter === 'remaining') {
                matchesFilter = !isCompleted;
            }

            // Show/hide item
            item.style.display = matchesSearch && matchesFilter ? '' : 'none';
        });
    }
}

// Export for use in the template
window.TableOfContents = TableOfContents;

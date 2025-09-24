// Image optimization
class ImageOptimizer {
    constructor() {
        if (ImageOptimizer.instance) {
            return ImageOptimizer.instance;
        }
        ImageOptimizer.instance = this;
        
        // Track preloaded images
        this.preloadedImages = new Set();

        this.loadedImages = new Set();
        this.supportsWebP = null;
        this.supportsAVIF = null;
        this.checkImageSupport();
        
        // Initialize connection monitoring
        this.connectionType = 'unknown';
        this.setupConnectionMonitoring();
        
        this.observer = new IntersectionObserver(
            this.handleIntersection.bind(this),
            {
                root: null,
                rootMargin: '50px',
                threshold: 0.1
            }
        );

        return this;
    }

    handleIntersection(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                this.loadImage(entry.target);
                this.observer.unobserve(entry.target);
            }
        });
    }

    loadImage(img) {
        const src = img.dataset.src;
        if (!src || this.loadedImages.has(src)) return;

        // Add native loading hint
        img.loading = 'lazy';
        
        // Create blur-up preview if provided
        if (img.dataset.preview) {
            const wrapper = document.createElement('div');
            wrapper.className = 'img-wrapper';
            img.parentNode.insertBefore(wrapper, img);
            wrapper.appendChild(img);
            
            const blurUp = document.createElement('div');
            blurUp.className = 'blur-up';
            blurUp.style.backgroundImage = `url(${img.dataset.preview})`;
            wrapper.appendChild(blurUp);
        }

        // Load responsive image based on viewport width
        const viewportWidth = window.innerWidth;
        const srcset = img.dataset.srcset;

        if (srcset) {
            const sources = srcset.split(',').map(s => {
                const [url, width] = s.trim().split(' ');
                return {
                    url: this.getBestFormat(url),
                    width: parseInt(width.replace('w', ''))
                };
            });

            // Find the best matching image size based on connection
            const bestMatch = this.getOptimalImageSize(sources, viewportWidth);

            img.src = bestMatch.url;
        } else {
            img.src = src;
        }

        img.onload = () => {
            img.classList.add('loaded');
            this.loadedImages.add(src);
        };

        img.onerror = () => {
            // Add error class for styling
            img.classList.add('error');
            // Try to load fallback image if provided
            const fallback = img.dataset.fallback;
            if (fallback && !this.loadedImages.has(fallback)) {
                img.src = fallback;
                this.loadedImages.add(fallback);
            } else {
                // If no fallback, show error placeholder
                img.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"%3E%3Cpath d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z" fill="%23ccc"/%3E%3C/svg%3E';
            }
        };
    }

    observe(img) {
        if (!img.dataset.src) return;
        this.observer.observe(img);
    }

    observeAll() {
        document.querySelectorAll('img[data-src]').forEach(img => {
            this.observe(img);
        });
    }

    static getInstance() {
        if (!this.instance) {
            this.instance = new ImageOptimizer();
        }
        return this.instance;
    }

    async checkImageSupport() {
        // Check WebP support
        this.supportsWebP = await new Promise(resolve => {
            const webP = new Image();
            webP.onload = webP.onerror = function() {
                resolve(webP.height === 2);
            };
            webP.src = 'data:image/webp;base64,UklGRjoAAABXRUJQVlA4IC4AAACyAgCdASoCAAIALmk0mk0iIiIiIgBoSygABc6WWgAA/veff/0PP8bA//LwYAAA';
        });

        // Check AVIF support
        this.supportsAVIF = await new Promise(resolve => {
            const avif = new Image();
            avif.onload = avif.onerror = function() {
                resolve(avif.height === 2);
            };
            avif.src = 'data:image/avif;base64,AAAAIGZ0eXBhdmlmAAAAAGF2aWZtaWYxbWlhZk1BMUIAAADybWV0YQAAAAAAAAAoaGRscgAAAAAAAAAAcGljdAAAAAAAAAAAAAAAAGxpYmF2aWYAAAAADnBpdG0AAAAAAAEAAAAeaWxvYwAAAABEAAABAAEAAAABAAABGgAAABcAAAAoaWluZgAAAAAAAQAAABppbmZlAgAAAAABAABhdjAxQ29sb3IAAAAAamlwcnAAAABLaXBjbwAAABRpc3BlAAAAAAAAAAEAAAABAAAAEHBpeGkAAAAAAwgICAAAAAxhdjFDgQAMAAAAABNjb2xybmNseAACAAIABoAAAAAXaXBtYQAAAAAAAAABAAEEAQKDBAAAAB9tZGF0EgAKCBgABogQEDQgMgkQAAAAB8dSLfI=';
        });
    }

    getBestFormat(src) {
        const ext = src.split('.').pop().toLowerCase();
        const basePath = src.slice(0, -ext.length - 1);

        if (this.supportsAVIF && this.hasFormat(basePath, 'avif')) {
            return `${basePath}.avif`;
        }
        if (this.supportsWebP && this.hasFormat(basePath, 'webp')) {
            return `${basePath}.webp`;
        }
        return src;
    }

    hasFormat(basePath, format) {
        // You can implement a more sophisticated check here if needed
        // For now, we'll assume if the base image exists, the converted format exists too
        return true;
    }

    setupConnectionMonitoring() {
        if ('connection' in navigator) {
            this.updateConnectionType(navigator.connection);
            navigator.connection.addEventListener('change', () => {
                this.updateConnectionType(navigator.connection);
            });
        }
    }

    updateConnectionType(connection) {
        const effectiveType = connection?.effectiveType || 'unknown';
        const saveData = connection?.saveData || false;
        
        if (saveData) {
            this.connectionType = 'saveData';
        } else {
            switch (effectiveType) {
                case 'slow-2g':
                case '2g':
                    this.connectionType = 'slow';
                    break;
                case '3g':
                    this.connectionType = 'medium';
                    break;
                case '4g':
                    this.connectionType = 'fast';
                    break;
                default:
                    this.connectionType = 'unknown';
            }
        }
    }

    preloadCriticalImages() {
        // Find all critical images (those marked with data-critical="true")
        document.querySelectorAll('img[data-critical="true"]').forEach(img => {
            const src = img.dataset.src;
            if (!src || this.preloadedImages.has(src)) return;

            // Create a link preload tag
            const preloadLink = document.createElement('link');
            preloadLink.rel = 'preload';
            preloadLink.as = 'image';
            preloadLink.href = this.getBestFormat(src);
            
            if (img.dataset.srcset) {
                const sources = img.dataset.srcset.split(',').map(s => {
                    const [url, width] = s.trim().split(' ');
                    return {
                        url: this.getBestFormat(url),
                        width: parseInt(width.replace('w', ''))
                    };
                });
                
                const bestMatch = this.getOptimalImageSize(sources, window.innerWidth);
                preloadLink.href = bestMatch.url;
            }

            document.head.appendChild(preloadLink);
            this.preloadedImages.add(src);
            
            // Load the image immediately
            this.loadImage(img);
        });
    }

    getOptimalImageSize(sources, viewportWidth) {
        // Adjust image size based on connection type
        const connectionFactor = {
            'saveData': 0.5,  // Load much smaller images in save-data mode
            'slow': 0.7,      // Load smaller images on slow connections
            'medium': 0.85,   // Load slightly smaller images on medium connections
            'fast': 1,        // Load full size on fast connections
            'unknown': 1      // Default to full size if connection type unknown
        };

        const factor = connectionFactor[this.connectionType];
        const targetWidth = viewportWidth * factor;

        return sources.reduce((prev, curr) => {
            const prevDiff = Math.abs(prev.width - targetWidth);
            const currDiff = Math.abs(curr.width - targetWidth);
            return currDiff < prevDiff ? curr : prev;
        });
    }
}

// Initialize lazy loading on page load
document.addEventListener('DOMContentLoaded', () => {
    const imageOptimizer = ImageOptimizer.getInstance();
    // First preload critical images
    imageOptimizer.preloadCriticalImages();
    // Then set up lazy loading for the rest
    imageOptimizer.observeAll();

    // Rerun observation when new content is loaded dynamically
    const observer = new MutationObserver((mutations) => {
        mutations.forEach(mutation => {
            mutation.addedNodes.forEach(node => {
                if (node instanceof HTMLElement) {
                    node.querySelectorAll('img[data-src]').forEach(img => {
                        imageOptimizer.observe(img);
                    });
                }
            });
        });
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
});
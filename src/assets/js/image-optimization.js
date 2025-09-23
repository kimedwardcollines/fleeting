// Image optimization
class ImageOptimizer {
    constructor() {
        if (ImageOptimizer.instance) {
            return ImageOptimizer.instance;
        }
        ImageOptimizer.instance = this;

        this.loadedImages = new Set();
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

        // Load responsive image based on viewport width
        const viewportWidth = window.innerWidth;
        const srcset = img.dataset.srcset;

        if (srcset) {
            const sources = srcset.split(',').map(s => {
                const [url, width] = s.trim().split(' ');
                return {
                    url,
                    width: parseInt(width.replace('w', ''))
                };
            });

            // Find the best matching image size
            const bestMatch = sources.reduce((prev, curr) => {
                const prevDiff = Math.abs(prev.width - viewportWidth);
                const currDiff = Math.abs(curr.width - viewportWidth);
                return currDiff < prevDiff ? curr : prev;
            });

            img.src = bestMatch.url;
        } else {
            img.src = src;
        }

        img.onload = () => {
            img.classList.add('loaded');
            this.loadedImages.add(src);
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
}

// Initialize lazy loading on page load
document.addEventListener('DOMContentLoaded', () => {
    const imageOptimizer = ImageOptimizer.getInstance();
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
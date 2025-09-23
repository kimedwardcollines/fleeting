// Lazy loading and responsive image handling
class ImageOptimizer {
    private static instance: ImageOptimizer;
    private observer: IntersectionObserver;
    private loadedImages: Set<string>;

    private constructor() {
        this.loadedImages = new Set();
        this.observer = new IntersectionObserver(
            this.handleIntersection.bind(this),
            {
                root: null,
                rootMargin: '50px',
                threshold: 0.1
            }
        );
    }

    static getInstance(): ImageOptimizer {
        if (!ImageOptimizer.instance) {
            ImageOptimizer.instance = new ImageOptimizer();
        }
        return ImageOptimizer.instance;
    }

    private handleIntersection(entries: IntersectionObserverEntry[]) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target as HTMLImageElement;
                this.loadImage(img);
                this.observer.unobserve(img);
            }
        });
    }

    private loadImage(img: HTMLImageElement) {
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

    observe(img: HTMLImageElement) {
        if (!img.dataset.src) return;
        this.observer.observe(img);
    }

    observeAll() {
        document.querySelectorAll('img[data-src]').forEach(img => {
            this.observe(img as HTMLImageElement);
        });
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
                        imageOptimizer.observe(img as HTMLImageElement);
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
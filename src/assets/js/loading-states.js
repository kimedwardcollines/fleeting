// Enhanced loading states with progressive image loading and lazy loading
document.addEventListener('DOMContentLoaded', () => {
    // Initialize lazy loading for images
    const lazyImages = document.querySelectorAll('img[data-src], source[data-srcset]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                loadImage(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, {
        rootMargin: '50px 0px', // Start loading images 50px before they enter viewport
        threshold: 0.01
    });

    function loadImage(element) {
        if (element.tagName === 'IMG') {
            const src = element.getAttribute('data-src');
            if (src) {
                element.src = src;
                element.classList.add('fade-in');
                element.removeAttribute('data-src');
            }
        } else if (element.tagName === 'SOURCE') {
            const srcset = element.getAttribute('data-srcset');
            if (srcset) {
                element.srcset = srcset;
                element.removeAttribute('data-srcset');
            }
        }
    }

    // Apply lazy loading to all images
    lazyImages.forEach(img => imageObserver.observe(img));

    // Loading state handler
    class LoadingState {
        constructor(element, loadingClass = 'loading', ariaLabel = 'Loading...') {
            this.element = element;
            this.loadingClass = loadingClass;
            this.ariaLabel = ariaLabel;
        }

        start() {
            this.element.classList.add(this.loadingClass);
            this.element.setAttribute('aria-busy', 'true');
            this.element.setAttribute('aria-label', this.ariaLabel);
        }

        stop() {
            this.element.classList.remove(this.loadingClass);
            this.element.removeAttribute('aria-busy');
            this.element.removeAttribute('aria-label');
        }
    }

    // Image preloader for critical images
    class ImagePreloader {
        static preloadImages(images) {
            return Promise.all(images.map(imageUrl => {
                return new Promise((resolve, reject) => {
                    const img = new Image();
                    img.onload = resolve;
                    img.onerror = reject;
                    img.src = imageUrl;
                });
            }));
        }
    }
        this.images = this.gallery.querySelectorAll('img');
        this.loadingState = new LoadingState(this.gallery, 'gallery-loading', 'Loading gallery images...');
        this.init();
    }

    init() {
        this.loadingState.start();
        let loadedImages = 0;

        const checkAllLoaded = () => {
            loadedImages++;
            if (loadedImages === this.images.length) {
                this.loadingState.stop();
            }
        };

        this.images.forEach(img => {
            if (img.complete) {
                checkAllLoaded();
            } else {
                img.addEventListener('load', checkAllLoaded);
                img.addEventListener('error', checkAllLoaded);
            }
        });
    }
}

// Sermon player loading handler
class SermonPlayerLoader {
    constructor(playerId) {
        const player = document.getElementById(playerId);
        if (!player) {
            console.warn(`Player with id ${playerId} not found`);
            return;
        }
        this.player = player;
        
        const audio = player.querySelector('audio');
        if (!audio) {
            console.warn(`Audio element not found in player ${playerId}`);
            return;
        }
        this.audio = audio;

        this.loadingState = new LoadingState(this.player, 'player-loading', 'Loading sermon audio...');
        this.init();
    }

    init() {
        this.audio.addEventListener('loadstart', () => {
            this.loadingState.start();
        });

        this.audio.addEventListener('canplay', () => {
            this.loadingState.stop();
        });

        this.audio.addEventListener('error', () => {
            this.loadingState.stop();
            this.player.classList.add('error');
        });
    }
}

// Initialize loading states
document.addEventListener('DOMContentLoaded', () => {
    // Initialize gallery loaders
    document.querySelectorAll('.gallery').forEach((gallery, index) => {
        gallery.id = gallery.id || `gallery-${index}`;
        new ImageGalleryLoader(gallery.id);
    });

    // Initialize sermon players
    document.querySelectorAll('.sermon-player').forEach((player, index) => {
        player.id = player.id || `sermon-player-${index}`;
        new SermonPlayerLoader(player.id);
    });
});
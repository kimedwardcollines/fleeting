// Loading states
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

// Image gallery loading handler
class ImageGalleryLoader {
    constructor(galleryId) {
        const gallery = document.getElementById(galleryId);
        if (!gallery) {
            console.warn(`Gallery with id ${galleryId} not found`);
            return;
        }
        this.gallery = gallery;
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
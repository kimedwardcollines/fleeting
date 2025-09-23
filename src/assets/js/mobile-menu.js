// Mobile menu enhancements
class MobileMenu {
    constructor() {
        this.menu = document.querySelector('.nav-menu');
        this.toggle = document.querySelector('.mobile-menu');
        this.isOpen = false;
        this.touchStartX = 0;
        this.touchStartY = 0;
        this.SWIPE_THRESHOLD = 50;
        
        if (!this.menu || !this.toggle) {
            console.warn('Mobile menu elements not found');
            return;
        }

        this.createOverlay();
        this.init();
    }

    createOverlay() {
        this.overlay = document.createElement('div');
        this.overlay.className = 'mobile-menu-overlay';
        document.body.appendChild(this.overlay);

        this.overlay.addEventListener('click', () => {
            this.close();
        });
    }

    init() {
        // Toggle button click handler
        this.toggle.addEventListener('click', (e) => {
            e.preventDefault();
            this.isOpen ? this.close() : this.open();
        });

        // Touch event handlers
        this.menu.addEventListener('touchstart', (e) => {
            this.touchStartX = e.touches[0].clientX;
            this.touchStartY = e.touches[0].clientY;
        });

        this.menu.addEventListener('touchmove', (e) => {
            if (!this.isOpen) return;

            const touchX = e.touches[0].clientX;
            const touchY = e.touches[0].clientY;
            
            // Calculate swipe distance and angle
            const deltaX = touchX - this.touchStartX;
            const deltaY = touchY - this.touchStartY;
            const angle = Math.abs(Math.atan2(deltaY, deltaX) * 180 / Math.PI);

            // Only handle horizontal swipes (angle less than 45 degrees)
            if (angle < 45) {
                e.preventDefault();
                if (deltaX < 0) {
                    this.menu.style.transform = `translateX(${deltaX}px)`;
                }
            }
        });

        this.menu.addEventListener('touchend', (e) => {
            if (!this.isOpen) return;

            const touchX = e.changedTouches[0].clientX;
            const deltaX = touchX - this.touchStartX;

            if (Math.abs(deltaX) > this.SWIPE_THRESHOLD) {
                if (deltaX < 0) {
                    this.close();
                }
            } else {
                this.menu.style.transform = '';
            }
        });

        // Handle escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.close();
            }
        });

        // Close menu on resize if in desktop view
        window.addEventListener('resize', () => {
            if (window.innerWidth > 768 && this.isOpen) {
                this.close();
            }
        });
    }

    open() {
        this.isOpen = true;
        this.menu.classList.add('active');
        this.toggle.classList.add('active');
        this.overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
        
        // Animate menu items
        this.menu.querySelectorAll('.nav-item').forEach((item, index) => {
            setTimeout(() => {
                item.style.opacity = '1';
                item.style.transform = 'translateX(0)';
            }, 100 * index);
        });
    }

    close() {
        this.isOpen = false;
        this.menu.style.transform = '';
        this.menu.classList.remove('active');
        this.toggle.classList.remove('active');
        this.overlay.classList.remove('active');
        document.body.style.overflow = '';

        // Reset menu items
        this.menu.querySelectorAll('.nav-item').forEach(item => {
            item.style.opacity = '';
            item.style.transform = '';
        });
    }
}

// Initialize mobile menu on page load
document.addEventListener('DOMContentLoaded', () => {
    new MobileMenu();
});
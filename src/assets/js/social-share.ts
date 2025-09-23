// Social sharing functionality
class SocialShare {
    private static readonly SHARE_APIS = {
        facebook: (url: string, title: string) => 
            `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`,
        twitter: (url: string, title: string) => 
            `https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=${encodeURIComponent(title)}`,
        whatsapp: (url: string, title: string) => 
            `https://wa.me/?text=${encodeURIComponent(`${title} ${url}`)}`,
        email: (url: string, title: string) => 
            `mailto:?subject=${encodeURIComponent(title)}&body=${encodeURIComponent(`Check this out: ${url}`)}`,
        linkedin: (url: string, title: string) => 
            `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`
    };

    private container: HTMLElement;
    private url: string;
    private title: string;
    private description: string;

    constructor(container: HTMLElement, title: string, description: string = '') {
        this.container = container;
        this.title = title;
        this.description = description;
        this.url = window.location.href;
        this.init();
    }

    private init() {
        // Create share buttons container
        const shareButtonsContainer = document.createElement('div');
        shareButtonsContainer.className = 'share-buttons';
        
        // Add share heading
        const heading = document.createElement('h4');
        heading.className = 'share-heading';
        heading.textContent = 'Share This';
        shareButtonsContainer.appendChild(heading);

        // Add share buttons
        Object.keys(SocialShare.SHARE_APIS).forEach(platform => {
            const button = this.createShareButton(platform);
            shareButtonsContainer.appendChild(button);
        });

        // Add native share button if available
        if (navigator.share) {
            const nativeButton = this.createNativeShareButton();
            shareButtonsContainer.appendChild(nativeButton);
        }

        this.container.appendChild(shareButtonsContainer);
    }

    private createShareButton(platform: string): HTMLButtonElement {
        const button = document.createElement('button');
        button.className = `share-button share-${platform}`;
        button.setAttribute('aria-label', `Share on ${platform}`);

        const icon = document.createElement('i');
        icon.className = `fab fa-${platform}`;
        if (platform === 'email') {
            icon.className = 'fas fa-envelope';
        }
        
        button.appendChild(icon);

        button.addEventListener('click', (e) => {
            e.preventDefault();
            const shareUrl = SocialShare.SHARE_APIS[platform](this.url, this.title);
            window.open(shareUrl, '_blank', 'width=600,height=400');
        });

        return button;
    }

    private createNativeShareButton(): HTMLButtonElement {
        const button = document.createElement('button');
        button.className = 'share-button share-native';
        button.setAttribute('aria-label', 'Share');

        const icon = document.createElement('i');
        icon.className = 'fas fa-share-alt';
        button.appendChild(icon);

        button.addEventListener('click', async () => {
            try {
                await navigator.share({
                    title: this.title,
                    text: this.description,
                    url: this.url
                });
            } catch (err) {
                console.log('Error sharing:', err);
            }
        });

        return button;
    }

    static init() {
        // Initialize share buttons for all sharable content
        document.querySelectorAll('[data-sharable]').forEach(element => {
            if (element instanceof HTMLElement) {
                const title = element.getAttribute('data-share-title') || document.title;
                const description = element.getAttribute('data-share-description') || '';
                new SocialShare(element, title, description);
            }
        });
    }
}

// Initialize social sharing on page load
document.addEventListener('DOMContentLoaded', () => {
    SocialShare.init();
});
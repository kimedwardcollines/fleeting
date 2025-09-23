// About section functionality
class AboutSection {
    constructor() {
        this.features = [
            {
                iconClass: "fas fa-heart",
                title: "Loving Community",
                description: "A welcoming family where everyone belongs and grows together in faith."
            },
            {
                iconClass: "fas fa-book",
                title: "Biblical Teaching",
                description: "Grounded in Scripture with practical application for daily living and spiritual growth."
            },
            {
                iconClass: "fas fa-users",
                title: "Active Ministry",
                description: "Engaging ministries for all ages, especially our vibrant youth community."
            }
        ];
        this.init();
    }

    createFeatureCard(feature) {
        return `
            <div class="card p-6 hover-shadow-gentle transition-all duration-300 hover-scale-105">
                <div class="flex items-start space-x-4">
                    <div class="flex-shrink-0">
                        <i class="${feature.iconClass} w-8 h-8 text-warm-gold"></i>
                    </div>
                    <div>
                        <h4 class="text-lg font-semibold text-spiritual mb-2">
                            ${feature.title}
                        </h4>
                        <p class="text-muted-foreground">
                            ${feature.description}
                        </p>
                    </div>
                </div>
            </div>
        `;
    }

    init() {
        const aboutSection = document.getElementById('about');
        if (!aboutSection) return;

        // Render features
        const featuresContainer = aboutSection.querySelector('.features-grid');
        if (featuresContainer) {
            featuresContainer.innerHTML = this.features
                .map(feature => this.createFeatureCard(feature))
                .join('');
        }

        // Add animation on scroll
        const cards = aboutSection.querySelectorAll('.card');
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-fade-in');
                }
            });
        }, { threshold: 0.1 });

        cards.forEach(card => observer.observe(card));
    }

    static init() {
        new AboutSection();
    }
}

// Initialize about section on page load
document.addEventListener('DOMContentLoaded', AboutSection.init);
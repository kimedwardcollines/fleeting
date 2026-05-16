# Fleeting Logistics Company Limited - Website Specification

## 1. Project Overview
- **Project Name**: Fleeting Logistics Company Limited
- **Type**: Corporate logistics company website
- **Core Functionality**: Informational website showcasing logistics services with contact form
- **Target Users**: Businesses and individuals seeking logistics services

## 2. Technology Stack
- Backend: Python Django 4.x
- Frontend: HTML5, CSS3, Bootstrap 5.3
- Database: SQLite (development)
- Media Files: Local storage

## 3. UI/UX Specification

### Color Palette
- Primary: `#0A2463` (Deep Blue)
- Secondary: `#1E5AA8` (Medium Blue)
- Accent: `#FF6B35` (Orange - CTA buttons)
- Light: `#F8F9FA` (Off-white background)
- Dark: `#212529` (Text)
- White: `#FFFFFF`

### Typography
- Headings: 'Poppins', sans-serif (Google Fonts)
- Body: 'Open Sans', sans-serif (Google Fonts)
- H1: 48px, weight 700
- H2: 36px, weight 600
- H3: 24px, weight 600
- Body: 16px, weight 400

### Layout Structure
- Max content width: 1200px
- Responsive breakpoints:
  - Mobile: < 768px
  - Tablet: 768px - 1024px
  - Desktop: > 1024px

### Components
- **Navbar**: Fixed-top, white background, shadow on scroll
- **Hero**: Full-width, 80vh height, gradient overlay
- **Cards**: White background, subtle shadow, rounded corners (8px)
- **Buttons**: Rounded corners (4px), transition effects
- **Footer**: Dark blue background, multi-column layout

## 4. Page Specifications

### Home Page
- Hero section with logistics truck background image
- Tagline: "Fast, Reliable, and Efficient Logistics Solutions"
- Company intro (2-3 sentences)
- CTA button: "Get a Quote" (accent orange)
- Services preview (3 cards)
- Why choose us snapshot

### About Page
- Company description (400-500 words)
- Mission statement
- Vision statement
- Why choose us (4 key points with icons)

### Services Page
- 4 service cards in grid:
  1. Cargo Transportation - Truck icon
  2. Freight Forwarding - Ship icon
  3. Warehousing - Warehouse icon
  4. Delivery Services - Box icon
- Each card: icon, title, description (100-150 words)

### Contact Page
- Two-column layout:
  - Left: Contact form (Name, Email, Message)
  - Right: Contact info + map placeholder
- Form validation with Bootstrap

## 5. Animations
- Fade-in on page load (0.5s)
- Button hover: scale(1.05) with 0.3s transition
- Card hover: translateY(-5px) with shadow increase
- Navbar: smooth scroll behavior

## 6. Django Structure
```
logistics_project/
├── manage.py
├── logistics_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── logistics/
    ├── __init__.py
    ├── views.py
    ├── urls.py
    └── templates/
        └── logistics/
            ├── base.html
            ├── home.html
            ├── about.html
            ├── services.html
            └── contact.html
```

## 7. Acceptance Criteria
- [ ] All pages render without errors
- [ ] Navigation works between all pages
- [ ] Forms display and are validated
- [ ] Responsive on mobile/tablet/desktop
- [ ] Animations work smoothly
- [ ] Bootstrap styling applied correctly
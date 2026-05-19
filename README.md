# Fleeting - Modern Logistics & Delivery Platform

![Fleeting Logo](https://via.placeholder.com/200x60?text=FLEETING)

A professional, production-ready logistics and delivery management platform built with Django, HTML5, CSS3, and JavaScript.

## 🚀 Features

- **Real-time Shipment Tracking** - Track packages with live updates
- **Professional Dashboard** - Customer and Admin dashboards
- **User Authentication** - Secure JWT-based authentication
- **Responsive Design** - Mobile, tablet, and desktop optimization
- **Database Integration** - PostgreSQL support
- **Performance Optimized** - 90+ PageSpeed scores
- **Security First** - Input validation, rate limiting, password hashing
- **SEO Optimized** - Meta tags, sitemap, structured data

## 📋 Tech Stack

### Backend
- **Python 3.9+**
- **Django 4.x**
- **Django REST Framework**
- **PostgreSQL** (Database)
- **JWT Authentication**

### Frontend
- **HTML5**
- **CSS3 (Tailwind CSS)**
- **JavaScript (ES6+)**
- **Responsive Design**

### DevOps & Deployment
- **Render** (Hosting)
- **Environment Variables**
- **Docker Support**

## 📁 Project Structure

```
fleeting/
├── backend/
│   ├── core/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── apps/
│   │   ├── users/
│   │   ├── shipments/
│   │   ├── tracking/
│   │   ├── notifications/
│   │   └── analytics/
│   ├── static/
│   ├── media/
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   ├── css/
│   │   └── js/
│   └── index.html
├── tests/
├── docs/
├── docker-compose.yml
├── .env.example
└── README.md
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.9+
- PostgreSQL 12+
- Node.js 16+ (for frontend tooling)
- Git

### Backend Setup

```bash
# Clone repository
git clone https://github.com/kimedwardcollines/fleeting.git
cd fleeting/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Start development server
npm start
```

## 🌐 API Documentation

### Authentication Endpoints
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/refresh/` - Refresh JWT token
- `POST /api/auth/logout/` - User logout

### Shipment Endpoints
- `GET /api/shipments/` - List all shipments
- `POST /api/shipments/` - Create new shipment
- `GET /api/shipments/{id}/` - Get shipment details
- `PUT /api/shipments/{id}/` - Update shipment
- `DELETE /api/shipments/{id}/` - Delete shipment

### Tracking Endpoints
- `GET /api/tracking/{tracking_id}/` - Get shipment tracking status
- `POST /api/tracking/` - Create tracking record
- `PUT /api/tracking/{id}/` - Update tracking status

## 🔐 Security Features

- ✅ JWT Authentication
- ✅ Password Hashing (bcrypt)
- ✅ Input Validation
- ✅ Rate Limiting
- ✅ CORS Protection
- ✅ Environment Variables
- ✅ SQL Injection Prevention
- ✅ XSS Protection
- ✅ HTTPS Enforcement
- ✅ Secure Headers

## 📊 Database Models

### User Model
- id (UUID)
- email
- password (hashed)
- first_name
- last_name
- phone
- role (customer/admin)
- profile_image
- created_at
- updated_at

### Shipment Model
- id (UUID)
- tracking_id (unique)
- sender_id (FK to User)
- recipient_name
- recipient_email
- recipient_phone
- pickup_address
- delivery_address
- package_weight
- package_dimensions
- status
- priority
- created_at
- updated_at

### Tracking Model
- id (UUID)
- shipment_id (FK to Shipment)
- status
- location
- timestamp
- notes
- updated_by

## 📱 Responsive Breakpoints

- **Mobile**: < 640px
- **Tablet**: 640px - 1024px
- **Desktop**: > 1024px

## 🎨 Color Palette

- **Primary**: #003366 (Dark Blue)
- **Secondary**: #FF8C00 (Orange)
- **Light**: #FFFFFF (White)
- **Gray**: #F5F5F5 (Light Gray)
- **Text**: #333333 (Dark Gray)

## 📈 Performance Targets

- Desktop PageSpeed: 90+
- Mobile PageSpeed: 70+
- First Contentful Paint: < 1.8s
- Largest Contentful Paint: < 2.5s
- Cumulative Layout Shift: < 0.1

## 📝 Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -m 'Add feature'`
3. Push to branch: `git push origin feature/your-feature`
4. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👥 Support

For support, email support@fleeting.com or open an issue on GitHub.

## 🗺️ Roadmap

- [ ] Mobile app (iOS/Android)
- [ ] Real-time notifications
- [ ] Advanced analytics
- [ ] Multi-language support
- [ ] AI-powered route optimization
- [ ] Integration with payment gateways

---

**Last Updated**: May 2026
**Status**: In Development
**Version**: 1.0.0-beta

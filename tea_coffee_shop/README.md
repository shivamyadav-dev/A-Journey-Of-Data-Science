# Brew & Sip - Premium Tea & Coffee Shop

A modern, interactive web application for an online tea and coffee shop with instant delivery service. Built with Flask, featuring a beautiful responsive UI and full e-commerce functionality.

## Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation
```bash
cd tea_coffee_shop
pip install -r requirements.txt
python app.py
```

Open your browser at `http://localhost:5000`.

## Project Structure
```
tea_coffee_shop/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── menu.html
│   ├── cart.html
│   ├── checkout.html
│   ├── product_detail.html
│   ├── order_confirmation.html
│   ├── about.html
│   └── contact.html
└── static/
    ├── styles.css
    └── images/
```

## Notes
- SQLite database (`tea_coffee_shop.db`) is created on first run.
- Sample products are auto-seeded.
- CSRF protection is enabled for all forms.
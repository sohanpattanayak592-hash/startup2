# NOVOPLAST Store 🛍️

> Premium Non-Tearable Plastic Prints — E-Commerce Platform

A high-end e-commerce site for **NOVOPLAST by EVERRLEAF**, selling personalized non-tearable plastic prints including Custom Posters, Spiritual Prints (Shlokas & Artis), and Custom Stickers.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 18 + Vite + Tailwind CSS 3 |
| **Backend** | Python + FastAPI |
| **Animations** | Framer Motion |
| **Icons** | Lucide React |
| **Payments** | Razorpay (configurable) |

## Features

- 🖼 **Custom Posters** — HD plastic prints with personalization
- 🕉 **Spiritual Prints** — Shlokas & Artis with gold/saffron theme + personal dedications
- ✨ **Custom Stickers** — Upload your design (JPG/PNG/SVG) with neon cyberpunk theme
- 🛡 **Durability Badges** — Visual emphasis on Non-Tearable, Waterproof, UV-Resistant properties
- 💳 **Razorpay Integration** — Payment gateway with order creation
- 📱 **Fully Responsive** — Mobile-first dark mode design
- 🎨 **Premium Glassmorphism UI** — Glass cards, animated gradients, floating orbs

## Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.10+

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`

### Backend

```bash
cd backend
pip install -r requirements.txt
python main.py
```

Backend runs on `http://localhost:8000`

### Environment Variables (Backend)

```env
RAZORPAY_KEY_ID=rzp_test_XXXXXXXXXX
RAZORPAY_KEY_SECRET=your_razorpay_secret
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API status |
| `POST` | `/orders` | Create a new custom order |
| `GET` | `/orders` | List all orders |
| `GET` | `/orders/{order_id}` | Get order details |

### POST /orders — Form Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `product_id` | string | ✅ | Product slug |
| `product_name` | string | ✅ | Product display name |
| `size` | string | ❌ | Selected size |
| `quantity` | string | ❌ | Selected quantity |
| `personalization_text` | string | ❌ | Custom dedication text |
| `shloka` | string | ❌ | Selected shloka/arti |
| `total_price` | float | ✅ | Total order price |
| `customer_name` | string | ✅ | Customer name |
| `customer_email` | string | ✅ | Customer email |
| `customer_phone` | string | ✅ | Customer phone |
| `design_file` | file | ❌ | Uploaded sticker design |

## Project Structure

```
novoplast-store/
├── frontend/
│   ├── public/             # Static assets & product images
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   │   ├── Navbar.jsx
│   │   │   ├── Footer.jsx
│   │   │   ├── DurabilityBadges.jsx
│   │   │   ├── PersonalizationInput.jsx
│   │   │   └── StickerUploader.jsx
│   │   ├── pages/
│   │   │   ├── HomePage.jsx
│   │   │   ├── ProductPage.jsx
│   │   │   └── CheckoutPage.jsx
│   │   ├── data/
│   │   │   └── products.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── tailwind.config.js
│   ├── vite.config.js
│   └── package.json
├── backend/
│   ├── main.py             # FastAPI application
│   ├── requirements.txt
│   └── uploads/            # Uploaded sticker designs
└── README.md
```

## Design System

- **Dark Mode**: `#0a0a0f` base with glassmorphism cards
- **Spiritual Theme**: Gold/Saffron palette (`#ffa000` → `#ffd54f`)
- **Sticker Theme**: Neon accents (`#00f5ff`, `#ff00e5`, `#39ff14`)
- **Typography**: Outfit (display), Inter (body), Playfair Display (spiritual)

---

Made with ♻️ by EVERRLEAF | © 2026

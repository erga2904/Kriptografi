# CipherLab — Cryptography Learning & Simulation Platform

A modern SaaS-style web application for learning, visualizing, and simulating cryptographic algorithms.

---

## Architecture

```
Kriptografi/
├── run.py                      # Entry point (local dev + Vercel)
├── vercel.json                 # Vercel deployment config
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not committed)
├── .gitignore
│
├── app/
│   ├── __init__.py             # Flask app factory (create_app)
│   ├── config.py               # Configuration from env vars
│   ├── extensions.py           # Flask extensions (db, csrf, login, bcrypt)
│   ├── models.py               # SQLAlchemy models (User, CipherHistory)
│   │
│   ├── blueprints/
│   │   ├── main/               # HTML page routes (Dashboard, pages)
│   │   │   └── routes.py
│   │   ├── auth/               # Authentication API (register, login, logout)
│   │   │   ├── routes.py
│   │   │   └── services.py     # Validation logic
│   │   ├── classical/          # Classical ciphers API
│   │   │   ├── routes.py       # REST endpoints
│   │   │   └── services.py     # Caesar, Vigenère, Affine, Hill, Playfair
│   │   ├── modern/             # Modern crypto API
│   │   │   ├── routes.py
│   │   │   └── services.py     # AES, RSA, SHA-256, Digital Signature
│   │   ├── math_tools/         # Math foundation API
│   │   │   ├── routes.py
│   │   │   └── services.py     # Modular arith, Euclidean, mod inverse, fast exp
│   │   └── attacks/            # Attack simulation API
│   │       ├── routes.py
│   │       └── services.py     # Brute force, frequency analysis, RSA weak key
│   │
│   ├── templates/              # Jinja2 HTML templates
│   │   ├── base.html           # Master layout (sidebar, header, scripts)
│   │   ├── index.html          # Dashboard
│   │   ├── classical.html      # Classical ciphers page
│   │   ├── modern.html         # Modern crypto page
│   │   ├── math_tools.html     # Math foundation page
│   │   ├── attacks.html        # Attack lab page
│   │   ├── login.html
│   │   └── register.html
│   │
│   └── static/
│       ├── css/
│       │   └── main.css        # Design system (cards, buttons, forms, etc.)
│       └── js/
│           ├── app.js          # Core utilities (clipboard, toasts, shortcuts)
│           ├── cursor.js       # Custom glow cursor with lerp
│           └── interactions.js # Ripple effects, light bursts, nav, animations
```

---

## Quick Start

### 1. Clone and install

```bash
cd Kriptografi
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
```

### 2. Run locally

```bash
python run.py
```

Open http://localhost:5000

### 3. Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

Set `SECRET_KEY` as an environment variable in Vercel dashboard.

---

## Features

### Classical Cryptography
| Algorithm | Encrypt | Decrypt | Steps |
|-----------|---------|---------|-------|
| Caesar    | ✓       | ✓       | Per-character shift formula |
| Vigenère  | ✓       | ✓       | Extended key + polyalphabetic steps |
| Affine    | ✓       | ✓       | `ax+b mod 26`, coprimality check |
| Hill      | ✓       | ✓       | Matrix multiplication, inverse |
| Playfair  | ✓       | ✓       | 5×5 matrix, digraph rules |

### Modern Cryptography
| Algorithm        | Features |
|------------------|----------|
| AES-128          | Educational single-block encryption with 10-round step visualization |
| RSA              | Key generation (visual p,q,n,φ(n),e,d), encrypt, decrypt |
| SHA-256          | Hash computation with process explanation |
| Digital Signature| Sign + verify with RSA, full step-by-step |

### Mathematical Foundation
- Modular arithmetic (add, sub, mul, pow)
- Euclidean Algorithm (step-by-step GCD)
- Extended Euclidean Algorithm (find x, y)
- Modular Inverse calculator
- Fast Exponentiation (square-and-multiply)

### Attack Simulation
- **Brute Force Caesar**: All 26 shifts ranked by English frequency
- **Frequency Analysis**: Interactive chart (Chart.js), χ², IC
- **RSA Weak Key**: Trial division + Fermat factorization

---

## Design System

- **Theme**: Dark navy (#0B1120 background) with glassmorphism cards
- **Accent**: Cyan / Electric Blue (#06B6D4)
- **Font**: Figtree + JetBrains Mono
- **Components**: Glassmorphism cards, buttons, inputs, tabs, tags — all reusable CSS classes
- **Microinteractions**: Custom cursor glow with trailing blur, liquid ripple clicks, circular light burst on submit, SVG icon hover animations, card entrance stagger
- **Accessibility**: WCAG focus-visible outlines, prefers-reduced-motion support, aria labels, semantic nav

---

## Security

- bcrypt password hashing (Flask-Bcrypt)
- CSRF protection (Flask-WTF) on forms, exempted on API routes
- Environment variables for secrets (.env + python-dotenv)
- Session cookie: HttpOnly + SameSite=Lax
- Input validation on all endpoints
- Clean JSON error responses

---

## Module Documentation

### `app/__init__.py` — App Factory
Creates and configures the Flask app, initializes extensions, registers blueprints, creates DB tables.

### `app/config.py` — Config
Loads `SECRET_KEY` and `DATABASE_URL` from environment, with safe defaults for local development.

### `app/extensions.py` — Extensions
Single point of initialization for SQLAlchemy, CSRFProtect, LoginManager, Bcrypt.

### `app/models.py` — Database Models
- `User`: username, email, bcrypt password, creation date
- `CipherHistory`: logs of cipher operations (optional)

### Service Layers (`services.py`)
Each blueprint has a pure `services.py` module with no Flask dependencies — testable algorithms that return dictionaries with step-by-step data.

### Routes (`routes.py`)
Thin HTTP layer: parse JSON input → call service → return JSON response.

---

## License

Educational project — open source.

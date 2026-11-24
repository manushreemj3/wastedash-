# WasteDash — Waste, sorted. World, better.

A modern, premium waste collection web application inspired by the polished UI/UX of top on-demand platforms (Swiggy, Zomato), specifically re-engineered for community waste segregation and doorstep pickup.

Built with **Python** and **Streamlit**.

---

## Highlights & Features

### 1. Visual Design & Startup Branding
- **Eco-Friendly Palette:** Curated forest-green (`#1B4332`), sage-green (`#74C69D`), mint (`#EAF7EE`), and warm-white backgrounds.
- **Modern Typography:** Styled with Google Fonts (`Outfit` + `Plus Jakarta Sans`) with balanced hierarchy and generous whitespace.
- **Rich Vector Illustrations:** Custom inline SVG graphics for the WasteDash brand mark, neighborhood collection van, and waste stream icons.
- **Swiggy/Zomato Polish:** Custom navigation bar, category badges, responsive cards, micro-interactions, and live status progress timelines.

### 2. Startup Landing Page (Homepage)
- Clean sticky top navigation bar with WasteDash branding, navigation anchors, dedicated account dashboard links, and login triggers.
- Prominent hero section with the headline **“Waste, sorted. World, better.”** and supporting value proposition.
- Quick action CTA buttons: **Book a Pickup** (Primary) and **Become a Collector** (Secondary).
- Three color-coded waste stream cards:
  - **Wet Waste (Biodegradable):** Organics, kitchen peels, compostable scraps.
  - **Dry Waste (Recyclable):** Clean cardboard, flattened cartons, rinsed plastic and glass bottles.
  - **Sanitary Waste (Safe Disposal):** Wrapped hygiene products, diapers, and pads.
- Three-step workflow breakdown: **Sort Your Waste -> Book a Slot -> Get It Collected**.
- **Partner Opportunity Banner:** Highlighting part-time earnings for community collectors.
- Polished footer with directory links, sorting pledges, and copyright.

### 3. Authentication & Fixed Account Roles
- Dedicated auth portal with **Log In** and **Create New Account** tabs.
- Fixed role registration: choose **Get My Waste Collected** (Customer) or **Collect Waste and Earn** (Collector Partner). Roles are permanently fixed per account to prevent accidental cross-role contamination.
- Secure PBKDF2-HMAC-SHA256 password hashing with unique salt generation.
- **One-Click Demo Accounts:**
  - Customer: `rahul@wastedash.in` (Password: `wastedash123`)
  - Collector: `priya@wastedash.in` (Password: `wastedash123`)

### 4. Mandatory Waste Segregation Tutorial & Quiz
- Non-skippable visual first-time onboarding guide explaining proper segregation rules and precautions.
- 3-Question interactive quiz evaluating practical waste sorting scenarios. Doorstep pickup booking is locked until a passing score (≥ 2/3) is achieved.
- Instant score calculation, detailed explanations, and review feedback.
- Certification records stored persistently in MongoDB.

### 5. Customer Dashboard & Booking Experience
- Personalized welcome banner with real-time impact metrics (Total Pickups, Active Jobs, Kg Waste Diverted).
- Doorstep collection scheduling flow:
  1. Waste category selection (Wet, Dry, Sanitary).
  2. Date picker (validation preventing past dates) & 2-hour window selection.
  3. Estimated volume selection (1 bag, 2-3 bags, bulk).
  4. Complete doorstep address with optional gate/access instructions.
- **Live Status Tracker:** 4-stage visual timeline tracker (Requested -> Collector Assigned -> Collected -> Recycled).
- Booking history and request cancellation for open bookings.

### 6. Collector Partner Hub
- Operational duty toggle: **ONLINE & READY** vs **OFFLINE**.
- Performance metrics: Nearby Open Requests, Active Jobs, Completed Collections, and Estimated Earnings (e.g., `~INR 75/trip`).
- **Open Requests Board:** View resident address, scheduled slot, and volume.
- **Concurrency-Safe Job Acceptance:** Atomic MongoDB document updates prevent two collectors from claiming the same booking.
- Workflow progression buttons: **Mark as Picked Up** -> **Mark as Completed & Handed Over**.
- Completed collections ledger with payout calculation.

---

## Tech Stack & Architecture

- **Frontend & App Framework:** [Streamlit](https://streamlit.io/) (1.36+)
- **Backend & Logic:** Python 3.10+
- **Database:** MongoDB (MongoDB Atlas / local) configured via `pymongo` and `.env` with atomic operations
- **Styling:** Custom CSS injected via `unsafe_allow_html=True` with `.streamlit/config.toml` theme tokens
- **Vector Graphics:** Custom SVGs for retina crispness

```
wastedash/
├── .streamlit/
│   └── config.toml      # Theme tokens (Forest Green, Mint, Sans-Serif font)
├── .env                 # MongoDB connection credentials & cluster URI
├── app.py               # Main application router and view controllers
├── db.py                # MongoDB collections, schema indexing, and demo seeds
├── styles.py            # CSS design system, typography, and SVG illustrations
├── requirements.txt     # Python dependencies (Streamlit, PyMongo, Python-Dotenv, Certifi)
└── README.md            # Documentation and setup instructions
```

---

## How to Run Locally

### 1. Clone & Set Up Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Launch WasteDash

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## Security & Data Integrity

- Passwords are encrypted with standard PBKDF2-HMAC-SHA256 with 100,000 iterations.
- Concurrency race conditions are handled via atomic SQL updates (`WHERE id=? AND status='Open'`).
- Role permissions are validated per view: customers cannot accept jobs, and collectors only see open jobs when toggled online.

# EcoGo — Waste, sorted. World, better.

A modern, premium waste collection web application inspired by the polished UI/UX of top on-demand platforms (Swiggy, Zomato), specifically re-engineered for community waste segregation and doorstep pickup.

Built with **Python** and **Streamlit**.

---

## Highlights & Features

### 1. Visual Design & Startup Branding
- **Eco-Friendly Palette:** Curated forest-green (`#1B4332`), sage-green (`#74C69D`), mint (`#EAF7EE`), and warm-white backgrounds.
- **Modern Typography:** Styled with Google Fonts (`Outfit` + `Plus Jakarta Sans`) with balanced hierarchy and generous whitespace.
- **Rich Vector Illustrations:** Custom inline SVG graphics for the EcoGo brand mark, neighborhood collection van, and waste stream icons.
- **Swiggy/Zomato Polish:** Custom navigation bar, category badges, responsive cards, micro-interactions, and live status progress timelines.

### 2. Startup Landing Page (Homepage)
- Clean sticky top navigation bar with EcoGo branding, navigation anchors, role switcher, and login triggers.
- Prominent hero section with the headline **“Waste, sorted. World, better.”** and supporting value proposition.
- Quick action CTA buttons: **Book a Pickup** (Primary) and **Become a Collector** (Secondary).
- Three color-coded waste stream cards:
  - **Wet Waste (Biodegradable):** Organics, kitchen peels, compostable scraps.
  - **Dry Waste (Recyclable):** Clean cardboard, flattened cartons, rinsed plastic and glass bottles.
  - **Sanitary Waste (Safe Disposal):** Wrapped hygiene products, diapers, and pads.
- Three-step workflow breakdown: **Sort Your Waste -> Book a Slot -> Get It Collected**.
- **Partner Opportunity Banner:** Highlighting part-time earnings for community collectors.
- Polished footer with directory links, sorting pledges, and copyright.

### 3. Authentication & Role Switching
- Dedicated auth portal with **Log In** and **Create New Account** tabs.
- Multi-mode registration: choose **Get My Waste Collected** (Customer) or **Collect Waste and Earn** (Collector Partner).
- Seamless mode switching at any time via the top navigation bar.
- Secure PBKDF2-HMAC-SHA256 password hashing with unique salt generation.
- **One-Click Demo Accounts:**
  - Customer: `rahul@ecogo.in` (Password: `ecogo123`)
  - Collector: `priya@ecogo.in` (Password: `ecogo123`)

### 4. Waste Segregation Tutorial & Interactive Quiz
- Visual first-time onboarding guide explaining proper segregation rules and precautions.
- 3-Question interactive quiz evaluating practical waste sorting scenarios.
- Instant score calculation and detailed explanations for questions.
- Certification records stored persistently in the database.

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
- **Concurrency-Safe Job Acceptance:** Atomic SQLite database transactions prevent two collectors from claiming the same booking.
- Workflow progression buttons: **Mark as Picked Up** -> **Mark as Completed & Handed Over**.
- Completed collections ledger with payout calculation.

---

## Tech Stack & Architecture

- **Frontend & App Framework:** [Streamlit](https://streamlit.io/) (1.36+)
- **Backend & Logic:** Python 3.10+
- **Database:** SQLite (`ecogo.db`) with parameterized queries and atomic updates
- **Styling:** Custom CSS injected via `unsafe_allow_html=True` with `.streamlit/config.toml` theme tokens
- **Vector Graphics:** Custom SVGs for retina crispness

```
EcoGo_Streamlit/
├── .streamlit/
│   └── config.toml      # Theme tokens (Forest Green, Mint, Sans-Serif font)
├── app.py               # Main application router and view controllers
├── db.py                # Database queries, schema migrations, and demo data
├── styles.py            # CSS design system, typography, and SVG illustrations
├── ecogo.db             # Persistent SQLite database
├── requirements.txt     # Python dependencies
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

### 3. Launch EcoGo

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## Security & Data Integrity

- Passwords are encrypted with standard PBKDF2-HMAC-SHA256 with 100,000 iterations.
- Concurrency race conditions are handled via atomic SQL updates (`WHERE id=? AND status='Open'`).
- Role permissions are validated per view: customers cannot accept jobs, and collectors only see open jobs when toggled online.

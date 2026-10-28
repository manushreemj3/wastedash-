# WasteDash Design System and Styles
# Inspired by modern delivery platforms (Swiggy, Zomato) adapted for eco-friendly waste management

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Outfit:wght@500;600;700;800&display=swap');

/* Reset and base font */
html, body, [class*="css"], .stMarkdown, .stText {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #172D21;
}

h1, h2, h3, h4, .brand-font {
    font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif !important;
    letter-spacing: -0.025em;
    font-weight: 700;
}

/* Background */
.stApp {
    background-color: #F8FAF7;
    background-image: 
        radial-gradient(at 0% 0%, rgba(216, 243, 220, 0.35) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(183, 228, 199, 0.25) 0px, transparent 50%);
    background-attachment: fixed;
}

/* Hide default streamlit decorations */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header[data-testid="stHeader"] {
    background: transparent;
    height: 1.5rem;
}
.stDeployButton {display: none;}
[data-testid="stDecoration"] {display: none;}

/* Main container spacing */
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 3rem !important;
    max-width: 1200px !important;
}

/* Top Navigation Bar */
.wastedash-nav, .ecogo-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(255, 255, 255, 0.92);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid #E3ECE5;
    border-radius: 20px;
    padding: 0.85rem 1.6rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 20px rgba(22, 62, 47, 0.05);
}

.nav-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    text-decoration: none;
    color: #143A29;
}

.nav-brand-title {
    font-family: 'Outfit', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    line-height: 1;
    color: #1B4332;
    display: flex;
    align-items: center;
    gap: 6px;
}

.nav-brand-tagline {
    font-size: 0.72rem;
    color: #52796F;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

.nav-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 0.4rem 0.9rem;
    background: #EAF7EE;
    border: 1px solid #C7E8D2;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 700;
    color: #1B4332;
}

.role-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 0.35rem 0.85rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 700;
}
.role-badge-customer {
    background: #E8F5E9;
    color: #2E7D32;
    border: 1px solid #C8E6C9;
}
.role-badge-collector {
    background: #FFF3E0;
    color: #E65100;
    border: 1px solid #FFE0B2;
}

/* Hero Section */
.hero-box {
    background: linear-gradient(135deg, #16382B 0%, #1E503C 55%, #2D6A4F 100%);
    border-radius: 28px;
    padding: 3.2rem 3rem;
    color: white;
    box-shadow: 0 20px 45px rgba(22, 56, 43, 0.18);
    position: relative;
    overflow: hidden;
    margin-bottom: 2rem;
    border: 1px solid rgba(255, 255, 255, 0.12);
}

.hero-box::after {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba(116, 198, 157, 0.18) 0%, transparent 65%);
    pointer-events: none;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(255, 255, 255, 0.14);
    border: 1px solid rgba(255, 255, 255, 0.25);
    backdrop-filter: blur(8px);
    padding: 0.4rem 1rem;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 700;
    color: #D8F3DC;
    letter-spacing: 0.04em;
    margin-bottom: 1.2rem;
}

.hero-title {
    font-family: 'Outfit', sans-serif;
    font-size: clamp(2.4rem, 4.2vw, 3.6rem);
    font-weight: 800;
    line-height: 1.08;
    color: #FFFFFF;
    margin: 0 0 1.1rem 0;
}

.hero-title span {
    background: linear-gradient(90deg, #95D5B2 0%, #D8F3DC 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    font-size: 1.15rem;
    line-height: 1.6;
    color: #E2F0E7;
    max-width: 580px;
    margin-bottom: 1.8rem;
    font-weight: 400;
}

.hero-features {
    display: flex;
    flex-wrap: wrap;
    gap: 14px;
    margin-top: 1.6rem;
}

.hero-feature-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.86rem;
    color: #D8F3DC;
    font-weight: 600;
}

/* General Cards */
.eco-card {
    background: #FFFFFF;
    border: 1px solid #E6EFE8;
    border-radius: 22px;
    padding: 1.8rem 1.8rem;
    box-shadow: 0 8px 24px rgba(23, 62, 45, 0.04);
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    height: 100%;
    position: relative;
    overflow: hidden;
}

.eco-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 36px rgba(23, 62, 45, 0.09);
    border-color: #B7E4C7;
}

/* Waste Category Cards */
.waste-card-wet {
    border-top: 5px solid #2D6A4F;
    background: linear-gradient(180deg, #F6FBF7 0%, #FFFFFF 100%);
}

.waste-card-dry {
    border-top: 5px solid #1E88E5;
    background: linear-gradient(180deg, #F3F9FD 0%, #FFFFFF 100%);
}

.waste-card-sanitary {
    border-top: 5px solid #D84315;
    background: linear-gradient(180deg, #FDF7F5 0%, #FFFFFF 100%);
}

.waste-card-icon {
    width: 64px;
    height: 64px;
    border-radius: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1.2rem;
}

.waste-card-icon.wet {
    background: #E8F5E9;
    color: #2D6A4F;
}

.waste-card-icon.dry {
    background: #E1F5FE;
    color: #0277BD;
}

.waste-card-icon.sanitary {
    background: #FBE9E7;
    color: #D84315;
}

.category-badge {
    display: inline-block;
    padding: 0.3rem 0.75rem;
    border-radius: 999px;
    font-size: 0.74rem;
    font-weight: 700;
    letter-spacing: 0.03em;
    margin-bottom: 0.8rem;
}

.category-badge.wet { background: #E8F5E9; color: #2D6A4F; }
.category-badge.dry { background: #E1F5FE; color: #0277BD; }
.category-badge.sanitary { background: #FBE9E7; color: #C62828; }

/* Steps Section */
.step-number {
    font-family: 'Outfit', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: #74C69D;
    line-height: 1;
    margin-bottom: 0.7rem;
}

/* Stat Metrics (Swiggy / Zomato style) */
.metric-box {
    background: #FFFFFF;
    border: 1px solid #E5EFE7;
    border-radius: 20px;
    padding: 1.3rem 1.4rem;
    box-shadow: 0 4px 16px rgba(22, 62, 47, 0.04);
}

.metric-box-title {
    font-size: 0.82rem;
    font-weight: 700;
    color: #52796F;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.metric-box-value {
    font-family: 'Outfit', sans-serif;
    font-size: 2.1rem;
    font-weight: 800;
    color: #1B4332;
    margin: 0.3rem 0 0.1rem 0;
}

.metric-box-sub {
    font-size: 0.8rem;
    color: #718F83;
}

/* Status Timeline (Live Tracker) */
.timeline-container {
    background: #FFFFFF;
    border: 1px solid #E3ECE5;
    border-radius: 20px;
    padding: 1.4rem 1.6rem;
    margin: 1rem 0;
}

.timeline-step {
    display: flex;
    align-items: center;
    gap: 12px;
    position: relative;
}

.timeline-dot {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.78rem;
    font-weight: 800;
}

.timeline-dot.done {
    background: #2D6A4F;
    color: white;
}

.timeline-dot.active {
    background: #52B788;
    color: white;
    box-shadow: 0 0 0 4px rgba(82, 183, 136, 0.25);
}

.timeline-dot.pending {
    background: #E8EFEA;
    color: #849A8F;
}

/* Buttons Styling */
div.stButton > button,
div[data-testid="stFormSubmitButton"] > button,
button[data-testid="baseButton-primary"],
button[data-testid="baseButton-secondary"],
button[kind="primary"],
button[kind="secondary"],
button[kind="formSubmit"] {
    border-radius: 14px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 0.65rem 1.4rem !important;
    min-height: 2.85rem !important;
    transition: all 0.25s ease !important;
    border: 1px solid transparent !important;
}

div.stButton > button[kind="primary"],
div[data-testid="stFormSubmitButton"] > button,
button[data-testid="baseButton-primary"],
button[kind="primary"],
button[kind="formSubmit"] {
    background: linear-gradient(135deg, #1B4332 0%, #2D6A4F 100%) !important;
    color: #FFFFFF !important;
    box-shadow: 0 6px 18px rgba(45, 106, 79, 0.24) !important;
    border: 1px solid #1B4332 !important;
}

div.stButton > button[kind="primary"]:hover,
div[data-testid="stFormSubmitButton"] > button:hover,
button[data-testid="baseButton-primary"]:hover,
button[kind="primary"]:hover,
button[kind="formSubmit"]:hover {
    background: linear-gradient(135deg, #143527 0%, #245741 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(45, 106, 79, 0.32) !important;
}

div.stButton > button[kind="secondary"],
button[data-testid="baseButton-secondary"],
button[kind="secondary"] {
    background: #FFFFFF !important;
    border: 1px solid #C7DBCF !important;
    color: #1B4332 !important;
}

div.stButton > button[kind="secondary"]:hover,
button[data-testid="baseButton-secondary"]:hover,
button[kind="secondary"]:hover {
    background: #F0F7F2 !important;
    border-color: #2D6A4F !important;
    color: #143527 !important;
    transform: translateY(-2px) !important;
}

/* Radio & Checkbox focus and selection accents */
div[data-testid="stRadio"] [aria-checked="true"] {
    color: #2D6A4F !important;
}
div[data-testid="stRadio"] label,
div[data-testid="stCheckbox"] label {
    font-weight: 600 !important;
    color: #16382B !important;
}

/* Streamlit Forms & Inputs */
div[data-testid="stForm"] {
    background: #FFFFFF;
    border: 1px solid #E3ECE5;
    border-radius: 22px;
    padding: 1.8rem 2rem;
    box-shadow: 0 8px 28px rgba(22, 62, 47, 0.05);
}

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea,
div[data-testid="stSelectbox"] select {
    border-radius: 12px !important;
    border: 1px solid #D5E3D8 !important;
    background-color: #FAFCFA !important;
    color: #17382B !important;
    font-size: 0.95rem !important;
}

div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color: #2D6A4F !important;
    box-shadow: 0 0 0 3px rgba(45, 106, 79, 0.15) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: #EEF4F0;
    padding: 6px;
    border-radius: 14px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    padding: 8px 18px;
    font-weight: 700;
    color: #52796F;
    border: none !important;
}

.stTabs [aria-selected="true"] {
    background-color: #FFFFFF !important;
    color: #1B4332 !important;
    box-shadow: 0 3px 10px rgba(0,0,0,0.06) !important;
}

.stTabs [data-baseweb="tab-highlight"] {
    background-color: #2D6A4F !important;
    height: 3px !important;
    border-radius: 999px !important;
}

.stTabs [data-baseweb="tab-border"] {
    display: none !important;
}

/* Baseweb Radio and Selection Elements */
div[data-testid="stRadio"] div[data-baseweb="radio"] input:checked + div {
    border-color: #2D6A4F !important;
    background-color: #2D6A4F !important;
}

div[data-testid="stRadio"] div[data-baseweb="radio"] div:first-child {
    border-color: #8EBCA4 !important;
}

div[data-testid="stRadio"] svg {
    fill: #2D6A4F !important;
}

/* Datepicker & Calendar Accent */
[data-baseweb="calendar"] button[aria-selected="true"] {
    background-color: #2D6A4F !important;
}

/* Hide Streamlit dev warnings / header clutter */
div[data-testid="stStatusWidget"] {display: none !important;}
div[data-testid="stToolbar"] {display: none !important;}
header[data-testid="stHeader"] .stDeployButton {display: none !important;}

/* Footer */
.wastedash-footer, .ecogo-footer {
    background: #14382A;
    color: #E2ECE5;
    border-radius: 24px;
    padding: 3rem 2.8rem 2rem 2.8rem;
    margin-top: 3.5rem;
}

.footer-col-title {
    font-family: 'Outfit', sans-serif;
    font-weight: 700;
    font-size: 1.05rem;
    color: #FFFFFF;
    margin-bottom: 1rem;
}

.footer-link {
    color: #A3C9B4;
    text-decoration: none;
    font-size: 0.88rem;
    display: block;
    margin-bottom: 0.6rem;
    transition: color 0.2s ease;
}

.footer-link:hover {
    color: #D8F3DC;
}

/* Alert boxes */
.stAlert {
    border-radius: 16px !important;
    border: 1px solid #D4E8DC !important;
}

/* Radio button horizontal styling */
div[role="radiogroup"] {
    gap: 12px;
}
</style>
"""

# Custom SVG illustrations for crisp retina rendering
SVG_LOGO = """
<svg width="38" height="38" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="14" fill="#1B4332"/>
  <path d="M24 10C16.268 10 10 16.268 10 24C10 28.3 11.95 32.14 15 34.72V29.5C14.07 27.92 13.5 26.04 13.5 24C13.5 18.2 18.2 13.5 24 13.5C27.05 13.5 29.8 14.81 31.7 16.9L28 20.6H38V10.6L34.2 14.4C31.65 11.7 28.02 10 24 10Z" fill="#74C69D"/>
  <path d="M34.5 24C34.5 29.8 29.8 34.5 24 34.5C20.95 34.5 18.2 33.19 16.3 31.1L20 27.4H10V37.4L13.8 33.6C16.35 36.3 19.98 38 24 38C31.732 38 38 31.732 38 24C38 19.7 36.05 15.86 33 13.28V18.5C33.93 20.08 34.5 21.96 34.5 24Z" fill="#D8F3DC"/>
  <circle cx="24" cy="24" r="4" fill="#52B788"/>
</svg>
"""

SVG_HERO_ILLUSTRATION = """<svg width="100%" height="340" viewBox="0 0 520 340" fill="none" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; display: block; margin: auto;">
<defs>
<linearGradient id="skyGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#2D6A4F" stop-opacity="0.3"/><stop offset="100%" stop-color="#1B4332" stop-opacity="0"/></linearGradient>
<linearGradient id="vanGrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#74C69D"/><stop offset="100%" stop-color="#52B788"/></linearGradient>
<linearGradient id="roadGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#214D3A"/><stop offset="100%" stop-color="#143527"/></linearGradient>
</defs>
<circle cx="430" cy="90" r="50" fill="#95D5B2" fill-opacity="0.15"/>
<path d="M0 240 Q130 180 280 230 T520 220 L520 340 L0 340 Z" fill="#184230" fill-opacity="0.6"/>
<path d="M0 260 Q180 220 360 255 T520 250 L520 340 L0 340 Z" fill="#143A29"/>
<path d="M0 285 Q260 275 520 285 L520 340 L0 340 Z" fill="url(#roadGrad)"/>
<path d="M40 310 H90 M140 310 H200 M250 310 H310 M360 310 H420 M470 310 H510" stroke="#74C69D" stroke-width="3" stroke-dasharray="8 8" stroke-linecap="round" stroke-opacity="0.6"/>
<rect x="50" y="160" width="46" height="85" rx="6" fill="#1F4E38"/>
<rect x="58" y="172" width="10" height="12" rx="2" fill="#95D5B2" fill-opacity="0.7"/>
<rect x="76" y="172" width="10" height="12" rx="2" fill="#95D5B2" fill-opacity="0.7"/>
<rect x="58" y="196" width="10" height="12" rx="2" fill="#95D5B2" fill-opacity="0.7"/>
<rect x="76" y="196" width="10" height="12" rx="2" fill="#95D5B2" fill-opacity="0.7"/>
<rect x="105" y="180" width="55" height="65" rx="6" fill="#255C43"/>
<rect x="115" y="192" width="12" height="14" rx="2" fill="#D8F3DC" fill-opacity="0.8"/>
<rect x="135" y="192" width="12" height="14" rx="2" fill="#D8F3DC" fill-opacity="0.8"/>
<path d="M175 245 C165 220 185 200 195 200 C205 200 225 220 215 245 Z" fill="#52B788"/>
<rect x="192" y="240" width="6" height="20" rx="2" fill="#3E2723"/>
<path d="M440 240 C430 215 450 195 460 195 C470 195 490 215 480 240 Z" fill="#74C69D"/>
<rect x="457" y="235" width="6" height="25" rx="2" fill="#3E2723"/>
<g transform="translate(180, 195)">
<rect x="20" y="30" width="145" height="62" rx="12" fill="#FFFFFF"/>
<rect x="115" y="40" width="45" height="35" rx="6" fill="#D8F3DC"/>
<path d="M125 44 H154 V68 H125 Z" fill="#1B4332" fill-opacity="0.25"/>
<rect x="20" y="65" width="145" height="14" fill="#2D6A4F"/>
<text x="24" y="76" fill="#FFFFFF" font-family="'Outfit', sans-serif" font-size="10" font-weight="bold" letter-spacing="0.5">WASTEDASH</text>
<circle cx="100" cy="50" r="10" fill="#E8F5E9"/>
<path d="M100 44 C96 46 95 50 100 55 C105 50 104 46 100 44 Z" fill="#2D6A4F"/>
<circle cx="162" cy="72" r="5" fill="#FFE082"/>
<circle cx="50" cy="92" r="15" fill="#143527"/>
<circle cx="50" cy="92" r="8" fill="#D8F3DC"/>
<circle cx="135" cy="92" r="15" fill="#143527"/>
<circle cx="135" cy="92" r="8" fill="#D8F3DC"/>
<path d="M17 48 L22 40 H16 L20 32" stroke="#FFD166" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
</g>
<g transform="translate(370, 225)">
<rect x="0" y="10" width="28" height="42" rx="4" fill="#2D6A4F"/>
<rect x="-3" y="6" width="34" height="6" rx="3" fill="#1B4332"/>
<circle cx="14" cy="28" r="7" fill="#E8F5E9" fill-opacity="0.3"/>
<circle cx="14" cy="28" r="3.5" fill="#74C69D"/>
</g>
<g transform="translate(405, 225)">
<rect x="0" y="10" width="28" height="42" rx="4" fill="#1E88E5"/>
<rect x="-3" y="6" width="34" height="6" rx="3" fill="#0D47A1"/>
<circle cx="14" cy="28" r="7" fill="#E1F5FE" fill-opacity="0.3"/>
<rect x="10.5" y="24.5" width="7" height="7" rx="1.5" fill="#BBDEFB"/>
</g>
<g transform="translate(440, 225)">
<rect x="0" y="10" width="28" height="42" rx="4" fill="#D84315"/>
<rect x="-3" y="6" width="34" height="6" rx="3" fill="#BF360C"/>
<circle cx="14" cy="28" r="7" fill="#FBE9E7" fill-opacity="0.3"/>
<rect x="13" y="24.5" width="2" height="7" fill="#FFCCBC"/>
<rect x="10.5" y="27" width="7" height="2" fill="#FFCCBC"/>
</g>
<circle cx="120" cy="80" r="4" fill="#74C69D" fill-opacity="0.4"/>
<circle cx="135" cy="65" r="2" fill="#74C69D" fill-opacity="0.5"/>
<circle cx="340" cy="70" r="5" fill="#95D5B2" fill-opacity="0.3"/>
<circle cx="360" cy="90" r="3" fill="#95D5B2" fill-opacity="0.4"/>
</svg>"""

# Waste Category SVG Icons
SVG_WET_ICON = """
<svg width="36" height="36" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M18 3C18 3 8 15 8 22C8 27.52 12.48 32 18 32C23.52 32 28 27.52 28 22C28 15 18 3 18 3Z" fill="#52B788"/>
  <path d="M18 9C18 9 12 18 12 23C12 26.31 14.69 29 18 29C21.31 29 24 26.31 24 23C24 18 18 9 18 9Z" fill="#74C69D"/>
  <path d="M16 16C15 19 15 22 17 24" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round"/>
</svg>
"""

SVG_DRY_ICON = """
<svg width="36" height="36" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M18 4L4 11L18 18L32 11L18 4Z" fill="#42A5F5"/>
  <path d="M4 11V25L18 32V18L4 11Z" fill="#1E88E5"/>
  <path d="M32 11V25L18 32V18L32 11Z" fill="#1976D2"/>
  <path d="M18 18L25 14.5" stroke="#FFFFFF" stroke-width="1.5" stroke-linecap="round"/>
</svg>
"""

SVG_SANITARY_ICON = """
<svg width="36" height="36" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M18 4L6 9V17C6 24.5 11.1 31.4 18 33C24.9 31.4 30 24.5 30 17V9L18 4Z" fill="#FF7043"/>
  <path d="M18 6L8 10.2V17C8 23.3 12.3 29.2 18 30.8C23.7 29.2 28 23.3 28 17V10.2L18 6Z" fill="#F4511E"/>
  <path d="M18 12V22M13 17H23" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>
</svg>
"""

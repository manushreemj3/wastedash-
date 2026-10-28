import streamlit as st
from datetime import datetime, date, timedelta
import textwrap
import styles
import db

# -----------------------------------------------------------------------------
# App Configuration & Theme Initialization
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="EcoGo — Waste, sorted. World, better.",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize database schema, migrations, and demo seeds
db.init_db()

# Helper for reliable HTML rendering without markdown code block indentation issues
def render_html(html_str):
    lines = [line.strip() for line in html_str.splitlines() if line.strip()]
    clean_html = "\n".join(lines)
    st.markdown(clean_html, unsafe_allow_html=True)

# Inject modern Swiggy/Zomato inspired CSS and font styling
st.markdown(styles.CUSTOM_CSS, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Session State Setup
# -----------------------------------------------------------------------------
if "current_page" not in st.session_state:
    st.session_state.current_page = "Landing"
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"
if "quiz_completed" not in st.session_state:
    st.session_state.quiz_completed = False
if "toast_msg" not in st.session_state:
    st.session_state.toast_msg = None

# Show any pending toast notification
if st.session_state.toast_msg:
    st.toast(st.session_state.toast_msg)
    st.session_state.toast_msg = None

def get_current_user():
    if not st.session_state.user_id:
        return None
    return db.get_user_by_id(st.session_state.user_id)

user = get_current_user()

def navigate_to(page_name):
    st.session_state.current_page = page_name
    st.rerun()

def logout():
    st.session_state.user_id = None
    st.session_state.current_page = "Landing"
    st.session_state.quiz_completed = False
    st.session_state.toast_msg = "You have been logged out"
    st.rerun()

# -----------------------------------------------------------------------------
# Top Navigation Bar (Header)
# -----------------------------------------------------------------------------
def render_navbar():
    nav_col1, nav_col2 = st.columns([1.5, 2.5], vertical_alignment="center")

    with nav_col1:
        render_html(f"""
        <div style="display: flex; align-items: center; gap: 12px; padding: 2px 0;">
            {styles.SVG_LOGO.strip()}
            <div>
                <div style="font-family: 'Outfit', sans-serif; font-size: 1.55rem; font-weight: 800; line-height: 1.1; color: #1B4332;">EcoGo</div>
                <div style="font-size: 0.72rem; color: #52796F; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase;">Waste, sorted. World, better.</div>
            </div>
        </div>
        """)

    with nav_col2:
        if user is None:
            # Public navigation
            _, b1, b2 = st.columns([1.6, 1.0, 1.4])
            with b1:
                if st.button("Home", key="nav_home", use_container_width=True):
                    navigate_to("Landing")
            with b2:
                if st.button("Log In / Register", key="nav_auth", type="primary", use_container_width=True):
                    st.session_state.auth_mode = "login"
                    navigate_to("Auth")
        else:
            # Logged-in navigation: strictly My Bookings, Switch to Collector (or Customer), and Logout
            is_collector = bool(user["worker_enabled"])
            b1, b2, b3 = st.columns([1.2, 1.4, 0.9])

            with b1:
                is_bookings_active = st.session_state.get("current_page") == "CustomerDashboard"
                if st.button("My Bookings", key="nav_bookings", type="primary" if is_bookings_active else "secondary", use_container_width=True):
                    if is_collector:
                        db.set_user_mode(user["id"], 0)
                    navigate_to("CustomerDashboard")

            with b2:
                if is_collector:
                    if st.button("Switch to Customer", key="switch_to_cust", use_container_width=True):
                        db.set_user_mode(user["id"], 0)
                        st.session_state.toast_msg = "Switched to Customer mode"
                        navigate_to("CustomerDashboard")
                else:
                    if st.button("Switch to Collector", key="switch_to_coll", use_container_width=True):
                        db.set_user_mode(user["id"], 1)
                        st.session_state.toast_msg = "Switched to Collector mode"
                        navigate_to("CollectorDashboard")

            with b3:
                if st.button("Logout", key="nav_logout", use_container_width=True):
                    logout()

    render_html("<hr style='margin: 0.6rem 0 1.6rem 0; border: none; border-top: 1px solid #E6ECE8;'>")

render_navbar()

# -----------------------------------------------------------------------------
# PAGE 1: Landing Page (Homepage)
# -----------------------------------------------------------------------------
def render_landing_page():
    # 1. Hero Section: Headline, CTAs on left, Illustration on right
    hero_left, hero_right = st.columns([1.15, 0.85], gap="large", vertical_alignment="center")

    with hero_left:
        render_html("""
        <div style="background: linear-gradient(135deg, #16382B 0%, #1E503C 55%, #2D6A4F 100%); border-radius: 26px; padding: 2.6rem 2.4rem; color: white; box-shadow: 0 16px 40px rgba(22, 56, 43, 0.16); border: 1px solid rgba(255, 255, 255, 0.12); margin-bottom: 1.2rem;">
            <div class="hero-badge">
                <span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:#74C69D;"></span>
                RELIABLE NEIGHBOURHOOD WASTE MANAGEMENT
            </div>
            <div class="hero-title" style="margin: 0.6rem 0 0.8rem 0; font-size: clamp(2rem, 3.6vw, 3rem);">
                Waste, sorted.<br><span style="background: linear-gradient(90deg, #95D5B2 0%, #D8F3DC 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">World, better.</span>
            </div>
            <div class="hero-subtitle" style="font-size: 1.05rem; line-height: 1.55; margin-bottom: 0;">
                Schedule a pickup, sort responsibly, and help build a cleaner neighbourhood. On-demand doorstep collection for segregated wet, dry, and sanitary waste.
            </div>
        </div>
        """)

        b_col1, b_col2 = st.columns(2)
        with b_col1:
            if st.button("Book a Pickup", key="hero_book", type="primary", use_container_width=True):
                if user is None:
                    st.session_state.auth_mode = "login"
                    st.session_state.toast_msg = "Please log in or sign up to schedule your pickup"
                    navigate_to("Auth")
                else:
                    navigate_to("CustomerDashboard")
        with b_col2:
            if st.button("Become a Collector", key="hero_collect", type="secondary", use_container_width=True):
                if user is None:
                    st.session_state.auth_mode = "signup"
                    st.session_state.signup_role = "collector"
                    st.session_state.toast_msg = "Join EcoGo as a Collection Partner"
                    navigate_to("Auth")
                else:
                    db.set_user_mode(user["id"], 1)
                    navigate_to("CollectorDashboard")

        # Key Features Row
        render_html("""
        <div class="hero-features" style="margin-top: 1.2rem; background: #FFFFFF; border-radius: 16px; padding: 1rem 1.4rem; border: 1px solid #E5EFE7; box-shadow: 0 4px 16px rgba(22, 62, 47, 0.04);">
            <div style="display: flex; gap: 20px; flex-wrap: wrap;">
                <div style="display: flex; align-items: center; gap: 8px; color: #1B4332; font-size: 0.86rem; font-weight: 700;">
                    <span style="display:inline-block; width:6px; height:6px; border-radius:50%; background:#2D6A4F;"></span> 30-Min Window Pickups
                </div>
                <div style="display: flex; align-items: center; gap: 8px; color: #1B4332; font-size: 0.86rem; font-weight: 700;">
                    <span style="display:inline-block; width:6px; height:6px; border-radius:50%; background:#2D6A4F;"></span> 100% Landfill Diversion
                </div>
                <div style="display: flex; align-items: center; gap: 8px; color: #1B4332; font-size: 0.86rem; font-weight: 700;">
                    <span style="display:inline-block; width:6px; height:6px; border-radius:50%; background:#2D6A4F;"></span> Flexible Partner Earnings
                </div>
            </div>
        </div>
        """)

    with hero_right:
        render_html("""
        <div style="background: #FFFFFF; border: 1px solid #E2EFE5; border-radius: 26px; padding: 1.4rem; box-shadow: 0 12px 32px rgba(22, 62, 47, 0.06); text-align: center;">
        """ + styles.SVG_HERO_ILLUSTRATION + """
            <div style="display: flex; justify-content: center; gap: 18px; margin-top: 12px; font-size: 0.82rem; font-weight: 700; color: #1B4332;">
                <span>Wet Organics</span>
                <span>Dry Recyclables</span>
                <span>Sanitary Waste</span>
            </div>
        </div>
        """)

    render_html("<div style='height: 2.8rem;'></div>")

    # 2. Three Colorful Waste Category Cards
    render_html("""
    <div style="text-align: center; max-width: 680px; margin: 0 auto 2.2rem auto;">
        <span class="category-badge wet" style="background:#EAF7EE; color:#1B4332; font-size:0.8rem; padding:0.4rem 1rem;">SOURCE SEGREGATION</span>
        <h2 style="font-size: 2.1rem; color: #16382B; margin: 0.4rem 0 0.6rem 0;">Three Waste Streams. Zero Confusion.</h2>
        <p style="color: #52796F; font-size: 1.02rem; line-height: 1.5;">Segregating at source protects sanitation workers, enables recycling, and creates nutrient-rich compost.</p>
    </div>
    """)

    w1, w2, w3 = st.columns(3, gap="medium")

    with w1:
        render_html(f"""
        <div class="eco-card waste-card-wet">
            <div class="waste-card-icon wet">{styles.SVG_WET_ICON.strip()}</div>
            <span class="category-badge wet">BIODEGRADABLE</span>
            <h3 style="color: #1B4332; margin: 0.2rem 0 0.6rem 0; font-size: 1.45rem;">Wet Waste</h3>
            <p style="color: #4A6356; font-size: 0.92rem; line-height: 1.5; margin-bottom: 1rem;">
                Food scraps, fruit and vegetable peels, cooked meal leftovers, coffee grounds, eggshells, and garden trimmings.
            </p>
            <div style="background: #EAF7EE; border-radius: 12px; padding: 0.7rem 0.9rem; font-size: 0.82rem; color: #1B4332; font-weight: 600;">
                Destination: Turned into organic soil compost & bio-gas
            </div>
        </div>
        """)

    with w2:
        render_html(f"""
        <div class="eco-card waste-card-dry">
            <div class="waste-card-icon dry">{styles.SVG_DRY_ICON.strip()}</div>
            <span class="category-badge dry">RECYCLABLE</span>
            <h3 style="color: #0D47A1; margin: 0.2rem 0 0.6rem 0; font-size: 1.45rem;">Dry Waste</h3>
            <p style="color: #3F5E72; font-size: 0.92rem; line-height: 1.5; margin-bottom: 1rem;">
                Clean cardboard delivery boxes, shredded paper, plastic beverage bottles, aluminum cans, glass jars, and containers.
            </p>
            <div style="background: #E1F5FE; border-radius: 12px; padding: 0.7rem 0.9rem; font-size: 0.82rem; color: #0277BD; font-weight: 600;">
                Destination: Upcycled into raw materials for manufacturing
            </div>
        </div>
        """)

    with w3:
        render_html(f"""
        <div class="eco-card waste-card-sanitary">
            <div class="waste-card-icon sanitary">{styles.SVG_SANITARY_ICON.strip()}</div>
            <span class="category-badge sanitary">SAFE DISPOSAL</span>
            <h3 style="color: #BF360C; margin: 0.2rem 0 0.6rem 0; font-size: 1.45rem;">Sanitary Waste</h3>
            <p style="color: #6E4F47; font-size: 0.92rem; line-height: 1.5; margin-bottom: 1rem;">
                Used sanitary napkins, baby and adult diapers, hygiene wipes, grooming cotton, and bandages. Securely wrapped in paper.
            </p>
            <div style="background: #FBE9E7; border-radius: 12px; padding: 0.7rem 0.9rem; font-size: 0.82rem; color: #C62828; font-weight: 600;">
                Destination: High-temperature medical incineration
            </div>
        </div>
        """)

    render_html("<div style='height: 3rem;'></div>")

    # 3. Simple Three-Step Section: Sort -> Book -> Collected
    render_html("""
    <div style="text-align: center; max-width: 640px; margin: 0 auto 2.2rem auto;">
        <span class="category-badge wet" style="background:#EAF7EE; color:#1B4332; font-size:0.8rem; padding:0.4rem 1rem;">HOW IT WORKS</span>
        <h2 style="font-size: 2.1rem; color: #16382B; margin: 0.4rem 0 0.6rem 0;">Sort Your Waste &rarr; Book a Slot &rarr; Get It Collected</h2>
        <p style="color: #52796F; font-size: 1.02rem;">Simple, predictable garbage pickups modeled after top on-demand delivery apps.</p>
    </div>
    """)

    s1, s2, s3 = st.columns(3, gap="medium")

    with s1:
        render_html("""
        <div class="eco-card">
            <div class="step-number">01</div>
            <h3 style="color: #16382B; font-size: 1.35rem; margin-bottom: 0.6rem;">Sort Your Waste</h3>
            <p style="color: #52796F; font-size: 0.93rem; line-height: 1.55;">
                Keep kitchen organics in a green bin, rinsed recyclables dry in a carton, and wrap sanitary waste in paper with a red mark.
            </p>
        </div>
        """)

    with s2:
        render_html("""
        <div class="eco-card">
            <div class="step-number">02</div>
            <h3 style="color: #16382B; font-size: 1.35rem; margin-bottom: 0.6rem;">Book a Slot</h3>
            <p style="color: #52796F; font-size: 0.93rem; line-height: 1.55;">
                Pick your preferred day and 2-hour window. Enter your doorstep address and specific notes like gate code or flat number.
            </p>
        </div>
        """)

    with s3:
        render_html("""
        <div class="eco-card">
            <div class="step-number">03</div>
            <h3 style="color: #16382B; font-size: 1.35rem; margin-bottom: 0.6rem;">Get It Collected</h3>
            <p style="color: #52796F; font-size: 0.93rem; line-height: 1.55;">
                A verified collection partner in your neighborhood accepts your request, picks up your segregated bins, and updates the tracker.
            </p>
        </div>
        """)

    render_html("<div style='height: 3rem;'></div>")

    # 4. Collector / Partner Section (Earn by Collecting Part-Time)
    col_banner_left, col_banner_right = st.columns([1.3, 0.7], gap="large")

    with col_banner_left:
        render_html("""
        <div style="background: linear-gradient(135deg, #184230 0%, #255C43 100%); border-radius: 26px; padding: 2.4rem 2.6rem; color: white;">
            <span style="background: rgba(255, 255, 255, 0.16); padding: 0.35rem 0.9rem; border-radius: 999px; font-size: 0.78rem; font-weight: 700; color: #D8F3DC; text-transform: uppercase; letter-spacing: 0.05em;">
                PARTNER OPPORTUNITY
            </span>
            <h2 style="color: white; font-size: 2rem; margin: 1rem 0 0.8rem 0;">Earn by Collecting Waste in Your Area</h2>
            <p style="color: #D8F3DC; font-size: 1.02rem; line-height: 1.6; margin-bottom: 1.5rem;">
                Turn your free hours into supplemental income while keeping your locality spotless. Pick up sorted waste requests on your own schedule with zero minimum commitments.
            </p>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 1.5rem;">
                <div style="background: rgba(255, 255, 255, 0.1); border-radius: 14px; padding: 0.9rem 1.1rem;">
                    <div style="font-size: 1.3rem; font-weight: 800; color: #95D5B2;">INR 60 - 120</div>
                    <div style="font-size: 0.82rem; color: #E2ECE5;">Estimated payout per pickup trip</div>
                </div>
                <div style="background: rgba(255, 255, 255, 0.1); border-radius: 14px; padding: 0.9rem 1.1rem;">
                    <div style="font-size: 1.3rem; font-weight: 800; color: #95D5B2;">Flexible Hours</div>
                    <div style="font-size: 0.82rem; color: #E2ECE5;">Accept jobs only when you are online</div>
                </div>
            </div>
        </div>
        """)

        if st.button("Register as a Collector Partner", key="earn_btn", type="primary", use_container_width=True):
            if user is None:
                st.session_state.auth_mode = "signup"
                st.session_state.signup_role = "collector"
                navigate_to("Auth")
            else:
                db.set_user_mode(user["id"], 1)
                st.session_state.toast_msg = "Collector mode activated"
                navigate_to("CollectorDashboard")

    with col_banner_right:
        render_html("""
        <div class="eco-card" style="height: 100%;">
            <h4 style="color: #16382B; margin-top: 0; font-size: 1.25rem;">Why Partners Love EcoGo</h4>
            <div style="margin-top: 1rem; display: flex; flex-direction: column; gap: 16px;">
                <div style="display: flex; gap: 12px; align-items: flex-start;">
                    <div style="background: #E8F5E9; border-radius: 8px; padding: 4px 10px; font-weight: 800; color: #2D6A4F; font-size: 0.9rem;">01</div>
                    <div>
                        <b style="color: #1B4332; font-size: 0.95rem;">App-Based Task Queue</b>
                        <div style="color: #557063; font-size: 0.85rem;">View address, distance, and waste type before accepting.</div>
                    </div>
                </div>
                <div style="display: flex; gap: 12px; align-items: flex-start;">
                    <div style="background: #E1F5FE; border-radius: 8px; padding: 4px 10px; font-weight: 800; color: #0277BD; font-size: 0.9rem;">02</div>
                    <div>
                        <b style="color: #1B4332; font-size: 0.95rem;">Pre-Sorted Waste Only</b>
                        <div style="color: #557063; font-size: 0.85rem;">Customers take our quiz so waste is ready for easy handling.</div>
                    </div>
                </div>
                <div style="display: flex; gap: 12px; align-items: flex-start;">
                    <div style="background: #FFF3E0; border-radius: 8px; padding: 4px 10px; font-weight: 800; color: #E65100; font-size: 0.9rem;">03</div>
                    <div>
                        <b style="color: #1B4332; font-size: 0.95rem;">Community Recognition</b>
                        <div style="color: #557063; font-size: 0.85rem;">Be the local green champion for your street and neighborhood.</div>
                    </div>
                </div>
            </div>
        </div>
        """)

    # 5. Polished Footer
    render_html("""
    <div class="ecogo-footer">
        <div style="display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 30px; margin-bottom: 2rem;">
            <div>
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 0.8rem;">
                    <span style="font-family: 'Outfit', sans-serif; font-size: 1.6rem; font-weight: 800; color: #FFFFFF;">EcoGo</span>
                </div>
                <p style="color: #9EC0AD; font-size: 0.92rem; line-height: 1.6; max-width: 320px;">
                    EcoGo connects households with local waste collection partners to make segregated doorstep garbage collection effortless and rewarding.
                </p>
                <div style="color: #74C69D; font-size: 0.85rem; font-weight: 700; margin-top: 0.8rem;">
                    Waste, sorted. World, better.
                </div>
            </div>
            <div>
                <div class="footer-col-title">Navigation</div>
                <div style="margin-bottom: 0.5rem;"><a class="footer-link" href="#home">Home</a></div>
                <div style="margin-bottom: 0.5rem;"><a class="footer-link" href="#book">Book Pickup</a></div>
            </div>
            <div>
                <div class="footer-col-title">Waste Guidelines</div>
                <div style="margin-bottom: 0.5rem;"><a class="footer-link" href="#wet">Wet Biodegradable</a></div>
                <div style="margin-bottom: 0.5rem;"><a class="footer-link" href="#dry">Dry Recyclables</a></div>
                <div style="margin-bottom: 0.5rem;"><a class="footer-link" href="#sanitary">Sanitary Hygiene</a></div>
                <div style="margin-bottom: 0.5rem;"><a class="footer-link" href="#hazardous">Hazardous / E-Waste</a></div>
            </div>
            <div>
                <div class="footer-col-title">Community</div>
                <div style="margin-bottom: 0.5rem;"><a class="footer-link" href="#collector">Collector Program</a></div>
                <div style="margin-bottom: 0.5rem;"><a class="footer-link" href="#safety">Partner Safety Kit</a></div>
                <div style="margin-bottom: 0.5rem;"><a class="footer-link" href="#faq">Frequently Asked Questions</a></div>
                <div style="margin-bottom: 0.5rem;"><a class="footer-link" href="#contact">Contact Support</a></div>
            </div>
        </div>
        <div style="border-top: 1px solid rgba(255,255,255,0.12); padding-top: 1.5rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; color: #8BAF9A; font-size: 0.85rem;">
            <div>&copy; 2026 EcoGo Technologies. All rights reserved. Built with Python &amp; Streamlit.</div>
            <div style="display: flex; gap: 18px;">
                <span>Privacy Policy</span>
                <span>Terms of Service</span>
                <span>Responsible Sorting Pledge</span>
            </div>
        </div>
    </div>
    """)

# -----------------------------------------------------------------------------
# PAGE 2: Dedicated Authentication Screen (Login / Register)
# -----------------------------------------------------------------------------
def render_auth_page():
    render_html("""
    <div style="max-width: 580px; margin: 1.5rem auto 1rem auto; text-align: center;">
        <span class="category-badge wet" style="background:#EAF7EE; color:#1B4332;">ACCOUNT ACCESS</span>
        <h2 style="font-size: 2.2rem; color: #16382B; margin: 0.4rem 0 0.5rem 0;">Welcome to EcoGo</h2>
        <p style="color: #52796F; font-size: 1rem;">Log in to schedule waste pickups or earn as a neighborhood collector.</p>
    </div>
    """)

    auth_col1, auth_col2, auth_col3 = st.columns([0.15, 0.7, 0.15])
    with auth_col2:
        tab_login, tab_signup = st.tabs(["Log In", "Create New Account"])

        with tab_login:
            render_html("<div style='height: 0.6rem;'></div>")
            with st.form("login_form"):
                contact = st.text_input("Email or Phone Number", placeholder="e.g. rahul@ecogo.in or +91 9876543210")
                password = st.text_input("Password", type="password", placeholder="Enter your account password")
                submitted = st.form_submit_button("Sign In to EcoGo", type="primary", use_container_width=True)

            if submitted:
                if not contact.strip() or not password:
                    st.error("Please enter both your email/phone and password.")
                else:
                    found = db.get_user_by_contact(contact)
                    if found and db.verify_password(password, found["password_hash"]):
                        st.session_state.user_id = found["id"]
                        st.session_state.toast_msg = f"Welcome back, {found['name']}"
                        db.set_user_mode(found["id"], 0)
                        navigate_to("CustomerDashboard")
                    else:
                        st.error("Invalid credentials. Please verify your email/phone and password.")

            # Quick Demo Login Shortcut Buttons for easy review
            render_html("<div style='text-align: center; color: #718F83; font-size: 0.85rem; margin: 1.4rem 0 0.8rem 0;'>Instant Demo Sign-in for Evaluation:</div>")
            demo_col1, demo_col2 = st.columns(2)
            with demo_col1:
                if st.button("Demo Customer (Rahul)", key="demo_cust_btn", use_container_width=True):
                    found = db.get_user_by_contact("rahul@ecogo.in")
                    if found:
                        st.session_state.user_id = found["id"]
                        st.session_state.toast_msg = "Logged in as Customer (Rahul Sharma)"
                        navigate_to("CustomerDashboard")
            with demo_col2:
                if st.button("Demo Collector (Priya)", key="demo_coll_btn", use_container_width=True):
                    found = db.get_user_by_contact("priya@ecogo.in")
                    if found:
                        st.session_state.user_id = found["id"]
                        st.session_state.toast_msg = "Logged in as Collector (Priya Patel)"
                        navigate_to("CollectorDashboard")

        with tab_signup:
            render_html("<div style='height: 0.6rem;'></div>")
            default_role = st.session_state.get("signup_role", "customer")
            with st.form("signup_form"):
                new_name = st.text_input("Full Name", placeholder="e.g. Ananya Rao")
                new_contact = st.text_input("Email or Phone Number", placeholder="e.g. ananya@example.com or 9876543210")
                new_pass = st.text_input("Create Password (min. 8 characters)", type="password")
                new_pass_confirm = st.text_input("Confirm Password", type="password")

                render_html("<div style='font-size: 0.88rem; font-weight: 700; color: #16382B; margin-top: 0.8rem;'>I want to use EcoGo to:</div>")
                mode_choice = st.radio(
                    "Select your primary mode:",
                    options=["Get My Waste Collected (Customer)", "Collect Waste and Earn (Collector Partner)"],
                    index=1 if default_role == "collector" else 0,
                    label_visibility="collapsed"
                )

                signup_submit = st.form_submit_button("Create My EcoGo Account", type="primary", use_container_width=True)

            if signup_submit:
                if not new_name.strip() or not new_contact.strip() or not new_pass:
                    st.error("Please fill in all required fields.")
                elif len(new_pass) < 8:
                    st.error("Password must be at least 8 characters long.")
                elif new_pass != new_pass_confirm:
                    st.error("Passwords do not match. Please re-type.")
                else:
                    existing = db.get_user_by_contact(new_contact)
                    if existing:
                        st.error("An account with this email or phone number already exists.")
                    else:
                        is_worker = 1 if "Collect Waste and Earn" in mode_choice else 0
                        user_id = db.create_user(
                            name=new_name,
                            contact=new_contact,
                            password=new_pass,
                            role="collector" if is_worker else "customer",
                            worker_enabled=is_worker
                        )
                        st.session_state.user_id = user_id
                        st.session_state.toast_msg = f"Account created. Welcome, {new_name.split()[0]}"
                        navigate_to("Tutorial")

        render_html("<div style='height: 1.2rem;'></div>")
        if st.button("Return to Homepage", key="back_home_btn", use_container_width=True):
            navigate_to("Landing")

# -----------------------------------------------------------------------------
# PAGE 3: Waste Segregation Tutorial & Interactive Quiz
# -----------------------------------------------------------------------------
def render_tutorial_page():
    render_html("""
    <div style="max-width: 800px; margin: 0 auto 1.5rem auto; text-align: center;">
        <span class="category-badge wet" style="background:#EAF7EE; color:#1B4332;">FIRST-TIME ONBOARDING</span>
        <h2 style="font-size: 2.2rem; color: #16382B; margin: 0.4rem 0 0.5rem 0;">Waste Segregation 101</h2>
        <p style="color: #52796F; font-size: 1.05rem; line-height: 1.5;">
            Proper segregation at home ensures that clean recyclables stay recyclable, food waste turns into nutrient compost, and our collection partners stay safe.
        </p>
    </div>
    """)

    # 3 Visual Explanatory Cards
    col_t1, col_t2, col_t3 = st.columns(3, gap="medium")

    with col_t1:
        render_html(f"""
        <div class="eco-card waste-card-wet" style="height: 100%;">
            <div class="waste-card-icon wet">{styles.SVG_WET_ICON.strip()}</div>
            <h3 style="color: #1B4332; margin-top: 0;">1. Wet Waste</h3>
            <div style="font-size: 0.85rem; color: #2D6A4F; font-weight: 700; margin-bottom: 0.5rem;">GREEN BIN (Organic)</div>
            <p style="color: #4A6356; font-size: 0.88rem; line-height: 1.5;">
                <b>Included:</b> Food scraps, fruit peels, vegetable ends, eggshells, tea bags, leftover bread, fallen leaves.<br><br>
                <b>Avoid:</b> Plastic bags, twist ties, milk packets, aluminum foil.
            </p>
        </div>
        """)

    with col_t2:
        render_html(f"""
        <div class="eco-card waste-card-dry" style="height: 100%;">
            <div class="waste-card-icon dry">{styles.SVG_DRY_ICON.strip()}</div>
            <h3 style="color: #0D47A1; margin-top: 0;">2. Dry Waste</h3>
            <div style="font-size: 0.85rem; color: #1976D2; font-weight: 700; margin-bottom: 0.5rem;">BLUE BIN (Recyclable)</div>
            <p style="color: #3F5E72; font-size: 0.88rem; line-height: 1.5;">
                <b>Included:</b> Flattened cardboard boxes, newspapers, plastic bottles (rinsed), beverage cans, clean glass bottles.<br><br>
                <b>Avoid:</b> Oily pizza grease boxes, soiled paper tissues.
            </p>
        </div>
        """)

    with col_t3:
        render_html(f"""
        <div class="eco-card waste-card-sanitary" style="height: 100%;">
            <div class="waste-card-icon sanitary">{styles.SVG_SANITARY_ICON.strip()}</div>
            <h3 style="color: #BF360C; margin-top: 0;">3. Sanitary Waste</h3>
            <div style="font-size: 0.85rem; color: #D84315; font-weight: 700; margin-bottom: 0.5rem;">RED / PAPER WRAP (Hygiene)</div>
            <p style="color: #6E4F47; font-size: 0.88rem; line-height: 1.5;">
                <b>Included:</b> Used sanitary pads, baby and adult diapers, grooming cotton, bandages.<br><br>
                <b>Rule:</b> Always wrap securely in newspaper or biodegradable pouch and mark with a red cross.
            </p>
        </div>
        """)

    render_html("<div style='height: 2rem;'></div>")

    # 3-Question Quiz
    render_html("""
    <div style="max-width: 800px; margin: 0 auto; background: #FFFFFF; border: 1px solid #E3ECE5; border-radius: 22px; padding: 2rem 2.2rem; box-shadow: 0 8px 24px rgba(22, 62, 47, 0.05);">
        <h3 style="color: #16382B; margin-top: 0; font-size: 1.4rem;">Knowledge Check (3 Questions)</h3>
        <p style="color: #52796F; font-size: 0.95rem; margin-bottom: 1.5rem;">Answer these 3 practical questions to certify your account for collection bookings.</p>
    </div>
    """)

    with st.form("quiz_form"):
        q1 = st.radio(
            "1. Where should banana peels, apple cores, and coffee grounds be placed?",
            options=[
                "In the Blue Dry Waste bin with cardboard",
                "In the Green Wet Waste bin (Organic)",
                "In the Sanitary Waste pouch"
            ],
            index=None
        )

        render_html("<div style='height: 0.8rem;'></div>")

        q2 = st.radio(
            "2. You finished a cardboard delivery package and rinsed out a plastic water bottle. Where do they belong?",
            options=[
                "In the Green Wet Waste bin",
                "In the Blue Dry Waste bin (Recyclable)",
                "Mixed together with food leftovers"
            ],
            index=None
        )

        render_html("<div style='height: 0.8rem;'></div>")

        q3 = st.radio(
            "3. What is the correct protocol for disposing of sanitary items (diapers, pads)?",
            options=[
                "Toss loosely into the open dry recyclables bin",
                "Flush them down the household toilet",
                "Wrap securely in newspaper/paper pouch and label as Sanitary Waste"
            ],
            index=None
        )

        render_html("<div style='height: 1rem;'></div>")
        quiz_submit = st.form_submit_button("Submit Answers & Verify", type="primary", use_container_width=True)

    if quiz_submit:
        if None in (q1, q2, q3):
            st.warning("Please select an answer for all 3 questions before submitting.")
        else:
            ans1_correct = "Green Wet Waste bin" in q1
            ans2_correct = "Blue Dry Waste bin" in q2
            ans3_correct = "Wrap securely in newspaper" in q3

            score = sum([ans1_correct, ans2_correct, ans3_correct])
            db.record_quiz_result(user["id"], score, 3)

            if score == 3:
                st.success("Perfect 3/3! You are certified for EcoGo collection bookings.")
                st.session_state.quiz_completed = True
            elif score >= 2:
                st.success(f"Great job! You scored {score}/3. You are ready to book pickups.")
                st.session_state.quiz_completed = True
            else:
                st.error(f"You scored {score}/3. Please review the explanations below and try again.")

            # Explanations for questions
            st.markdown("#### Review & Explanations:")
            if ans1_correct:
                st.markdown("**Question 1 [Correct]:** Fruit peels and vegetable scraps are biodegradable organic waste that decompose into rich compost.")
            else:
                st.markdown("**Question 1 [Review]:** Banana peels and coffee grounds are **Wet Waste (Green bin)**, never dry recycling.")

            if ans2_correct:
                st.markdown("**Question 2 [Correct]:** Rinsed plastics and dry cardboard are valuable recyclables for the Blue bin.")
            else:
                st.markdown("**Question 2 [Review]:** Clean, dry packaging materials belong in **Dry Waste (Blue bin)**.")

            if ans3_correct:
                st.markdown("**Question 3 [Correct]:** Sanitary waste must always be securely wrapped to protect sanitation workers from infection.")
            else:
                st.markdown("**Question 3 [Review]:** Sanitary waste must be **wrapped securely in paper** and segregated. Never flush or mix loose.")

    if st.session_state.get("quiz_completed", False) or db.has_completed_quiz(user["id"]):
        render_html("<div style='height: 1.2rem;'></div>")
        if st.button("Continue to Dashboard", type="primary", use_container_width=True):
            if user["worker_enabled"]:
                navigate_to("CollectorDashboard")
            else:
                navigate_to("CustomerDashboard")

# -----------------------------------------------------------------------------
# PAGE 4: Customer Dashboard & Pickup Booking
# -----------------------------------------------------------------------------
def render_customer_dashboard():
    # Welcome Header & Metrics
    first_name = user["name"].split()[0]
    my_bookings = db.get_bookings_for_customer(user["id"])
    active_bookings = [b for b in my_bookings if b["status"] in ("Open", "Accepted", "Picked up")]
    completed_bookings = [b for b in my_bookings if b["status"] == "Completed"]

    render_html(f"""
    <div style="background: linear-gradient(135deg, #184230 0%, #2D6A4F 100%); border-radius: 24px; padding: 2.2rem 2.4rem; color: white; margin-bottom: 2rem; box-shadow: 0 12px 36px rgba(22, 62, 47, 0.12);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
            <div>
                <span class="role-badge role-badge-customer" style="margin-bottom: 0.6rem;">MY BOOKINGS</span>
                <h1 style="color: white; margin: 0.3rem 0; font-size: clamp(1.8rem, 3.5vw, 2.4rem);">My Bookings · {first_name}</h1>
                <p style="color: #D8F3DC; font-size: 1rem; margin: 0; max-width: 600px;">
                    Track your active waste collection requests, schedule a new pickup, and view completed history.
                </p>
            </div>
            <div style="display: flex; gap: 12px;">
                <div style="background: rgba(255,255,255,0.12); border-radius: 16px; padding: 0.9rem 1.4rem; text-align: center; border: 1px solid rgba(255,255,255,0.2);">
                    <div style="font-size: 1.8rem; font-weight: 800; color: #FFFFFF; font-family: 'Outfit';">{len(my_bookings)}</div>
                    <div style="font-size: 0.78rem; color: #D8F3DC; font-weight: 600; text-transform: uppercase;">Total Pickups</div>
                </div>
                <div style="background: rgba(255,255,255,0.12); border-radius: 16px; padding: 0.9rem 1.4rem; text-align: center; border: 1px solid rgba(255,255,255,0.2);">
                    <div style="font-size: 1.8rem; font-weight: 800; color: #74C69D; font-family: 'Outfit';">{len(active_bookings)}</div>
                    <div style="font-size: 0.78rem; color: #D8F3DC; font-weight: 600; text-transform: uppercase;">Active Jobs</div>
                </div>
                <div style="background: rgba(255,255,255,0.12); border-radius: 16px; padding: 0.9rem 1.4rem; text-align: center; border: 1px solid rgba(255,255,255,0.2);">
                    <div style="font-size: 1.8rem; font-weight: 800; color: #95D5B2; font-family: 'Outfit';">{len(completed_bookings) * 5} kg</div>
                    <div style="font-size: 0.78rem; color: #D8F3DC; font-weight: 600; text-transform: uppercase;">Waste Diverted</div>
                </div>
            </div>
        </div>
    </div>
    """)

    # 2 Tabs: "My Bookings & Live Tracking" vs "Schedule a New Pickup"
    cust_tab1, cust_tab2 = st.tabs([f"My Bookings & Live Tracking ({len(my_bookings)})", "Schedule a New Pickup"])

    with cust_tab1:
        if not my_bookings:
            render_html("""
            <div class="eco-card" style="text-align: center; padding: 3rem 2rem;">
                <h3 style="color: #16382B;">No Bookings Scheduled Yet</h3>
                <p style="color: #52796F; max-width: 440px; margin: 0 auto 1.5rem auto;">
                    You have not scheduled any waste collections yet. Keep your home clutter-free by booking your first pickup in the "Schedule a New Pickup" tab.
                </p>
            </div>
            """)
        else:
            # Active Bookings
            if active_bookings:
                st.markdown("### Active & Upcoming Pickups")
                for b in active_bookings:
                    status = b["status"]
                    status_badge = {
                        "Open": ("#FFF3E0", "#E65100", "Open — Finding Nearby Collector"),
                        "Accepted": ("#E1F5FE", "#0277BD", f"Accepted by {b['collector_name'] or 'Partner'}"),
                        "Picked up": ("#EDE7F6", "#512DA8", "In Transit — Picked Up from Doorstep")
                    }.get(status, ("#E8F5E9", "#2E7D32", status))

                    render_html(f"""
                    <div class="eco-card" style="margin-bottom: 1.2rem; border-left: 6px solid #2D6A4F;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: gap: 10px;">
                            <div>
                                <span style="background: {status_badge[0]}; color: {status_badge[1]}; padding: 0.35rem 0.85rem; border-radius: 999px; font-size: 0.8rem; font-weight: 700;">
                                    {status_badge[2]}
                                </span>
                                <h3 style="color: #16382B; margin: 0.7rem 0 0.3rem 0; font-size: 1.35rem;">
                                    Booking #{b['id']} · {b['waste_type']}
                                </h3>
                                <div style="color: #52796F; font-size: 0.92rem; font-weight: 600;">
                                    Date: {b['pickup_date']} &nbsp;|&nbsp; Slot: {b['pickup_slot']} &nbsp;|&nbsp; Volume: {b['quantity']}
                                </div>
                            </div>
                        </div>

                        <!-- Progress Tracker -->
                        <div style="display: flex; align-items: center; gap: 8px; margin: 1.4rem 0 1rem 0; flex-wrap: wrap;">
                            <div class="timeline-step">
                                <div class="timeline-dot {'done' if status in ('Open', 'Accepted', 'Picked up', 'Completed') else 'pending'}">1</div>
                                <span style="font-size: 0.82rem; font-weight: 700; color: #16382B;">Requested</span>
                            </div>
                            <div style="width: 30px; height: 2px; background: {'#2D6A4F' if status in ('Accepted', 'Picked up', 'Completed') else '#DCE7DE'};"></div>
                            <div class="timeline-step">
                                <div class="timeline-dot {'done' if status in ('Accepted', 'Picked up', 'Completed') else ('active' if status == 'Open' else 'pending')}">2</div>
                                <span style="font-size: 0.82rem; font-weight: 700; color: #16382B;">Collector Assigned</span>
                            </div>
                            <div style="width: 30px; height: 2px; background: {'#2D6A4F' if status in ('Picked up', 'Completed') else '#DCE7DE'};"></div>
                            <div class="timeline-step">
                                <div class="timeline-dot {'done' if status in ('Picked up', 'Completed') else ('active' if status == 'Accepted' else 'pending')}">3</div>
                                <span style="font-size: 0.82rem; font-weight: 700; color: #16382B;">Collected</span>
                            </div>
                            <div style="width: 30px; height: 2px; background: {'#2D6A4F' if status == 'Completed' else '#DCE7DE'};"></div>
                            <div class="timeline-step">
                                <div class="timeline-dot {'done' if status == 'Completed' else 'pending'}">4</div>
                                <span style="font-size: 0.82rem; font-weight: 700; color: #849A8F;">Recycled</span>
                            </div>
                        </div>

                        <div style="background: #F8FAF7; border-radius: 12px; padding: 0.8rem 1.1rem; margin-top: 0.8rem; font-size: 0.88rem;">
                            <div><b>Address:</b> {b['address']}</div>
                            {f"<div style='margin-top: 4px;'><b>Instructions:</b> {b['notes']}</div>" if b['notes'] else ""}
                            {f"<div style='margin-top: 6px; color: #0277BD;'><b>Assigned Partner:</b> {b['collector_name']} ({b['collector_contact']})</div>" if b['collector_name'] else "<div style='margin-top: 6px; color: #E65100;'>Waiting for collector assignment.</div>"}
                        </div>
                    </div>
                    """)

                    if status == "Open":
                        if st.button(f"Cancel Request #{b['id']}", key=f"cancel_btn_{b['id']}"):
                            db.update_booking_status(b["id"], "Cancelled")
                            st.session_state.toast_msg = f"Booking #{b['id']} has been cancelled"
                            st.rerun()

            # Completed & Past Bookings
            past_bookings = [b for b in my_bookings if b["status"] in ("Completed", "Cancelled")]
            if past_bookings:
                render_html("<div style='height: 1.5rem;'></div>")
                st.markdown("### Past Collection History")
                for b in past_bookings:
                    is_completed = b["status"] == "Completed"
                    badge_color = ("#E8F5E9", "#2E7D32") if is_completed else ("#ECEFF1", "#546E7A")

                    render_html(f"""
                    <div class="eco-card" style="margin-bottom: 0.85rem; padding: 1.2rem 1.4rem;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <b style="color: #16382B; font-size: 1.05rem;">#{b['id']} · {b['waste_type']}</b>
                                <div style="color: #6D8578; font-size: 0.84rem;">Date: {b['pickup_date']} · Slot: {b['pickup_slot']} · {b['address']}</div>
                            </div>
                            <span style="background: {badge_color[0]}; color: {badge_color[1]}; padding: 0.3rem 0.8rem; border-radius: 999px; font-size: 0.76rem; font-weight: 700;">
                                {b['status'].upper()}
                            </span>
                        </div>
                    </div>
                    """)

    with cust_tab2:
        render_html("""
        <div style="margin-bottom: 1.2rem;">
            <h3 style="color: #16382B; margin-bottom: 0.2rem;">Book Your Doorstep Collection</h3>
            <p style="color: #52796F; font-size: 0.95rem;">Select your sorted waste category, preferred collection time, and address.</p>
        </div>
        """)

        with st.form("customer_booking_form"):
            st.markdown("#### 1. Select Waste Category")
            waste_type = st.radio(
                "Waste Category",
                options=["Wet waste (Organic kitchen scraps & peels)", "Dry waste (Paper, clean cardboard, plastic & glass)", "Sanitary waste (Securely wrapped diapers & pads)"],
                index=0,
                label_visibility="collapsed"
            )

            # Extract clean title
            waste_clean = "Wet waste" if "Wet" in waste_type else ("Dry waste" if "Dry" in waste_type else "Sanitary waste")

            render_html("<div style='height: 0.8rem;'></div>")
            col_b1, col_b2 = st.columns(2)

            with col_b1:
                st.markdown("#### 2. Select Date & Window")
                min_p_date = date.today()
                pickup_date_input = st.date_input("Pickup Date", min_value=min_p_date, value=min_p_date)
                slot_choice = st.selectbox(
                    "Available Time Window",
                    options=[
                        "8:00 AM – 10:00 AM (Morning Slot)",
                        "10:00 AM – 12:00 PM (Midday Slot)",
                        "12:00 PM – 2:00 PM (Early Afternoon)",
                        "2:00 PM – 4:00 PM (Afternoon Slot)",
                        "4:00 PM – 6:00 PM (Evening Slot)"
                    ],
                    index=0
                )
                quantity_choice = st.selectbox(
                    "Estimated Volume",
                    options=["1 small bag / bin (< 5 kg)", "2-3 medium bags (5-15 kg)", "Bulk / Large carton box (> 15 kg)"]
                )

            with col_b2:
                st.markdown("#### 3. Pickup Address & Instructions")
                address_input = st.text_area(
                    "Complete Address",
                    placeholder="Apartment/House No., Building Name, Street, Locality, City",
                    help="Include landmark or floor details for easy access."
                )
                notes_input = st.text_input(
                    "Optional Gate or Contact Instructions",
                    placeholder="e.g. Leave by door, call on arrival, gate code 402"
                )

            render_html("""
            <div style="height: 0.5rem;'></div>
            <div style="background: #F4F9F5; border: 1px solid #CDE2D4; border-radius: 14px; padding: 0.9rem 1.2rem; font-size: 0.88rem; color: #1B4332;">
                <b>Free Neighborhood Pickup:</b> Our verified partner will arrive during your chosen slot. Please keep your waste segregated as selected.
            </div>
            <div style="height: 1rem;'></div>
            """)

            book_submit = st.form_submit_button("Confirm & Schedule Pickup", type="primary", use_container_width=True)

        if book_submit:
            if not address_input.strip():
                st.error("Please enter your complete pickup address.")
            elif pickup_date_input < date.today():
                st.error("Please select today or a future date for pickup.")
            else:
                new_b_id = db.create_booking(
                    customer_id=user["id"],
                    waste_type=waste_clean,
                    quantity=quantity_choice,
                    pickup_date=pickup_date_input,
                    pickup_slot=slot_choice.split(" (")[0],
                    address=address_input,
                    notes=notes_input
                )
                st.session_state.toast_msg = f"Booking #{new_b_id} successfully scheduled"
                st.rerun()

# -----------------------------------------------------------------------------
# PAGE 5: Collector Dashboard & Work Queue
# -----------------------------------------------------------------------------
def render_collector_dashboard():
    first_name = user["name"].split()[0]
    online = bool(user["online_status"]) if "online_status" in user.keys() else True

    # Collector Header Banner
    render_html(f"""
    <div style="background: linear-gradient(135deg, #1A4332 0%, #205740 60%, #2C6D51 100%); border-radius: 24px; padding: 2.2rem 2.4rem; color: white; margin-bottom: 1.8rem; box-shadow: 0 12px 36px rgba(22, 62, 47, 0.12);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
            <div>
                <span class="role-badge role-badge-collector" style="margin-bottom: 0.6rem;">COLLECTION PARTNER HUB</span>
                <h1 style="color: white; margin: 0.3rem 0; font-size: clamp(1.8rem, 3.5vw, 2.4rem);">Partner Portal — {first_name}</h1>
                <p style="color: #D8F3DC; font-size: 1rem; margin: 0; max-width: 600px;">
                    Accept neighborhood pickup jobs, navigate to collection addresses, and earn estimated rewards for keeping the city clean.
                </p>
            </div>
            <div style="background: rgba(255,255,255,0.12); border-radius: 18px; padding: 1rem 1.6rem; border: 1px solid rgba(255,255,255,0.22); text-align: center;">
                <div style="font-size: 0.8rem; color: #D8F3DC; font-weight: 700; text-transform: uppercase;">Duty Status</div>
                <div style="font-size: 1.35rem; font-weight: 800; color: {'#74C69D' if online else '#FFA726'}; margin-top: 4px;">
                    {'ONLINE & READY' if online else 'OFFLINE (PAUSED)'}
                </div>
            </div>
        </div>
    </div>
    """)

    # Online / Offline Toggle & Mode Switch
    tog_col1, tog_col2 = st.columns([1.5, 1])
    with tog_col1:
        new_online = st.toggle("Accepting New Collection Requests (Online Duty)", value=online, help="Turn this off when taking a break or outside working hours.")
        if new_online != online:
            db.set_collector_online_status(user["id"], new_online)
            st.rerun()

    with tog_col2:
        if st.button("Switch to Customer Mode (Book Pickups)", key="coll_switch_cust", use_container_width=True):
            db.set_user_mode(user["id"], 0)
            st.session_state.toast_msg = "Switched to Customer mode"
            navigate_to("CustomerDashboard")

    render_html("<div style='height: 0.8rem;'></div>")

    # Collector Stats & Earnings Summary
    open_requests = db.get_open_bookings() if new_online else []
    my_collections = db.get_collector_bookings(user["id"])
    active_jobs = [b for b in my_collections if b["status"] in ("Accepted", "Picked up")]
    completed_jobs = [b for b in my_collections if b["status"] == "Completed"]
    estimated_earnings = len(completed_jobs) * 75  # Estimated projection (INR 75 avg per pickup)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        render_html(f"""
        <div class="metric-box">
            <div class="metric-box-title">Nearby Open Requests</div>
            <div class="metric-box-value">{len(open_requests)}</div>
            <div class="metric-box-sub">{'Available to accept' if new_online else 'Turn duty online to view'}</div>
        </div>
        """)
    with m2:
        render_html(f"""
        <div class="metric-box">
            <div class="metric-box-title">Active Assigned Jobs</div>
            <div class="metric-box-value">{len(active_jobs)}</div>
            <div class="metric-box-sub">In progress today</div>
        </div>
        """)
    with m3:
        render_html(f"""
        <div class="metric-box">
            <div class="metric-box-title">Completed Collections</div>
            <div class="metric-box-value">{len(completed_jobs)}</div>
            <div class="metric-box-sub">Successfully recycled</div>
        </div>
        """)
    with m4:
        render_html(f"""
        <div class="metric-box">
            <div class="metric-box-title">Estimated Earnings</div>
            <div class="metric-box-value" style="color: #2E7D32;">INR {estimated_earnings}</div>
            <div class="metric-box-sub">Estimated (~INR 75/trip)</div>
        </div>
        """)

    render_html("<div style='height: 1.5rem;'></div>")

    tab_open, tab_active, tab_completed = st.tabs([
        f"Open Requests ({len(open_requests)})",
        f"In-Progress Jobs ({len(active_jobs)})",
        f"Completed & Earnings Log ({len(completed_jobs)})"
    ])

    with tab_open:
        if not new_online:
            st.info("You are currently OFFLINE. Toggle 'Accepting New Collection Requests' to Online above to see available requests.")
        elif not open_requests:
            render_html("""
            <div class="eco-card" style="text-align: center; padding: 2.8rem 2rem;">
                <h3 style="color: #16382B;">All Caught Up in Your Neighborhood</h3>
                <p style="color: #52796F; max-width: 440px; margin: 0 auto;">
                    There are no unassigned pickup requests right now. New requests will appear here as soon as residents book.
                </p>
            </div>
            """)
        else:
            st.markdown("### Available Pickup Requests Near You")
            st.caption("Review address and waste type. Click 'Accept Pickup' to claim. (First collector to accept gets the job.)")

            for b in open_requests:
                render_html(f"""
                <div class="eco-card" style="margin-bottom: 1.2rem; border-top: 4px solid #2D6A4F;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
                        <div>
                            <span class="category-badge wet" style="background:#EAF7EE; color:#1B4332;">OPEN REQUEST · #{b['id']}</span>
                            <h3 style="color: #16382B; margin: 0.5rem 0 0.2rem 0; font-size: 1.35rem;">
                                {b['waste_type']} ({b['quantity']})
                            </h3>
                            <div style="color: #2D6A4F; font-weight: 700; font-size: 0.95rem;">
                                Date: {b['pickup_date']} &nbsp;|&nbsp; Slot: {b['pickup_slot']}
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="background: #E8F5E9; border-radius: 12px; padding: 0.5rem 0.9rem; display: inline-block;">
                                <div style="font-size: 1.15rem; font-weight: 800; color: #2E7D32;">INR 60 - 80</div>
                                <div style="font-size: 0.72rem; color: #43A047; font-weight: 600;">EST. PAYOUT</div>
                            </div>
                        </div>
                    </div>

                    <div style="background: #F8FAF7; border-radius: 12px; padding: 0.9rem 1.1rem; margin: 1rem 0; font-size: 0.9rem;">
                        <div><b>Address:</b> {b['address']}</div>
                        <div><b>Resident:</b> {b['customer_name']} {f'({b["customer_contact"]})' if b['customer_contact'] else ''}</div>
                        {f"<div style='margin-top: 4px;'><b>Resident Note:</b> {b['notes']}</div>" if b['notes'] else ""}
                    </div>
                </div>
                """)

                # Concurrency-safe Accept button
                if st.button(f"Accept Pickup #{b['id']}", key=f"accept_job_{b['id']}", type="primary", use_container_width=True):
                    success = db.accept_booking(b["id"], user["id"])
                    if success:
                        st.session_state.toast_msg = f"Job #{b['id']} accepted. Added to your In-Progress list."
                        st.rerun()
                    else:
                        st.error(f"Booking #{b['id']} was just accepted by another collector! Refreshing list...")
                        st.rerun()

    with tab_active:
        if not active_jobs:
            render_html("""
            <div class="eco-card" style="text-align: center; padding: 2.8rem 2rem;">
                <h3 style="color: #16382B;">No Active Pickups in Progress</h3>
                <p style="color: #52796F; max-width: 440px; margin: 0 auto;">
                    Accept requests from the Open Requests tab to build your daily route.
                </p>
            </div>
            """)
        else:
            st.markdown("### Your Active Route & Next Actions")
            for b in active_jobs:
                curr_status = b["status"]
                render_html(f"""
                <div class="eco-card" style="margin-bottom: 1.2rem; border-left: 6px solid {'#0277BD' if curr_status == 'Accepted' else '#7B1FA2'};">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
                        <div>
                            <span style="background: {'#E1F5FE' if curr_status == 'Accepted' else '#EDE7F6'}; color: {'#0277BD' if curr_status == 'Accepted' else '#7B1FA2'}; padding: 0.35rem 0.85rem; border-radius: 999px; font-size: 0.78rem; font-weight: 700;">
                                {'ACCEPTED · READY FOR PICKUP' if curr_status == 'Accepted' else 'PICKED UP · IN TRANSIT TO RECYCLING'}
                            </span>
                            <h3 style="color: #16382B; margin: 0.6rem 0 0.2rem 0; font-size: 1.35rem;">
                                Pickup #{b['id']} · {b['waste_type']}
                            </h3>
                            <div style="color: #52796F; font-size: 0.92rem;">
                                Date: {b['pickup_date']} &nbsp;|&nbsp; Slot: {b['pickup_slot']} &nbsp;|&nbsp; Volume: {b['quantity']}
                            </div>
                        </div>
                    </div>

                    <div style="background: #F8FAF7; border-radius: 12px; padding: 0.9rem 1.1rem; margin: 1rem 0; font-size: 0.9rem;">
                        <div><b>Location:</b> {b['address']}</div>
                        <div><b>Resident Contact:</b> {b['customer_name']} · Phone: <b>{b['customer_contact']}</b></div>
                        {f"<div style='margin-top: 4px;'><b>Entry Note:</b> {b['notes']}</div>" if b['notes'] else ""}
                    </div>
                </div>
                """)

                col_act1, col_act2 = st.columns(2)
                with col_act1:
                    if curr_status == "Accepted":
                        if st.button(f"Mark as Picked Up #{b['id']}", key=f"mark_picked_{b['id']}", type="primary", use_container_width=True):
                            db.update_booking_status(b["id"], "Picked up")
                            st.session_state.toast_msg = f"Status updated: Pickup #{b['id']} collected from doorstep."
                            st.rerun()
                    elif curr_status == "Picked up":
                        if st.button(f"Mark as Completed & Handed Over #{b['id']}", key=f"mark_comp_{b['id']}", type="primary", use_container_width=True):
                            db.update_booking_status(b["id"], "Completed")
                            st.session_state.toast_msg = f"Collection #{b['id']} completed and credited to your log."
                            st.rerun()

                with col_act2:
                    st.caption("Coordinate with resident via phone if gate is locked or bins are inside.")

    with tab_completed:
        if not completed_jobs:
            render_html("""
            <div class="eco-card" style="text-align: center; padding: 2.8rem 2rem;">
                <h3 style="color: #16382B;">No Completed Pickups Yet</h3>
                <p style="color: #52796F; max-width: 440px; margin: 0 auto;">
                    Completed pickups will be logged here alongside your estimated payout calculations.
                </p>
            </div>
            """)
        else:
            st.markdown(f"### Completed Collection History ({len(completed_jobs)})")
            st.caption("Note: Payout figures are estimated projections based on trip volume and waste category.")

            for b in completed_jobs:
                render_html(f"""
                <div class="eco-card" style="margin-bottom: 0.85rem; padding: 1.1rem 1.4rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                        <div>
                            <b style="color: #16382B; font-size: 1.05rem;">Job #{b['id']} · {b['waste_type']}</b>
                            <div style="color: #6D8578; font-size: 0.84rem;">Date: {b['pickup_date']} · {b['address']} · Customer: {b['customer_name']}</div>
                        </div>
                        <div style="text-align: right;">
                            <span style="background: #E8F5E9; color: #2E7D32; padding: 0.3rem 0.8rem; border-radius: 999px; font-size: 0.78rem; font-weight: 700;">
                                COMPLETED · +INR 75 (Est.)
                            </span>
                        </div>
                    </div>
                </div>
                """)

# -----------------------------------------------------------------------------
# Main Router
# -----------------------------------------------------------------------------
page = st.session_state.get("current_page", "Landing")

# When a user is logged in, they can strictly only access My Bookings, Switch to Collector, or Tutorial
if user is not None and page in ("Landing", "Auth"):
    page = "CollectorDashboard" if user.get("worker_enabled") else "CustomerDashboard"
    st.session_state.current_page = page

if page == "Landing":
    if user is not None:
        render_customer_dashboard()
    else:
        render_landing_page()
elif page == "Auth":
    if user is not None:
        render_customer_dashboard()
    else:
        render_auth_page()
elif page == "Tutorial":
    if user is None:
        navigate_to("Auth")
    else:
        render_tutorial_page()
elif page == "CustomerDashboard":
    if user is None:
        navigate_to("Auth")
    else:
        render_customer_dashboard()
elif page == "CollectorDashboard":
    if user is None:
        navigate_to("Auth")
    else:
        render_collector_dashboard()
else:
    if user is not None:
        render_customer_dashboard()
    else:
        render_landing_page()

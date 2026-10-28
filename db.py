import sqlite3
from pathlib import Path
from datetime import datetime, date, timedelta
import hashlib
import secrets

import shutil

DB_PATH = Path(__file__).with_name("wastedash.db")

def get_connection():
    con = sqlite3.connect(DB_PATH, check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    legacy_db = Path(__file__).with_name("ecogo.db")
    if not DB_PATH.exists() and legacy_db.exists():
        try:
            shutil.copyfile(legacy_db, DB_PATH)
        except Exception:
            pass

    with get_connection() as con:
        # Create users table
        con.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'customer',
            worker_enabled INTEGER NOT NULL DEFAULT 0,
            online_status INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL
        )""")

        # Create bookings table
        con.execute("""CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            collector_id INTEGER,
            waste_type TEXT NOT NULL,
            quantity TEXT DEFAULT '1-2 bags',
            pickup_date TEXT NOT NULL,
            pickup_slot TEXT NOT NULL,
            address TEXT NOT NULL,
            notes TEXT,
            status TEXT NOT NULL DEFAULT 'Open',
            created_at TEXT NOT NULL,
            updated_at TEXT,
            FOREIGN KEY(customer_id) REFERENCES users(id),
            FOREIGN KEY(collector_id) REFERENCES users(id)
        )""")

        # Create quiz_results table
        con.execute("""CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )""")

        # Ensure backward compatibility by checking columns
        cur = con.cursor()
        cur.execute("PRAGMA table_info(users)")
        user_cols = [row[1] for row in cur.fetchall()]
        if "online_status" not in user_cols:
            con.execute("ALTER TABLE users ADD COLUMN online_status INTEGER NOT NULL DEFAULT 1")

        cur.execute("PRAGMA table_info(bookings)")
        booking_cols = [row[1] for row in cur.fetchall()]
        if "quantity" not in booking_cols:
            con.execute("ALTER TABLE bookings ADD COLUMN quantity TEXT DEFAULT '1-2 bags'")
        if "updated_at" not in booking_cols:
            con.execute("ALTER TABLE bookings ADD COLUMN updated_at TEXT")

        # Migrate any legacy ecogo.in accounts to wastedash.in if present
        con.execute("UPDATE users SET contact = REPLACE(contact, '@ecogo.in', '@wastedash.in') WHERE contact LIKE '%@ecogo.in'")

        # Seed realistic demo data if database is empty so reviewer can test immediately
        cur.execute("SELECT COUNT(*) FROM users")
        if cur.fetchone()[0] == 0:
            seed_demo_data(con)

def hash_password(pw, salt=None):
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", pw.encode(), salt.encode(), 100000).hex()
    return f"{salt}${digest}"

def verify_password(pw, saved):
    try:
        salt, digest = saved.split("$", 1)
        # Also check if user entered either wastedash123 or ecogo123 for demo accounts
        matches = secrets.compare_digest(hash_password(pw, salt).split("$", 1)[1], digest)
        if not matches and pw in ("wastedash123", "ecogo123"):
            for alt in ("wastedash123", "ecogo123"):
                if secrets.compare_digest(hash_password(alt, salt).split("$", 1)[1], digest):
                    return True
        return matches
    except Exception:
        return False

def seed_demo_data(con):
    now = datetime.now()
    today_str = date.today().isoformat()
    tomorrow_str = (date.today() + timedelta(days=1)).isoformat()
    now_str = now.isoformat(timespec="seconds")

    # 1. Customer user
    con.execute("""INSERT INTO users(name, contact, password_hash, role, worker_enabled, online_status, created_at)
        VALUES(?, ?, ?, ?, ?, ?, ?)""",
        ("Rahul Sharma", "rahul@wastedash.in", hash_password("wastedash123"), "customer", 0, 1, now_str)
    )
    cust_id = con.execute("SELECT last_insert_rowid()").fetchone()[0]

    # 2. Collector user
    con.execute("""INSERT INTO users(name, contact, password_hash, role, worker_enabled, online_status, created_at)
        VALUES(?, ?, ?, ?, ?, ?, ?)""",
        ("Priya Patel", "priya@wastedash.in", hash_password("wastedash123"), "collector", 1, 1, now_str)
    )
    collector_id = con.execute("SELECT last_insert_rowid()").fetchone()[0]

    # 3. Seed tutorial pass for Rahul
    con.execute("INSERT INTO quiz_results(user_id, score, total, created_at) VALUES(?, ?, ?, ?)",
                (cust_id, 3, 3, now_str))

    # 4. Seed initial bookings: 1 Active Open, 1 Accepted by Priya, 1 Completed
    con.execute("""INSERT INTO bookings(customer_id, collector_id, waste_type, quantity, pickup_date, pickup_slot, address, notes, status, created_at)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (cust_id, None, "Wet waste", "2 segregated bins", today_str, "2:00–4:00 PM",
         "A-402, Green Meadows, Indiranagar, Bangalore", "Doorbell works, bins placed by the main door", "Open", now_str)
    )

    con.execute("""INSERT INTO bookings(customer_id, collector_id, waste_type, quantity, pickup_date, pickup_slot, address, notes, status, created_at)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (cust_id, collector_id, "Dry waste", "3 large cardboard boxes", tomorrow_str, "10:00 AM–12:00 PM",
         "Flat 101, Palm Heights, Koramangala, Bangalore", "Flattened cardboard and plastic bottles rinsed", "Accepted", now_str)
    )

    con.execute("""INSERT INTO bookings(customer_id, collector_id, waste_type, quantity, pickup_date, pickup_slot, address, notes, status, created_at)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (cust_id, collector_id, "Wet waste", "1 bucket", (date.today() - timedelta(days=2)).isoformat(), "8:00–10:00 AM",
         "A-402, Green Meadows, Indiranagar, Bangalore", "Vegetable scraps and coffee grounds", "Completed", now_str)
    )

def get_user_by_contact(contact):
    if not contact:
        return None
    target = contact.strip().lower()
    with get_connection() as con:
        user = con.execute("SELECT * FROM users WHERE LOWER(contact)=?", (target,)).fetchone()
        if not user and "@wastedash.in" in target:
            legacy = target.replace("@wastedash.in", "@ecogo.in")
            user = con.execute("SELECT * FROM users WHERE LOWER(contact)=?", (legacy,)).fetchone()
        elif not user and "@ecogo.in" in target:
            modern = target.replace("@ecogo.in", "@wastedash.in")
            user = con.execute("SELECT * FROM users WHERE LOWER(contact)=?", (modern,)).fetchone()
        return user

def get_user_by_id(uid):
    if not uid:
        return None
    with get_connection() as con:
        return con.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()

def create_user(name, contact, password, role="customer", worker_enabled=0):
    contact = contact.strip().lower()
    now_str = datetime.now().isoformat(timespec="seconds")
    with get_connection() as con:
        cur = con.cursor()
        cur.execute("""INSERT INTO users(name, contact, password_hash, role, worker_enabled, online_status, created_at)
            VALUES(?, ?, ?, ?, ?, 1, ?)""",
            (name.strip(), contact, hash_password(password), role, int(worker_enabled), now_str)
        )
        return cur.lastrowid

def set_user_mode(user_id, worker_enabled):
    with get_connection() as con:
        con.execute("UPDATE users SET worker_enabled=? WHERE id=?", (int(worker_enabled), user_id))

def set_collector_online_status(user_id, online):
    with get_connection() as con:
        con.execute("UPDATE users SET online_status=? WHERE id=?", (int(online), user_id))

def has_completed_quiz(user_id):
    with get_connection() as con:
        row = con.execute("SELECT id FROM quiz_results WHERE user_id=? ORDER BY id DESC LIMIT 1", (user_id,)).fetchone()
        return row is not None

def record_quiz_result(user_id, score, total=3):
    now_str = datetime.now().isoformat(timespec="seconds")
    with get_connection() as con:
        con.execute("INSERT INTO quiz_results(user_id, score, total, created_at) VALUES(?, ?, ?, ?)",
                    (user_id, score, total, now_str))

def create_booking(customer_id, waste_type, quantity, pickup_date, pickup_slot, address, notes=""):
    now_str = datetime.now().isoformat(timespec="seconds")
    with get_connection() as con:
        cur = con.cursor()
        cur.execute("""INSERT INTO bookings(customer_id, waste_type, quantity, pickup_date, pickup_slot, address, notes, status, created_at)
            VALUES(?, ?, ?, ?, ?, ?, ?, 'Open', ?)""",
            (customer_id, waste_type, quantity, str(pickup_date), pickup_slot, address.strip(), notes.strip(), now_str)
        )
        return cur.lastrowid

def get_bookings_for_customer(customer_id):
    with get_connection() as con:
        return con.execute("""SELECT b.*, u.name AS collector_name, u.contact AS collector_contact
            FROM bookings b LEFT JOIN users u ON b.collector_id=u.id
            WHERE b.customer_id=? ORDER BY b.pickup_date DESC, b.id DESC""", (customer_id,)).fetchall()

def get_open_bookings():
    with get_connection() as con:
        return con.execute("""SELECT b.*, u.name AS customer_name, u.contact AS customer_contact
            FROM bookings b JOIN users u ON b.customer_id=u.id
            WHERE b.status='Open' ORDER BY b.pickup_date ASC, b.id ASC""").fetchall()

def get_collector_bookings(collector_id):
    with get_connection() as con:
        return con.execute("""SELECT b.*, c.name AS customer_name, c.contact AS customer_contact
            FROM bookings b JOIN users c ON b.customer_id=c.id
            WHERE b.collector_id=? ORDER BY b.pickup_date DESC, b.id DESC""", (collector_id,)).fetchall()

def accept_booking(booking_id, collector_id):
    """
    Concurrency-safe atomic acceptance:
    Only accepts if the booking is currently 'Open'.
    Returns True if successfully accepted, False if another collector already accepted it.
    """
    now_str = datetime.now().isoformat(timespec="seconds")
    with get_connection() as con:
        cur = con.cursor()
        cur.execute("""UPDATE bookings SET status='Accepted', collector_id=?, updated_at=?
            WHERE id=? AND status='Open'""", (collector_id, now_str, booking_id))
        return cur.rowcount > 0

def update_booking_status(booking_id, new_status):
    now_str = datetime.now().isoformat(timespec="seconds")
    with get_connection() as con:
        con.execute("UPDATE bookings SET status=?, updated_at=? WHERE id=?", (new_status, now_str, booking_id))

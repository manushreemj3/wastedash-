import os
import hashlib
import secrets
from pathlib import Path
from datetime import datetime, date, timedelta
from dotenv import load_dotenv
import pymongo
from bson import ObjectId

# Load environment variables from .env file
load_dotenv()

_client = None
_db = None

def get_client():
    global _client
    if _client is None:
        load_dotenv()
        uri = os.getenv("MONGODB_URI")
        if not uri:
            try:
                import streamlit as st
                uri = st.secrets.get("MONGODB_URI")
            except Exception:
                uri = None

        if not uri:
            raise ValueError(
                "MONGODB_URI is not set. Please add MONGODB_URI to your .env file or Streamlit secrets."
            )

        client_kwargs = {
            "serverSelectionTimeoutMS": 5000,
            "connectTimeoutMS": 5000,
        }

        # Use certifi bundle for robust SSL/TLS verification
        try:
            import certifi
            client_kwargs["tlsCAFile"] = certifi.where()
        except ImportError:
            pass

        _client = pymongo.MongoClient(uri, **client_kwargs)
    return _client

def get_db():
    global _db
    if _db is None:
        client = get_client()
        db_name = os.getenv("MONGODB_DB_NAME", "wastedash")
        try:
            default_db = client.get_default_database()
            _db = default_db if default_db is not None else client[db_name]
        except Exception:
            _db = client[db_name]
    return _db

def check_connection():
    """Verify that MongoDB is accessible."""
    try:
        client = get_client()
        client.admin.command("ping")
        return True, None
    except Exception as e:
        return False, str(e)

def _get_next_sequence_value(sequence_name):
    """Generates sequential integer IDs for backwards compatibility with UI components."""
    db = get_db()
    counter = db.counters.find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=pymongo.ReturnDocument.AFTER
    )
    return counter["seq"]

def _normalize_id(val):
    if val is None:
        return None
    try:
        return int(val)
    except (ValueError, TypeError):
        return str(val)

def _format_doc(doc):
    """Formats a MongoDB document so it behaves identically to a row/dict with an 'id' attribute."""
    if not doc:
        return None
    d = dict(doc)
    if "id" not in d and "_id" in d:
        d["id"] = str(d["_id"])
    return d

def _id_query(val):
    """Builds a query that matches either sequential int ID or MongoDB ObjectId/_id."""
    if val is None:
        return {"_id": None}
    clauses = [{"id": val}]
    try:
        clauses.append({"id": int(val)})
    except (ValueError, TypeError):
        pass
    if isinstance(val, str) and ObjectId.is_valid(val):
        clauses.append({"_id": ObjectId(val)})
    clauses.append({"_id": val})
    return {"$or": clauses}

def _user_field_query(field_name, val):
    clauses = [{field_name: val}]
    try:
        clauses.append({field_name: int(val)})
    except (ValueError, TypeError):
        pass
    return {"$or": clauses}

def _enrich_booking(db, b):
    """Populates customer and collector information for booking objects."""
    b = _format_doc(b)
    if not b:
        return None

    # Populate customer details
    cust_id = b.get("customer_id")
    if cust_id is not None:
        cust = db.users.find_one(_id_query(cust_id))
        if cust:
            b["customer_name"] = cust.get("name", "Resident")
            b["customer_contact"] = cust.get("contact", "")
        else:
            b["customer_name"] = b.get("customer_name", "Resident")
            b["customer_contact"] = b.get("customer_contact", "")
    else:
        b["customer_name"] = b.get("customer_name", "Resident")
        b["customer_contact"] = b.get("customer_contact", "")

    # Populate collector details
    coll_id = b.get("collector_id")
    if coll_id is not None:
        coll = db.users.find_one(_id_query(coll_id))
        if coll:
            b["collector_name"] = coll.get("name", "")
            b["collector_contact"] = coll.get("contact", "")
        else:
            b["collector_name"] = b.get("collector_name", None)
            b["collector_contact"] = b.get("collector_contact", None)
    else:
        b["collector_name"] = None
        b["collector_contact"] = None

    return b

def hash_password(pw, salt=None):
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", pw.encode(), salt.encode(), 100000).hex()
    return f"{salt}${digest}"

def verify_password(pw, saved):
    try:
        salt, digest = saved.split("$", 1)
        matches = secrets.compare_digest(hash_password(pw, salt).split("$", 1)[1], digest)
        if not matches and pw in ("wastedash123", "ecogo123"):
            for alt in ("wastedash123", "ecogo123"):
                if secrets.compare_digest(hash_password(alt, salt).split("$", 1)[1], digest):
                    return True
        return matches
    except Exception:
        return False

def seed_demo_data(database=None):
    db = database if database is not None else get_db()
    now = datetime.now()
    today_str = date.today().isoformat()
    tomorrow_str = (date.today() + timedelta(days=1)).isoformat()
    past_str = (date.today() - timedelta(days=2)).isoformat()
    now_str = now.isoformat(timespec="seconds")

    # 1. Customer user (Rahul Sharma)
    cust_id = 1
    db.users.update_one(
        {"id": cust_id},
        {"$setOnInsert": {
            "id": cust_id,
            "name": "Rahul Sharma",
            "contact": "rahul@wastedash.in",
            "password_hash": hash_password("wastedash123"),
            "role": "customer",
            "worker_enabled": 0,
            "online_status": 1,
            "created_at": now_str
        }},
        upsert=True
    )

    # 2. Collector user (Priya Patel)
    collector_id = 2
    db.users.update_one(
        {"id": collector_id},
        {"$setOnInsert": {
            "id": collector_id,
            "name": "Priya Patel",
            "contact": "priya@wastedash.in",
            "password_hash": hash_password("wastedash123"),
            "role": "collector",
            "worker_enabled": 1,
            "online_status": 1,
            "created_at": now_str
        }},
        upsert=True
    )

    # Maintain sequence counters
    db.counters.update_one(
        {"_id": "users"},
        {"$max": {"seq": 2}},
        upsert=True
    )

    # 3. Seed tutorial pass for Rahul (customer quiz)
    db.quiz_results.update_one(
        {"user_id": cust_id, "quiz_type": "customer"},
        {"$setOnInsert": {
            "id": 1,
            "user_id": cust_id,
            "quiz_type": "customer",
            "score": 3,
            "total": 3,
            "created_at": now_str
        }},
        upsert=True
    )
    # 3b. Seed collector quiz pass for Priya (collector quiz)
    db.quiz_results.update_one(
        {"user_id": collector_id, "quiz_type": "collector"},
        {"$setOnInsert": {
            "id": 2,
            "user_id": collector_id,
            "quiz_type": "collector",
            "score": 3,
            "total": 3,
            "created_at": now_str
        }},
        upsert=True
    )
    db.counters.update_one(
        {"_id": "quiz_results"},
        {"$max": {"seq": 2}},
        upsert=True
    )

    # 4. Seed initial bookings: 1 Active Open, 1 Accepted by Priya, 1 Completed
    b1 = {
        "id": 1,
        "customer_id": cust_id,
        "collector_id": None,
        "waste_type": "Wet waste",
        "quantity": "2 segregated bins",
        "pickup_date": today_str,
        "pickup_slot": "2:00–4:00 PM",
        "address": "A-402, Green Meadows, Indiranagar, Bangalore",
        "notes": "Doorbell works, bins placed by the main door",
        "status": "Open",
        "created_at": now_str,
        "updated_at": None
    }
    b2 = {
        "id": 2,
        "customer_id": cust_id,
        "collector_id": collector_id,
        "waste_type": "Dry waste",
        "quantity": "3 large cardboard boxes",
        "pickup_date": tomorrow_str,
        "pickup_slot": "10:00 AM–12:00 PM",
        "address": "Flat 101, Palm Heights, Koramangala, Bangalore",
        "notes": "Flattened cardboard and plastic bottles rinsed",
        "status": "Accepted",
        "created_at": now_str,
        "updated_at": now_str
    }
    b3 = {
        "id": 3,
        "customer_id": cust_id,
        "collector_id": collector_id,
        "waste_type": "Wet waste",
        "quantity": "1 bucket",
        "pickup_date": past_str,
        "pickup_slot": "8:00–10:00 AM",
        "address": "A-402, Green Meadows, Indiranagar, Bangalore",
        "notes": "Vegetable scraps and coffee grounds",
        "status": "Completed",
        "created_at": now_str,
        "updated_at": now_str
    }

    for b in (b1, b2, b3):
        db.bookings.update_one({"id": b["id"]}, {"$setOnInsert": b}, upsert=True)

    db.counters.update_one(
        {"_id": "bookings"},
        {"$max": {"seq": 3}},
        upsert=True
    )

def init_db():
    """Initializes MongoDB indexes and seeds initial collections if empty."""
    try:
        db = get_db()
        client = get_client()
        client.admin.command("ping")

        # Create indexes
        try:
            db.users.create_index("contact", unique=True)
            db.users.create_index("id", unique=True)
            db.bookings.create_index("id", unique=True)
            db.bookings.create_index("status")
            db.bookings.create_index("customer_id")
            db.bookings.create_index("collector_id")
            db.quiz_results.create_index("user_id")
        except Exception:
            pass

        # Ensure demo accounts and quiz passes exist
        try:
            seed_demo_data(db)
        except Exception:
            pass
        return True
    except Exception as e:
        print(f"[WasteDash DB Warning] MongoDB initialization note: {e}")
        return False

def get_user_by_contact(contact):
    if not contact:
        return None
    target = contact.strip().lower()
    db = get_db()
    user = db.users.find_one({"contact": target})
    if not user and "@wastedash.in" in target:
        legacy = target.replace("@wastedash.in", "@ecogo.in")
        user = db.users.find_one({"contact": legacy})
    elif not user and "@ecogo.in" in target:
        modern = target.replace("@ecogo.in", "@wastedash.in")
        user = db.users.find_one({"contact": modern})
    return _format_doc(user)

def get_user_by_id(uid):
    if uid is None:
        return None
    db = get_db()
    user = db.users.find_one(_id_query(uid))
    return _format_doc(user)

def create_user(name, contact, password, role="customer", worker_enabled=0):
    role = role.strip().lower()
<<<<<<< HEAD

    if role not in ("customer", "collector"):
        raise ValueError("Invalid account role")

    worker_enabled = 1 if role == "collector" else 0

    contact = contact.strip().lower()
    now_str = datetime.now().isoformat(timespec="seconds")

    with get_connection() as con:
        cur = con.cursor()
        cur.execute("""INSERT INTO users(name, contact, password_hash, role, worker_enabled, online_status, created_at)
            VALUES(?, ?, ?, ?, ?, 1, ?)""",
            (name.strip(), contact, hash_password(password), role, worker_enabled, now_str)
        )
        return cur.lastrowid

=======
    if role not in ("customer", "collector"):
        role = "customer"
    worker_enabled = 1 if role == "collector" else int(worker_enabled)
    contact = contact.strip().lower()
    now_str = datetime.now().isoformat(timespec="seconds")
    uid = _get_next_sequence_value("users")

    user_doc = {
        "id": uid,
        "name": name.strip(),
        "contact": contact,
        "password_hash": hash_password(password),
        "role": role,
        "worker_enabled": worker_enabled,
        "online_status": 1,
        "created_at": now_str
    }
    db = get_db()
    db.users.insert_one(user_doc)
    return uid

def set_user_mode(user_id, worker_enabled):
    db = get_db()
    db.users.update_one(_id_query(user_id), {"$set": {"worker_enabled": int(worker_enabled)}})
>>>>>>> 80bdadf (mongodb)

def set_collector_online_status(user_id, online):
    db = get_db()
    db.users.update_one(_id_query(user_id), {"$set": {"online_status": int(online)}})

def has_completed_quiz(user_id, quiz_type=None):
    try:
        db = get_db()
        q = _user_field_query("user_id", user_id)
        conditions = [q, {"score": {"$gte": 2}}]
        if quiz_type:
            conditions.append({
                "$or": [
                    {"quiz_type": quiz_type},
                    {"quiz_type": {"$exists": False}}
                ]
            })
        query = {"$and": conditions}
        row = db.quiz_results.find_one(query)
        return row is not None
    except Exception:
        return False

def record_quiz_result(user_id, score, total=3, quiz_type="customer"):
    now_str = datetime.now().isoformat(timespec="seconds")
    db = get_db()
    qid = _get_next_sequence_value("quiz_results")
    doc = {
        "id": qid,
        "user_id": _normalize_id(user_id),
        "quiz_type": quiz_type,
        "score": int(score),
        "total": int(total),
        "created_at": now_str
    }
    db.quiz_results.insert_one(doc)

def create_booking(customer_id, waste_type, quantity, pickup_date, pickup_slot, address, notes=""):
    now_str = datetime.now().isoformat(timespec="seconds")
    db = get_db()
    bid = _get_next_sequence_value("bookings")
    booking_doc = {
        "id": bid,
        "customer_id": _normalize_id(customer_id),
        "collector_id": None,
        "waste_type": waste_type,
        "quantity": quantity,
        "pickup_date": str(pickup_date),
        "pickup_slot": pickup_slot,
        "address": address.strip(),
        "notes": notes.strip(),
        "status": "Open",
        "created_at": now_str,
        "updated_at": None
    }
    db.bookings.insert_one(booking_doc)
    return bid

def get_bookings_for_customer(customer_id):
    db = get_db()
    cid = _normalize_id(customer_id)
    cursor = db.bookings.find(_user_field_query("customer_id", cid)).sort([("pickup_date", pymongo.DESCENDING), ("id", pymongo.DESCENDING)])
    return [_enrich_booking(db, b) for b in cursor]

def get_open_bookings():
    db = get_db()
    # Auto-release any expired accepted bookings so they immediately reappear
    release_expired_accepted_bookings()
    cursor = db.bookings.find({"status": "Open"}).sort([("pickup_date", pymongo.ASCENDING), ("id", pymongo.ASCENDING)])
    return [_enrich_booking(db, b) for b in cursor]

def get_collector_bookings(collector_id):
    db = get_db()
    cid = _normalize_id(collector_id)
    cursor = db.bookings.find(_user_field_query("collector_id", cid)).sort([("pickup_date", pymongo.DESCENDING), ("id", pymongo.DESCENDING)])
    return [_enrich_booking(db, b) for b in cursor]

def collector_has_active_job(collector_id):
    """Returns True if the collector already has an Accepted or Picked-up job in progress."""
    try:
        db = get_db()
        cid = _normalize_id(collector_id)
        row = db.bookings.find_one({
            "collector_id": cid,
            "status": {"$in": ["Accepted", "Picked up"]}
        })
        return row is not None
    except Exception:
        return False

def release_expired_accepted_bookings():
    """
    Auto-release bookings that were Accepted but NOT marked 'Picked up'
    within 5 minutes. Resets them to Open so another collector can claim them.
    Returns the count of bookings released.
    """
    try:
        db = get_db()
        cutoff = (datetime.now() - timedelta(minutes=5)).isoformat(timespec="seconds")
        res = db.bookings.update_many(
            {
                "status": "Accepted",
                "updated_at": {"$ne": None, "$exists": True, "$lte": cutoff}
            },
            {"$set": {
                "status": "Open",
                "collector_id": None,
                "updated_at": datetime.now().isoformat(timespec="seconds")
            }}
        )
        return res.modified_count
    except Exception:
        return 0

def reject_booking(booking_id, collector_id):
    """
    Allows a collector to reject/release an Accepted booking back to Open
    within the 5-minute acceptance window.
    """
    now_str = datetime.now().isoformat(timespec="seconds")
    db = get_db()
    cid = _normalize_id(collector_id)
    q = _id_query(booking_id)
    if "$or" in q:
        query = {"$and": [q, {"status": "Accepted", "collector_id": cid}]}
    else:
        query = dict(q)
        query["status"] = "Accepted"
        query["collector_id"] = cid

    res = db.bookings.update_one(
        query,
        {"$set": {
            "status": "Open",
            "collector_id": None,
            "updated_at": now_str
        }}
    )
    return res.modified_count > 0

def accept_booking(booking_id, collector_id):
    """
    Concurrency-safe atomic acceptance:
    Only accepts if the booking is currently 'Open'.
    Also stores accepted_at timestamp for the 5-minute auto-release window.
    Returns True if successfully accepted, False if another collector already accepted it.
    """
    now_str = datetime.now().isoformat(timespec="seconds")
    db = get_db()
    q = _id_query(booking_id)
    if "$or" in q:
        query = {"$and": [q, {"status": "Open"}]}
    else:
        query = dict(q)
        query["status"] = "Open"

    res = db.bookings.update_one(
        query,
        {"$set": {
            "status": "Accepted",
            "collector_id": _normalize_id(collector_id),
            "updated_at": now_str
        }}
    )
    return res.modified_count > 0

def update_booking_status(booking_id, new_status):
    now_str = datetime.now().isoformat(timespec="seconds")
    db = get_db()
    db.bookings.update_one(
        _id_query(booking_id),
        {"$set": {
            "status": new_status,
            "updated_at": now_str
        }}
    )

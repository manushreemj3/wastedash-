import sys
from db import (
    check_connection,
    init_db,
    get_user_by_contact,
    verify_password,
    get_open_bookings,
    accept_booking,
    create_booking,
    create_user,
    get_collector_bookings,
    get_db,
)

def run_collector_flow():
    print("1. Checking connection to MongoDB...")
    ok, err = check_connection()
    if not ok:
        print("\n❌ Connection Error: MongoDB Atlas blocked the connection.")
        print(f"Details: {err}\n")
        print("👉 Please add your current IP to MongoDB Atlas Network Access:")
        print("   1. Go to https://cloud.mongodb.com/")
        print("   2. Click 'Network Access' -> 'Add IP Address'")
        print("   3. Add your IP or '0.0.0.0/0' (Allow Access From Anywhere)")
        return False

    print("✅ Successfully connected to MongoDB Atlas!\n")

    print("2. Initializing database schema & demo accounts...")
    init_db()

    collector_email = "priya@wastedash.in"
    collector_pw = "wastedash123"

    print(f"3. Logging in as Collector ({collector_email})...")
    user = get_user_by_contact(collector_email)
    if not user:
        print("Creating collector account...")
        uid = create_user("Priya Patel", collector_email, collector_pw, role="collector", worker_enabled=1)
        user = get_user_by_contact(collector_email)

    if not verify_password(collector_pw, user["password_hash"]):
        print("❌ Authentication failed: password mismatch.")
        return False

    print(f"✅ Logged in successfully!")
    print(f"   - Name: {user['name']}")
    print(f"   - Role: {user['role']}")
    print(f"   - ID: {user['id']}")
    print(f"   - Worker Enabled: {user['worker_enabled']}")

    print("\n4. Adding a new doorstep waste collection request to the database...")
    new_bid = create_booking(
        customer_id=1,
        waste_type="Recyclable E-Waste",
        quantity="1 medium box (cables, old gadgets)",
        pickup_date="2026-11-25",
        pickup_slot="4:00–6:00 PM",
        address="Flat 304, Green Heights, Indiranagar, Bangalore",
        notes="Please call before reaching",
    )
    print(f"✅ Created new booking in MongoDB! Booking ID: #{new_bid}")

    print("\n5. Accepting the job as Collector Priya Patel...")
    accepted = accept_booking(new_bid, user["id"])
    if accepted:
        print(f"✅ Successfully claimed Booking #{new_bid} for Priya Patel!")
    else:
        print(f"⚠️ Booking #{new_bid} could not be accepted.")

    print("\n6. Fetching active collections for Priya Patel from MongoDB:")
    my_jobs = get_collector_bookings(user["id"])
    for job in my_jobs:
        print(f"   • [Job #{job['id']}] {job['waste_type']} - Status: {job['status']} - Customer: {job.get('customer_name', 'N/A')} ({job.get('address', '')})")

    print("\n🎉 Collector login & database write completed successfully!")
    return True

if __name__ == "__main__":
    success = run_collector_flow()
    sys.exit(0 if success else 1)

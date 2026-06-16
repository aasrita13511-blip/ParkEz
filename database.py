import sqlite3
import pandas as pd
from datetime import datetime

DB_NAME = "parkez.db"


def connect():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def create_tables():
    conn = connect()
    cur = conn.cursor()

    # Customers
    cur.execute("""
    CREATE TABLE IF NOT EXISTS customers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT UNIQUE,
        password TEXT
    )
    """)

    # Drivers
    cur.execute("""
    CREATE TABLE IF NOT EXISTS drivers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        status TEXT
    )
    """)

    # Bookings
    cur.execute("""
    CREATE TABLE IF NOT EXISTS bookings(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket TEXT,
        customer TEXT,
        phone TEXT,
        car_model TEXT,
        vehicle_number TEXT,
        arrival_time TEXT,
        driver TEXT,
        status TEXT,
        updated_time TEXT,
        current_lat REAL DEFAULT 17.545,
        current_lon REAL DEFAULT 78.390
    )
    """)

    # Insert demo drivers
    cur.execute("SELECT COUNT(*) FROM drivers")
    if cur.fetchone()[0] == 0:
        drivers = [
            ("Rahul", "9876543210", "Available"),
            ("Arjun", "9876543211", "Available"),
            ("Vikram", "9876543212", "Available")
        ]
        cur.executemany(
            "INSERT INTO drivers(name,phone,status) VALUES(?,?,?)",
            drivers
        )

    conn.commit()
    conn.close()


# ---------------- CUSTOMER ----------------
def register_customer(name, phone, password):
    conn = connect()
    try:
        conn.execute(
            "INSERT INTO customers(name,phone,password) VALUES(?,?,?)",
            (name, phone, password)
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


def customer_login(phone, password):
    conn = connect()
    data = conn.execute(
        "SELECT * FROM customers WHERE phone=? AND password=?",
        (phone, password)
    ).fetchone()
    conn.close()
    return data


# ---------------- DRIVER ----------------
def get_available_driver():
    conn = connect()
    driver = conn.execute("SELECT name FROM drivers LIMIT 1").fetchone()
    conn.close()
    if driver:
        return driver[0]
    return "Driver"


# ---------------- BOOKINGS ----------------
def add_booking(data):
    conn = connect()
    full_data = data + (17.545, 78.390)
    conn.execute(
        """
        INSERT INTO bookings(
            ticket, customer, phone, car_model, vehicle_number,
            arrival_time, driver, status, updated_time, current_lat, current_lon
        )
        VALUES(?,?,?,?,?,?,?,?,?,?,?)
        """,
        full_data
    )
    conn.commit()
    conn.close()


def get_booking(ticket):
    conn = connect()
    booking = conn.execute("SELECT * FROM bookings WHERE ticket=?", (ticket,)).fetchone()
    conn.close()
    return booking


def update_status(ticket, status):
    conn = connect()
    now = datetime.now().strftime("%I:%M %p")
    conn.execute(
        "UPDATE bookings SET status=?, updated_time=? WHERE ticket=?",
        (status, now, ticket)
    )
    conn.commit()
    conn.close()


def update_driver_location(ticket, lat, lon):
    conn = connect()
    conn.execute(
        "UPDATE bookings SET current_lat=?, current_lon=? WHERE ticket=?",
        (lat, lon, ticket)
    )
    conn.commit()
    conn.close()


def get_all_bookings():
    conn = connect()
    data = conn.execute("SELECT * FROM bookings ORDER BY id DESC").fetchall()
    conn.close()
    return data


# ---------------- DASHBOARD ----------------
def total_cars():
    conn = connect()
    total = conn.execute("SELECT COUNT(*) FROM bookings").fetchone()[0]
    conn.close()
    return total


def retrieved_cars():
    conn = connect()
    total = conn.execute("SELECT COUNT(*) FROM bookings WHERE status='Delivered Vehicle'").fetchone()[0]
    conn.close()
    return total


def active_drivers():
    conn = connect()
    drivers = conn.execute("SELECT * FROM drivers").fetchall()
    conn.close()
    return drivers


# ---------------- PANDAS EXTENSIONS ----------------
def get_bookings_df():
    conn = connect()
    query = "SELECT ticket, customer, phone, car_model, vehicle_number, arrival_time, driver, status, updated_time, current_lat, current_lon FROM bookings ORDER BY id DESC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def get_customer_history_df(phone):
    conn = connect()
    query = "SELECT ticket, car_model, vehicle_number, arrival_time, driver, status, updated_time FROM bookings WHERE phone=? ORDER BY id DESC"
    df = pd.read_sql_query(query, conn, params=(phone,))
    conn.close()
    return df

import sqlite3
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
        updated_time TEXT
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
            """
            INSERT INTO drivers(name,phone,status)
            VALUES(?,?,?)
            """,
            drivers
        )

    conn.commit()
    conn.close()


# ---------------- CUSTOMER ----------------

def register_customer(name, phone, password):

    conn = connect()

    try:

        conn.execute(
            """
            INSERT INTO customers(name,phone,password)
            VALUES(?,?,?)
            """,
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
        """
        SELECT *
        FROM customers
        WHERE phone=? AND password=?
        """,
        (phone, password)
    ).fetchone()

    conn.close()

    return data


# ---------------- DRIVER ----------------

def get_available_driver():

    conn = connect()

    driver = conn.execute(
        """
        SELECT name
        FROM drivers
        LIMIT 1
        """
    ).fetchone()

    conn.close()

    if driver:
        return driver[0]

    return "Driver"


# ---------------- BOOKINGS ----------------

def add_booking(data):

    conn = connect()

    conn.execute(
        """
        INSERT INTO bookings(
        ticket,
        customer,
        phone,
        car_model,
        vehicle_number,
        arrival_time,
        driver,
        status,
        updated_time
        )
        VALUES(?,?,?,?,?,?,?,?,?)
        """,
        data
    )

    conn.commit()
    conn.close()


def get_booking(ticket):

    conn = connect()

    booking = conn.execute(
        """
        SELECT *
        FROM bookings
        WHERE ticket=?
        """,
        (ticket,)
    ).fetchone()

    conn.close()

    return booking


def update_status(ticket, status):

    conn = connect()

    now = datetime.now().strftime("%I:%M %p")

    conn.execute(
        """
        UPDATE bookings
        SET status=?,
        updated_time=?
        WHERE ticket=?
        """,
        (
            status,
            now,
            ticket
        )
    )

    conn.commit()
    conn.close()


def get_all_bookings():

    conn = connect()

    data = conn.execute(
        """
        SELECT *
        FROM bookings
        ORDER BY id DESC
        """
    ).fetchall()

    conn.close()

    return data


# ---------------- DASHBOARD ----------------

def total_cars():

    conn = connect()

    total = conn.execute(
        """
        SELECT COUNT(*)
        FROM bookings
        """
    ).fetchone()[0]

    conn.close()

    return total


def retrieved_cars():

    conn = connect()

    total = conn.execute(
        """
        SELECT COUNT(*)
        FROM bookings
        WHERE status='Delivered Vehicle'
        """
    ).fetchone()[0]

    conn.close()

    return total


def active_drivers():

    conn = connect()

    drivers = conn.execute(
        """
        SELECT *
        FROM drivers
        """
    ).fetchall()

    conn.close()

    return drivers
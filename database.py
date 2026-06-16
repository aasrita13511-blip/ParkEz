import sqlite3

DB_NAME = "valet.db"


def connect():
    return sqlite3.connect(DB_NAME)


def create_tables():

    conn = connect()

    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS bookings(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket TEXT,
        customer TEXT,
        phone TEXT,
        car_name TEXT,
        car_number TEXT,
        arrival_time TEXT,
        driver TEXT,
        status TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS drivers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        available TEXT
    )
    """)

    drivers = [
        ("Rahul", "9876543210", "Yes"),
        ("Arjun", "9876543211", "Yes"),
        ("Vikram", "9876543212", "Yes")
    ]

    for driver in drivers:

        cur.execute(
            """
            INSERT OR IGNORE INTO drivers
            (name,phone,available)
            VALUES (?,?,?)
            """,
            driver
        )

    conn.commit()
    conn.close()


def get_driver():

    conn = connect()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT name
        FROM drivers
        LIMIT 1
        """
    )

    data = cur.fetchone()

    conn.close()

    return data[0] if data else "No Driver"


def add_booking(data):

    conn = connect()

    conn.execute(
        """
        INSERT INTO bookings
        (ticket,customer,phone,car_name,
        car_number,arrival_time,driver,status)

        VALUES (?,?,?,?,?,?,?,?)
        """,
        data
    )

    conn.commit()

    conn.close()


def get_booking(ticket):

    conn = connect()

    data = conn.execute(
        """
        SELECT *
        FROM bookings
        WHERE ticket=?
        """,
        (ticket,)
    ).fetchone()

    conn.close()

    return data


def update_status(ticket,status):

    conn = connect()

    conn.execute(
        """
        UPDATE bookings
        SET status=?
        WHERE ticket=?
        """,
        (status,ticket)
    )

    conn.commit()

    conn.close()


def all_bookings():

    conn = connect()

    data = conn.execute(
        """
        SELECT *
        FROM bookings
        """
    ).fetchall()

    conn.close()

    return data


def total_cars():

    conn = connect()

    count = conn.execute(
        """
        SELECT COUNT(*)
        FROM bookings
        """
    ).fetchone()[0]

    conn.close()

    return count


def cars_retrieved():

    conn = connect()

    count = conn.execute(
        """
        SELECT COUNT(*)
        FROM bookings
        WHERE status='Delivered'
        """
    ).fetchone()[0]

    conn.close()

    return count


def active_drivers():

    conn = connect()

    data = conn.execute(
        """
        SELECT name,phone
        FROM drivers
        """
    ).fetchall()

    conn.close()

    return data
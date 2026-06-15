import sqlite3


DB_NAME = "valet.db"



# Connect database
def connect():

    return sqlite3.connect(DB_NAME)




# Create tables
def create_tables():

    conn = connect()

    cur = conn.cursor()



    # Customer bookings table

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

        status TEXT,

        retrieve_time TEXT

    )
    """)



    # Drivers table

    cur.execute("""
    CREATE TABLE IF NOT EXISTS drivers(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT,

        phone TEXT,

        available TEXT

    )
    """)



    # Add default drivers

    drivers = [

        ("Rahul","9876543210","Yes"),

        ("Arjun","9876543211","Yes"),

        ("Vikram","9876543212","Yes")

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







# Add new valet booking

def add_booking(data):


    conn = connect()

    cur = conn.cursor()



    cur.execute(
    """

    INSERT INTO bookings

    (
    ticket,
    customer,
    phone,
    car_name,
    car_number,
    arrival_time,
    driver,
    status,
    retrieve_time
    )


    VALUES (?,?,?,?,?,?,?,?,?)

    """,

    data

    )



    conn.commit()

    conn.close()









# Find available driver

def get_driver():


    conn = connect()

    cur = conn.cursor()



    cur.execute(

    """

    SELECT name

    FROM drivers

    WHERE available='Yes'

    LIMIT 1

    """

    )


    driver = cur.fetchone()


    conn.close()



    if driver:

        return driver[0]


    return "No Driver Available"









# Get booking using ticket

def get_booking(ticket):


    conn = connect()

    cur = conn.cursor()



    cur.execute(

    """

    SELECT *

    FROM bookings

    WHERE ticket=?

    """,

    (ticket,)

    )



    data = cur.fetchone()


    conn.close()


    return data







# Update vehicle status

def update_status(ticket,status):


    conn = connect()

    cur = conn.cursor()



    cur.execute(

    """

    UPDATE bookings

    SET status=?

    WHERE ticket=?

    """,

    (status,ticket)

    )



    conn.commit()

    conn.close()









# Get all bookings

def all_bookings():


    conn = connect()


    cur = conn.cursor()


    cur.execute(

    """

    SELECT *

    FROM bookings

    """

    )


    data = cur.fetchall()



    conn.close()



    return data









# Manager Dashboard Functions



# Total cars handled

def total_cars():


    conn = connect()


    result = conn.execute(

    """

    SELECT COUNT(*)

    FROM bookings

    """

    ).fetchone()



    conn.close()



    return result[0]











# Cars delivered/retrieved

def cars_retrieved():


    conn = connect()



    result = conn.execute(

    """

    SELECT COUNT(*)

    FROM bookings

    WHERE status='Delivered'

    """

    ).fetchone()



    conn.close()



    return result[0]











# Active drivers

def active_drivers():


    conn = connect()



    result = conn.execute(

    """

    SELECT name,phone

    FROM drivers

    WHERE available='Yes'

    """

    ).fetchall()



    conn.close()



    return result











# Average waiting time

def average_wait():


    conn = connect()



    result = conn.execute(

    """

    SELECT AVG(

    (julianday(retrieve_time)

    -

    julianday(arrival_time))

    *24*60

    )


    FROM bookings


    WHERE retrieve_time!=''

    """

    ).fetchone()



    conn.close()



    if result[0]:

        return round(result[0],2)


    return 5
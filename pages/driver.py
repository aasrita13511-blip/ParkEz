def update_status(ticket, status, updated_time):
    # Example SQL modification context:
    cursor.execute(
        "UPDATE bookings SET status = ?, updated_time = ? WHERE ticket_id = ?", 
        (status, updated_time, ticket)
    )
    conn.commit()

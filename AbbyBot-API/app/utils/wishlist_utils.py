from ..utils.db import get_db_connection
import re  # Import the regular expression library
import os  # Import the os library to access environment variables

def add_wishlist(name, email, discord_username, reason=None, how_learned=None):
    # Normalize data before insert
    name = name.capitalize()
    email = email.lower()
    # Clean and validate the Discord username
    discord_username = discord_username.lower().split('#')[0]
    if not re.match("^[a-zA-Z0-9_.]+$", discord_username):
        return "Invalid Discord username. Only letters, numbers, underscores, and dots are allowed."

    reason = reason.capitalize() if reason else "Not Provided"
    how_learned = how_learned.capitalize() if how_learned else "Not Provided"

    # Database connection
    conn = get_db_connection(os.getenv("DB_WISHLIST_NAME"))
    cursor = conn.cursor(dictionary=True)

    # Check if the discord_username already exists in the wishlist
    check_query = """
    SELECT * FROM wishlist WHERE discord_username = %s;
    """
    cursor.execute(check_query, (discord_username,))
    if cursor.fetchone() is not None:
        cursor.close()
        conn.close()
        return "This Discord username has already been added to the wishlist."

    # Insert the new wishlist entry if the discord_username does not exist
    insert_query = """
    INSERT INTO wishlist (name, email, discord_username, reason, how_learned)
    VALUES (%s, %s, %s, %s, %s);
    """
    cursor.execute(insert_query, (name, email, discord_username, reason, how_learned))
    conn.commit()

    cursor.close()
    conn.close()

    return "Wishlist item added successfully."

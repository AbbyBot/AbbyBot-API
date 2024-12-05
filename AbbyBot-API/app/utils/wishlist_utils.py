from ..utils.db import get_db_connection

def add_wishlist(name, email, discord_username, reason, how_learned):
    # Normalize data before insert
    name = name.capitalize()
    email = email.lower()
    discord_username = discord_username.lower()
    reason = reason.capitalize()
    how_learned = how_learned.capitalize()

    # Database connection
    conn = get_db_connection("AbbyBot_Asuka")
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

from ..utils.db import get_db_connection

def add_wishlist(name, email, discord_username, reason, how_learned):
    conn = get_db_connection("AbbyBot_Asuka")
    cursor = conn.cursor(dictionary=True)
    
    query = """
    INSERT INTO wishlist (name, email, discord_username, reason, how_learned)
    VALUES (%s, %s, %s, %s, %s);
    """
    cursor.execute(query, (name, email, discord_username, reason, how_learned))
    conn.commit()  # Make commit to save the changes

    cursor.close()
    conn.close()

    return "Wishlist item added successfully."

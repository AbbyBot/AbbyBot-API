from ..utils.db import get_db_connection

def get_current_theme(user_id):
    conn = get_db_connection("AbbyBot_Rei")
    cursor = conn.cursor()
    
    try:
        query = "SELECT theme_id FROM user_profile WHERE user_id = %s;"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        return result[0] if result else None  
    finally:
        cursor.close()
        conn.close()

def theme_exists(theme_id):
    conn = get_db_connection("AbbyBot_Rei")
    cursor = conn.cursor()
    
    try:
        query = "SELECT 1 FROM AbbyBot_Themes WHERE id = %s;"
        cursor.execute(query, (theme_id,))
        result = cursor.fetchone()
        return result is not None
    finally:
        cursor.close()
        conn.close()

def update_abbybot_theme(user_id, theme_id):
    conn = get_db_connection("AbbyBot_Rei")
    cursor = conn.cursor()

    try:
        current_theme = get_current_theme(user_id)
        if current_theme == theme_id:
            return -1  

        query = """
            UPDATE user_profile 
            SET theme_id = %s 
            WHERE user_id = %s;
        """
        cursor.execute(query, (theme_id, user_id))
        conn.commit()  
        return cursor.rowcount  
    finally:
        cursor.close()
        conn.close()

def get_themes_data():
    conn = get_db_connection("AbbyBot_Rei")  
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT
	    id, title, theme_class from AbbyBot_Themes;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


from ..utils.db import get_db_connection

def get_user_info(user_id):
    conn = get_db_connection("AbbyBot_Rei")  
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT 
            up.user_username AS discord_username, 
            up.user_birthday AS birthday,
            up.user_id, 
            up.account_created_at,  
            COALESCE(p.privilege_name, 'No privilege') AS privilege,
            (SELECT COUNT(DISTINCT guild_id) 
            FROM dashboard 
            WHERE user_profile_id = up.id) AS servers_shared,
            t.id AS theme_id,
            t.title AS theme_name,
            t.theme_class AS theme_class
        FROM user_profile up
        LEFT JOIN privileges p ON up.user_privilege = p.id
        LEFT JOIN AbbyBot_Themes t ON up.theme_id = t.id
        WHERE up.user_id = %s;
    """
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result
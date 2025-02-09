from ..utils.db import get_db_connection
import os

def fetch_privileges_info():
    conn = get_db_connection(os.getenv('DB_DISCORD_NAME'))
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM privileges"
    cursor.execute(query)
    privileges_data = cursor.fetchall()

    cursor.close()
    conn.close()

    if privileges_data:
        privileges_list = []
        for privilege in privileges_data:
            privileges_list.append({
                "id": privilege["id"],
                "privilege_name": privilege["privilege_name"],
                "value": privilege["value"],
                "rol_meaning": privilege["rol_meaning"],
                "how_to_get": privilege["how_to_get"],
                "xp_multiplier": privilege["xp_multiplier"],
                "exclusive_access": privilege["exclusive_access"]
            })
        return {"privileges": privileges_list}
    else:
        return {"error": "No privileges information found"}, 404

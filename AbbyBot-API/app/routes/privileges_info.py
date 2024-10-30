from flask import Blueprint, jsonify, request
from ..utils.db import get_db_connection

privileges_info_bp = Blueprint('privileges_info', __name__)

@privileges_info_bp.route('/privileges-info', methods=['GET'])
def privileges_info():
    conn = get_db_connection("AbbyBot_Rei")
    cursor = conn.cursor(dictionary=True)
    
    # If it is a GET request, it returns the privilege information
    if request.method == 'GET':

        query = "SELECT * FROM privileges"
        cursor.execute(query)
        privileges_data = cursor.fetchall()

        cursor.close()
        conn.close()

        if privileges_data:
            # Transform the result into a more readable format
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

            return jsonify({
                "privileges": privileges_list
            })
        else:
            return jsonify({"error": "No privileges information found"}), 404
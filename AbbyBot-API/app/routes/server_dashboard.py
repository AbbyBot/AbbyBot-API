from flask import Blueprint, request, jsonify
from ..utils.db import get_db_connection

server_dashboard_bp = Blueprint('server_dashboard', __name__)

@server_dashboard_bp.route('/server-dashboard', methods=['GET'])
def get_server_dashboard():
    guild_id = request.args.get('guild_id')
    tab = request.args.get('tab', 1)

    if not guild_id:
        return jsonify({'error': 'Missing required parameter: guild_id'}), 400
    


    conn = get_db_connection("AbbyBot_Rei")
    
    try:
        with conn.cursor() as cursor:
            query = """
                    SELECT 
                        up.user_username AS 'Username',
                        d.user_server_nickname AS 'Nickname in server',
                        CASE 
                            WHEN ss.owner_id = up.user_id THEN 'Owner'
                            WHEN d.is_bot = 1 THEN 'BOT'
                            WHEN d.is_admin = 1 THEN 'Admin'
                            ELSE 'User'
                        END AS 'User type',
                        CAST(up.user_id AS CHAR) AS 'User ID',
                        ur.role_name AS 'Server roles',
                        up.user_birthday AS 'Birthday Date'  
                    FROM 
                        dashboard d
                    JOIN 
                        user_profile up ON d.user_profile_id = up.id
                    LEFT JOIN 
                        user_roles ur ON ur.user_profile_id = up.id AND ur.guild_id = d.guild_id
                    JOIN 
                        server_settings ss ON ss.guild_id = d.guild_id
                    WHERE 
                        d.guild_id = %s
                    ORDER BY 
                        up.user_username, ur.role_name
                    LIMIT 20 OFFSET %s
            """
            tab = int(tab)
            cursor.execute(query, (guild_id, (tab - 1) * 20))
            result = cursor.fetchall()
            
            response_object = []
            dashboard = {}
            for row in result:
                user_id = row[3]
                birthday_date = row[5]
                if birthday_date:
                    birthday_date = birthday_date.strftime('%Y-%m-%d')
                else:
                    birthday_date = None
                
                if user_id not in dashboard:
                    dashboard[user_id] = {
                        'username': row[0],
                        'nickname_in_server': row[1],
                        'user_type': row[2],
                        'user_id': row[3],
                        'server_roles': [],
                        'birthday_date': birthday_date
                    }
                if row[4]:
                    dashboard[user_id]['server_roles'].append(row[4])

            response_object = {
                'users': list(dashboard.values()),
                'total_users': len(dashboard),
                'tab': tab
            }
            return jsonify(response_object), 200
    except:
        return jsonify({'users': [], 'total_users': 0}), 200
    finally:
        conn.close()

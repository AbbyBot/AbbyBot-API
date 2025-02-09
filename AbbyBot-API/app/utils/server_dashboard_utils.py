from ..utils.db import get_db_connection
import os

def fetch_server_dashboard(guild_id, page, limit=10):
    conn = get_db_connection(os.getenv('DB_DISCORD_NAME'))
    
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
            """
            count_query = "SELECT member_count from server_settings WHERE guild_id = %s"
            page = int(page)

            # Fetching user data
            cursor.execute(query, (guild_id,))
            user_data = cursor.fetchall()

            dashboard = {}
            for row in user_data:
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
            users = list(dashboard.values())[(page-1)*limit:page*limit]

            # Fetching total members count
            cursor.execute(count_query, (guild_id,))
            total_members = cursor.fetchone()
            
            response_object = {
                'users': users,
                'total_users': total_members[0],
                'page_users': len(users),
                'page': page
            }
            return response_object
    except:
        return {'users': [], 'total_users': 0}
    finally:
        conn.close()

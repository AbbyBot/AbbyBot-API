from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import requests
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_API_BASE_URL = "https://discord.com/api/v10"
TOKEN = os.getenv('DISCORD_TOKEN')

app = Flask(__name__)

CORS(app)


def get_db_connection(database):
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=database
    )


def get_server_count():
    conn = get_db_connection("AbbyBot_Rei")  
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(DISTINCT guild_id) FROM dashboard;")
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count

def bot_info():
    conn = get_db_connection("AbbyBot_Asuka")
    cursor = conn.cursor(dictionary=True)
    
    # If it is a GET request, it returns the bot information
    if request.method == 'GET':
        query = "SELECT * FROM bot_info LIMIT 1"
        cursor.execute(query)
        bot_info = cursor.fetchone()

        cursor.close()
        conn.close()

        if bot_info:
            # Call server count
            server_count = get_server_count()

            return jsonify({
                "bot_id": bot_info["bot_id"],
                "bot_name": bot_info["bot_name"],
                "discriminator": bot_info["discriminator"],
                "avatar_url": bot_info["avatar_url"],
                "banner_url": bot_info["banner_url"],
                "server_count": server_count,  # get_server_count() value
                "version": bot_info["version"],
                "version_code": bot_info["version_code"],
                "status": bot_info.get("status", "unknown")
            })
        else:
            return jsonify({"error": "No bot information found"}), 404
def bot_info():
    conn = get_db_connection("AbbyBot_Asuka")
    cursor = conn.cursor(dictionary=True)
    
    # If it is a GET request, it returns the bot information
    if request.method == 'GET':
        query = "SELECT * FROM bot_info LIMIT 1"
        cursor.execute(query)
        bot_info = cursor.fetchone()

        cursor.close()
        conn.close()

        if bot_info:
            # Call server count
            server_count = get_server_count()

            return jsonify({
                "bot_id": bot_info["bot_id"],
                "bot_name": bot_info["bot_name"],
                "discriminator": bot_info["discriminator"],
                "avatar_url": bot_info["avatar_url"],
                "banner_url": bot_info["banner_url"],
                "server_count": server_count,  # get_server_count() value
                "version": bot_info["version"],
                "version_code": bot_info["version_code"],
                "status": bot_info.get("status", "unknown")
            })
        else:
            return jsonify({"error": "No bot information found"}), 404
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count


def get_bot_info_from_discord():
    url = f"{DISCORD_API_BASE_URL}/users/@me"
    headers = {
        "Authorization": f"Bot {TOKEN}"
    }


    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        bot_info = response.json()
        bot_data = {
            "bot_id": bot_info["id"],
            "bot_name": bot_info["username"],
            "discriminator": bot_info["discriminator"],
            "avatar_url": f"https://cdn.discordapp.com/avatars/{bot_info['id']}/{bot_info['avatar']}.png",
            "banner_url": f"https://example.com/bot/banner/{bot_info['id']}.png",  
            "server_count": get_server_count(),  
            "version": os.getenv('BOT_VERSION')
        }
        return bot_data
    else:
        print(f"Error fetching bot info: {response.status_code} {response.text}")
        return None


def update_bot_info_in_db(bot_info):
    conn = get_db_connection("AbbyBot_Asuka")  
    cursor = conn.cursor()

    sql = """
    INSERT INTO bot_info (bot_id, bot_name, discriminator, avatar_url, banner_url, version, server_count, last_updated)
    VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
    ON DUPLICATE KEY UPDATE
    bot_name = VALUES(bot_name), discriminator = VALUES(discriminator), avatar_url = VALUES(avatar_url), banner_url = VALUES(banner_url), 
    version = VALUES(version), server_count = VALUES(server_count), last_updated = NOW();
    """
    
    cursor.execute(sql, (
        bot_info['bot_id'], 
        bot_info['bot_name'], 
        bot_info['discriminator'], 
        bot_info['avatar_url'], 
        bot_info['banner_url'], 
        bot_info['version'], 
        bot_info['server_count']
    ))
    conn.commit()
    cursor.close()
    conn.close()

def get_user_server_data(user_id):
    conn = get_db_connection("AbbyBot_Rei")  
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT s.guild_id, s.guild_name, s.owner_id, d.is_admin, s.guild_icon_url, s.guild_icon_last_updated
    FROM dashboard d
    JOIN server_settings s ON d.guild_id = s.guild_id
    JOIN user_profile up ON d.user_profile_id = up.id
    LEFT JOIN privileges p ON up.user_privilege = p.id
    WHERE up.user_id = %s;
    """
    
    cursor.execute(query, (user_id,))
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    if result:
        user_id_int = int(user_id)

        for server in result:
            server['is_owner'] = 1 if server['owner_id'] == user_id_int else 0
            if server['guild_icon_url']:
                server['guild_icon_url']

        return result
    else:
        return None


app = Flask(__name__)

# Variable to store the state of the bot
bot_status = "offline"


@app.route('/bot-info', methods=['GET', 'POST'])
def bot_info():
    conn = get_db_connection("AbbyBot_Asuka")
    cursor = conn.cursor(dictionary=True)
    
    # If it is a GET request, it returns the bot information
    if request.method == 'GET':
        query = "SELECT * FROM bot_info LIMIT 1"
        cursor.execute(query)
        bot_info = cursor.fetchone()

        cursor.close()
        conn.close()

        if bot_info:
            # Call server count
            server_count = get_server_count()

            return jsonify({
                "bot_id": bot_info["bot_id"],
                "bot_name": bot_info["bot_name"],
                "discriminator": bot_info["discriminator"],
                "avatar_url": bot_info["avatar_url"],
                "banner_url": bot_info["banner_url"],
                "server_count": server_count,  # get_server_count() value
                "version": bot_info["version"],
                "version_code": bot_info["version_code"],
                "status": bot_info.get("status", "unknown")
            })
        else:
            return jsonify({"error": "No bot information found"}), 404

    
    # If it is a POST request, update the bot status
    elif request.method == 'POST':
        try:
            # Get the submitted status on the request
            data = request.json
            bot_status = data.get("status")
            
            # Check if the state value is valid
            if bot_status not in ["online", "offline"]:
                return jsonify({"error": "Invalid status value"}), 400

            # First select the bot_id
            cursor.execute("SELECT bot_id FROM bot_info LIMIT 1")
            bot_info = cursor.fetchone()

            if bot_info:
                bot_id = bot_info["bot_id"]
                
                # Then do the update using the bot_id
                update_query = """
                    UPDATE bot_info 
                    SET status = %s 
                    WHERE bot_id = %s
                """
                cursor.execute(update_query, (bot_status, bot_id))
                conn.commit()

                cursor.close()
                conn.close()

                return jsonify({"message": f"Bot status updated to {bot_status}"}), 200
            else:
                return jsonify({"error": "No bot information found"}), 404
        except Exception as e:
            cursor.close()
            conn.close()
            return jsonify({"error": str(e)}), 500






@app.route('/user-servers', methods=['GET'])
def user_servers():
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({"error": "No user_id provided"}), 400

    user_data = get_user_server_data(user_id)
    user_info = get_user_info(user_id)

    if user_data and user_info:
        return jsonify({
            "user_id": user_id,
            "servers": user_data
        })
    else:
        return jsonify({"error": "No data found for this user"}), 404
    


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


@app.route('/user-info', methods=['GET'])
def user_info():

    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({"error": "No user_id provided"}), 400

    user_data = get_user_info(user_id)

    if user_data:

        birthday = user_data["birthday"]
        if birthday:
            birthday = birthday.strftime('%Y-%m-%d')  
        else:
            birthday = None  

        return jsonify({
            "discord_username": user_data["discord_username"],
            "account_created_at": user_data["account_created_at"] or "No data available",
            "user_id": user_data["user_id"],
            "user_birthday": birthday,  
            "servers_shared": user_data["servers_shared"],
            "privilege": user_data["privilege"],
            "theme": {
                "theme_id": user_data["theme_id"],
                "theme_name": user_data["theme_name"],
                "theme_class": user_data["theme_class"]
            }
        })
    else:
        return jsonify({"error": "No data found for this user"}), 404


@app.route('/server-dashboard', methods=['GET'])
def get_server_dashboard():

    guild_id = request.args.get('guild_id')


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
                            WHEN ss.owner_id = up.user_id THEN 'Owner'  -- Prioritize "Owner"
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
                        up.user_username, ur.role_name;
            """
            cursor.execute(query, (guild_id,))
            result = cursor.fetchall()

            
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
                        'nickname in server': row[1],  
                        'user_type': row[2],  
                        'user_id': row[3],  
                        'server_roles': [],
                        'birthday_date': birthday_date  
                    }
                if row[4]:  
                    dashboard[user_id]['server_roles'].append(row[4])

            return jsonify(list(dashboard.values()))

    finally:
        conn.close()


from datetime import datetime


def get_current_birthday(user_id):
    conn = get_db_connection("AbbyBot_Rei")
    cursor = conn.cursor()

    try:
        query = "SELECT user_birthday FROM user_profile WHERE user_id = %s;"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        return result[0] if result else None  
    finally:
        cursor.close()
        conn.close()



def update_user_birthday(user_id, birthday_date):
    conn = get_db_connection("AbbyBot_Rei")
    cursor = conn.cursor()

    try:
        query = """
            UPDATE user_profile 
            SET user_birthday = %s 
            WHERE user_id = %s;
        """
        cursor.execute(query, (birthday_date, user_id))
        conn.commit() 
        return cursor.rowcount  

    finally:
        cursor.close()
        conn.close()



@app.route('/update-birthday', methods=['POST'])
def update_birthday():

    user_id = request.json.get('user_id')
    birthday = request.json.get('birthday_date')


    if not user_id or not birthday:
        return jsonify({"error": "Missing user_id or birthday_date", "status_code": 400}), 400


    try:
        birthday_date = datetime.strptime(birthday, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"error": "Invalid birthday format. Use YYYY-MM-DD.", "status_code": 400}), 400


    today = datetime.today().date()
    if birthday_date > today:
        return jsonify({"error": "Birthday cannot be in the future.", "status_code": 400}), 400
    elif birthday_date.year < 1900:
        return jsonify({"error": "Birthday is too old. Please enter a valid date after 1900.", "status_code": 400}), 400


    current_birthday = get_current_birthday(user_id)

    # Check if the user exists
    if current_birthday is None:
        return jsonify({"error": "No user found with the provided user_id", "status_code": 404}), 404


    if current_birthday == birthday_date:
        return jsonify({"info": "The birthday is already set to this value. No update needed.", "status_code": 200}), 200


    rows_affected = update_user_birthday(user_id, birthday_date)

    if rows_affected > 0:
        return jsonify({"success": f"Birthday updated for user {user_id}", "status_code": 200}), 200
    else:
        return jsonify({"error": "Failed to update the birthday for user {user_id}", "status_code": 500}), 500



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


@app.route('/update-abbybot_theme', methods=['POST'])
def update_theme():
    
    user_id = request.json.get('user_id')
    theme_id = request.json.get('theme_id')

    
    if not user_id or not theme_id:
        return jsonify({"error": "Missing user_id or theme_id", "status_code": 400}), 400

    
    rows_affected = update_abbybot_theme(user_id, theme_id)

    if rows_affected == -1:
        return jsonify({"info": "No update needed, the theme is already set to this value", "status_code": 200}), 200
    elif rows_affected > 0:
        return jsonify({"success": f"AbbyBot_theme updated for user {user_id}", "status_code": 200}), 200
    else:
        return jsonify({"error": "No user found with the provided user_id", "status_code": 404}), 404


def get_current_language(guild_id):
    conn = get_db_connection("AbbyBot_Rei")
    cursor = conn.cursor()
    
    try:
        query = "SELECT guild_language FROM server_settings WHERE guild_id = %s;"
        cursor.execute(query, (guild_id,))
        result = cursor.fetchone()
        return result[0] if result else None 
    finally:
        cursor.close()
        conn.close()



def update_language(guild_id, guild_language):
    conn = get_db_connection("AbbyBot_Rei")
    cursor = conn.cursor()

    try:
        
        current_language = get_current_language(guild_id)
        if current_language == guild_language:
            return -1  


        query = """
            UPDATE server_settings 
            SET guild_language = %s 
            WHERE guild_id = %s;
        """
        cursor.execute(query, (guild_language, guild_id))  
        conn.commit()  
        return cursor.rowcount  

    finally:
        cursor.close()
        conn.close()




@app.route('/update-language', methods=['POST'])
def update_guild_language_route():

    guild_id = request.json.get('guild_id')
    language_id = request.json.get('language_id')
    

    rows_affected = update_language(guild_id, language_id)

    if rows_affected == -1:
        return jsonify({"info": "No update needed, the language is already set", "status_code": 200}), 200
    elif rows_affected > 0:
        return jsonify({"success": f"Language updated for guild {guild_id}", "status_code": 200}), 200
    else:
        return jsonify({"error": "No guild found with the provided guild_id", "status_code": 404}), 404


def get_current_event_value(guild_id):
    conn = get_db_connection("AbbyBot_Rei")
    cursor = conn.cursor()
    
    try:
        query = "SELECT activated_events FROM server_settings WHERE guild_id = %s;"
        cursor.execute(query, (guild_id,))
        result = cursor.fetchone()
        return result[0] if result else None 
    finally:
        cursor.close()
        conn.close()



def toggle_events(guild_id, activated_events):
    conn = get_db_connection("AbbyBot_Rei")
    cursor = conn.cursor()

    try:
        
        current_events = get_current_event_value(guild_id)
        if current_events == activated_events:
            return -1  


        query = """
            UPDATE server_settings 
            SET activated_events = %s 
            WHERE guild_id = %s;
        """
        cursor.execute(query, (activated_events, guild_id))  
        conn.commit()  
        return cursor.rowcount  

    finally:
        cursor.close()
        conn.close()




@app.route('/toggle_automatic_events', methods=['POST'])
def toggle_automatic_event():

    guild_id = request.json.get('guild_id')
    activated_events = request.json.get('activated_events')
    

    if not isinstance(activated_events, int):
        return jsonify({"error": "Invalid value for activated_events. It must be a number (0 or 1).", "status_code": 400}), 400
  
    

    if activated_events not in [0, 1]:
        return jsonify({"error": "Invalid value for activated_events. It must be 0 or 1.", "status_code": 400}), 400


    rows_affected = toggle_birthday(guild_id, activated_events)

    if rows_affected == -1:
        return jsonify({"info": "No update needed, the activated_events value is already set", "status_code": 200}), 200
    elif rows_affected > 0:
        if activated_events == 1:
            return jsonify({"success": f"Activated auto events for guild {guild_id}", "status_code": 200}), 200
        else:
            return jsonify({"success": f"Deactivated auto events for guild {guild_id}", "status_code": 200}), 200
    else:
        return jsonify({"error": "No guild found with the provided guild_id", "status_code": 404}), 404



def toggle_birthday(guild_id, activated_birthday):
    conn = get_db_connection("AbbyBot_Rei")
    cursor = conn.cursor()

    try:
        
        current_events = get_current_toggle_birthday(guild_id)
        if current_events == activated_birthday:
            return -1  


        query = """
            UPDATE server_settings 
            SET activated_birthday = %s 
            WHERE guild_id = %s;
        """
        cursor.execute(query, (activated_birthday, guild_id))  
        conn.commit()  
        return cursor.rowcount  

    finally:
        cursor.close()
        conn.close()

def get_current_toggle_birthday(guild_id):
    conn = get_db_connection("AbbyBot_Rei")
    cursor = conn.cursor()
    
    try:
        query = "SELECT activated_birthday FROM server_settings WHERE guild_id = %s;"
        cursor.execute(query, (guild_id,))
        result = cursor.fetchone()
        return result[0] if result else None 
    finally:
        cursor.close()
        conn.close()



@app.route('/toggle-birthday-event', methods=['POST'])
def toggle_auto_birthday():

    guild_id = request.json.get('guild_id')
    activated_birthday = request.json.get('activated_birthday')
    

    if not isinstance(activated_birthday, int):
        return jsonify({"error": "Invalid value for activated_birthday. It must be a number (0 or 1).", "status_code": 400}), 400
  
    

    if activated_birthday not in [0, 1]:
        return jsonify({"error": "Invalid value for activated_birthday. It must be 0 or 1.", "status_code": 400}), 400


    rows_affected = toggle_birthday(guild_id, activated_birthday)

    if rows_affected == -1:
        return jsonify({"info": "No update needed, the activated_events value is already set", "status_code": 200}), 200
    elif rows_affected > 0:
        if activated_birthday == 1:
            return jsonify({"success": f"Activated birthday for guild {guild_id}", "status_code": 200}), 200
        else:
            return jsonify({"success": f"Deactivated birthday for guild {guild_id}", "status_code": 200}), 200
    else:
        return jsonify({"error": "No guild found with the provided guild_id", "status_code": 404}), 404



def toggle_logs(guild_id, activated_logs):
    conn = get_db_connection("AbbyBot_Rei")
    cursor = conn.cursor()

    try:
        
        current_events_logs = get_current_logs_value(guild_id)
        if current_events_logs == activated_logs:
            return -1 


        query = """
            UPDATE server_settings 
            SET activated_logs = %s 
            WHERE guild_id = %s;
        """
        cursor.execute(query, (activated_logs, guild_id))  
        conn.commit()  
        return cursor.rowcount  

    finally:
        cursor.close()
        conn.close()

def get_current_logs_value(guild_id):
    conn = get_db_connection("AbbyBot_Rei")
    cursor = conn.cursor()
    
    try:
        query = "SELECT activated_logs FROM server_settings WHERE guild_id = %s;"
        cursor.execute(query, (guild_id,))
        result = cursor.fetchone()
        return result[0] if result else None 
    finally:
        cursor.close()
        conn.close()


@app.route('/toggle-logs', methods=['POST'])
def toggle_auto_logs():

    guild_id = request.json.get('guild_id')
    activated_logs = request.json.get('activated_logs')
    

    if not isinstance(activated_logs, int):
        return jsonify({"error": "Invalid value for activated_logs. It must be a number (0 or 1).", "status_code": 400}), 400
  
    

    if activated_logs not in [0, 1]:
        return jsonify({"error": "Invalid value for activated_logs. It must be 0 or 1.", "status_code": 400}), 400


    rows_affected = toggle_logs(guild_id, activated_logs)

    if rows_affected == -1:
        return jsonify({"info": "No update needed, the activated_events value is already set", "status_code": 200}), 200
    elif rows_affected > 0:
        if activated_logs == 1:
            return jsonify({"success": f"Activated logs for guild {guild_id}", "status_code": 200}), 200
        else:
            return jsonify({"success": f"Deactivated logs for guild {guild_id}", "status_code": 200}), 200
    else:
        return jsonify({"error": "No guild found with the provided guild_id", "status_code": 404}), 404
    

def set_prefix(guild_id, prefix):
    conn = get_db_connection("AbbyBot_Rei")
    cursor = conn.cursor()

    try:
        
        current_events_logs = get_current_prefix(guild_id)
        if current_events_logs == prefix:
            return -1 


        query = """
            UPDATE server_settings 
            SET prefix = %s 
            WHERE guild_id = %s;
        """
        cursor.execute(query, (prefix, guild_id))  
        conn.commit()  
        return cursor.rowcount  

    finally:
        cursor.close()
        conn.close()

def get_current_prefix(guild_id):
    conn = get_db_connection("AbbyBot_Rei")
    cursor = conn.cursor()
    
    try:
        query = "SELECT prefix FROM server_settings WHERE guild_id = %s;"
        cursor.execute(query, (guild_id,))
        result = cursor.fetchone()
        return result[0] if result else None 
    finally:
        cursor.close()
        conn.close()

@app.route('/set-prefix', methods=['POST'])
def set_new_prefix():

    guild_id = request.json.get('guild_id')
    prefix = request.json.get('prefix')
    
    rows_affected = set_prefix(guild_id, prefix)

    if rows_affected == -1:
        return jsonify({"info": "No update needed, the prefix value is already set", "status_code": 200}), 200
    elif rows_affected > 0:
        return jsonify({"success": f"Changed prefix for guild {guild_id}", "status_code": 200}), 200
    else:
        return jsonify({"error": "No guild found with the provided guild_id", "status_code": 404}), 404



def set_birthday_channel(guild_id, birthday_channel):
    conn = get_db_connection("AbbyBot_Rei")
    cursor = conn.cursor()

    try:
        
        current_birthday_channel = get_current_birthday_channel(guild_id)
        if current_birthday_channel == birthday_channel:
            return -1 

        query = """
            UPDATE server_settings 
            SET birthday_channel = %s 
            WHERE guild_id = %s;
        """
        cursor.execute(query, (birthday_channel, guild_id))  
        conn.commit()  
        return cursor.rowcount  

    finally:
        cursor.close()
        conn.close()

def get_current_birthday_channel(guild_id):
    conn = get_db_connection("AbbyBot_Rei")
    cursor = conn.cursor()
    
    try:
        query = "SELECT birthday_channel FROM server_settings WHERE guild_id = %s;"
        cursor.execute(query, (guild_id,))
        result = cursor.fetchone()
        return result[0] if result else None 
    finally:
        cursor.close()
        conn.close()


@app.route('/set-birthday_channel', methods=['POST'])
def change_birthday_channel():

    guild_id = request.json.get('guild_id')
    birthday_channel = request.json.get('birthday_channel')

    # Check if birthday_channel is a number
    if not isinstance(birthday_channel, (int, str)) or not str(birthday_channel).isdigit():
        return jsonify({"error": "Invalid value for birthday_channel. It must be a numeric value.", "status_code": 400}), 400

    # Convert birthday_channel to int if it is a numeric string
    birthday_channel = int(birthday_channel)

    rows_affected = set_birthday_channel(guild_id, birthday_channel)

    if rows_affected == -1:
        return jsonify({"info": "No update needed, the birthday_channel value is already set", "status_code": 200}), 200
    elif rows_affected > 0:
        return jsonify({"success": f"Changed birthday_channel for guild {guild_id}", "status_code": 200}), 200
    else:
        return jsonify({"error": "No guild found with the provided guild_id", "status_code": 404}), 404


def set_logs_channel(guild_id, logs_channel):
    conn = get_db_connection("AbbyBot_Rei")
    cursor = conn.cursor()

    try:
        
        current_logs_channel = get_current_logs_channel(guild_id)
        if current_logs_channel == logs_channel:
            return -1 

        query = """
            UPDATE server_settings 
            SET birthday_channel = %s 
            WHERE guild_id = %s;
        """
        cursor.execute(query, (logs_channel, guild_id))  
        conn.commit()  
        return cursor.rowcount  

    finally:
        cursor.close()
        conn.close()

def get_current_logs_channel(guild_id):
    conn = get_db_connection("AbbyBot_Rei")
    cursor = conn.cursor()
    
    try:
        query = "SELECT logs_channel FROM server_settings WHERE guild_id = %s;"
        cursor.execute(query, (guild_id,))
        result = cursor.fetchone()
        return result[0] if result else None 
    finally:
        cursor.close()
        conn.close()


@app.route('/set-logs_channel', methods=['POST'])
def change_logs_channel():

    guild_id = request.json.get('guild_id')
    logs_channel = request.json.get('logs_channel')

    # Check if logs_channel is a number
    if not isinstance(logs_channel, (int, str)) or not str(logs_channel).isdigit():
        return jsonify({"error": "Invalid value for logs_channel. It must be a numeric value.", "status_code": 400}), 400

    # Convert logs_channel to int if it is a numeric string
    birthday_channel = int(logs_channel)

    rows_affected = set_logs_channel(guild_id, logs_channel)

    if rows_affected == -1:
        return jsonify({"info": "No update needed, the logs_channel value is already set", "status_code": 200}), 200
    elif rows_affected > 0:
        return jsonify({"success": f"Changed logs_channel for guild {guild_id}", "status_code": 200}), 200
    else:
        return jsonify({"error": "No guild found with the provided guild_id", "status_code": 404}), 404


@app.route('/privileges-info', methods=['GET'])
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


# Define the path to your image folder
IMAGE_FOLDER = os.path.join(os.getcwd(), 'AbbyBot-News')

# Endpoint to list all photo URLs
@app.route('/photos', methods=['GET'])
def list_photos():
    try:
        # Get a list of all files in the directory
        photos = [f for f in os.listdir(IMAGE_FOLDER) if os.path.isfile(os.path.join(IMAGE_FOLDER, f))]
        
        # Create URLs for each photo
        photo_urls = [
            {
                "file_name": photo,
                "url": f"{request.host_url}photos/{photo}"
            } for photo in photos
        ]

        return jsonify(photo_urls), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to serve a specific photo
@app.route('/photos/<filename>', methods=['GET'])
def get_photo(filename):
    try:
        # Serve the requested file from the directory
        return send_from_directory(IMAGE_FOLDER, filename)
    except Exception as e:
        return jsonify({"error": "File not found or an error occurred"}), 404

# Endpoint to generate URLs for photos
@app.route('/generate-photo-urls', methods=['POST'])
def generate_photo_urls():
    try:
        # Get the list of all files in the directory
        photos = [f for f in os.listdir(IMAGE_FOLDER) if os.path.isfile(os.path.join(IMAGE_FOLDER, f))]

        # Create URLs for each photo
        photo_urls = [
            {
                "file_name": photo,
                "url": f"{request.host_url}photos/{photo}"
            } for photo in photos
        ]

        return jsonify({
            "generated_urls": photo_urls
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5002)
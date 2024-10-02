from flask import Flask, jsonify, request
import requests
import mysql.connector
import os
from dotenv import load_dotenv
from flask import send_from_directory
from flask_cors import CORS

# Load environment variables from the .env file
load_dotenv()

DISCORD_API_BASE_URL = "https://discord.com/api/v10"
TOKEN = os.getenv('DISCORD_TOKEN')

# Load the image folder path from the .env file
IMAGE_FOLDER = os.getenv('IMAGE_FOLDER_PATH')
BASE_URL = "http://localhost:5002"  # Change this to the real domain when deployed

app = Flask(__name__)

CORS(app)

# Function to connect to the database
def get_db_connection(database):
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=database
    )

# Helper function to ensure proper URL construction
def construct_url(filename):
    """
    Concatenate BASE_URL and the path, ensuring there is no double slash.
    """
    return f"{BASE_URL.rstrip('/')}/images/{filename}"

# Function to get the number of servers from the "AbbyBot_Rei" database
def get_server_count():
    conn = get_db_connection("AbbyBot_Rei")  # "AbbyBot_Rei" database
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(DISTINCT guild_id) FROM dashboard WHERE is_active = 1;")
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count

# Function to get bot info from Discord API
def get_bot_info_from_discord():
    url = f"{DISCORD_API_BASE_URL}/users/@me"
    headers = {
        "Authorization": f"Bot {TOKEN}"
    }

    # Make the request to the Discord API
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        bot_info = response.json()
        bot_data = {
            "bot_id": bot_info["id"],
            "bot_name": bot_info["username"],
            "discriminator": bot_info["discriminator"],
            "avatar_url": f"https://cdn.discordapp.com/avatars/{bot_info['id']}/{bot_info['avatar']}.png",
            "banner_url": f"https://example.com/bot/banner/{bot_info['id']}.png",  # Personal banner URL
            "server_count": get_server_count(),  # Get from local database
            "version": os.getenv('BOT_VERSION')
        }
        return bot_data
    else:
        print(f"Error fetching bot info: {response.status_code} {response.text}")
        return None

# Function to insert or update bot info in the "AbbyBot_Asuka" database
def update_bot_info_in_db(bot_info):
    conn = get_db_connection("AbbyBot_Asuka")  # "AbbyBot_Asuka" database
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

# Function to get user server data from the "AbbyBot_Rei" database
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
                server['guild_icon_url'] = construct_url(server['guild_icon_url'])

        return result
    else:
        return None



# Endpoint to serve images from the absolute path defined in the .env file
@app.route('/images/<path:filename>')
def serve_image(filename):
    # Construct the full path of the image
    full_image_path = os.path.join(IMAGE_FOLDER, filename)
    print(f"Looking for the file in: {full_image_path}")
    
    return send_from_directory(IMAGE_FOLDER, filename)

# Endpoint to retrieve bot information
@app.route('/bot-info', methods=['GET'])
def bot_info():
    conn = get_db_connection("AbbyBot_Asuka")
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM bot_info LIMIT 1"
    cursor.execute(query)
    bot_info = cursor.fetchone()

    cursor.close()
    conn.close()

    if bot_info:
        return jsonify({
            "bot_id": bot_info["bot_id"],
            "bot_name": bot_info["bot_name"],
            "discriminator": bot_info["discriminator"],
            "avatar_url": bot_info["avatar_url"],
            "banner_url": bot_info["banner_url"],
            "server_count": bot_info["server_count"],
            "version": bot_info["version"]
        })
    else:
        return jsonify({"error": "No bot information found"}), 404

# Endpoint to retrieve user server data
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
            "privilege_name": user_info["privilege"],
            "servers": user_data
        })
    else:
        return jsonify({"error": "No data found for this user"}), 404
    

# Function to get user profile info from "AbbyBot_Rei"
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
            t.title AS abbybot_theme
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

# Endpoint to retrieve user profile information
@app.route('/user-info', methods=['GET'])
def user_info():

    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({"error": "No user_id provided"}), 400

    user_data = get_user_info(user_id)

    if user_data:
        # Handle birthday formatting to 'YYYY-MM-DD' or null if not available
        birthday = user_data["birthday"]
        if birthday:
            birthday = birthday.strftime('%Y-%m-%d')  # Format to 'YYYY-MM-DD'
        else:
            birthday = None  # Set as None if not defined

        return jsonify({
            "discord_username": user_data["discord_username"],
            "account_created_at": user_data["account_created_at"] or "No data available",
            "user_id": user_data["user_id"],
            "user_birthday": birthday,  # Formatted birthday
            "servers_shared": user_data["servers_shared"],
            "abbybot_theme": user_data["abbybot_theme"],
        })
    else:
        return jsonify({"error": "No data found for this user"}), 404

# Get all dashboard for a server ()
@app.route('/server-dashboard', methods=['GET'])
def get_server_dashboard():
    # Get guild_id from query parameters
    guild_id = request.args.get('guild_id')

    # Check if guild_id is provided
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

            # Creating a structure to group roles for each user
            dashboard = {}
            for row in result:
                user_id = row[3]  # Index 3 is 'User ID'

                # Handle Birthday Date formatting to 'YYYY-MM-DD' or set it as None
                birthday_date = row[5]  # Index 5 is 'Birthday Date'
                if birthday_date:
                    birthday_date = birthday_date.strftime('%Y-%m-%d')  # Format to 'YYYY-MM-DD'
                else:
                    birthday_date = None  # Set as None if not defined
                
                if user_id not in dashboard:
                    dashboard[user_id] = {
                        'username': row[0],  # Index 0 is 'Username'
                        'nickname in server': row[1],  # Index 1 is 'Nickname in server'
                        'user_type': row[2],  # Index 2 is 'User type'
                        'user_id': row[3],  # Index 3 is 'User ID'
                        'server_roles': [],
                        'birthday_date': birthday_date  # Formatted 'Birthday Date'
                    }
                if row[4]:  # Index 4 is 'server_roles'
                    dashboard[user_id]['server_roles'].append(row[4])

            return jsonify(list(dashboard.values()))

    finally:
        conn.close()


from datetime import datetime

# Function to get the current birthday of a user
def get_current_birthday(user_id):
    conn = get_db_connection("AbbyBot_Rei")
    cursor = conn.cursor()

    try:
        query = "SELECT user_birthday FROM user_profile WHERE user_id = %s;"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        return result[0] if result else None  # Return the current birthday if exists
    finally:
        cursor.close()
        conn.close()


# Function to update the birthday of a user in "AbbyBot_Rei"
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
        conn.commit()  # Commit the transaction
        return cursor.rowcount  # Return number of affected rows

    finally:
        cursor.close()
        conn.close()


# Endpoint to update the user's birthday
@app.route('/update-birthday', methods=['POST'])
def update_birthday():
    # Get data from the request
    user_id = request.json.get('user_id')
    birthday = request.json.get('birthday_date')

    # Validate that both user_id and birthday are provided
    if not user_id or not birthday:
        return jsonify({"error": "Missing user_id or birthday_date", "status_code": 400}), 400

    # Validate the birthday format (YYYY-MM-DD)
    try:
        birthday_date = datetime.strptime(birthday, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"error": "Invalid birthday format. Use YYYY-MM-DD.", "status_code": 400}), 400

    # Validate that the birthday is not in the future or too old (e.g., before 1900)
    today = datetime.today().date()
    if birthday_date > today:
        return jsonify({"error": "Birthday cannot be in the future.", "status_code": 400}), 400
    elif birthday_date.year < 1900:
        return jsonify({"error": "Birthday is too old. Please enter a valid date after 1900.", "status_code": 400}), 400

    # Get the current birthday of the user from the database
    current_birthday = get_current_birthday(user_id)

    # Check if the user exists
    if current_birthday is None:
        return jsonify({"error": "No user found with the provided user_id", "status_code": 404}), 404

    # Check if the new birthday is the same as the current one
    if current_birthday == birthday_date:
        return jsonify({"info": "The birthday is already set to this value. No update needed.", "status_code": 200}), 200

    # Update the user's birthday in the database
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
        return result[0] if result else None  # Return the current theme_id if exists
    finally:
        cursor.close()
        conn.close()



# Function to update the birthday of a user in "AbbyBot_Rei"
def update_abbybot_theme(user_id, theme_id):
    conn = get_db_connection("AbbyBot_Rei")
    cursor = conn.cursor()

    try:
        # Check if the user already has this theme_id
        current_theme = get_current_theme(user_id)
        if current_theme == theme_id:
            return -1  # Indicating that no update is needed (same theme)

        # Proceed with the update
        query = """
            UPDATE user_profile 
            SET theme_id = %s 
            WHERE user_id = %s;
        """
        cursor.execute(query, (theme_id, user_id))
        conn.commit()  # Commit the transaction
        return cursor.rowcount  # Return number of affected rows

    finally:
        cursor.close()
        conn.close()

# Endpoint to update the user's AbbyBot_Theme (dashboard skin)
@app.route('/update-abbybot_theme', methods=['POST'])
def update_theme():
    # Get data from the request
    user_id = request.json.get('user_id')
    theme_id = request.json.get('theme_id')

    # Validate that both user_id and theme_id are provided
    if not user_id or not theme_id:
        return jsonify({"error": "Missing user_id or theme_id", "status_code": 400}), 400

    # Update the user's abbybot_theme in the database
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
        # Asegúrate de que estás consultando la tabla correcta
        query = "SELECT guild_language FROM server_settings WHERE guild_id = %s;"
        cursor.execute(query, (guild_id,))
        result = cursor.fetchone()
        return result[0] if result else None 
    finally:
        cursor.close()
        conn.close()


# Function to update the language of a guild in "AbbyBot_Rei"
def update_language(guild_id, guild_language):
    conn = get_db_connection("AbbyBot_Rei")
    cursor = conn.cursor()

    try:
        # Check if the guild already has this language
        current_language = get_current_language(guild_id)
        if current_language == guild_language:
            return -1  # Indicating that no update is needed (same language)

        # Proceed with the update
        query = """
            UPDATE server_settings 
            SET guild_language = %s 
            WHERE guild_id = %s;
        """
        cursor.execute(query, (guild_language, guild_id))  # Note the correct parameter order
        conn.commit()  # Commit the transaction
        return cursor.rowcount  # Return number of affected rows

    finally:
        cursor.close()
        conn.close()



# Endpoint to update AbbyBot language in a server 
@app.route('/update-language', methods=['POST'])
def update_guild_language_route():
    # Get data from the request
    guild_id = request.json.get('guild_id')
    language_id = request.json.get('language_id')
    
    # Update guild_language
    rows_affected = update_language(guild_id, language_id)

    if rows_affected == -1:
        return jsonify({"info": "No update needed, the language is already set", "status_code": 200}), 200
    elif rows_affected > 0:
        return jsonify({"success": f"Language updated for guild {guild_id}", "status_code": 200}), 200
    else:
        return jsonify({"error": "No guild found with the provided guild_id", "status_code": 404}), 404




if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5002)

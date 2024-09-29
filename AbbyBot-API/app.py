from flask import Flask, jsonify, request
import requests
import mysql.connector
import os
from dotenv import load_dotenv
from flask import send_from_directory

# Load variables from dotenv file
load_dotenv()

DISCORD_API_BASE_URL = "https://discord.com/api/v10"
TOKEN = os.getenv('DISCORD_TOKEN')

# Load the image folder path from the .env file
IMAGE_FOLDER = os.getenv('IMAGE_FOLDER_PATH')
BASE_URL = "http://localhost:5002"  # Change this to the real domain when deployed

app = Flask(__name__)

# Function to connect to the databases
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
    # The URL should be constructed using BASE_URL and the subdirectory where the images are.
    return f"{BASE_URL.rstrip('/')}/images/{filename}"

# Get the number of servers from the "AbbyBot_Rei" database
def get_server_count():
    conn = get_db_connection("AbbyBot_Rei")  # "AbbyBot_Rei" database
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(DISTINCT guild_id) FROM dashboard WHERE is_active = 1;")
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count

# Function to get real bot info from Discord API
def get_bot_info_from_discord():
    url = f"{DISCORD_API_BASE_URL}/users/@me"
    headers = {
        "Authorization": f"Bot {TOKEN}"
    }

    # Make the request to the Discord API
    response = requests.get(url, headers=headers)

    # Check if the response was successful
    if response.status_code == 200:
        bot_info = response.json()

        # Create the bot info dictionary
        bot_data = {
            "bot_id": bot_info["id"],
            "bot_name": bot_info["username"],
            "discriminator": bot_info["discriminator"],
            "avatar_url": f"https://cdn.discordapp.com/avatars/{bot_info['id']}/{bot_info['avatar']}.png",
            "banner_url": f"https://example.com/bot/banner/{bot_info['id']}.png",  # Personal banner URL (you can modify this)
            "server_count": get_server_count(),  # Get from local database
            "version": os.getenv('BOT_VERSION')
        }
        return bot_data
    else:
        print(f"Error fetching bot info: {response.status_code} {response.text}")
        return None

# Insert or update data in bot_info in the "AbbyBot_Asuka" database
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

# Function to get user server data from AbbyBot
def get_user_server_data(user_id):
    conn = get_db_connection("AbbyBot_Rei")  
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT s.guild_id, s.guild_name, s.owner_id, d.is_admin, s.guild_icon_url, s.guild_icon_last_updated, p.privilege_name
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
            # Construct the full URL for the server icon using the file name
            if server['guild_icon_url']:
                server['guild_icon_url'] = construct_url(server['guild_icon_url'])

        return result
    else:
        return None


# Endpoint to serve images from the absolute path defined in the .env file
@app.route('/images/<path:filename>')
def serve_image(filename):
    # Verify the full path from where the images are served, without adding guild_images again
    full_image_path = os.path.join(IMAGE_FOLDER, filename)
    print(f"Looking for the file in: {full_image_path}")
    
    # Use send_from_directory to serve the file from the correct directory
    return send_from_directory(IMAGE_FOLDER, filename)



# Main route to get the bot information
@app.route('/bot-info', methods=['GET'])
def bot_info():
    conn = get_db_connection("AbbyBot_Asuka")
    cursor = conn.cursor(dictionary=True)

    # Query to get the bot information from the bot_info table
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

# Endpoint to retrieve servers and privileges for a user
@app.route('/user-servers', methods=['GET'])
def user_servers():

    # Get user_id from request
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({"error": "No user_id provided"}), 400

    # Get user data
    user_data = get_user_server_data(user_id)

    if user_data:
        return jsonify({
            "user_id": user_id,
            "servers": user_data
        })
    else:
        return jsonify({"error": "No data found for this user"}), 404


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5002)

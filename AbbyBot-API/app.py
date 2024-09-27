from flask import Flask, jsonify
import requests
import mysql.connector
import os
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

DISCORD_API_BASE_URL = "https://discord.com/api/v10"
TOKEN = os.getenv('DISCORD_TOKEN')

app = Flask(__name__)

# Function to connect to the databases
def get_db_connection(database):
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=database
    )

# Get the number of servers from the "abbybot" database
def get_server_count():
    conn = get_db_connection("abbybot")  # "abbybot" database
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

# Insert or update data in bot_info in the "abbybot_wishlist" database
def update_bot_info_in_db(bot_info):
    conn = get_db_connection("abbybot_wishlist")  # "wishlist" database
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

# Main route to get the bot information
@app.route('/bot-info', methods=['GET'])
def bot_info():
    # Get the bot information from the Discord API
    discord_info = get_bot_info_from_discord()

    if discord_info:
        # Update or insert the information in the "wishlist" database
        update_bot_info_in_db(discord_info)
        
        return jsonify({
            "bot_id": discord_info["bot_id"],
            "bot_name": discord_info["bot_name"],
            "discriminator": discord_info["discriminator"],
            "avatar_url": discord_info["avatar_url"],
            "banner_url": discord_info["banner_url"],
            "server_count": discord_info["server_count"],
            "version": discord_info["version"],
            "status": "online"
        })
    else:
        return jsonify({"error": "Could not retrieve bot information"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

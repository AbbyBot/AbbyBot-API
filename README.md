
# AbbyBot API

This API is part of the AbbyBot project and serves data related to Discord bot servers, users, and bot information.

## Requirements

- Python 3.x
- Flask
- MySQL connector
- dotenv
- requests

Make sure you have all the necessary packages installed by running:
```
pip install -r requirements.txt
```

## Environment Variables

To configure the API, you need a `.env` file with the following variables:

```
DISCORD_TOKEN=your_discord_token
DB_HOST=your_database_host
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DISCORD_API_BASE_URL=https://discord.com/api/v10
IMAGE_FOLDER_PATH=path_to_your_image_folder
BOT_VERSION=your_bot_version
```

## Running the API

1. Clone the repository and navigate to the folder.
2. Set up your `.env` file with the appropriate values.
3. Run the Flask application:
```
python app.py
```

The API will be available at `http://127.0.0.1:5002/`.

## Endpoints

### 1. Get Bot Information

**URL:** `/bot-info`  
**Method:** `GET`

Returns information about the bot, including its ID, name, discriminator, avatar, server count, and version.

#### Example Response:
```json
{
  "bot_id": "123456789",
  "bot_name": "AbbyBot",
  "discriminator": "1234",
  "avatar_url": "https://cdn.discordapp.com/avatars/123456789/avatar.png",
  "banner_url": "https://example.com/bot/banner/123456789.png",
  "server_count": 12,
  "version": "1.0.0"
}
```

### 2. Get User Servers

**URL:** `/user-servers`  
**Method:** `GET`  
**Parameters:**
- `user_id`: Discord user ID (required)

Returns the list of servers a user belongs to, their privileges, and whether they are an owner.

#### Example Response:
```json
{
  "user_id": "987654321",
  "privilege_name": "Admin",
  "servers": [
    {
      "guild_id": "123456789",
      "guild_name": "Test Server",
      "owner_id": "987654321",
      "is_admin": 1,
      "guild_icon_url": "http://localhost:5002/images/server_icon.png",
      "is_owner": 1
    }
  ]
}
```

### 3. Get User Info

**URL:** `/user-info`  
**Method:** `GET`  
**Parameters:**
- `user_id`: Discord user ID (required)

Returns information about the user's profile, including their Discord username, account creation date, birthday, shared servers, and AbbyBot theme.

#### Example Response:
```json
{
  "discord_username": "User123",
  "account_created_at": "2020-01-01",
  "user_id": "987654321",
  "user_birthday": "No data available",
  "servers_shared": 3,
  "abbybot_theme": "Dark Theme"
}
```

### 4. Serve Images

**URL:** `/images/<filename>`  
**Method:** `GET`

Serves images stored in the folder specified by the `IMAGE_FOLDER_PATH` environment variable. Images are accessed by their filename.

## Notes

- Ensure your image paths are correctly set up in the database. The `IMAGE_FOLDER_PATH` should contain the images referenced in the API.
- The bot information is periodically updated in the local database, but real-time data is fetched from the Discord API.

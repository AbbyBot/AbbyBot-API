
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
  "account_created_at": "Sat, 14 Jul 2018 23:00:44 GMT",
  "user_id": "987654321",
  "user_birthday": "1986-08-12",
  "servers_shared": 3,
  "abbybot_theme": "Dark Theme"
}
```

### 4. Serve Images

**URL:** `/images/<filename>`  
**Method:** `GET`

Serves images stored in the folder specified by the `IMAGE_FOLDER_PATH` environment variable. Images are accessed by their filename.

### 5. Get Server Dashboard

**URL:** `/server-dashboard`  
**Method:** `GET`  
**Parameters:**
- `guild_id`: Discord Server ID (required)

Returns the list of all users (dashboard) on a server where AbbyBot is, bringing data such as their nicknames, user types (user, admin, owner), their user IDs, birthdays and server roles..

#### Example Response:
```json
[
  {
    "Username": "katsuragimisato",
    "Nickname in server": "Misato Katsuragi",
    "User type": "Owner",
    "User ID": "123456789012345678",
    "Server roles": [
      "rizz",
      "gyatt"
    ],
    "Birthday Date": "1986-08-12"
  },
  {
    "Username": "reiayanami",
    "Nickname in server": "Rei Ayanami",
    "User type": "Admin",
    "User ID": "876543210987654321",
    "Server roles": [
      "fortnite-player"
    ],
    "Birthday Date": null
  },
  {
    "Username": "asukalangleyshyru",
    "Nickname in server": "Asuka Langley Sohryu",
    "User type": "User",
    "User ID": "367397873597284352",
    "Server roles": [
      "abbybot_dev"
    ],
    "Birthday Date": "2001-12-04"
  }
]

```

### 6. Update Birthday

**URL:** `/update-birthday`  
**Method:** `POST`  
**Parameters:**
- `user_id`: The ID of the user whose birthday needs to be updated (required).
- `birthday_date`: The new birthday date in `YYYY-MM-DD` format (required).

Updates the birthday of a user in the AbbyBot dashboard. If the user exists, their birthday is updated to the new provided date.

#### Example Request:
```json
{
  "user_id": "123456789012345678",
  "birthday_date": "1992-05-14"
}

```

#### Example Response:
```json
{
  "success": "Birthday updated for user 123456789012345678"
}

```


### 7. Update AbbyBot Theme

**URL:** `/update-abbybot_theme`  
**Method:** `POST`  
**Parameters:**
- `user_id`: The ID of the user whose birthday needs to be updated (required).
- `theme_id`: The new theme ID to be applied (required).

Updates the birthday of a user in the AbbyBot dashboard. If the user exists, their birthday is updated to the new provided date.

#### Example Request:
```json
{
  "user_id": "123456789012345678",
  "theme_id": 2
}

```

#### Example Response (Theme Updated):
```json
{
  "success": "AbbyBot_theme updated for user 123456789012345678"
}


```
#### Example Response (No Update Needed):
```json
{
  "info": "No update needed, the theme is already set to this value"
}


```
#### Example Response (No User Found):
```json
{
  "info": "No user found with the provided user_id"
}


```

## Notes

- Ensure your image paths are correctly set up in the database. The `IMAGE_FOLDER_PATH` should contain the images referenced in the API.
- The bot information is periodically updated in the local database, but real-time data is fetched from the Discord API.

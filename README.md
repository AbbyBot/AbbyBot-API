![AbbyBot-Api](https://github.com/user-attachments/assets/d17a12fc-bb64-4b7c-88dc-529505f1a5c6)


- This API is part of the AbbyBot project and serves data related to Discord bot servers, users, and bot information.

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-v8.0-orange?logo=mysql&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-v2.1-black?logo=flask&logoColor=white)
![Dotenv](https://img.shields.io/badge/Dotenv-Config-green?logo=dotenv&logoColor=white)



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
  "servers": [
      {
      "activated_birthday": 1,
      "activated_events": 1,
      "activated_logs": 0,
      "birthday_channel": 1234567890123456789,
      "default_bot_role_id": null,
      "default_role_id": null,
      "guild_icon_last_updated": "Thu, 24 Oct 2024 21:33:53 GMT",
      "guild_icon_url": "https://image-sample.com",
      "guild_id": 9876543210123456789,
      "guild_language": 1,
      "guild_name": "Sever",
      "is_admin": 1,
      "is_owner": 0,
      "join_channel_id": null,
      "kick_channel_id": null,
      "ban_channel_id": null,
      "logs_channel": null,
      "owner_id": 1234567890123456789
    },
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
    "account_created_at": "Tue, 05 Jun 2017 15:34:20 GMT",
    "discord_username": "unit01shinji",
    "privilege": "Normal User 🐱",
    "servers_shared": 3,
    "theme": {
        "theme_class": "abby-theme",
        "theme_id": 1,
        "theme_name": "Abby"
    },
    "user_birthday": "2001-11-22",
    "user_id": 573829101284550144
}
```

### 4. Get Server Dashboard

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

### 5. Update Birthday

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
  "success": "Birthday updated for user 123456789012345678",
  "status_code": 200
}

```

#### Example Response (Same birthday_date as database):
```json
{
  "info": "The birthday is already set to this value. No update needed.",
  "status_code": 200
}

```

#### Example Response (If any field is missing):
```json
{
  "error": "Missing user_id or birthday_date",
  "status_code": 400
}

```
#### Example Response (If the date format is incorrect):
```json
{
  "error": "Invalid birthday format. Use YYYY-MM-DD.",
  "status_code": 400
}

```

#### Example Response (If the date is in the future or too old):
```json
{
  "error": "Birthday cannot be in the future.",
  "status_code": 400
}

```

or

```json
{
  "error": "Birthday is too old. Please enter a valid date after 1900.",
  "status_code": 400
}

```

#### Example Response (If the user is not found):
```json
{
  "error": "No user found with the provided user_id",
  "status_code": 404
}

```


### 6. Update AbbyBot Theme

**URL:** `/update-abbybot_theme`  
**Method:** `POST`  
**Parameters:**
- `user_id`: The ID of the user whose AbbyBot theme needs to be updated (required).
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
  "success": "AbbyBot_theme updated for user 123456789012345678",
  "status_code": 200
}


```
#### Example Response (No Update Needed):
```json
{
  "info": "No update needed, the theme is already set to this value",
  "status_code": 200
}


```
#### Example Response (No User Found):
```json
{
  "info": "No user found with the provided user_id",
  "status_code": 404
}


```

### 7. Update AbbyBot Language

**URL:** `/update-language`  
**Method:** `POST`  
**Parameters:**
- `guild_id`: The ID of the guild who the language needs to be updated (required).
- `language_id`: The new language ID to be applied (required).

Updates the language of a guild in the AbbyBot dashboard. If the guild exists, their language is updated to the new provided date.

#### Example Request:
```json
{
  "guild_id": "123456789012345678",
  "language_id": 2
}

```

#### Example Response (Language Updated):
```json
{
  "success": "Language updated for guild 123456789012345678",
  "status_code": 200
}


```
#### Example Response (No Update Needed):
```json
{
  "info": "No update needed, the language is already set",
  "status_code": 200
}


```
#### Example Response (No Guild Found):
```json
{
  "info": "No guild found with the provided guild_id",
  "status_code": 404
}


```

### 8. Update AbbyBot Auto events

**URL:** `/toggle_automatic_events`  
**Method:** `POST`  
**Parameters:**
- `guild_id`: The ID of the guild who the language needs to be updated (required).
- `activated_events`: The value to enable/disable AbbyBot automatic events, 1 = activated, 0 = deactivated (required).

Update the automatic event trigger for a guild in AbbyBot. If the guild exists, its events are updated to the new value provided.

#### Example Request:
```json
{
  "guild_id": "123456789012345678",
  "activated_events": 1
}

```

#### Example Response (Activated events):
```json
{
  "success": "Activated auto events for guild 123456789012345678",
  "status_code": 200
}


```

#### Example Response (Deactivated events):
```json
{
  "success": "Deactivated auto events for guild 123456789012345678",
  "status_code": 200
}


```

#### Example Response (Value is greater than one or less than zero):
```json
{
  "error": "Invalid value for activated_events. It must be 0 or 1.",
  "status_code": 400
}


```

#### Example Response (activated_events is not a number):
```json
{
  "error": "Invalid value for activated_events. It must be a number (0 or 1).",
  "status_code": 400
}


```

#### Example Response (No Update Needed):
```json
{
  "info": "No update needed, the activated_events value is already set",
  "status_code": 200
}


```
#### Example Response (No Guild Found):
```json
{
  "info": "No guild found with the provided guild_id",
  "status_code": 404
}


```


### 9. Update AbbyBot Birthday events

**URL:** `/toggle-birthday-event`  
**Method:** `POST`  
**Parameters:**
- `guild_id`: The ID of the guild who the language needs to be updated (required).
- `activated_birthday`: The value to enable/disable AbbyBot birthday events, 1 = activated, 0 = deactivated (required).

Update the birthday event trigger for a guild in AbbyBot. If the guild exists, its birthday  events are updated to activated/deactivated.

#### Example Request:
```json
{
  "guild_id": "123456789012345678",
  "activated_birthday": 1
}

```

#### Example Response (Activated birthday):
```json
{
  "success": "Activated auto events for guild 123456789012345678",
  "status_code": 200
}


```

#### Example Response (Deactivated birthday):
```json
{
  "success": "Deactivated auto events for guild 123456789012345678",
  "status_code": 200
}


```

#### Example Response (Value is greater than one or less than zero):
```json
{
  "error": "Invalid value for activated_birthday. It must be 0 or 1.",
  "status_code": 400
}


```

#### Example Response (activated_birthday is not a number):
```json
{
  "error": "Invalid value for activated_birthday. It must be a number (0 or 1).",
  "status_code": 400
}


```

#### Example Response (No Update Needed):
```json
{
  "info": "No update needed, the activated_birthday value is already set",
  "status_code": 200
}


```
#### Example Response (No Guild Found):
```json
{
  "info": "No guild found with the provided guild_id",
  "status_code": 404
}


```

### 10. Update AbbyBot Logs events

**URL:** `/toggle-logs`  
**Method:** `POST`  
**Parameters:**
- `guild_id`: The ID of the guild who the language needs to be updated (required).
- `activated_logs`: The value to enable/disable AbbyBot logs events, 1 = activated, 0 = deactivated (required).

Update the logs event trigger for a guild in AbbyBot. If the guild exists, its logs  events are updated to activated/deactivated.

#### Example Request:
```json
{
  "guild_id": "123456789012345678",
  "activated_logs": 1
}

```

#### Example Response (Activated Logs):
```json
{
  "success": "Activated auto events for guild 123456789012345678",
  "status_code": 200
}


```

#### Example Response (Deactivated Logs):
```json
{
  "success": "Deactivated auto events for guild 123456789012345678",
  "status_code": 200
}


```

#### Example Response (Value is greater than one or less than zero):
```json
{
  "error": "Invalid value for activated_logs. It must be 0 or 1.",
  "status_code": 400
}


```

#### Example Response (activated_logs is not a number):
```json
{
  "error": "Invalid value for activated_logs. It must be a number (0 or 1).",
  "status_code": 400
}


```

#### Example Response (No Update Needed):
```json
{
  "info": "No update needed, the activated_logs value is already set",
  "status_code": 200
}


```
#### Example Response (No Guild Found):
```json
{
  "info": "No guild found with the provided guild_id",
  "status_code": 404
}


```


### 11. Change AbbyBot prefix

**URL:** `/set-prefix`  
**Method:** `POST`  
**Parameters:**
- `guild_id`: The ID of the guild who the language needs to be updated (required).
- `prefix`: The prefix for AbbyBot in a guild, ex: abbybot_ (required).

Updates the prefix only in the specified guild.

#### Example Request:
```json
{
  "guild_id": "123456789012345678",
  "prefix": "abbybot_"
}

```

#### Example Response (Updated prefix):
```json
{
  "success": "Changed prefix for guild 123456789012345678",
  "status_code": 200
}


```


#### Example Response (No Update Needed):
```json
{
  "info": "No update needed, the prefix value is already set",
  "status_code": 200
}


```
#### Example Response (No Guild Found):
```json
{
  "info": "No guild found with the provided guild_id",
  "status_code": 404
}


```


### 12. Set AbbyBot birthday channel

**URL:** `/set-birthday_channel`  
**Method:** `POST`  
**Parameters:**
- `guild_id`: The ID of the guild who the language needs to be updated (required).
- `birthday_channel`: The ID for the channel where AbbyBot greet users in their birthdays (required).

Updates the prefix only in the specified guild.

#### Example Request:
```json
{
  "guild_id": "123456789012345678",
  "birthday_channel": 123456789012345678
}

```

#### Example Request (if birthday_channel is not a number):
```json
{
  "error": "Invalid value for birthday_channel. It must be a numeric value.",
  "status_code": 400
}

```

#### Example Response (Updated birthday_channel):
```json
{
  "success": "Changed birthday_channel for guild 123456789012345678",
  "status_code": 200
}


```


#### Example Response (No Update Needed):
```json
{
  "info": "No update needed, the birthday_channel value is already set",
  "status_code": 200
}


```
#### Example Response (No Guild Found):
```json
{
  "info": "No guild found with the provided guild_id",
  "status_code": 404
}


```

### 13. Set AbbyBot logs channel

**URL:** `/set-logs_channel`  
**Method:** `POST`  
**Parameters:**
- `guild_id`: The ID of the guild who the language needs to be updated (required).
- `logs_channel`: The ID for the channel where AbbyBot greet users in their birthdays (required).

Updates the logs_channel only in the specified guild.

#### Example Request:
```json
{
  "guild_id": "123456789012345678",
  "logs_channel": 123456789012345678
}

```

#### Example Request (if logs_channel is not a number):
```json
{
  "error": "Invalid value for logs_channel. It must be a numeric value.",
  "status_code": 400
}

```

#### Example Response (Updated logs_channel):
```json
{
  "success": "Changed logs_channel for guild 123456789012345678",
  "status_code": 200
}


```


#### Example Response (No Update Needed):
```json
{
  "info": "No update needed, the logs_channel value is already set",
  "status_code": 200
}


```
#### Example Response (No Guild Found):
```json
{
  "info": "No guild found with the provided guild_id",
  "status_code": 404
}


```

**URL:** `/privileges-info`  
**Method:** `GET`

Returns information about AbbyBot's privileges. Explaining its meaning, how to get it, XP multiplier and exclusive advantages.

#### Example Response:
```json
privileges:
  {
    "exclusive_access": "TBA",
    "id	": 1,
    "privilege_name":"Normal User 🐱",
    "rol_meaning": "Users who have just joined the server. No specific advantages but they earn 1.0 XP.",
    "xp_multiplier": "1.00",

  }
```

### 14. Get AbbyBot Themes

**URL:** `/abbybot-themes`  
**Method:** `GET`

Returns information about all AbbyBot themes registered, with their ID, title and class themes.

#### Example Response:
```json
{
    "abbybot_themes": [
        {
            "theme_class": "abby-theme",
            "theme_id": 1,
            "theme_title": "Abby"
        },
        {
            "theme_class": "d0z3r-theme",
            "theme_id": 2,
            "theme_title": "D0Z3R"
        },
        {
            "theme_class": "masky-theme",
            "theme_id": 3,
            "theme_title": "Masky"
        },
        {
            "theme_class": "nebulanight-theme",
            "theme_id": 4,
            "theme_title": "Nebula Night"
        },
        {
            "theme_class": "lightone-theme",
            "theme_id": 5,
            "theme_title": "Light 01"
        },
        {
            "theme_class": "mia-theme",
            "theme_id": 6,
            "theme_title": "MIA"
        },
        {
            "theme_class": "python-theme",
            "theme_id": 7,
            "theme_title": "Python"
        },
        {
            "theme_class": "node-theme",
            "theme_id": 8,
            "theme_title": "Node"
        }
    ]
}
```

### 15. Get Server Channels

**URL:** `/server-channels`  
**Method:** `GET`  
**Parameters:**
- `guild_id`: Discord Server ID (required)

Returns the list of channels in a server, including their IDs and titles.

#### Example Response:
```json
[
  {
    "channel_id": 1234567898232352134,
    "channel_title": "misato-house",
    "guild_id": 999999999999999999,
    "id": 54
  },
  {
    "channel_id": 12343458982323234134,
    "channel_title": "rei-party",
    "guild_id": 999999999999999999,
    "id": 55
  },
]
```



### 16. Update AbbyBot JOIN card channel

**URL:** `/update-join-channel`  
**Method:** `POST`  
**Parameters:**
- `guild_id`: The Guild ID (required).
- `join_channel_id`: The ID for show kick card (required).

Updates the prefix only in the specified guild.

#### Example Request:
```json
{
  "guild_id": "123456789012345678",
  "join_channel_id": 123456789012345678
}

```

#### Example Response (Updated join_channel_id):
```json
{
  "success": "Changed join_channel_id for guild 123456789012345678",
  "status_code": 200
}


```


#### Example Response (No Update Needed):
```json
{
  "info": "No update needed, the join_channel_id value is already set",
  "status_code": 200
}


```
#### Example Response (No Guild Found):
```json
{
  "info": "No guild found with the provided guild_id",
  "status_code": 404
}


```

### 16. Update AbbyBot KICK card channel

**URL:** `/update-kick-channel`  
**Method:** `POST`  
**Parameters:**
- `guild_id`: The Guild ID (required).
- `kick_channel_id`: The ID for show kick card (required).

Updates the prefix only in the specified guild.

#### Example Request:
```json
{
  "guild_id": "123456789012345678",
  "kick_channel_id": 123456789012345678
}

```

#### Example Response (Updated kick_channel_id):
```json
{
  "success": "Changed kick_channel_id for guild 123456789012345678",
  "status_code": 200
}


```


#### Example Response (No Update Needed):
```json
{
  "info": "No update needed, the kick_channel_id value is already set",
  "status_code": 200
}


```
#### Example Response (No Guild Found):
```json
{
  "info": "No guild found with the provided guild_id",
  "status_code": 404
}


```


### 17. Update AbbyBot BAN card channel

**URL:** `/update-ban-channel`  
**Method:** `POST`  
**Parameters:**
- `guild_id`: The Guild ID (required).
- `ban_channel_id`: The ID for show ban card (required).

Updates the prefix only in the specified guild.

#### Example Request:
```json
{
  "guild_id": "123456789012345678",
  "ban_channel_id": 123456789012345678
}

```

#### Example Response (Updated ban_channel_id):
```json
{
  "success": "Changed ban_channel_id for guild 123456789012345678",
  "status_code": 200
}


```


#### Example Response (No Update Needed):
```json
{
  "info": "No update needed, the ban_channel_id value is already set",
  "status_code": 200
}


```
#### Example Response (No Guild Found):
```json
{
  "info": "No guild found with the provided guild_id",
  "status_code": 404
}


```


### 18. Add Wishlist User

**URL:** `/add-wishlist`  
**Method:** `POST`  
**Parameters:**
- `name`: The name of the user (required).
- `email`: The email of the user (required).
- `discord_username`: The Discord username of the user (required).
- `reason`: The reason for adding to the wishlist (optional field).
- `how_learned`: How the user learned about the wishlist (optional field).

Adds a new user to the wishlist if the Discord username does not already exist.

#### Example Request:
```json
{
  "name": "John Smith",
  "email": "john.smith@example.com",
  "discord_username": "john_smith", // 
  "reason": "Interested in the project",
  "how_learned": "Through a friend"
}
```

> Note: If you use the old format (user#9999) or the new one (user), the system will auto-validate the form anyway!

#### Example Response (User Added):
```json
{
  "success": "User added to the wishlist",
  "status_code": 200
}
```

#### Example Response (User Already Exists):
```json
{
  "error": "User with this Discord username already exists",
  "status_code": 400
}
```


### 19. Get News List

**URL:** `/news`  
**Method:** `GET`

Returns a list of news articles, including their ID, title, description, content, image URL, category, creation date, and slug.

#### Example Response:
```json
{
  "news": [
    {
      "id": 1,
      "title": "New Feature Release",
      "description": "We have released a new feature...",
      "content": "Detailed content of the news article...",
      "image_url": "https://example.com/news/image1.png",
      "category": "Release",
      "created_at": "2023-10-01T12:00:00Z",
      "slug": "new-feature-release"
    },
    {
      "id": 2,
      "title": "Maintenance Update",
      "description": "Scheduled maintenance on...",
      "content": "Detailed content of the maintenance update...",
      "image_url": "https://example.com/news/image2.png",
      "category": "Maintenance",
      "created_at": "2023-10-05T08:00:00Z",
      "slug": "maintenance-update"
    }
  ]
}
```

### 20. Get News by Slug

**URL:** `/news/<slug>`  
**Method:** `GET`  
**Parameters:**
- `slug`: The slug of the news article (required)

Returns a single news article based on the provided slug, including its ID, title, description, content, image URL, category, creation date, and slug.

#### Example Response:
```json
{
  "id": 1,
  "title": "New Feature Release",
  "description": "We have released a new feature...",
  "content": "Detailed content of the news article...",
  "image_url": "https://example.com/news/image1.png",
  "category": "Release",
  "created_at": "2023-10-01T12:00:00Z",
  "slug": "new-feature-release"
}
```

## Notes

- The bot information is periodically updated in the local database, but real-time data is fetched from the Discord API.

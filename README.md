
# AbbyBot-API

AbbyBot-API is a Flask-based API that provides information about AbbyBot, including server details and user privileges, by interacting with Discord's API and local databases.

## Requirements

To run the API, make sure you have the following installed:
- Python 3.x
- Flask
- Requests library
- MySQL Connector
- dotenv

## Environment Variables

The following environment variables should be defined in a `.env` file in the root of your project:

```env
DB_HOST=<Your MySQL database host>
DB_USER=<Your MySQL database username>
DB_PASSWORD=<Your MySQL database password>
DB_NAME_MAIN=<Database name for abbybot>
DB_NAME_WISHLIST=<Database name for abbybot_wishlist>
DISCORD_TOKEN=<Your Discord Bot Token>
BOT_VERSION=<Current version of AbbyBot>
```

### Example `.env` File:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=password123
DB_NAME_MAIN=abbybot
DB_NAME_WISHLIST=abbybot_wishlist
DISCORD_TOKEN=your_discord_bot_token
BOT_VERSION=1.0.0
```

## Endpoints

### 1. **Get Bot Information**
- **Endpoint:** `/bot-info`
- **Method:** `GET`
- **Description:** Retrieves bot information, including the bot's ID, name, avatar, server count, and version, from both Discord API and the local database.

#### Example Response:
```json
{
    "bot_id": "123456789012345678",
    "bot_name": "AbbyBot",
    "discriminator": "1234",
    "avatar_url": "https://cdn.discordapp.com/avatars/123456789012345678/avatar.png",
    "banner_url": "https://example.com/bot/banner/123456789012345678.png",
    "server_count": 100,
    "version": "1.0.0",
    "status": "online"
}
```

### 2. **Get User Server Data**
- **Endpoint:** `/user-servers`
- **Method:** `GET`
- **Description:** Retrieves server and privilege data for a given user.
- **Parameters:** 
  - `user_id` (required) – The ID of the Discord user.
  
#### Example Request:
```bash
curl "http://localhost:5000/user-servers?user_id=123456789012345678"
```

#### Example Response:
```json
{
    "user_id": "123456789012345678",
    "servers": [
        {
            "guild_id": "987654321098765432",
            "guild_name": "Example Server",
            "owner_id": "123456789012345678",
            "is_admin": 1,
            "privilege_name": "Admin",
            "is_owner": 1
        },
        {
            "guild_id": "876543210987654321",
            "guild_name": "Another Server",
            "owner_id": "123456789012345678",
            "is_admin": 0,
            "privilege_name": "Member",
            "is_owner": 0
        }
    ]
}
```

## How to Run

1. Clone the repository.
2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

3. Set up the `.env` file with your environment variables (see **Environment Variables** section).
4. Run the Flask app:

```bash
python app.py
```

5. The API will be available at `http://localhost:5000`.

## Database Structure

### `dashboard` Table (abbybot database)
- `guild_id` (BIGINT)
- `user_id` (BIGINT)
- `is_admin` (TINYINT)
- `user_privilege` (INT)
- `is_active` (TINYINT)

### `bot_info` Table (abbybot_wishlist database)
- `bot_id` (BIGINT)
- `bot_name` (VARCHAR)
- `discriminator` (VARCHAR)
- `avatar_url` (TEXT)
- `banner_url` (TEXT)
- `version` (VARCHAR)
- `server_count` (INT)
- `last_updated` (TIMESTAMP)


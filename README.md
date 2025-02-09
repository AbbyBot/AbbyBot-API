![AbbyBot-Api](https://github.com/user-attachments/assets/d17a12fc-bb64-4b7c-88dc-529505f1a5c6)


This API is an integral component of the AbbyBot project, providing comprehensive data services related to Discord bot servers, users, and bot-specific information.

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.10.0+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/MySQL-v8.0-3776AB?style=flat-square&logo=mysql&logoColor=white" alt="MySQL">
  <img src="https://img.shields.io/badge/Flask-v2.1-3776AB?style=flat-square&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/Docker-dockerfile-3776AB?style=flat-square&logo=docker&logoColor=white" alt="Docker">
</div>



## Requirements
- ![Python](https://img.shields.io/badge/Python-3.10.0+-3776AB?style=flat-square&logo=python&logoColor=white) Python 3.10.0 or later
- ![Flask](https://img.shields.io/badge/Flask-2.1-3776AB?style=flat-square&logo=flask&logoColor=white) Flask
- ![MySQL](https://img.shields.io/badge/MySQL-8.0-3776AB?style=flat-square&logo=mysql&logoColor=white) MySQL connector
- ![dotenv](https://img.shields.io/badge/dotenv-5.0-3776AB?style=flat-square&logo=dotenv&logoColor=white) dotenv
- ![requests](https://img.shields.io/badge/requests-2.26.0-3776AB?style=flat-square&logo=python&logoColor=white) requests

Make sure you have all the necessary packages installed by running:
```
pip install -r requirements.txt
```

## Environment Variables

To configure the API, you need a `.env` file with the following variables:

```
DB_HOST=example.com
DB_USER=example_user
DB_PASSWORD=example_password
BOT_VERSION=1.0.0
DB_DISCORD_NAME=example_discord_db
DB_API_NAME=example_api_db
DB_WISHLIST_NAME=example_wishlist_db
```
>Note: The system is designed for the database user (DB_USER) to use only one host (DB_HOST) and must have the necessary read and write permissions for all databases (DB_DISCORD_NAME, DB_API_NAME, DB_WISHLIST_NAME). Therefore, everything should be unified.

## Running the API

1. Clone the repository and navigate to the folder.
2. Set up your `.env` file with the appropriate values.
3. Run the Flask application:
```
python main.py
```

> The API will be available at `http://127.0.0.1:5002/`.

<div align="center">

  ## Endpoints list

  <a href="https://api.abbybotproject.com/docs">
    <img src="https://img.shields.io/badge/View%20Endpoints-API%20Docs-3776AB?style=flat-square&logo=read-the-docs&logoColor=white" alt="View Endpoints">
  </a>
</div>




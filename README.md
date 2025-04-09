![AbbyBot-Api](https://github.com/user-attachments/assets/d17a12fc-bb64-4b7c-88dc-529505f1a5c6)


This API is an integral component of the AbbyBot project, providing comprehensive data services related to Discord bot servers, users, and bot-specific information.

## Requirements file

```
requirements.txt
```


Make sure you have all the necessary packages installed by running:

```
pip install -r requirements.txt
```

## Environment Variables

The environment variables required for the API are now included in the `.env.example` file. You can use this file as a template to create your own `.env` file.

```bash
# Copy the example file to create your .env file
cp .env.example .env
```

Make sure to update the values in the `.env` file with 
your specific configuration.

1. Clone the repository and navigate to the folder.
2. Set up your `.env` file with the appropriate values.

## Running the API (Development)

3. Run the Flask application (development mode):
```
python main.py
```

> The API will be available at `http://127.0.0.1:5002/`.

<div align="center">

  ## Endpoints list

  <a href="https://api.abbybotproject.com/docs">
    <img src="https://img.shields.io/badge/View%20Endpoints-API%20Docs-4caf50?style=flat-square&logo=read-the-docs&logoColor=white" alt="View Endpoints">
  </a>
</div>

## Running the API (Production)
For greater ease, this API can be deployed using Docker along with Docker Compose.

This Docker setup is specifically designed for production, not for development. It will expose a port on the server, specifically **5002**.

As mentioned, this is for production, so the first step would be to clone the repository on your server in a folder appropriate for the HTTP server you are using, such as Apache or Nginx.

Steps to build and run the container:

1. Make sure you have completed the previous step of creating the `.env` file based on `.env.example` and filling it with your actual variables.

2. Execute the following command:

```
sudo docker compose build
```

3. The blue whale 🐳 will start building the API container, copying all the files, including the `.env`. For this reason, the `.env` file must be created before starting the Docker build process.

4. If everything went well, the terminal will display messages like the following:

```
[+] Building 1/1
 ✔ web  Built       
```

If you see "built," it indicates that the build was successful.

5. To start the Docker container, simply run:

```
sudo docker compose up -d
```

> Note: We add the `-d` flag to run the container in the background on your server.

6. If everything went well, the terminal will return to showing your username as usual. The next step will be to set up a reverse proxy using your HTTP server, such as Apache or Nginx.

## Reverse Proxy Setup

To set up a reverse proxy for port **5002**, you can use either Apache or Nginx. Below are examples for both:

### Apache
1. Enable the required modules:
  ```bash
  sudo a2enmod proxy proxy_http
  sudo systemctl restart apache2 #or httpd
  ```
2. Add the following to your Apache configuration file:
  ```apache
  <VirtualHost *:80>
     ServerName yourdomain.com
     ProxyPass / http://127.0.0.1:5002/
     ProxyPassReverse / http://127.0.0.1:5002/
  </VirtualHost>
  ```
3. Restart Apache:
  ```bash
  sudo systemctl restart apache2 #or httpd
  ```

### Nginx
1. Add the following to your Nginx configuration file:
  ```nginx
  server {
     listen 80;
     server_name yourdomain.com;

     location / {
        proxy_pass http://127.0.0.1:5002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
     }
  }
  ```
2. Test and reload Nginx:
  ```bash
  sudo nginx -t
  sudo systemctl reload nginx
  ```

Replace `yourdomain.com` with your actual domain name.


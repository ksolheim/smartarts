<p align="center">
  <img src="https://github.com/user-attachments/assets/36e0a6f7-fdda-4e07-adc2-00e0436f2f01" />
</p>


# :art: SmartArts

SmartArts is a web application designed to showcase artwork and manage a raffle system for selecting winners. The application is built using Flask and provides both public and admin interfaces.

## :sparkles: Features

- **Public Interface**: Displays the latest artwork winner and a list of recent winners.
- **Admin Interface**: Allows administrators to manage artworks and record winners.
- **Responsive Design**: Utilizes Bootstrap for a responsive and modern UI.
- **Data Management**: Uses SQLite for storing artworks and winners.

## :whale: Run with Docker Compose

1. Create a `docker-compose.yml` file:

   ```yaml
   version: '3.8'

   services:
      smartarts:
         image: ghcr.io/ksolheim/smartarts:latest
         container_name: smartarts-container
         ports:
            - "5000:5000"
         volumes:
            - smartarts_db:/app/database
         env_file:
            - .env
         restart: unless-stopped

   volumes:
      smartarts_db:
         name: smartarts_db
   ```

2. Run the container:

      ```bash
      docker compose up
      ```

3. Put a reverse proxy in front of it, for example nginx.

## :construction: Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ksolheim/smartarts.git
   cd smartarts
   ```

2. **Build the Docker image**:

   ```bash
   docker build -t smartarts .
   ```

4. **Run the Docker container**:
   ```bash
   docker run -d \
   -p 5000:5000 \
   -v smartarts_db:/app/database \
   --env-file .env \
   --name smartarts-container \
   smartarts
   ```

## :file_folder:File Structure

- **app.py**: Main application file containing route definitions and logic.
- **static/**: Contains static files like CSS, JavaScript, and images.
- **templates/**: HTML templates for rendering the public and admin interfaces.
- **database/**: Contains the SQLite database and schema.

## :page_facing_up: License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

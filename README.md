# SmartArts

SmartArts is a web application designed to showcase artwork and manage a raffle system for selecting winners. The application is built using Flask and provides both public and admin interfaces.

## Features

- **Public Interface**: Displays the latest artwork winner and a list of recent winners.
- **Admin Interface**: Allows administrators to manage artworks and record winners.
- **Responsive Design**: Utilizes Bootstrap for a responsive and modern UI.
- **Data Management**: Uses SQLite for storing artworks and winners.

## Installation with Docker

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ksolheim/smartarts.git
   cd smartarts
   ```

2. **Build the Docker image**:
   Ensure you have Docker installed, then run:
   ```bash
   docker build -t smartarts .
   ```

3. **Run the Docker container**:
   Ensure you have a .env file with the following variables:
   ```bash
   BASIC_AUTH_USERNAME=your_username
   BASIC_AUTH_PASSWORD=your_password
   ```
    Start the application using Docker:
    ```bash
    docker run -d -p 5000:5000 --name smartarts-container \
    --env-file .env \
    smartarts
    ```

4. **Access the application**:
   Open your web browser and go to `http://localhost:5000` to view the application.

## File Structure

- **app.py**: Main application file containing route definitions and logic.
- **static/**: Contains static files like CSS, JavaScript, and images.
- **templates/**: HTML templates for rendering the public and admin interfaces.
- **database/**: Contains the SQLite database and schema.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

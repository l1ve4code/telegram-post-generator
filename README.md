# telegram-post-generator

## About

- **Purpose**: Automatically generate and post motivational content to a Telegram channel.
- **Key Features**:
  - Generates motivational quotes, facts, tips, and calls to action using AI.
  - Posts content with images to a Telegram channel.
  - Schedules posts every 3 hours.
  - Handles errors and reconnects automatically.

### Technologies

* Language: **Python**
* Libraries: **Telethon, Requests, Schedule, Asyncio**
* Deployment: **Docker, Docker Compose**
* API: **Telegram API, Hugging Face API (or DeepSeek API)**

## Installing

### Clone the Project

```shell
git clone https://github.com/l1ve4code/telegram-post-generator.git
```

### Replace Placeholders in `docker-compose.yml`

```yaml
services:
  telegram-autoposter:
    build: .
    container_name: telegram-autoposter
    network_mode: host
    environment:
      - THEME=YOUR_THEME
      - LINK=YOUR_LINK
      - API_KEY=YOUR_API_KEY
      - API_ID=YOUR_API_ID
      - API_HASH=YOUR_API_HASH
      - CHANNEL_ID=YOUR_CHANNEL_ID
    restart: unless-stopped
```

## Running the Project

### Using Docker Compose

1. Build and start the container:

```shell
docker-compose up --build
```

2. Stop the container:

```shell
docker-compose down
```

### Running Locally

1. Install dependencies:

```shell
pip install -r requirements.txt
```

2. Run the script:

```shell
python main.py
```

## How It Works

1. **Content Generation**:
   - The script uses an AI API (Hugging Face or DeepSeek) to generate motivational quotes, facts, tips, and calls to action.
   - The generated content is formatted into a post with Markdown and emojis.

2. **Posting to Telegram**:
   - The script sends the generated post along with an image to the specified Telegram channel using the `Telethon` library.
   - It handles errors such as network interruptions and reconnects automatically.

3. **Scheduling**:
   - Posts are scheduled every 3 hours using the `schedule` library.
   - The script runs continuously, checking for new posts to send.

4. **Session Management**:
   - The session file (`session_file`) is used to maintain the Telegram connection, ensuring that the bot stays logged in.

## Author

* Telegram: **[@live4code](https://t.me/live4code)**
* Email: **steven.marelly@gmail.com**

Good luck with your Telegram AutoPoster! 🚀
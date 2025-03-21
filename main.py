import os
import asyncio
import requests
from telethon import TelegramClient
from telethon.errors import FloodWaitError
from schedule import Scheduler

THEME = os.getenv("THEME")
LINK = os.getenv("LINK")
API_KEY = os.getenv("API_KEY")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

class ContentGenerator:
    def __init__(self, api_key, theme):
        self.api_key = api_key
        self.theme = theme
        self.base_url = "https://api.zukijourney.com/v1/chat/completions"

    def generate_quote(self):
        prompt = f"Сгенерируй мотивирующую цитату на тему {self.theme}. Не более 200 символов."
        response = self._send_request(prompt)
        return response["choices"][0]["message"]["content"]

    def generate_fact(self):
        prompt = f"Расскажи краткую историческую справку или интересный факт на тему {self.theme}. Не более 300 символов."
        response = self._send_request(prompt)
        return response["choices"][0]["message"]["content"]

    def generate_tips(self):
        prompt = f"Сгенерируй 2-3 практических совета на тему {self.theme}. Каждый совет должен начинаться с эмодзи. Не более 100 символов."
        response = self._send_request(prompt)
        return response["choices"][0]["message"]["content"]

    def generate_call_to_action(self):
        prompt = f"Придумай призыв к действию или вопрос для обсуждения на тему {self.theme}. Не более 100 символов."
        response = self._send_request(prompt)
        return response["choices"][0]["message"]["content"]

    def _send_request(self, prompt):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-4o-mini",
            "messages": [
                { "role": "user", "content": prompt }
            ]
        }
        try:
            response = requests.post(self.base_url, headers=headers, json=data)
            return response.json()
        except Exception as e:
            print(f"Ошибка при запросе к API: {e}")
            return {}

class TelegramPoster:
    def __init__(self, api_id, api_hash):
        self.client = TelegramClient("session_file", api_id, api_hash)

    async def send_post(self, channel, text, image_path):
        try:
            await self.client.send_file(channel, image_path, caption=text, parse_mode="md")
            print("Пост успешно отправлен!")
        except FloodWaitError as e:
            print(f"Ошибка FloodWait: {e}")
        except Exception as e:
            print(f"Ошибка при отправке поста: {e}")

content_generator = ContentGenerator(API_KEY, THEME)
telegram_poster = TelegramPoster(API_ID, API_HASH)

def generate_post():
    quote = content_generator.generate_quote()
    fact = content_generator.generate_fact()
    tips = content_generator.generate_tips()
    call_to_action = content_generator.generate_call_to_action()
    return f"""
🌟 **{quote}**

📜 **Историческая справка:** {fact}

💡 **Практические советы:**
{tips}

📢 **{call_to_action}**

👉 [Перейти по ссылке]({LINK})
    """

async def send_post():
    post_text = generate_post()
    image_path = "images/header.jpg"
    await telegram_poster.send_post(CHANNEL_ID, post_text, image_path)

scheduler = Scheduler()
scheduler.every(3).hours.do(lambda: asyncio.create_task(send_post()))

async def run_scheduler():
    while True:
        scheduler.run_pending()
        await asyncio.sleep(1)

async def main():
    await telegram_poster.client.start()

    asyncio.create_task(run_scheduler())

    print("Клиент запущен.")
    await telegram_poster.client.run_until_disconnected()


if __name__ == "__main__":
    with telegram_poster.client:
        telegram_poster.client.loop.run_until_complete(main())
import os
import sys
import time
import requests
import telebot
import re

sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

# Токен берём из настроек Render
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = "@news_dept"

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def get_live_disaster():
    """Тупо заходим на главную страницу GDACS и забираем ссылку на самую первую новость"""
    try:
        url = "https://gdacs.org"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        res = requests.get(url, headers=headers, timeout=15)
        
        if res.status_code == 200:
            # Ищем на странице любую длинную ссылку на отчет (report.aspx?eventid=...)
            links = re.findall(r'report\.aspx\?eventid=\d+&amp;eventtype=[A-Z]+', res.text)
            if links:
                # Берём самую первую свежую ссылку со страницы и чистим её
                clean_link = links[0].replace('&amp;', '&')
                full_url = f"https://gdacs.org{clean_link}"
                return full_url
    except Exception as e:
        print("Ошибка получения страницы:", e)
    
    # Железный фолбек, но уже СРАЗУ с конкретной длинной ссылкой на отчёт!
    return "https://gdacs.orgreport.aspx?eventid=1100234&eventtype=FL"

def generate_simple_script():
    # Забираем прямую ссылку на конкретное ЧС со страницы
    news_url = get_live_disaster()
    
    # Вытаскиваем ID происшествия для ИИ
    event_id = re.search(r'eventid=(\d+)', news_url)
    eid = event_id.group(1) if event_id else "1100234"

    return f"""📌 TIKTOK TITLE: GUYS THIS IS CRAZY INSANE! 🚨

🔥 **ХУК** 🔥
[ВИЗУАЛ: Блогер держится за голову на фоне карты ЧС]
Ребята, вы вообще видели, что только что произошло? Я просто в шоке!

🎙️ **ОСНОВНОЙ ТЕКСТ** 🎙️
[ВИЗУАЛ: Кадры стихийного бедствия из соцсетей]
В сети массово публикуют видео масштабного происшествия под номером {eid}. Ситуация в регионе очень опасная, люди экстренно эвакуируются из зоны бедствия.

🎬 **ЗАКЛЮЧЕНИЕ** 🎬
[ВИЗУАЛ: Стрелка указывает на комменты]
Напишите в комментариях, кто-то из вас сейчас находится рядом с этим местом?

#️⃣ HASHTAGS: #breakingnews #crazy #disaster #news #global #fyp

🔗 **Официальный первоисточник (ООН/GDACS):** {news_url}"""

if __name__ == "__main__":
    print("🚀 Скрипт прямой ссылки запущен...")
    
    # Принудительно отправляем пост в канал СРАЗУ при запуске
    try:
        post_text = generate_simple_script()
        bot.send_message(CHANNEL_ID, post_text)
        print("🎉 SUCCESS! Живой разговорный пост с ПРЯМОЙ ссылкой ушел в канал!")
    except Exception as err:
        print("Ошибка Telegram:", err)

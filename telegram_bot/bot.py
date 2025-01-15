import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pythonchi.settings')
django.setup()

from telebot import TeleBot
from django.contrib.auth import get_user_model
from project.models import Student

User = get_user_model()

BOT_TOKEN = "1398484716:AAE2nhlFvHPBWwK4V35IvssAneHimEjSgxQ"
bot = TeleBot(BOT_TOKEN)

user_states = {}

def reset_user_state(chat_id):
    if chat_id in user_states:
        del user_states[chat_id]

# Команда /start
@bot.message_handler(commands=["start"])
def start_handler(message):
    chat_id = message.chat.id
    user_states[chat_id] = {"step": "username"}
    bot.send_message(chat_id, "👋 Assalomu aleykum! *Ismingizni* yozing.", parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.chat.id in user_states)
def login_handler(message):
    chat_id = message.chat.id
    state = user_states[chat_id]

    if state["step"] == "username":
        state["username"] = message.text

        try:
            user = User.objects.get(username=state["username"])
            if user.is_superuser:
                state["is_admin"] = True
                state["step"] = "password"
                bot.send_message(chat_id, "Siz administratorsiz. *Parolingizni* yozing.", parse_mode="Markdown")
            else:
                state["is_admin"] = False
                state["step"] = "last_name"
                bot.send_message(chat_id, "*Familiyangizni* yozing.", parse_mode="Markdown")
        except User.DoesNotExist:
            state["is_admin"] = False
            state["step"] = "last_name"
            bot.send_message(chat_id, "*Familiyangizni* yozing.", parse_mode="Markdown")

    elif state["step"] == "last_name":
        state["last_name"] = message.text
        state["step"] = "password"
        bot.send_message(chat_id, "*Parolingizni* yozing.", parse_mode="Markdown")

    elif state["step"] == "password":
        state["password"] = message.text

        if state.get("is_admin"):
            try:
                admin_user = User.objects.get(username=state["username"])
                if admin_user.check_password(state["password"]):
                    if not admin_user.telegram_chat_id:
                        admin_user.telegram_chat_id = chat_id
                        admin_user.save()
                        bot.send_message(chat_id, "✅ Siz administrator sifatida ro'yxatdan o'tdingiz")
                    else:
                        bot.send_message(chat_id, "✅ Siz administrator sifatida ro'yxatdan o'tdingiz.")
                else:
                    bot.send_message(chat_id,
                                     "❌ Nato'g'ri parol kiritildi. Boshqattan harakat qilib ko'rin, /start buyrug'ini yuborib.")
            except User.DoesNotExist:
                bot.send_message(chat_id, "❌ Administrator nato'g'ri kiritildi. Boshqattan harakat qilib ko'rin, /start buyrug'ini yuborib.")
            finally:
                reset_user_state(chat_id)
        else:
            try:
                student = Student.objects.get(username=state["username"], last_name=state["last_name"])
                if student.password == state["password"]:
                    student.telegram_chat_id = chat_id
                    student.save()
                    bot.send_message(chat_id, f"✅ Xush kelibsiz, {student.username}!")
                else:
                    bot.send_message(chat_id, "❌ Nato'g'ri parol kiritildi. Boshqattan harakat qilib ko'rin, /start buyrug'ini yuborib.")
            except Student.DoesNotExist:
                bot.send_message(chat_id, "❌ Nato'gri ma'lumotlar kiritildi. Boshqattan harakat qilib ko'rin, /start buyrug'ini yuborib.")
            finally:
                reset_user_state(chat_id)


if __name__ == "__main__":
    bot.infinity_polling()

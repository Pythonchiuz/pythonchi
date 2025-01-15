from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task, Chat
from telebot import TeleBot
from django.contrib.auth import get_user_model

BOT_TOKEN = "1398484716:AAE2nhlFvHPBWwK4V35IvssAneHimEjSgxQ"
bot = TeleBot(BOT_TOKEN)

User = get_user_model()

@receiver(post_save, sender=Task)
def notify_admin_student(sender, instance, created, **kwargs):

    if created:
        try:
            admin_user = User.objects.filter(username="pythonchi-admin").first()

            if admin_user:
                chat_id = admin_user.telegram_chat_id

                if chat_id:
                    message = (
                        f"🆕 Yangi uy ishi yuborildi!\n\n"
                        f"👤 Student: {instance.student.last_name} {instance.student.username}\n"
                        f"📌 Modul: {instance.group.course.name}\n"
                        f"📚 Mavzu: {instance.modul.name}\n"
                        f"📝 Vazifa: {instance.hw.title}-vazifa\n"
                        f"📎 Link: {instance.homework}\n"
                    )
                    bot.send_message(chat_id, message)
                else:
                    print(f"⚠️ Telegram ID {admin_user.username}")
        except Exception as e:
            print(f"❌ Ошибка: {e}")

    elif instance.comment_status == "IS_ACTIVE":
        if instance.homework_status == "IS_ACTIVE":
            message = (
                f"🆕 Sizga yangi xabar keldi:\n\n"
                f"📌 Modul: {instance.group.course.name}\n"
                f"📚 Mavzu: {instance.modul.name}\n"
                f"📝 Vazifa: {instance.hw.title}-vazifa\n"
                f"📎 Link: {instance.homework}\n"
                f"👤 Mentor: {instance.comment_text}\n"
                "📊 Status: Bajarildi✅"
            )
        else:

            message = (
                f"🆕 Sizga yangi xabar keldi:\n\n"
                f"📌 Modul: {instance.group.course.name}\n"
                f"📚 Mavzu: {instance.modul.name}\n"
                f"📝 Vazifa: {instance.hw.title}-vazifa\n"
                f"📎 Link: {instance.homework}\n"
                f"👤 Mentor: {instance.comment_text}\n"

            )

        chat_id = instance.student.telegram_chat_id
        if chat_id:
            bot.send_message(chat_id, message)
        else:
            print(f"⚠️ Telegram ID {instance.student.username}")
    


@receiver(post_save, sender=Chat)
def notify_group_students(sender, instance, created, **kwargs):

    try:
        print(f"created={created}, status={instance.status}")

        if instance.status == "IS_ACTIVE":
            if instance.lesson_link is not None:
                message = (
                    f"🆕 Darsga kiring!\n\n"
                    f"📌 Mavzu: {instance.title}\n"
                    f"📎 Link: {instance.lesson_link}\n"
                )
            else:
                message = (
                    f"🆕 Yangi xabar!\n\n"
                    f"📌 Mavzu: {instance.title}\n"
                    f"📝 Xabar: {instance.text}\n"
                )

            students = instance.group.student.all()

            for student in students:
                chat_id = student.telegram_chat_id

                if chat_id:
                    bot.send_message(chat_id, message)
                else:
                    print(f"⚠️ Telegram ID {student.username}")
    except Exception as e:
        print(f"Ошибка: {e}")

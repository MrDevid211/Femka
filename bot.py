import os
import logging
import markovify
import gender
import random
import telegram
from telegram.ext import (Updater, CommandHandler, MessageHandler, ConversationHandler, Filters)
from gtts import gTTS

try:
    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
    logger = logging.getLogger(__name__)

    def generate(text, out_file):
        tts = gTTS(text, lang="ru")
        tts.save(out_file)

    def get_model(filename):
        with open(filename, encoding="utf-8") as f:
            text = f.read()

        return markovify.Text(text)

    def start(update, context):
        name = update.message.from_user.username
        fir = update.message.from_user.first_name
        id = update.message.from_user.id
        print("\nSTART\n\n" + "User ID: " + str(id) + "\nFirst name: " + fir + "\nUsername: " + str(name) + "\n")
        update.message.reply_text("Это самый навороченый фемкобот на этой планете! Закинь мне свою фоточку и посмотрим что Я отвечу")

    def error(update, context):
        logger.warning('update "%s" casused error "%s"', update, context.error)

    def photo(update, context):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=telegram.ChatAction.RECORD_AUDIO)

        id = update.message.from_user.id
        name = str(id) + ".jpg"
        filepath = "./user_data/" + name

        largest_photo = update.message.photo[-1].get_file()
        largest_photo.download(filepath)

        genders = gender.resolve(filepath)
        if len(genders) == 0:
            update.message.reply_text("Или это Я в глаза ебусь или ты мне кидаешь нифига не фото человека")
            os.remove(filepath)
            return

        out_file = "./user_data/" + str(id) + "mp3"
        text = ""
        generator = None

        if genders[0] == "female":
            sex = "female"
        else:
            sex = "male"

        if sex == "female":
            female = open("female", "r")
            spisok = []
            for i in female:
                spisok.append(i)
            dlinna = len(spisok)
            dlinna = int(dlinna)
            ran = random.randint(0, dlinna)
            text = spisok[ran]

        elif sex == "male":
            male = open("male", "r")
            spisok = []
            for i in male:
                spisok.append(i)
            dlinna = len(spisok)
            dlinna = int(dlinna)
            ran = random.randint(0, dlinna)
            text = spisok[ran]

        name = update.message.from_user.username
        print((name) + ": ", text)

        generate(text, out_file)

        update.message.reply_text(text)
        #update.message.reply_audio(audio=open(out_file, "rb"))

        os.remove(out_file)
        os.remove(filepath)


    def cancel(update, context):
        return ConversationHandler.END

    def main():
        updater = Updater("Тут должен быть токен", use_context=True)
        dp = updater.dispatcher

        photo_handler = MessageHandler(Filters.photo, photo)

        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("cancel", cancel))
        dp.add_handler(photo_handler)
        dp.add_error_handler(error)

        updater.start_polling()
        updater.idle()

    if __name__ == "__main__":
        main()

except:
    update.message.reply_text("Хватит кормить нейросеть какой-то петрушкой. Сорян, она это фото не распознала")
    print("Опять петрушкой кормят")



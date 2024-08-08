from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from pytube import YouTube
import os

# Function to start the bot
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Send me a YouTube link to download the video or audio.')

# Function to handle YouTube links
def download(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    try:
        yt = YouTube(url)
        video = yt.streams.filter(progressive=True, file_extension='mp4').first()
        audio = yt.streams.filter(only_audio=True).first()

        video_path = video.download()
        audio_path = audio.download(filename='audio.mp4')

        update.message.reply_text('Choose format to download: /video or /audio')

        context.user_data['video_path'] = video_path
        context.user_data['audio_path'] = audio_path

    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

# Function to send video
def send_video(update: Update, context: CallbackContext) -> None:
    video_path = context.user_data.get('video_path', '')
    if os.path.exists(video_path):
        update.message.reply_video(video=open(video_path, 'rb'))
        os.remove(video_path)
    else:
        update.message.reply_text('No video to send.')

# Function to send audio
def send_audio(update: Update, context: CallbackContext) -> None:
    audio_path = context.user_data.get('audio_path', '')
    if os.path.exists(audio_path):
        update.message.reply_audio(audio=open(audio_path, 'rb'))
        os.remove(audio_path)
    else:
        update.message.reply_text('No audio to send.')

def main() -> None:
    # Create the Updater and pass it your bot's token
    updater = Updater("YOUR_TELEGRAM_BOT_TOKEN")

    dispatcher = updater.dispatcher

    # Add command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("video", send_video))
    dispatcher.add_handler(CommandHandler("audio", send_audio))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, download))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()

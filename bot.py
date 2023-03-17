#!/bin/python3
import telebot
import speech_recognition as sr
from pydub import AudioSegment
from moviepy.editor import *

# Введите ваш API-ключ, полученный от BotFather
API_KEY = '<BOT_TOKEN>'
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот, который преобразует голосовые и круглые видеосообщения в текст. Просто отправьте мне сообщение!")

def process_audio(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)

    text = recognizer.recognize_google(audio, language='ru-RU')
    return text

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    try:
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with open('voice.ogg', 'wb') as f:
            f.write(downloaded_file)

        ogg_audio = AudioSegment.from_ogg("voice.ogg")
        ogg_audio.export("voice.wav", format="wav")

        text = process_audio('voice.wav')
        bot.reply_to(message, text)

    except Exception as e:
        print(e)
        bot.reply_to(message, "Произошла ошибка при обработке голосового сообщения. Пожалуйста, попробуйте снова.")

@bot.message_handler(content_types=['video_note'])
def handle_video(message):
    try:
        file_info = bot.get_file(message.video_note.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with open('video_note.mp4', 'wb') as f:
            f.write(downloaded_file)

        video = VideoFileClip("video_note.mp4")
        audio = video.audio
        audio.write_audiofile("video_note.wav")

        text = process_audio('video_note.wav')
        bot.reply_to(message, text)

    except Exception as e:
        print(e)
        bot.reply_to(message, "Произошла ошибка при обработке видеосообщения. Пожалуйста, попробуйте снова.")

bot.polling()

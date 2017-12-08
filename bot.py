# -*- coding: utf-8 -*-

import config
import os
from buttons import recieve_button, repeat_or_exit_button
import telebot
from telebot import types
import datetime
from telegramcalendar import create_calendar

bot = telebot.TeleBot(config.token)
current_shown_dates = {}


@bot.message_handler(commands=['start'])
def get_button(message):
    """Show Button 'Recieve'"""
    markup = recieve_button()
    bot.send_message(message.chat.id, "Welcome, " + str(message.chat.first_name), reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'calendar')
def get_calendar(call):
    """Show calendar
        Current date"""
    now = datetime.datetime.now()
    chat_id = call.message.chat.id
    date = (now.year, now.month)
    """Saving the current date in a dict"""
    current_shown_dates[chat_id] = date
    markup = create_calendar(now.year, now.month)
    bot.send_message(call.message.chat.id, "Please, choose a date", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data[0:13] == 'calendar-day-')
def get_day(call):
    """Show selected day and Recieve dicument"""
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if saved_date is not None:
        day = call.data[13:]
        date = datetime.datetime(int(saved_date[0]), int(saved_date[1]), int(day), 0, 0, 0)
        bot.send_message(chat_id, str(date))
        bot.answer_callback_query(call.id, text="")

    else:
        #Do something to inform of the error
        pass
    for file in os.listdir('ratings/'):
            if file.split('.')[-1] == 'pdf':
                f = open('ratings/'+file, 'rb')
                msg = bot.send_document(call.message.chat.id, f, reply_to_message_id=None, timeout=5)
                bot.send_message(call.message.chat.id, msg.document.file_id, reply_to_message_id=msg.message_id)
    markup = repeat_or_exit_button()
    bot.send_message(call.message.chat.id, "Select another rating, " + str(call.message.chat.first_name),
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'next-month')
def next_month(call):
    """Show next month"""
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if saved_date is not None:
        year, month = saved_date
        month += 1
        if month > 12:
            month = 1
            year += 1
        date = (year, month)
        current_shown_dates[chat_id] = date
        markup = create_calendar(year, month)
        bot.edit_message_text("Please, choose a date", call.from_user.id, call.message.message_id, reply_markup=markup)
        bot.answer_callback_query(call.id, text="")
    else:
        #Do something to inform of the error
        pass


@bot.callback_query_handler(func=lambda call: call.data == 'previous-month')
def previous_month(call):
    """Show previous month"""
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if saved_date is not None:
        year, month = saved_date
        month -= 1
        if month < 1:
            month = 12
            year -= 1
        date = (year, month)
        current_shown_dates[chat_id] = date
        markup = create_calendar(year, month)
        bot.edit_message_text("Please, choose a date", call.from_user.id, call.message.message_id, reply_markup=markup)
        bot.answer_callback_query(call.id, text="")
    else:
        #Do something to inform of the error
        pass


@bot.callback_query_handler(func=lambda call: call.data == 'ignore')
def ignore(call):
    """Click on empty button"""
    bot.answer_callback_query(call.id, text="")


if __name__ == '__main__':
    bot.polling(none_stop=True)

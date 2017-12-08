from telebot import types


def recieve_button():
    """Create Button 'Recieve' """
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton('Recieve rating', callback_data='calendar')
    markup.add(button)
    return markup


def repeat_or_exit_button():
    """Create Buttons 'Repeate and Exit' """
    row = list()
    markup = types.InlineKeyboardMarkup()
    row.append(types.InlineKeyboardButton('Recieve another rating', callback_data='calendar'))
    row.append(types.InlineKeyboardButton('Exit', callback_data='ignore'))
    markup.row(*row)
    return markup

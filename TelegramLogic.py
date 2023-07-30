from TranslatorLogic import add_words, check_alphabet, translate_func, del_word, edit_word, top
from settings import bot
from aiogram.types import ParseMode
from aiogram import types

user_list = {"g": "q", "j": "k"}
types_list = ["{Word}", "Ukrainian = English", "Previous = New"]


def markup():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text="translate🔃", callback_data='button_translate', row_width=3),
        types.InlineKeyboardButton(text="best🥇", callback_data='button_best'),
        types.InlineKeyboardButton(text="add➕", callback_data='button_add'),
        types.InlineKeyboardButton(text="delete❌", callback_data='button_delete'),
        types.InlineKeyboardButton(text="test❔", callback_data='button_test'),
        types.InlineKeyboardButton(text="edit✏", callback_data='button_edit'),
    )
    return keyboard


async def list_add(call):
    content_type = 0
    user_list[call.message.chat.id] = call.data
    print(call.data)
    if call.data == "button_add":
        content_type = 1

    elif call.data == "button_translate" or call.data == "button_delete":
        content_type = 0

    elif call.data == "button_edit":
        content_type = 2

    elif call.data == "button_best":
        await call.message.edit_text(f"the bests are: {top()}")
        return True

    await call.message.edit_text(f"Good, now send me message like ``` {types_list[content_type]} ```", parse_mode=ParseMode.MARKDOWN)


async def checking(message):
    UsLt = user_list[message.chat.id]
    if UsLt == "button_add":
        word_list = message.text.split(" = ")
        add_words(word_list[1], word_list[0])
        await bot.send_message(message.chat.id, "Word was successfully added")

    if UsLt == "button_translate":
        await bot.send_message(message.chat.id, check_alphabet(message.text, translate_func))

    if UsLt == "button_delete":
        check_alphabet(message.text, del_word)

    if UsLt == "button_edit":
        text_list = message.text.split(" = ")
        check_alphabet(text_list, edit_word)

    if UsLt == "test":
        pass

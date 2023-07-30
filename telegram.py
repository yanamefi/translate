from settings import dp, bot
from aiogram import executor
from aiogram import types
from TelegramLogic import markup, list_add, checking


@dp.message_handler(commands=["start"])
async def type_check(message: types.Message):
    await message.answer("Hi🤗\nPick what you want to do today", reply_markup=markup())


@dp.callback_query_handler()
async def call_hand(call: types.CallbackQuery):
    await list_add(call)


@dp.message_handler()
async def message_hand(message: types.Message):
    await checking(message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

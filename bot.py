from aiogram import Bot, Dispatcher, executor, types
from config import *
from controller import Controller
import logging
import asyncio

bot = Bot(TOKEN)
dp = Dispatcher(bot)
cn = Controller()
# async def send_post():
#     while True:
#         await bot.send_message()
channel = CHANNEL_ID
scheduled = 60*10


async def add_post():
    while True:
        cn.clear_data()
        cn.save_all_vac()
        vacs = cn.get_vac()
        for vac in vacs:
            header = f'<b>{vac["name"]}</b>\n' \
                     f'\nАдресс: <i>{vac["address"]}</i>\n'
            content = f'\nРаботодатель: {vac["employer"]}\n' \
                      f'\nРоль: {vac["role"]}\n' \
                      f'Задачи: {vac["responsibility"]}\n' \
                      f'\n\nЗарплата: \n<i>{vac["salary"]}</i>'
            text = header + content
            urlkb = types.InlineKeyboardMarkup()
            url_button = types.InlineKeyboardButton(text="Изучить", url=f"{vac['link']}")
            urlkb.add(url_button)
            await bot.send_message(chat_id=channel, text=text, parse_mode="html", reply_markup=urlkb)
            await asyncio.sleep(scheduled)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(add_post())
    executor.start_polling(dp, skip_updates=True)

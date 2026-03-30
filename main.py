import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from datetime import datetime

# Берем токен из настроек Render
TOKEN = os.getenv("BOT_TOKEN")
# Твой ID, чтобы бот слал сообщения именно тебе
MY_CHAT_ID = 693240058 

bot = Bot(token=TOKEN)
dp = Dispatcher()

PLAN = {
    "09:00": "🥣 Завтрак: Овсянка на воде + яйцо всмятку. Теплую воду выпил?",
    "11:00": "🍎 Перекус: Запеченное яблоко из аэрогриля (180°C/10м).",
    "12:15": "🍗 Обед: Рис + курица/индейка в фольге. Скоро на курсы!",
    "15:30": "🍌 ПАУЗА НА КУРСАХ! Срочно съешь банан, не давай желудку пустовать.",
    "18:30": "🐟 Ужин: Рыба + картошка из аэрогриля. Отдыхай.",
    "21:00": "🥚 Поздний ужин: Легкий омлет или галетное печенье."
}

WORKOUTS = {
    "Mon": "💪 Верх: Отжимания (https://www.youtube.com/watch?v=wD1M-f69Yy8) и Подтягивания.",
    "Wed": "🦵 Низ: Приседания (https://www.youtube.com/watch?v=gcNh17Ckjgg) и Выпады.",
    "Fri": "🔄 Full Body: Всё тело понемногу. Дыши правильно!"
}

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(f"Привет, Макс! Твой ID: {message.from_user.id}. Я буду присылать напоминалки.")

async def scheduler():
    while True:
        now = datetime.now().strftime("%H:%M")
        day = datetime.now().strftime("%a")
        
        if now in PLAN:
            try:
                await bot.send_message(MY_CHAT_ID, PLAN[now])
            except Exception as e:
                print(f"Ошибка: {e}")
            
        if now == "10:30" and day in WORKOUTS:
            try:
                await bot.send_message(MY_CHAT_ID, f"🏋️‍♂️ Время тренировки!\n{WORKOUTS[day]}")
            except Exception as e:
                print(f"Ошибка: {e}")
            
        await asyncio.sleep(60)

async def main():
    asyncio.create_task(scheduler())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

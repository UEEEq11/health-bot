import os
import asyncio
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# --- НАСТРОЙКИ ---
TOKEN = os.getenv("BOT_TOKEN")
MY_ID = 1130349282 # Твой проверенный ID

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Состояние (в идеале нужна БД, но для теста храним в памяти)
user_data = {
    "is_working": False,
    "clean_days": 1,
    "weight_history": [],
    "fridge": ["Курица", "Яйца", "Овсянка"]
}

# --- КЛАВИАТУРЫ ---
def main_menu():
    kb = ReplyKeyboardBuilder()
    kb.row(KeyboardButton(text="💪 Тренировка"), KeyboardButton(text="🍎 Еда и Kaufland"))
    kb.row(KeyboardButton(text="📉 Прогресс и Чистота"), KeyboardButton(text="💼 Моя Работа"))
    return kb.as_markup(resize_keyboard=True)

# --- ОБРАБОТЧИКИ КНОПОК ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if message.from_user.id != MY_ID: return
    await message.answer(
        "Здорово, Макс! Я перенастроен. Теперь всё на кнопках. "
        "Твой график и пуши активны. Погнали на массу! 🦾",
        reply_markup=main_menu()
    )

@dp.message(F.text == "💼 Моя Работа")
async def work_settings(message: types.Message):
    status = "РАБОТАЮ (5-11)" if user_data["is_working"] else "ВЫХОДНОЙ"
    kb = InlineKeyboardBuilder()
    kb.button(text="Сменить статус", callback_data="toggle_work")
    await message.answer(f"Текущий режим: {status}\nЕсли работаешь, я сдвину пуши на еду.", reply_markup=kb.as_markup())

@dp.message(F.text == "📉 Прогресс и Чистота")
async def progress_view(message: types.Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="🆘 ТЯГА / SOS", callback_data="sos_help")
    kb.button(text="Ввести вес", callback_data="input_weight")
    await message.answer(
        f"🗓 Дней в завязке: {user_data['clean_days']}\n"
        f"⚖️ Последний вес: {user_data['weight_history'][-1] if user_data['weight_history'] else 'Нет данных'}",
        reply_markup=kb.as_markup()
    )

@dp.callback_query(F.data == "sos_help")
async def sos_handler(callback: types.CallbackQuery):
    await callback.message.answer("🚨 ТАК, СТОП! Прямо сейчас: сделай 20 глубоких вдохов или присядь 30 раз. "
                                 "Мозг отпустит через 5 минут. Ты сильнее этой херни!")
    await callback.answer()

# --- ФУНКЦИЯ ПУШЕЙ (УВЕДОМЛЕНИЙ) ---
async def scheduler():
    while True:
        now = datetime.now().strftime("%H:%M")
        
        # Утренний пуш
        if now == "09:00":
            await bot.send_message(MY_ID, "🍎 ЗАВТРАК: Овсянка + 2 яйца. Включай Nutribullet!\nКнопка после еды:", 
                                   reply_markup=InlineKeyboardBuilder().button(text="Сделал ✅", callback_data="done").as_markup())
        
        # Пуш тренировки (если не работаешь)
        if now == "17:00" and not user_data["is_working"]:
            await bot.send_message(MY_ID, "💪 ВРЕМЯ ЖАТЬ! Сегодня День Ног.\n1. Присед 4х12\n2. Выпады 3х15\nКнопка после:")
            
        await asyncio.sleep(60)

# Запуск
async def main():
    asyncio.create_task(scheduler())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

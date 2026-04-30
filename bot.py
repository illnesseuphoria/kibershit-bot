import asyncio
import os
import re
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ===== БЫСТРАЯ ПАНЕЛЬ ВНИЗУ =====
def quick_panel():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔍 Проверить ссылку")],
            [KeyboardButton(text="💬 Проверить сообщение")],
            [KeyboardButton(text="📚 Тест на безопасность")],
            [KeyboardButton(text="✅ Чек-лист")]
        ],
        resize_keyboard=True
    )
    return keyboard

# ===== КОМАНДА /start =====
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "🛡️ *КиберЩит | Бот против мошенников*\n\n"
        "Привет! Я помогу тебе не попасться на удочку кибермошенников.\n\n"
        "🔍 *Проверить ссылку* — отправь мне ссылку\n"
        "💬 *Проверить сообщение* — отправь текст\n"
        "📚 *Тест на безопасность* — проверь свои знания\n"
        "✅ *Чек-лист* — узнай, насколько ты защищен\n\n"
        "#КиберПраво",
        reply_markup=quick_panel(),
        parse_mode="Markdown"
    )

# ===== АНАЛИЗ ССЫЛКИ =====
def analyze_link(url):
    danger_score = 0
    reasons = []
    
    if re.match(r'https?://\d+\.\d+\.\d+\.\d+', url):
        danger_score += 3
        reasons.append("🔴 IP-адрес вместо домена")
    
    suspicious = ['.xyz', '.top', '.click', '.loan', '.gq', '.ml', '.tk']
    for dom in suspicious:
        if dom in url:
            danger_score += 2
            reasons.append(f"⚠️ Подозрительный домен {dom}")
    
    words = ['login', 'verify', 'secure', 'bank', 'confirm', 'signin', 'account']
    for word in words:
        if word in url.lower():
            danger_score += 1
            reasons.append(f"⚠️ Слово '{word}' в ссылке")
    
    if len(url) > 100:
        danger_score += 1
        reasons.append("📏 Очень длинная ссылка")
    
    if danger_score >= 5:
        verdict = "🚨 *ОПАСНО!* Мошенническая ссылка!"
    elif danger_score >= 2:
        verdict = "⚠️ *ПОДОЗРИТЕЛЬНО!* Будьте осторожны!"
    else:
        verdict = "✅ *БЕЗОПАСНО*"
    
    if not reasons:
        reasons.append("✅ Явных признаков не обнаружено")
    
    result = f"{verdict}\n\n🔍 *Признаки:*\n"
    for r in reasons:
        result += f"• {r}\n"
    result += f"\n📊 *Риск:* {danger_score}/10\n\n#КиберПраво"
    return result

# ===== АНАЛИЗ ТЕКСТА =====
def analyze_text(text):
    danger_score = 0
    reasons = []
    
    urgency = ['срочно', 'немедленно', 'сейчас же', 'в течение часа', 'сегодня']
    for w in urgency:
        if w in text.lower():
            danger_score += 2
            reasons.append(f"⏰ Давление срочности: '{w}'")
            break
    
    prize = ['выиграл', 'приз', 'выигрыш', 'подарок', 'акция', 'лотерея']
    for w in prize:
        if w in text.lower():
            danger_score += 2
            reasons.append(f"🎁 Подозрительный выигрыш: '{w}'")
            break
    
    personal = ['код', 'пароль', 'смс', 'карта', 'паспорт', 'реквизиты']
    for w in personal:
        if w in text.lower():
            danger_score += 3
            reasons.append(f"🔐 Запрос личных данных: '{w}'")
            break
    
    if 'http' in text.lower():
        danger_score += 2
        reasons.append("🔗 В сообщении есть ссылка")
    
    official = ['банк', 'мвд', 'налоговая', 'безопасность', 'служба']
    for w in official:
        if w in text.lower():
            danger_score += 2
            reasons.append(f"🏛️ Имитация организации: '{w}'")
            break
    
    if danger_score >= 5:
        verdict = "🚨 *ОПАСНО!* Мошенническое сообщение!"
    elif danger_score >= 2:
        verdict = "⚠️ *ПОДОЗРИТЕЛЬНО!* Будьте осторожны!"
    else:
        verdict = "✅ *БЕЗОПАСНО*"
    
    if not reasons:
        reasons.append("✅ Явных признаков не обнаружено")
    
    result = f"{verdict}\n\n🔍 *Признаки:*\n"
    for r in reasons:
        result += f"• {r}\n"
    result += f"\n📊 *Риск:* {danger_score}/10\n\n💡 *Совет:* Не переходите по ссылкам и не сообщайте коды!\n\n#КиберПраво"
    return result

# ===== ТЕСТ (5 вопросов) =====
quiz_questions = [
    {"question": "1️⃣ Вам пришло СМС: 'Ваша карта заблокирована. Перейдите по ссылке'. Что делать?",
     "options": ["Перейти по ссылке", "Позвонить в банк", "Удалить СМС"],
     "correct": 1, "explanation": "Правильно: позвонить в банк. Никогда не переходите по ссылкам из СМС!"},
    {"question": "2️⃣ Какой пароль самый надежный?",
     "options": ["123456", "qwerty123", "К$9m#2Lp!7Qx"],
     "correct": 2, "explanation": "Надежный пароль: 12+ символов, цифры, спецсимволы."},
    {"question": "3️⃣ Что такое фишинг?",
     "options": ["Вирус", "Выманивание данных", "Антивирус"],
     "correct": 1, "explanation": "Фишинг — выманивание личных данных под видом официальных организаций."},
    {"question": "4️⃣ Можно ли переходить по ссылкам от незнакомцев?",
     "options": ["Да", "Нет", "Если интересно"],
     "correct": 1, "explanation": "Никогда! Это может быть фишинг или вирус."},
    {"question": "5️⃣ Зачем мошенникам код из СМС?",
     "options": ["Подтвердить номер", "Войти в ваш аккаунт", "Отправить подарок"],
     "correct": 1, "explanation": "Код из СМС — ключ к вашему аккаунту!"}
]

user_quiz = {}

@dp.callback_query(lambda c: c.data == "quiz")
async def start_quiz(callback: types.CallbackQuery):
    user_quiz[callback.from_user.id] = {"current": 0, "score": 0}
    await send_quiz_question(callback.message, callback.from_user.id)
    await callback.answer()

async def send_quiz_question(message, user_id):
    q_num = user_quiz[user_id]["current"]
    if q_num >= len(quiz_questions):
        score = user_quiz[user_id]["score"]
        result = f"📊 *Результаты:* {score}/{len(quiz_questions)}\n\n#КиберПраво"
        await message.answer(result, parse_mode="Markdown")
        return
    q = quiz_questions[q_num]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=opt, callback_data=f"quiz_{q_num}_{idx}")] 
        for idx, opt in enumerate(q["options"])
    ])
    await message.answer(f"📚 *Тест*\n\n{q['question']}", reply_markup=keyboard, parse_mode="Markdown")

@dp.callback_query(lambda c: c.data.startswith("quiz_"))
async def quiz_answer(callback: types.CallbackQuery):
    data = callback.data.split("_")
    q_num = int(data[1])
    answer_idx = int(data[2])
    user_id = callback.from_user.id
    if user_id not in user_quiz:
        return
    q = quiz_questions[q_num]
    if answer_idx == q["correct"]:
        user_quiz[user_id]["score"] += 1
        await callback.answer("✅ Правильно!", show_alert=True)
        await callback.message.answer(f"✅ Верно!\n\n{q['explanation']}\n\n#КиберПраво", parse_mode="Markdown")
    else:
        await callback.answer("❌ Неправильно", show_alert=True)
        await callback.message.answer(f"❌ Неправильно.\n\n{q['explanation']}\n\n#КиберПраво", parse_mode="Markdown")
    user_quiz[user_id]["current"] += 1
    await send_quiz_question(callback.message, user_id)

@dp.callback_query(lambda c: c.data == "checklist")
async def checklist(callback: types.CallbackQuery):
    text = "✅ *Чек-лист*\n\n🔐 Разные пароли\n📱 Двухфакторка\n⚠️ Не переходить по ссылкам\n\n#КиберПраво"
    await callback.message.answer(text, parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(lambda c: c.data == "check_link")
async def check_link_button(callback: types.CallbackQuery):
    await callback.message.answer("🔍 Отправьте ссылку")
    await callback.answer()

@dp.callback_query(lambda c: c.data == "check_message")
async def check_message_button(callback: types.CallbackQuery):
    await callback.message.answer("💬 Отправьте текст")
    await callback.answer()

@dp.message(lambda message: message.text == "🔍 Проверить ссылку")
async def quick_check_link(message: types.Message):
    await message.answer("🔍 Отправьте ссылку")

@dp.message(lambda message: message.text == "💬 Проверить сообщение")
async def quick_check_message(message: types.Message):
    await message.answer("💬 Отправьте текст")

@dp.message(lambda message: message.text == "📚 Тест на безопасность")
async def quick_quiz(message: types.Message):
    user_quiz[message.from_user.id] = {"current": 0, "score": 0}
    await send_quiz_question(message, message.from_user.id)

@dp.message(lambda message: message.text == "✅ Чек-лист")
async def quick_checklist(message: types.Message):
    text = "✅ *Чек-лист*\n\n🔐 Разные пароли\n📱 Двухфакторка\n⚠️ Не переходить по ссылкам\n\n#КиберПраво"
    await message.answer(text, parse_mode="Markdown")

@dp.message()
async def handle_message(message: types.Message):
    text = message.text
    if not text:
        return
    if "http" in text or "https" in text:
        result = analyze_link(text)
        await message.answer(result, parse_mode="Markdown")
    else:
        result = analyze_text(text)
        await message.answer(result, parse_mode="Markdown")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

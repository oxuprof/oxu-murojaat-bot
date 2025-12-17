from aiogram import Bot, Dispatcher, executor, types

TOKEN = "8560400675:AAESOyMCrtwIXoDG7v9-6kXGetDLlNnuQOY"
GROUP_ID = -5066509199

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# Guruhdagi murojaat ID -> foydalanuvchi ID
message_map = {}

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        "Hurmatli o‘qituvchi!\n\n"
        "Agar HEMIS tizimida darsingiz xato qo‘yilgan bo‘lsa, muammoni quyidagicha tushuntirib yuboring:\n\n"
        "Sana, Guruh, Juftlik, Muammo va aslida qanday bo‘lishi kerakligini qisqacha yozing.\n\n"
        "Shuningdek, kerak bo‘lsa rasm yoki fayl ham yuborishingiz mumkin."
    )

@dp.message_handler(content_types=types.ContentType.ANY, chat_type=types.ChatType.PRIVATE)
async def user_message(message: types.Message):
    user = message.from_user

    user_link = f"<a href='tg://user?id={user.id}'>👤 Profilga o‘tish</a>"

    caption = (
        "📩 <b>Yangi murojaat</b>\n\n"
        f"👤 Ism: {user.full_name}\n"
        f"🆔 ID: {user.id}\n\n"
        "💬 Xabar:\n"
    )

    if message.text:
        sent = await bot.send_message(GROUP_ID, caption + message.text + "\n\n" + user_link)

    elif message.photo:
        sent = await bot.send_photo(
            GROUP_ID,
            message.photo[-1].file_id,
            caption=caption + (message.caption or "") + "\n\n" + user_link
        )

    elif message.document:
        sent = await bot.send_document(
            GROUP_ID,
            message.document.file_id,
            caption=caption + (message.caption or "") + "\n\n" + user_link
        )

    else:
        sent = await bot.send_message(GROUP_ID, caption + "❗ Noma’lum format\n\n" + user_link)

    message_map[sent.message_id] = user.id

@dp.message_handler(chat_id=GROUP_ID, reply=True, content_types=types.ContentType.ANY)
async def staff_reply(message: types.Message):
    reply = message.reply_to_message
    if reply and reply.message_id in message_map:
        user_id = message_map[reply.message_id]

        if message.text:
            await bot.send_message(user_id, f"💬 <b>Xodim javobi:</b>\n{message.text}")

        elif message.photo:
            await bot.send_photo(
                user_id,
                message.photo[-1].file_id,
                caption="💬 Xodim javobi"
            )

        elif message.document:
            await bot.send_document(
                user_id,
                message.document.file_id,
                caption="💬 Xodim javobi"
            )

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

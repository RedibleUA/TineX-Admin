import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.exceptions import BotBlocked
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from config import TOKEN
from DB import StickerWrite, StickersLeft, StickersAllCount, StickersCategoryCount, StickerInsert, StickerDelete, MakeStickerFree , CheckLevelAdmin, AddAdmin, DeleteAdmin, ChangeLevelAdmin

API_TOKEN = TOKEN

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Ячейки памяти
class Form(StatesGroup):
    AddUser = State()
    DelUser = State()
    ChangeUser = State()



@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    try:
        if CheckLevelAdmin(message.from_user.id) == 1:
            await message.answer("🔮 Welcome to TineX Admin", reply_markup=menulvl1_kb)
        elif CheckLevelAdmin(message.from_user.id) > 1:
            await message.answer("🔮 Welcome to TineX Admin", reply_markup=menulvl2_kb)
        else:
            await message.answer("🔮 Ууууу...\nШар говорит что \nТы не админ!")

    except BotBlocked as E:
        pass


@dp.message_handler(commands=['stop'])
async def send_stop(message: types.Message):
    try:
        if CheckLevelAdmin(message.from_user.id) == 1:
            await message.answer(f"🔮 {MakeStickerFree(message.from_user.id)}", reply_markup=menulvl1_kb)
        elif CheckLevelAdmin(message.from_user.id) > 1:
            await message.answer(f"🔮 {MakeStickerFree(message.from_user.id)}", reply_markup=menulvl2_kb)
        else:
            await message.answer("🔮 Ууууу...\nШар говорит что \nТы не админ!")

    except BotBlocked as E:
        pass


@dp.message_handler(commands=['all'])
async def send_all(message: types.Message):
    try:
        if CheckLevelAdmin(message.from_user.id) == 1:
            await message.answer(f"{StickersAllCount()} stickers 🔮", reply_markup=menulvl1_kb)
        elif CheckLevelAdmin(message.from_user.id) > 1:
            await message.answer(f"{StickersAllCount()} stickers 🔮", reply_markup=menulvl2_kb)
        else:
            await message.answer("🔮 Ууууу...\nШар говорит что \nТы не админ!")

    except BotBlocked as E:
        pass


@dp.message_handler(commands=['category'])
async def send_welcome(message: types.Message):
    try:
        if CheckLevelAdmin(message.from_user.id) > 0:
            await message.answer('Select the category', reply_markup=selectButtons)
        else:
            await message.answer("🔮 Ууууу...\nШар говорит что \nТы не админ!")

    except BotBlocked as E:
        pass


@dp.callback_query_handler(text='Count Anime')
async def count_anime(callback: types.CallbackQuery):
    try:
        if CheckLevelAdmin(callback.from_user.id) > 0:
            await bot.send_message(callback.message.chat.id, f"<b>Anime</b> 🔮\n{StickersCategoryCount('Anime')} stickers", parse_mode='HTML')
        else:
            await bot.send_message(callback.message.chat.id, "🔮 Ууууу...\nШар говорит что \nТы не админ!")
        await callback.answer()

    except BotBlocked as E:
        pass


@dp.callback_query_handler(text='Count Cute cats')
async def count_cats(callback: types.CallbackQuery):
    try:
        if CheckLevelAdmin(callback.from_user.id) > 0:
            await bot.send_message(callback.message.chat.id, f"<b>Cute cats</b> 🔮\n{StickersCategoryCount('Cute cats')} stickers", parse_mode='HTML')
        else:
            await bot.send_message(callback.message.chat.id, "🔮 Ууууу...\nШар говорит что \nТы не админ!")
        await callback.answer()

    except BotBlocked as E:
        pass


@dp.callback_query_handler(text='Count Meme')
async def count_meme(callback: types.CallbackQuery):
    try:
        if CheckLevelAdmin(callback.from_user.id) > 0:
            await bot.send_message(callback.message.chat.id, f"<b>Meme</b> 🔮\n{StickersCategoryCount('Meme')} stickers", parse_mode='HTML')
        else:
            await bot.send_message(callback.message.chat.id, "🔮 Ууууу...\nШар говорит что \nТы не админ!")
        await callback.answer()

    except BotBlocked as E:
        pass

@dp.message_handler()
async def send_message(message: types.Message):
    try:
        if CheckLevelAdmin(message.from_user.id) > 0:
            match message.text:
                case 'Start':
                    await send_stickers(message)
                case '✅':
                    await message.answer(f"🔮 {StickerInsert(message.from_user.id)}")
                    await send_stickers(message)
                case '❌':
                    StickerDelete(message.from_user.id)
                    await message.answer("🔮 Done")
                    await send_stickers(message)

                case 'All Stickers':
                    await message.answer(f"{StickersAllCount()} stickers 🔮")

                case 'Count Category':
                    await message.answer('Select the category', reply_markup=selectButtons)
                case 'Manage users':
                    if CheckLevelAdmin(message.from_user.id) == 2:
                        await message.answer('Welcome to admin panel', reply_markup=adminMenulvl2_kb)
                    elif CheckLevelAdmin(message.from_user.id) > 2:
                        await message.answer('Welcome to admin panel', reply_markup=adminMenulvl3_kb)
                case 'Go back':
                    if CheckLevelAdmin(message.from_user.id) > 1:
                        await message.answer('Main manu', reply_markup=menulvl2_kb)
                case 'Add user':
                    if CheckLevelAdmin(message.from_user.id) > 1:
                        await message.answer('Send: Name - UserID - Level\nor type /exit')
                        await Form.AddUser.set()
                case 'Delete user':
                    if CheckLevelAdmin(message.from_user.id) > 1:
                        await message.answer('Send: UserID\nor type /exit')
                        await Form.DelUser.set()
                case 'Change user level':
                    if CheckLevelAdmin(message.from_user.id) > 2:
                        await message.answer('Send: UserID - Level\nor type /exit')
                        await Form.ChangeUser.set()

        else:
            await message.answer("🔮 Ууууу...\nШар говорит что \nТы не админ!")

    except BotBlocked as E:
        pass


async def send_stickers(message: types.Message):
    if (StickersLeft() > 1):

        rows = StickerWrite(message.from_user.id)
        for r in rows:
            Category = r[0]
            Url = r[2]
        await message.answer(f"{StickersLeft()} stickers left")
        await message.answer(f"{Category}:", reply_markup=work_kb)
        await bot.send_sticker(chat_id=message.chat.id, sticker=Url)

    elif (StickersLeft() == 1):
        rows = StickerWrite(message.from_user.id)
        for r in rows:
            Category = r[0]
            Url = r[2]
        await message.answer(f"🔮 The last one")
        await message.answer(f"{Category}:", reply_markup=work_kb)
        await bot.send_sticker(chat_id=message.chat.id, sticker=Url)

    elif (StickersLeft() == 0):
        if CheckLevelAdmin(message.from_user.id) == 1:
            await message.answer(f"🔮 No sticker packs left!", reply_markup=menulvl1_kb)
        elif CheckLevelAdmin(message.from_user.id) > 1:
            await message.answer(f"🔮 No sticker packs left!", reply_markup=menulvl2_kb)



@dp.message_handler(state=Form.AddUser)
async def process_name(message: types.Message, state: FSMContext):
    if (message.text.lower() != '/exit'):
        textelemrnts = message.text.split(" - ")
        Name = textelemrnts[0]
        UserID = int(textelemrnts[1])
        Level = int(textelemrnts[2])
        await message.answer(AddAdmin(Name, UserID, Level, message.from_user.id))
    else:
        await message.answer(f"Bye")
    await state.finish()

@dp.message_handler(state=Form.DelUser)
async def process_name(message: types.Message, state: FSMContext):
    if (message.text.lower() != '/exit'):
        await message.answer(DeleteAdmin(message.text, message.from_user.id))
    else:
        await message.answer(f"Bye")
    await state.finish()


@dp.message_handler(state=Form.ChangeUser)
async def process_name(message: types.Message, state: FSMContext):
    if (message.text.lower() != '/exit'):
        text = message.text.split(' - ')
        await message.answer(ChangeLevelAdmin(text[0], text[1]))
    else:
        await message.answer(f"Bye")
    await state.finish()


# Кнопки Main menu lvl 1
button_Start = KeyboardButton('Start')
button_AllStickers = KeyboardButton('All Stickers')
button_CountCategory = KeyboardButton('Count Category')
menulvl1_kb = ReplyKeyboardMarkup(resize_keyboard=True)
menulvl1_kb.row(button_Start).add(button_AllStickers, button_CountCategory)


# Кнопки Main menu lvl 2
button_Start = KeyboardButton('Start')
button_AllStickers = KeyboardButton('All Stickers')
button_CountCategory = KeyboardButton('Count Category')
button_AdminPanel = KeyboardButton('Manage users')
menulvl2_kb = ReplyKeyboardMarkup(resize_keyboard=True)
menulvl2_kb.row(button_Start).add(button_AllStickers, button_CountCategory).row(button_AdminPanel)


# Кнопки Admin menu lvl 3
button_AddUser = KeyboardButton('Add user')
button_DeleteUser = KeyboardButton('Delete user')
button_ChangeLevel = KeyboardButton('Change user level')
button_GoBack = KeyboardButton('Go back')
adminMenulvl3_kb = ReplyKeyboardMarkup(resize_keyboard=True)
adminMenulvl3_kb.add(button_AddUser, button_DeleteUser).row(button_ChangeLevel).row(button_GoBack)


# Кнопки Admin menu lvl 2
adminMenulvl2_kb = ReplyKeyboardMarkup(resize_keyboard=True)
adminMenulvl2_kb.add(button_AddUser, button_DeleteUser).row(button_GoBack)

# Кнопки select
button_Accept = KeyboardButton('✅')
button_Cansel = KeyboardButton('❌')
work_kb = ReplyKeyboardMarkup(resize_keyboard=True)
work_kb.add(button_Accept, button_Cansel)

# Кнопки add
selectButtons = InlineKeyboardMarkup(row_width=1)
selectAnimeButton = InlineKeyboardButton(text='Anime', callback_data='Count Anime')
selectCuteCatsButton = InlineKeyboardButton(text='Cute cats', callback_data='Count Cute cats')
selectMemeButton = InlineKeyboardButton(text='Meme', callback_data='Count Meme')
selectButtons.add(selectAnimeButton, selectCuteCatsButton, selectMemeButton)




if __name__ == '__main__':
    executor.start_polling(dp)
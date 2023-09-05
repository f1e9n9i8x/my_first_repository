from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from random import randint

from data_bota import token

BOT_TOKEN = token
bot: Bot = Bot(BOT_TOKEN)
dp: Dispatcher = Dispatcher()
ATTEMPS: int = 5
users: dict = {}


def get_random_number() -> int:
    return randint(1, 100)


@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer('Здарова!\nИгра угадай число\n\n'
                         'Помощь - /help\n\n'
                         "Напиши 'да' для начала игры"
                         "Если не хочешь играть, напиши 'нет'")
    if message.from_user.id not in users:
        users[message.from_user.id] = {'is_in_game': False,
                                       'secret_number': None,
                                       'attemps': None,
                                       'total_game': 0,
                                       'wins': 0}
        

@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer("Правила игры: Генерируется число от 1 до 100\n"
                         f"Его нужно угадать за {ATTEMPS} попыток\n\n"
                         "Команды:\n"
                         "Правила - /help\nСтатистика игр - /stat\nПрервать игру - /cancel")


@dp.message(Command(commands=['stat']))
async def process_stat_command(message: Message):
    await message.answer(f"Общее колличество игр: {users[message.from_user.id]['total_game']}\n"
                         f"Колличество побед: {users[message.from_user.id]['wins']}")
    

@dp.message(Command(commands=['cancel']))
async def process_cancel_command(message: Message):
    if not users[message.from_user.id]['is_in_game']:
        await message.answer("Ты не в игре\n\n"
                             "Напиши 'да', для начала игры")
    else:
        users[message.from_user.id]['is_in_game'] = False
        users[message.from_user.id]['total_game'] += 1
        await message.answer("Ты закончил игру\n\n"
                            "Если хочешь начать занова, напиши 'да'")
        

@dp.message(F.text.lower().in_(['да']))
async def process_yes(message: Message):
    if users[message.from_user.id]['is_in_game']:
        await message.answer("Ты уже в игре\n"
                             "Помощь - /help\n"
                             "Напиши цифру от 1 до 100")
    else:
        users[message.from_user.id]['is_in_game'] = True
        users[message.from_user.id]['secret_number'] = get_random_number()
        users[message.from_user.id]['attemps'] = ATTEMPS
        await message.answer("Ты в игре!\n"
                      "Введи число от 1 до 100")
    print(users)


@dp.message(F.text.lower().in_(['нет']))
async def process_no(message: Message):
    if users[message.from_user.id]['is_in_game']:
        await message.answer("Ты в игре\n"
                             "Помощь /help\n"
                             "Введите число от 1 до 100")
    else:
        await message.answer("Как хочешь\n"
                             "Пиши 'да', если  захочешь\n"
                             "Помощь - /help")


@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_number_answer(message: Message):
    if not users[message.from_user.id]['is_in_game']:
        await message.answer("Вы не играете\n\n"
                             "Напишите 'да' для начала игры")
    else:
            users[message.from_user.id]['attemps'] -= 1

            if int(message.text) == users[message.from_user.id]['secret_number']:
                users[message.from_user.id]['is_in_game'] = False
                users[message.from_user.id]['total_game'] += 1
                users[message.from_user.id]['wins'] += 1
                await message.answer("Ты победил\n"
                                     "Напиши 'да' для начала новой игры")
            elif int(message.text) > users[message.from_user.id]['secret_number']:
                await message.answer('Число меньше')
            elif int(message.text) < users[message.from_user.id]['secret_number']:
                await message.answer('Число больше')
            
            if users[message.from_user.id]['attemps'] == 0:
                users[message.from_user.id]['is_in_game'] = False
                users[message.from_user.id]['total_game'] += 1
                await message.answer("Попытки закончились. Ты проиграл\n"
                                     "Напиши 'да' для начала новой игры")
                

@dp.message()
async def process_other_answers(message: Message):
    if users[message.from_user.id]['is_in_game']:
        await message.answer('Ты в игре. Пришли число от 1 до 100')
    else:
        await message.answer('Я не знаю, что тебе на это ответить')
        
        










if __name__ == '__main__':
    dp.run_polling(bot)
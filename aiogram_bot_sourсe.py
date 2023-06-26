from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from TGtoken import read_token
import time

parse_state = True

try:
    async def bot_start():

        class add_link(StatesGroup):
            state_add = State()

        memory_storage = MemoryStorage()
        bot = Bot(token=read_token)
        dp = Dispatcher(bot, storage=memory_storage)

        @dp.message_handler(commands=['start'])
        async def start(message: types.Message):
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = ['Получить последние посты', 'Авто парсинг', 'Добавить каналы', 'список добавленных каналов']
            keyboard.add(*buttons)
            await message.answer('Привет, это бот парсер тг каналов\nЯ могу собирать из определенных каналов все последний посты', reply_markup=keyboard)

        @dp.message_handler(Text(equals='Получить последние посты'))
        async def start(message: types.Message):
            await message.answer('Собираю данные ждите')
            from parse_func import start_parse
            for i in start_parse():
                await message.answer(i)
        
        @dp.message_handler(commands=['stop'])
        async def stop(message: types.Message):
            global parse_state
            parse_state = False
            await message.answer('Авто парсинг остановлен')
        
        @dp.message_handler(Text(equals='Авто парсинг'))
        async def auto_parsing(message: types.Message):
            await message.answer('Авто парсинг запущен, я буду кидать новые посты по мере их появлений с добавленных каналов, для остановки автопарсинга напишите команду /stop')
            from Real_time_cheker import real_t_chek
            global parse_state
            parse_state = True
            while True:
                if not parse_state:
                    break
                await message.answer(real_t_chek())

        @dp.message_handler(Text(equals='Добавить каналы'), state=None)
        # @dp.message_handler(commands='add', state=None)
        async def add_link_func(message: types.Message):
            await message.answer('Введите список каналов через пробел, пример chanel1 chanel2 и отправьте')
            # await state.set_state(add_link.state_add.state)
            await add_link.state_add.set()

        @dp.message_handler(state=add_link.state_add)
        async def state_add(message: types.Message, state: FSMContext):
            msg_txt = message.text
            await message.answer(msg_txt + ' канал\лы добавлены\n чтобы удалить каналы напишите команду /drop')
            with open('tg_chanels.txt', 'w') as file:
                file.writelines(msg_txt)
            await state.finish()

        @dp.message_handler(commands=['drop'])
        async def drop(message: types.Message):
            from drop_chanels import drop_func
            drop_func()
            await message.answer('Каналы очищены')

        @dp.message_handler(Text(equals='список добавленных каналов'))
        async def chek_chanels(message: types.Message):
            from read_chanels import read_chanels_func
            if read_chanels_func() == '':
                await message.answer('Ваш список каналов пуст')
            else:
                await message.answer('Ваш список каналов, убедитесь что каждый канал должен начинатся с пробела ' + read_chanels_func())

        @dp.message_handler(commands=['help'])
        async def help_list(message: types.Message):
            await message.answer('Список команд\n'
                                '/start команда старта\n'
                                '/drop очистка списка каналов\n' 
                                '/help список команд\n'
                                '/stop остановить авто парсинг\n')  
        await dp.start_polling()

    print('Бот запущен')

except Exception as Ex:
    print('Ошибка запуска бота')
    
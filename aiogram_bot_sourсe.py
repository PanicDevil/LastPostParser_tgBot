from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from TGtoken import read_token
import time

try:
    async def bot_start():
        memory_storage = MemoryStorage()
        bot = Bot(token=read_token)
        dp = Dispatcher(bot, storage=memory_storage)

        @dp.message_handler(commands=['start'])
        async def start(message: types.Message):
            await message.answer('Привет, это бот парсер тг каналов\nЯ могу собирать из определенных каналов все последний посты')

        @dp.message_handler(commands=['parse'])
        async def start(message: types.Message):
            from parse_func import start_parse
            for i in start_parse():
                await message.answer(i)
        
        # @dp.message_handler(commands=['set_timer'])
        # async def set_timer_func(message: types.Message):
        #     for i in start_parse():
                
        #         print(chanels_mem)
                # await message.answer(i)
                # time.sleep(10)
                

        class add_link(StatesGroup):
            state_add = State()

        @dp.message_handler(commands=['add'], state=None)
        async def add_link_func(message: types.Message):
            await message.answer('Введите список каналов через пробел, пример chanel1 chanel2')
            # await state.set_state(add_link.state_add.state)
            await add_link.state_add.set()

        @dp.message_handler(state=add_link.state_add)
        async def state_add(message: types.Message, state: FSMContext):
            msg_txt = message.text
            await message.answer(msg_txt + ' канал\лы добавлены\n Для начала парсинга напишите команду /parse')
            with open('tg_chanels.txt', 'w') as file:
                file.writelines(msg_txt)
            await state.finish()

        @dp.message_handler(commands=['drop'])
        async def drop(message: types.Message):
            from drop_chanels import drop_func
            drop_func()
            await message.answer('Каналы очищены\nДля добавления каналов напишите команду /add')

        @dp.message_handler(commands=['chek'])
        async def chek_chanels(message: types.Message):
            from read_chanels import read_chanels_func
            await message.answer('Ваш список каналов, убедитесь что каждый канал должен начинатся с пробела ' + read_chanels_func())

        @dp.message_handler(commands=['help'])
        async def help_list(message: types.Message):
            await message.answer('Список команд\n'
                                '/start команда старта\n'
                                '/add добавление списка каналов\n'
                                '/parse вывод последних постов из всех добавленных каналов\n'
                                '/drop очистка списка каналов\n'
                                '/chek список добавленных каналов\n' 
                                '/help очистка списка каналов\n')  
        await dp.start_polling()

    print('Бот запущен')

except Exception as Ex:
    print('Ошибка запуска бота')
    
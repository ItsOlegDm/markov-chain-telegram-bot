import markovify
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineQuery, InlineQueryResultArticle
from config import *
import random
model = markovify.NewlineText.from_json(open('model.json', 'r', encoding='utf-8').read())
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['hey', 'start'])
async def process_help_command(message: types.Message):
    await message.reply(model.make_short_sentence(300))
@dp.message_handler(commands=['tag'])
async def process_help_command(message: types.Message):
    args = message.get_args()
    if args == "":
        await message.reply(f'Please provide username, !without @!')
    else:
        await bot.send_message(message["chat"]["id"], f"@{args} {model.make_short_sentence(300)}")
        try:
             await bot.delete_message(message["chat"]["id"], message["message_id"])
        except:
             pass
@dp.message_handler()
async def process_help_command(message: types.Message):
    print(message)
    if "reply_to_message" in message:
        if message["reply_to_message"]["from"]["id"] == USER_ID:
            if random.randint(1, 20) == 1:
                await message.reply(model.make_short_sentence(300)) 
        elif message["reply_to_message"]["from"]["username"] == BOT_USERNAME:
            await message.reply(model.make_short_sentence(300))
    
    elif BOT_USERNAME in message["text"]:
            await message.reply(model.make_short_sentence(300))     
    else:
        if random.randint(1, 50) == 1:
                await message.reply(model.make_short_sentence(300))
@dp.inline_handler()
async def inline_echo(inline_query: InlineQuery):
    text = inline_query.query or "null"
    if text == "null":
        res = []
        res = [InlineQueryResultArticle(
            id= 0,
            title= "Say something",
            input_message_content= {"message_text": model.make_short_sentence(300)},
        )]
    await bot.answer_inline_query(inline_query.id, results=res, cache_time=1, )

if __name__ == '__main__':
    executor.start_polling(dp) 
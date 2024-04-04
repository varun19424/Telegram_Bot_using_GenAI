from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
import logging
import openai


load_dotenv()
API_TOKEN = os.getenv("TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Connect with OpenAI

openai.api_key = OPENAI_API_KEY
# print("ok")


MODEL_NAME = "gpt-3.5-turbo"

# Initialize the Bot

bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher(bot)

class Reference:
    def __init__(self) -> None:
        self.response = ""
    
reference = Reference()

def clear_past():
    reference.reference = ""

@dispatcher.message_handler(commands=['clear'])
async def clear(message: types.Message):
    """A hander to clear the previous conversation.
        """
    await message.reply("I have clear the pas conversation and context")


@dispatcher.message_handler(commands=['start'])
async def command_start_handeler(message: types.Message):
    """This handler receives messages with `/start` or `/help` command
        Args:
            message:( types.Message): _description_
        """
    await message.reply("Hi! \n I am an Chat Bot! Created by Varun. How can I assist you?")


@dispatcher.message_handler(commands=['help'])
async def helper(message: types.Message):
    """A handler to display the help menu.
    """
    help_command = """
    Hi There, I'm a bot created by Bappy! Please follow these commands - 
    /start - to start the conversation
    /clear - to clear the past conversation and context.
    /help - to get this help menu.
    I hope this helps. :)
        """
    await message.reply(help_command)


    await message.reply("Hi! \n I am an Chat Bot! Created by Varun. How can I assist you?")


@dispatcher.message_handler()
async def main_bot(message: types.Message):
    """
        A handler to process the user's input and generate a response using the openai API.
    """
    print(f">>> USER: \n\t{message.text}")

    response = openai.ChatCompletion.create(
        model = MODEL_NAME,
        messages = [
            {"role": "assistant", "content": reference.response}, # role assistant
            {"role": "user", "content": message.text} #our query 
        ]
    )
    reference.response = response['choices'][0]['message']['content']
    print(f">>> chatGPT: \n\t{reference.response}")
    await bot.send_message(chat_id = message.chat.id, text = reference.response)


if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=True)
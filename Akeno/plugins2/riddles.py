import google.generativeai as genai
from pyrogram import Client, filters
from pyrogram.types import Message

GOOGLE_API_KEY = "AIzaSyBZr5CYt5bhIsRz6KTDlclM3hLBbgwSGq0"

genai.configure(api_key=GOOGLE_API_KEY)

# Define target chat and channel IDs
TARGET_CHAT_ID = [-1002214107507,-1002190474758]
TARGET_CHANNEL_ID = [-1002212156629,-1002148723094]

def chatgpt(query):
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model_flash = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction="You are a helpful assistant.",
            safety_settings={
                genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: genai.types.HarmBlockThreshold.BLOCK_NONE,
                genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT: genai.types.HarmBlockThreshold.BLOCK_NONE,
                genai.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: genai.types.HarmBlockThreshold.BLOCK_NONE,
                genai.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: genai.types.HarmBlockThreshold.BLOCK_NONE,
            }
        )
        chat_session = model_flash.start_chat(history=[])
        response_data = chat_session.send_message(query)
        output = response_data.text
        return output
    except Exception as e:
        return str(e)

async def is_riddle_detected(query):
    """Ask the AI if the given query is a riddle."""
    response = chatgpt(f"Is this a riddle? '{query}' Please answer with 'yes' or 'no'.")
    return response.strip().lower() == 'yes'

@Client.on_message(filters.chat(TARGET_CHAT_ID) & ~filters.service & ~filters.bot, group=-2)
async def reply_to_message(client: Client, message: Message):
    if message.sender_chat and message.sender_chat.id in TARGET_CHANNEL_ID:
        if message.text and '?' in message.text:  # Check if the message contains a question mark
            # Ask the AI to detect if the message is a riddle
            is_riddle_answer = await is_riddle_detected(message.text)

            if is_riddle_answer:
                riddle = f"{message.text.strip()} give answer only"

                # Get the AI's response to the riddle
                answer = chatgpt(riddle)  # Using the new chatgpt function

                # Reply to the riddle in the comments (as a reply to the original message)
                await message.reply_text(answer)  # This will post as a comment in the channel
        else:
            return None  # Do nothing if the conditions are not met

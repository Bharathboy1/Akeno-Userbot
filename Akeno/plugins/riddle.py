import google.generativeai as genai
from pyrogram import Client, filters
from pyrogram.types import Message


GOOGLE_API_KEY = "AIzaSyBZr5CYt5bhIsRz6KTDlclM3hLBbgwSGq0"



genai.configure(api_key=GOOGLE_API_KEY)


TARGET_CHAT_ID = [-1002068064532, -1002214107507]
TARGET_CHANNEL_ID = [-1002195132204, -1002212156629]

def is_riddle(text):
    """Check if the message contains a riddle."""
    keywords = ["riddle", "I am", "what am I", "guess", "solve"]  # Keywords to detect riddles
    return any(keyword in text.lower() for keyword in keywords)

async def solve_riddle(riddle):
    """Send the riddle to the AI and get the answer."""
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.chat(riddle)
    return response.messages[0]['content'] if response else "Sorry, I couldn't solve this riddle."


@Client.on_message(filters.chat(TARGET_CHAT_ID) & ~filters.service & ~filters.bot, group=-2)
async def reply_to_message(client: Client, message: Message):
    if message.sender_chat and message.sender_chat.id in TARGET_CHANNEL_ID:
        if message.text and is_riddle(message.text):
            riddle = message.text.strip()
            print(f"Riddle detected: {riddle}")

            
            answer = await solve_riddle(riddle)
            print(f"Answer: {answer}")

            
            await message.reply_text(answer)
        else:
            print("Message is not a riddle, ignoring.")


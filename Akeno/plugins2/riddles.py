import google.generativeai as genai
from pyrogram import Client, filters
from pyrogram.types import Message


GOOGLE_API_KEY = "AIzaSyBZr5CYt5bhIsRz6KTDlclM3hLBbgwSGq0"



genai.configure(api_key=GOOGLE_API_KEY)

# Define target chat and channel IDs
TARGET_CHAT_ID = [-1002068064532, -1002214107507]
TARGET_CHANNEL_ID = [-1002195132204, -1002212156629]

def is_riddle(text):
    """Check if the message contains a riddle."""
    keywords = ["riddle", "I am", "what am I", "guess", "solve"]  # Keywords to detect riddles
    return any(keyword in text.lower() for keyword in keywords)

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

@Client.on_message(filters.chat(TARGET_CHAT_ID) & ~filters.service & ~filters.bot, group=-2)
async def reply_to_message(client: Client, message: Message):
    if message.sender_chat and message.sender_chat.id in TARGET_CHANNEL_ID:
        if message.text and is_riddle(message.text):
            riddle = f"{message.text.strip()} give answer only"
            print(f"Riddle detected: {riddle}")

            # Get the AI's response to the riddle
            answer = chatgpt(riddle)  # Using the new chatgpt function
            print(f"Answer: {answer}")

            # Reply to the riddle in the comments (as a reply to the original message)
            await message.reply_text(answer)  # This will post as a comment in the channel
        else:
            print("Message is not a riddle, ignoring.")


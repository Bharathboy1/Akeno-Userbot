import re
import random
import string
from pyrogram import Client, filters
from pyrogram.types import Message

# Constants for target chat and channel IDs
TARGET_CHAT_ID = [-1002068064532, -1002214107507]
TARGET_CHANNEL_ID = [-1002195132204, -1002212156629]
client_reply_messages = {
    "two": "UQAXRBHAaTZcyRgVN54K8FqnAS9ZnhLT8NOhV36EHUtrpCQi",
    "one": "UQBqAubq2phpLyOXyQT4twxryLsWZFIJ437gwLhvohAc18kq",
    "three": "UQAwSUTZe3FZXbCdz8fCbqyvoHKEE5r-2k93dO7X_eXsic91",
    "four": "UQDoiTdMCqHvV93tGiCeHW4s5ULnFPnjpkC0tZbOyi_IAEJR",
    "five": "UQDVAvu6YJcm5E90OGD6FGaqmakDCS8QdMeJXW13DsOFdNsH",
    "six": "UQA89uwzmb0kjzzQunF-NH0G7pQvVj2k5awqWduQKOyTiw96",
    "sev": "UQAcpGyz8ciRwYMBQIwT7cHrrmaPgAKNMF95PG-qaPc-hpEA", #"UQDmw_yd95yWYjFnPnHZgFmgfslqNjI9qUp3_NTN_KuX0fSi",
    "eig": "UQB1jY2VVGR9g0nHbLnBm6xiJjstGsyGkjy_SPVzMocXJWIj",#"UQDkUJr4Otn4is--C26zmhvg7mEWRooHv7urvom93gBrZ_80",
    "nin": "", 
    "ten": ""   
}

# Optimized list of target patterns with non-capturing groups
TARGET_PATTERNS = [
    r"Drop your TON wallet address",
    r"giving away \d+(?:\.\d+)?(?: TON)?",
    r"\d+(?:\.\d+)?(?: first comments| first \d+(?:\.\d+)? comments)",
    r"\bTON\b",  # Use word boundary to avoid partial matches
    r"\bton\b"  # Use word boundary to avoid partial matches
]

@Client.on_message(filters.chat(TARGET_CHAT_ID) & ~filters.service & ~filters.bot, group=-1)
async def reply_to_message(client: Client, message: Message):
    try:
        # Check if the message contains text or a caption
        content = message.text or message.caption
        if not content:
            return  # Ignore if there's no content to process

        # Check if the content matches any of the target patterns with case-insensitive search
        if any(re.search(pattern, content, re.IGNORECASE) for pattern in TARGET_PATTERNS):
            if message.sender_chat and message.sender_chat.id in TARGET_CHANNEL_ID:  # Fix the condition to check in list
                chars = string.ascii_letters + string.digits
                random_char = random.choice(chars)
            
                client_name = next((name for name in client_reply_messages if client.name == name), None)
                if client_name:
                    reply_message = client_reply_messages.get(client_name, f"{random_char}")
                    if reply_message:  # Avoid sending empty replies
                        await message.reply_text(reply_message)
    except Exception as e:
        # Handle and log the exception
        print(f"An error occurred: {e}")

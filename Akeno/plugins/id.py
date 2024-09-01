import asyncio
import os
import random
import time

from pyrogram import Client, filters
from pyrogram.errors import ChannelInvalid
from pyrogram.types import Message

from Akeno.utils.handler import Akeno
from config import CMD_HANDLER

@Akeno(
    ~filters.scheduled
    & filters.command(["id"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def get_id(bot: Client, message: Message):
    file_id = None
    user_id = None
    user_detail = ""

    if message.reply_to_message:
        rep = message.reply_to_message
        if rep.audio:
            file_id = f"**File ID**: `{rep.audio.file_id}`\n**File Type**: `audio`"
        elif rep.document:
            file_id = f"**File ID**: `{rep.document.file_id}`\n**File Type**: `{rep.document.mime_type}`"
        elif rep.photo:
            file_id = f"**File ID**: `{rep.photo.file_id}`\n**File Type**: `photo`"
        elif rep.sticker:
            file_id = f"**Sticker ID**: `{rep.sticker.file_id}`\n"
            file_id += f"**Sticker Set**: `{rep.sticker.set_name or 'None'}`\n"
            file_id += f"**Sticker Emoji**: `{rep.sticker.emoji or 'None'}`\n"
            file_id += f"**Animated Sticker**: `{rep.sticker.is_animated}`\n"
            file_id += f"**Video Sticker**: `{rep.sticker.is_video}`\n"
            file_id += f"**Premium Sticker**: `{rep.sticker.is_premium}`\n"
        elif rep.video:
            file_id = f"**File ID**: `{rep.video.file_id}`\n**File Type**: `video`"
        elif rep.animation:
            file_id = f"**File ID**: `{rep.animation.file_id}`\n**File Type**: `GIF`"
        elif rep.voice:
            file_id = f"**File ID**: `{rep.voice.file_id}`\n**File Type**: `Voice Note`"
        elif rep.video_note:
            file_id = f"**File ID**: `{rep.video_note.file_id}`\n**File Type**: `Video Note`"
        elif rep.location:
            file_id = f"**Location**:\n**longitude**: `{rep.location.longitude}`\n**latitude**: `{rep.location.latitude}`"
        elif rep.venue:
            file_id = f"**Location**:\n**longitude**: `{rep.venue.location.longitude}`\n**latitude**: `{rep.venue.location.latitude}`\n\n"
            file_id += f"**Address**:\n**title**: `{rep.venue.title}`\n**detailed**: `{rep.venue.address}`\n\n"
        elif rep.from_user:
            user_id = rep.from_user.id

        if user_id:
            if rep.forward_from:
                user_detail = f"**Forwarded User ID**: `{rep.forward_from.id}`\n"
            elif rep.forward_from_chat:
                user_detail = (
                    f"**Forwarded Channel ID**: `{rep.forward_from_chat.id}`\n"
                    f"**Forwarded Channel Title**: `{rep.forward_from_chat.title}`\n"
                    f"**Forwarded Channel Username**: `@{rep.forward_from_chat.username or 'None'}`\n"
                )
            else:
                user_detail = f"**User ID**: `{rep.from_user.id}`\n"
            user_detail += f"**Message ID**: `{rep.id}`"
            await message.edit_text(user_detail)
        elif file_id:
            if rep.forward_from:
                user_detail = f"**Forwarded User ID**: `{rep.forward_from.id}`\n"
            else:
                user_detail = (
                    f"**User ID**: `{rep.from_user.id or 'None'}`\n"
                    f"**Sender Chat ID**: `{rep.sender_chat.id if rep.sender_chat else 'None'}`\n"
                    f"**Sender Chat Title**: `{rep.sender_chat.title if rep.sender_chat else 'None'}`\n"
                    f"**Sender Chat Username**: `@{rep.sender_chat.username if rep.sender_chat else 'None'}`\n"
                )
            user_detail += f"**Message ID**: `{rep.id}`\n\n"
            user_detail += file_id
            try:
                await message.reply_text(user_detail)
            except ChannelInvalid:
                await message.reply_text("Channel Invalid")
            except Exception as e:
                await message.reply_text(f"Error: {e}")
        else:
            await message.reply_text(f"**Chat ID**: `{message.chat.id}`")

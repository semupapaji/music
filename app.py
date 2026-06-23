# audio_bot.py
import os
import json
import logging
import aiohttp
import asyncio
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from telegram.constants import ParseMode

# ============ CONFIG ============
BOT_TOKEN = "8870758259:AAFw__OmkcH1L8yrmFBXzKnVvq3NnlwK2Wg"  # @BotFather se lo
OWNER_ID = 7326248826  # Apna Telegram ID
API_URL = "https://r-gengpt-api.vercel.app/api/video/download?url={url}"
DATA_FILE = "user_data.json"
VERIFIED_USERS_FILE = "verified_users.json"

# ============ CHANNELS ============
CHANNELS = [
    {
        "id": "-1003849265448", 
        "link": "https://t.me/SEMY_FF",
        "name": "MAIN CHANNEL"
    },
    {
        "id": "-1003885062938", 
        "link": "https://t.me/+n0W7fc-r35JjNDRl",
        "name": "📢 SEMY BOT"
    }
]

# ============ LOGGING ============
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============ DATA FUNCTIONS ============
def load_data():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        return {"users": []}
    except:
        return {"users": []}

def save_data(data):
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except:
        pass

def load_verified():
    try:
        if os.path.exists(VERIFIED_USERS_FILE):
            with open(VERIFIED_USERS_FILE, 'r') as f:
                return json.load(f)
        return {"verified": []}
    except:
        return {"verified": []}

def save_verified(data):
    try:
        with open(VERIFIED_USERS_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except:
        pass

def add_user(user_id):
    data = load_data()
    if user_id not in data["users"]:
        data["users"].append(user_id)
        save_data(data)

def add_verified(user_id):
    data = load_verified()
    if user_id not in data["verified"]:
        data["verified"].append(user_id)
        save_verified(data)

def remove_verified(user_id):
    data = load_verified()
    if user_id in data["verified"]:
        data["verified"].remove(user_id)
        save_verified(data)

def is_verified(user_id):
    data = load_verified()
    return user_id in data["verified"]

# ============ FORCE JOIN FUNCTIONS ============
async def check_user_joined(user_id, context):
    """Check if user has joined all channels"""
    try:
        for channel in CHANNELS:
            try:
                member = await context.bot.get_chat_member(
                    chat_id=channel["id"], 
                    user_id=user_id
                )
                if member.status in ['left', 'kicked']:
                    return False
            except Exception as e:
                logger.error(f"Error checking channel {channel['id']}: {e}")
                # If can't check, assume not joined
                return False
        return True
    except:
        return False

async def show_join_channels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show join channels message with horizontal buttons"""
    # Create horizontal buttons for channels
    keyboard = []
    
    # Channel buttons in horizontal rows (2 per row)
    row = []
    for i, channel in enumerate(CHANNELS):
        row.append(InlineKeyboardButton(
            channel["name"], 
            url=channel["link"]
        ))
        if len(row) == 2 or i == len(CHANNELS) - 1:
            keyboard.append(row)
            row = []
    
    # Verify button (full width)
    keyboard.append([InlineKeyboardButton(
        "✅ ᴠᴇʀɪꜰʏ", 
        callback_data="verify"
    )])
    
    await update.message.reply_text(
        "🔐 *ᴊᴏɪɴ ʀᴇQᴜɪʀᴇᴅ ᴄʜᴀɴɴᴇʟꜱ*\n\n"
        "• ᴛᴏ ᴜꜱᴇ ᴛʜɪꜱ ʙᴏᴛ, ʏᴏᴜ ᴍᴜꜱᴛ ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟꜱ\n"
        "• ᴄʟɪᴄᴋ ᴇᴀᴄʜ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ᴊᴏɪɴ\n"
        "• ᴀꜰᴛᴇʀ ᴊᴏɪɴɪɴɢ, ᴄʟɪᴄᴋ ᴠᴇʀɪꜰʏ\n\n"
        "📌 *ʀᴇQᴜɪʀᴇᴅ ᴄʜᴀɴɴᴇʟꜱ:*",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def show_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show welcome message after verification"""
    welcome_text = (
        "🎵 *ᴀᴜᴅɪᴏ ᴅᴏᴡɴʟᴏᴀᴅᴇʀ ʙᴏᴛ*\n\n"
        "✅ *ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ!*\n\n"
        "📤 ꜱᴇɴᴅ ᴍᴇ ᴀɴʏ ʟɪɴᴋ ꜰʀᴏᴍ:\n"
        "• ʏᴏᴜᴛᴜʙᴇ 🎬\n"
        "• ɪɴꜱᴛᴀɢʀᴀᴍ 📸\n"
        "• ꜰᴀᴄᴇʙᴏᴏᴋ 📘\n\n"
        "ɪ ᴡɪʟʟ ꜱᴇɴᴅ ʏᴏᴜ ᴛʜᴇ ᴀᴜᴅɪᴏ! 🎧"
    )
    
    # Check if it's a callback query or message
    if update.callback_query:
        await update.callback_query.message.reply_text(
            welcome_text,
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await update.message.reply_text(
            welcome_text,
            parse_mode=ParseMode.MARKDOWN
        )

async def handle_verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle verify button"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    # Show verifying status
    await query.message.edit_text(
        "⏳ *ᴠᴇʀɪꜰʏɪɴɢ...*",
        parse_mode=ParseMode.MARKDOWN
    )
    
    joined = await check_user_joined(user_id, context)
    
    if joined:
        add_verified(user_id)
        await query.message.delete()
        await show_welcome(update, context)
    else:
        await query.message.edit_text(
            "❌ *ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ꜰᴀɪʟᴇᴅ!*\n\n"
            "ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ ᴊᴏɪɴᴇᴅ ᴀʟʟ ᴄʜᴀɴɴᴇʟꜱ ʏᴇᴛ.\n\n"
            "ᴘʟᴇᴀꜱᴇ ᴊᴏɪɴ ᴀʟʟ ᴄʜᴀɴɴᴇʟꜱ ᴀɴᴅ ᴄʟɪᴄᴋ ᴠᴇʀɪꜰʏ ᴀɢᴀɪɴ.",
            parse_mode=ParseMode.MARKDOWN
        )
        # Show join channels again
        await show_join_channels(update, context)

async def check_verification_and_handle(update: Update, context: ContextTypes.DEFAULT_TYPE, is_callback=False):
    """Check verification and handle accordingly"""
    user_id = update.effective_user.id
    
    # First check if user is in channels
    joined = await check_user_joined(user_id, context)
    
    if joined:
        # User is in channels, add to verified if not already
        add_verified(user_id)
        return True
    else:
        # User is not in channels, remove from verified if exists
        remove_verified(user_id)
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    add_user(user_id)
    
    # Check if user is already in channels
    joined = await check_user_joined(user_id, context)
    
    if joined:
        # User is in channels, add to verified and show welcome
        add_verified(user_id)
        await show_welcome(update, context)
    else:
        # User is not in channels, remove from verified and show join buttons
        remove_verified(user_id)
        await show_join_channels(update, context)

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    add_user(user_id)
    
    # Check if user is in channels
    joined = await check_user_joined(user_id, context)
    
    if not joined:
        # User left channel, remove verification and show join buttons
        remove_verified(user_id)
        await show_join_channels(update, context)
        return
    
    # User is joined, ensure verified status
    add_verified(user_id)
    
    text = update.message.text.strip()
    
    # Check if it's a link
    if not text.startswith(('http://', 'https://')):
        await update.message.reply_text(
            "❌ *ᴘʟᴇᴀꜱᴇ ꜱᴇɴᴅ ᴀ ᴠᴀʟɪᴅ ʟɪɴᴋ!*\n\n"
            "ꜱᴜᴘᴘᴏʀᴛᴇᴅ:\n"
            "• ʏᴏᴜᴛᴜʙᴇ: ʏᴏᴜᴛᴜʙᴇ.ᴄᴏᴍ, ʏᴏᴜᴛᴜ.ʙᴇ\n"
            "• ɪɴꜱᴛᴀɢʀᴀᴍ: ɪɴꜱᴛᴀɢʀᴀᴍ.ᴄᴏᴍ\n"
            "• ꜰᴀᴄᴇʙᴏᴏᴋ: ꜰᴀᴄᴇʙᴏᴏᴋ.ᴄᴏᴍ, ꜰʙ.ᴡᴀᴛᴄʜ",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Check platform
    platform = None
    platform_emoji = ""
    if 'youtube.com' in text or 'youtu.be' in text:
        platform = "YouTube"
        platform_emoji = "🎬"
    elif 'instagram.com' in text:
        platform = "Instagram"
        platform_emoji = "📸"
    elif 'facebook.com' in text or 'fb.watch' in text:
        platform = "Facebook"
        platform_emoji = "📘"
    else:
        await update.message.reply_text(
            "❌ *ᴜɴꜱᴜᴘᴘᴏʀᴛᴇᴅ ʟɪɴᴋ!*\n\n"
            "ᴏɴʟʏ ʏᴏᴜᴛᴜʙᴇ, ɪɴꜱᴛᴀɢʀᴀᴍ, ᴀɴᴅ ꜰᴀᴄᴇʙᴏᴏᴋ ᴀʀᴇ ꜱᴜᴘᴘᴏʀᴛᴇᴅ.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Send processing message
    msg = await update.message.reply_text(
        f"⏳ *ᴘʀᴏᴄᴇꜱꜱɪɴɢ* {platform_emoji} *{platform} ʟɪɴᴋ...*\n\n"
        "ꜰᴇᴛᴄʜɪɴɢ ᴀᴜᴅɪᴏ...",
        parse_mode=ParseMode.MARKDOWN
    )
    
    try:
        # Fetch data from API
        api_url = API_URL.format(url=text)
        
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, timeout=6000) as response:
                if response.status != 200:
                    await msg.edit_text(
                        "❌ *ꜰᴀɪʟᴇᴅ ᴛᴏ ꜰᴇᴛᴄʜ!*\n\n"
                        "ᴘʟᴇᴀꜱᴇ ᴛʀʏ ᴀɢᴀɪɴ.",
                        parse_mode=ParseMode.MARKDOWN
                    )
                    return
                
                data = await response.json()
                
                if data.get('status') != 'success':
                    await msg.edit_text(
                        "❌ *ꜰᴀɪʟᴇᴅ ᴛᴏ ꜰᴇᴛᴄʜ!*\n\n"
                        "ᴘʟᴇᴀꜱᴇ ᴛʀʏ ᴀɢᴀɪɴ.",
                        parse_mode=ParseMode.MARKDOWN
                    )
                    return
                
                video_data = data.get('data', {})
                title = video_data.get('title', 'Audio')
                medias = video_data.get('medias', [])
                
                # Find audio
                audio_url = None
                best_quality = 0
                
                for media in medias:
                    if media.get('type') == 'audio':
                        bitrate = media.get('bitrate', 0)
                        url = media.get('url')
                        if url and bitrate > best_quality:
                            best_quality = bitrate
                            audio_url = url
                
                # If no dedicated audio, try video with audio
                if not audio_url:
                    for media in medias:
                        if media.get('type') == 'video' and media.get('is_audio', False):
                            url = media.get('url')
                            if url:
                                audio_url = url
                                break
                
                if not audio_url:
                    await msg.edit_text(
                        "❌ *ɴᴏ ᴀᴜᴅɪᴏ ꜰᴏᴜɴᴅ!*\n\n"
                        "ᴛʜɪꜱ ᴠɪᴅᴇᴏ ᴍɪɢʜᴛ ɴᴏᴛ ʜᴀᴠᴇ ᴀᴜᴅɪᴏ.",
                        parse_mode=ParseMode.MARKDOWN
                    )
                    return
                
                # Download audio
                await msg.edit_text(
                    f"⬇️ *ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴀᴜᴅɪᴏ...*\n\n"
                    f"📌 *ᴛɪᴛʟᴇ:* {title[:50]}...",
                    parse_mode=ParseMode.MARKDOWN
                )
                
                # Download file
                filename = f"audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(audio_url, timeout=6000) as response:
                        if response.status == 200:
                            with open(filename, 'wb') as f:
                                while True:
                                    chunk = await response.content.read(8192)
                                    if not chunk:
                                        break
                                    f.write(chunk)
                            
                            # Send audio
                            await msg.edit_text(
                                f"📤 *ꜱᴇɴᴅɪɴɢ ᴀᴜᴅɪᴏ...*\n\n"
                                f"📌 *ᴛɪᴛʟᴇ:* {title[:50]}...",
                                parse_mode=ParseMode.MARKDOWN
                            )
                            
                            with open(filename, 'rb') as f:
                                await update.message.reply_audio(
                                    audio=f,
                                    title=title[:100],
                                    performer=platform,
                                    caption=f"🎵 *ᴀᴜᴅɪᴏ ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ*\n\n📌 *ꜱᴏᴜʀᴄᴇ:* {platform_emoji} {platform}",
                                    parse_mode=ParseMode.MARKDOWN
                                )
                            
                            # Delete file
                            os.remove(filename)
                            
                            await msg.delete()
                        else:
                            await msg.edit_text(
                                "❌ *ᴅᴏᴡɴʟᴏᴀᴅ ꜰᴀɪʟᴇᴅ!*\n\n"
                                "ᴘʟᴇᴀꜱᴇ ᴛʀʏ ᴀɢᴀɪɴ.",
                                parse_mode=ParseMode.MARKDOWN
                            )
                            
    except asyncio.TimeoutError:
        await msg.edit_text(
            "⏰ *ᴛɪᴍᴇᴏᴜᴛ!*\n\n"
            "ᴘʟᴇᴀꜱᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ.",
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        logger.error(f"Error: {e}")
        await msg.edit_text(
            "❌ *ꜱᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ!*\n\n"
            "ᴘʟᴇᴀꜱᴇ ᴛʀʏ ᴀɢᴀɪɴ.",
            parse_mode=ParseMode.MARKDOWN
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # Check if user is in channels
    joined = await check_user_joined(user_id, context)
    
    if not joined:
        remove_verified(user_id)
        await show_join_channels(update, context)
        return
    
    add_verified(user_id)
    
    await update.message.reply_text(
        "🎵 *ʜᴏᴡ ᴛᴏ ᴜꜱᴇ:*\n\n"
        "1️⃣ ꜱᴇɴᴅ ᴍᴇ ᴀɴʏ ʟɪɴᴋ ꜰʀᴏᴍ:\n"
        "   • ʏᴏᴜᴛᴜʙᴇ 🎬 (ʏᴏᴜᴛᴜʙᴇ.ᴄᴏᴍ, ʏᴏᴜᴛᴜ.ʙᴇ)\n"
        "   • ɪɴꜱᴛᴀɢʀᴀᴍ 📸 (ɪɴꜱᴛᴀɢʀᴀᴍ.ᴄᴏᴍ)\n"
        "   • ꜰᴀᴄᴇʙᴏᴏᴋ 📘 (ꜰᴀᴄᴇʙᴏᴏᴋ.ᴄᴏᴍ, ꜰʙ.ᴡᴀᴛᴄʜ)\n\n"
        "2️⃣ ɪ'ʟʟ ᴇxᴛʀᴀᴄᴛ ᴀɴᴅ ꜱᴇɴᴅ ᴛʜᴇ ᴀᴜᴅɪᴏ! 🎧\n\n"
        "📌 *ɴᴏᴛᴇ:* ᴏɴʟʏ ᴀᴜᴅɪᴏ ɪꜱ ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ.",
        parse_mode=ParseMode.MARKDOWN
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != OWNER_ID:
        await update.message.reply_text("⚠️ *ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ!*", parse_mode=ParseMode.MARKDOWN)
        return
    
    data = load_data()
    verified_data = load_verified()
    total = len(data["users"])
    verified = len(verified_data["verified"])
    
    await update.message.reply_text(
        f"📊 *ʙᴏᴛ ꜱᴛᴀᴛɪꜱᴛɪᴄꜱ*\n\n"
        f"👥 *ᴛᴏᴛᴀʟ ᴜꜱᴇʀꜱ:* {total}\n"
        f"✅ *ᴠᴇʀɪꜰɪᴇᴅ ᴜꜱᴇʀꜱ:* {verified}",
        parse_mode=ParseMode.MARKDOWN
    )

async def broadcast_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != OWNER_ID:
        await update.message.reply_text("⚠️ *ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ!*", parse_mode=ParseMode.MARKDOWN)
        return
    
    context.user_data['broadcast'] = True
    await update.message.reply_text(
        "📢 *ʙʀᴏᴀᴅᴄᴀꜱᴛ*\n\n"
        "ꜱᴇɴᴅ ᴍᴇ ᴛʜᴇ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ʙʀᴏᴀᴅᴄᴀꜱᴛ:",
        parse_mode=ParseMode.MARKDOWN
    )

async def broadcast_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != OWNER_ID:
        return
    
    if not context.user_data.get('broadcast'):
        return
    
    text = update.message.text
    data = load_data()
    users = data["users"]
    
    keyboard = [
        [
            InlineKeyboardButton("✅ ᴄᴏɴꜰɪʀᴍ", callback_data="confirm_broadcast"),
            InlineKeyboardButton("❌ ᴄᴀɴᴄᴇʟ", callback_data="cancel_broadcast")
        ]
    ]
    
    await update.message.reply_text(
        f"📢 *ᴘʀᴇᴠɪᴇᴡ:*\n\n{text}\n\n"
        f"ꜱᴇɴᴅ ᴛᴏ {len(users)} ᴜꜱᴇʀꜱ?",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
    context.user_data['broadcast_msg'] = text

async def broadcast_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.from_user.id != OWNER_ID:
        return
    
    text = context.user_data.get('broadcast_msg')
    data = load_data()
    users = data["users"]
    
    await query.edit_message_text("📤 *ꜱᴇɴᴅɪɴɢ ʙʀᴏᴀᴅᴄᴀꜱᴛ...*", parse_mode=ParseMode.MARKDOWN)
    
    success = 0
    failed = 0
    
    for user_id in users:
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=text,
                parse_mode=ParseMode.MARKDOWN
            )
            success += 1
            await asyncio.sleep(0.05)
        except:
            failed += 1
    
    context.user_data['broadcast'] = False
    context.user_data.pop('broadcast_msg', None)
    
    await query.message.reply_text(
        f"✅ *ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴄᴏᴍᴘʟᴇᴛᴇ*\n\n"
        f"✅ *ꜱᴇɴᴛ:* {success}\n"
        f"❌ *ꜰᴀɪʟᴇᴅ:* {failed}",
        parse_mode=ParseMode.MARKDOWN
    )

async def broadcast_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.from_user.id != OWNER_ID:
        return
    
    context.user_data['broadcast'] = False
    context.user_data.pop('broadcast_msg', None)
    
    await query.edit_message_text("❌ *ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴄᴀɴᴄᴇʟʟᴇᴅ.*", parse_mode=ParseMode.MARKDOWN)

# ============ MAIN ============
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("broadcast", broadcast_start))
    
    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    
    # Callbacks
    app.add_handler(CallbackQueryHandler(handle_verify, pattern="verify"))
    app.add_handler(CallbackQueryHandler(broadcast_confirm, pattern="confirm_broadcast"))
    app.add_handler(CallbackQueryHandler(broadcast_cancel, pattern="cancel_broadcast"))
    
    print("🎵 Bot started! Send any link to get audio.")
    app.run_polling()

if __name__ == "__main__":
    main()
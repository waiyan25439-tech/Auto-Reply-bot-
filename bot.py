import logging
import random
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# -------------------------------------------------------------
# 🌟 ကိုယ်ပိုင်သတ်မှတ်ထားသော တုံ့ပြန်မှုများ (Custom Triggers)
# -------------------------------------------------------------
CUSTOM_TRIGGERS = {
    "ပျင်းတယ်": [
        "ပျင်းရင် ဖင်ခံပါလား",
        "လာလာ အသဲ စကားဝင်ပြော",
        "မပျင်းနဲ့ တို့ရှိတယ်",
    ],
    "hi": [
        "Hello",
        "စကားဝင်ပြောအသဲ",
    ],
    "နယူး": [
        "လပ်တယ်",
        "မယုံဘူး",
    ],
    "စပ့": [
        "စပ့ မို့ဆဲနာလား",
        "စပ့လား အမဲသားမ",
    ],
    "အသစ်": [
        "လာလာ စကားဝင်ပြောအသဲ",
        "စကားဝင်ပြော လူလေးပိစိထည့်ပေး",
    ],
    "ရည်းစားရှာပေး": [
        "တို့နဲ့တွဲမလား",
        "ရှာပေးမယ် ဘယ်လို type ကြိုက်လဲ",
    ],
    "ချစ်တယ်": [
        "ငြင်းတယ်",
        "ပိုချစ်တယ်",
    ],
    "မမရေ": [
        "ရှင့်မောင်မောင်🤪💕",
        "မမရဲ့ကလေးလေးဘာဖြစ်လို့လဲ😭",
    ],
    "ဝေယံ": [
        "မောင်မောင်မအားဘူး တို့ကိုပြော",
        "မောင်ရေ ခေါ်နေတယ်",
    ],
    "ဟလူး": [
        "ရှောင်ကြရှားကြ လင်များတဲ့ခင်ထားလာပီ",
        "လင်များတဲ့ခင်ထားလေးလာလာ",
    ],
    "ဝင်ထားတယ်": [
        "ကျေးဇူးပါရှင့်",
        "ကျေးကြူးဖာ",
    ],
    "မောနင်း": [
        "မောနင်းပါရှင်",
        "ကောင်းသောမနက်ခင်းလေးပါ",
    ],
    "ထွက်ပီ": [
        "ထွက်ပါနက်",
        "ထားခဲ့တော့မာလား",
    ]
}

# -------------------------------------------------------------
# /start Command Handler
# -------------------------------------------------------------
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🌸 **𝐁𝐞𝐫𝐫𝐲** 🌸\n\n"
        "၂၄ နာရီ မအိပ်ဘဲ စကားပြောပေးမယ့် Auto Reply Bot ။ Link တွေ Forward တွေ ဖျက်ပေးသည့် Bot သင့် groupရှင်းလင်းရန်အသုံးပြုပါ bot ကို Adm ပေးပါ။\n\n"
        "hello"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

# -------------------------------------------------------------
# Admin ဟုတ်မဟုတ် စစ်ဆေးပေးသည့် Helper Function
# -------------------------------------------------------------
async def is_user_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    chat = update.effective_chat
    user = update.effective_user
    
    if chat.type == "private":
        return True
        
    try:
        member = await chat.get_member(user.id)
        if member.status in ["creator", "administrator"]:
            return True
    except Exception as e:
        logging.error(f"Error checking admin status: {e}")
        
    return False

# -------------------------------------------------------------
# 👥 အသစ်ဝင်လာသူများကို Welcome နှုတ်ဆက်ခြင်းနှင့် System မက်ဆေ့ချ်ဖျက်ခြင်း
# -------------------------------------------------------------
async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.new_chat_members:
        return

    try:
        await message.delete()
    except Exception as e:
        logging.error(f"Could not delete join message: {e}")

    current_date = datetime.now().strftime("%Y-%m-%d | %H:%M:%S")
    chat_title = message.chat.title

    for new_member in message.new_chat_members:
        if new_member.id == context.bot.id:
            continue

        user_mention = new_member.mention_html()
        
        try:
            photos = await context.bot.get_user_profile_photos(new_member.id, limit=1)
            
            welcome_text = (
                f"🌸 <b>𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐭𝐨 {chat_title}</b> 🌸\n\n"
                f"✨ မင်္ဂလာပါ {user_mention} ရေ...\n"
                f"✨ ကျွန်ုပ်တို့ရဲ့ Group လေးထဲကို နွေးထွေးစွာ ကြိုဆိုပါတယ်ရှင် 💕\n\n"
                f"📅 ဝင်ရောက်သည့်အချိန်: <code>{current_date}</code>\n\n"
                f"📌 ကျေးဇူးပြု၍ Group ၏ စည်းကမ်းများကို လိုက်နာပေးပါရန် မေတ္တာရပ်ခံအပ်ပါတယ်ရှင်။"
            )

            if photos.total_count > 0:
                photo_file_id = photos.photos[0][-1].file_id
                await context.bot.send_photo(
                    chat_id=message.chat_id,
                    photo=photo_file_id,
                    caption=welcome_text,
                    parse_mode="HTML"
                )
            else:
                await context.bot.send_message(
                    chat_id=message.chat_id,
                    text=welcome_text,
                    parse_mode="HTML"
                )
        except Exception as e:
            logging.error(f"Error sending welcome message: {e}")

# -------------------------------------------------------------
# Message Handling Logic (Link & Forward ဖျက်ခြင်း + Auto Reply)
# -------------------------------------------------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message:
        return

    chat_type = message.chat.type
    
    # ၁။ Group ထဲတွင် Link သို့မဟုတ် Forward Message များစစ်ဆေးပြီး ဖျက်ခြင်း
    if chat_type in ["group", "supergroup"]:
        user_is_admin = await is_user_admin(update, context)
        
        if not user_is_admin:
            is_forwarded = message.forward_date is not None
            has_link = False
            
            if message.entities:
                for entity in message.entities:
                    if entity.type in ["url", "text_link"]:
                        has_link = True
                        break
            
            if not has_link and message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type in ["url", "text_link"]:
                        has_link = True
                        break

            if is_forwarded or has_link:
                try:
                    await message.delete()
                    warning_msg = await message.reply_text(
                        f"⚠️ {message.from_user.mention_html()}၊ ဤ Group ထဲတွင် Admin များမှလွဲ၍ Link နှင့် Forward များ တင်ခွင့်မရှိပါ။", 
                        parse_mode="HTML"
                    )
                    await asyncio.sleep(5)
                    await warning_msg.delete()
                except Exception as e:
                    logging.error(f"Failed to delete message: {e}")
                return

    # ၂။ 🔑 သတ်မှတ်ထားသော စာသား (Keyword) ပါလျှင် မန်းရှင်းခေါ်စရာမလိုဘဲ အော်တို Reply ပြန်ခြင်း
    message_text = message.text or message.caption
    if not message_text:
        return

    text_lower = message_text.lower()
    response = None

    for keyword, replies in CUSTOM_TRIGGERS.items():
        if keyword in text_lower:
            response = random.choice(replies)
            break

    if response:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        await asyncio.sleep(1)
        await message.reply_text(response)

# -------------------------------------------------------------
# Main Function
# -------------------------------------------------------------
if __name__ == "__main__":
    TOKEN = "8784248371:AAGjQJ5YO_VQPxVSUYji2iz-Gfh8DMLg9TA"  # BotFather Token

    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start_command))
    
    # 👥 အသစ်ဝင်လာသူများကို စောင့်ကြည့်ရန် Handler
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))
    
    # မက်ဆေ့ချ်အမျိုးအစားများကို စစ်ဆေးရန် Handler
    app.add_handler(MessageHandler((filters.TEXT | filters.PHOTO | filters.VIDEO | filters.Document.ALL) & (~filters.COMMAND), handle_message))

    print("Bot လေး စတင်အလုပ်လုပ်နေပါပြီရှင်...")
    app.run_polling()

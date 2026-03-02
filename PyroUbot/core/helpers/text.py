from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from PyroUbot import OWNER_ID, bot, ubot, get_expired_date

class MSG:     

    def EXP_MSG_UBOT(X):

        return f"""

<blockquote><b>❏ ᴘᴇᴍʙᴇʀɪᴛᴀʜᴜᴀɴ</b>

<b>├ ᴀᴋᴜɴ:</b> <a href=tg://user?id={X.me.id}>{X.me.first_name} {X.me.last_name or ''}</a>

<b>├ ɪᴅ:</b> <code>{X.me.id}</code>

<b>╰ ᴍᴀsᴀ ᴀᴋᴛɪꜰ ᴛᴇʟᴀʜ ʜᴀʙɪs</b></blockquote>

"""

    def START(message):

        return f"""

<blockquote><b>👋 ʜᴀʟᴏ <a href=tg://user?id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a>!

<blockquote> 📚💎@{bot.me.username} ᴀᴅᴀʟᴀʜ ʙᴏᴛ ʏᴀɴɢ ᴅᴀᴘᴀᴛ ᴍᴇᴍʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ ᴅᴇɴɢᴀɴ ᴍᴜᴅᴀʜ</blockquote>

🚀ʙᴏᴛ ɪɴɪ ᴅɪᴋᴇᴍʙᴀɴɢᴋᴀɴ ᴏʟᴇʜ <a href=tg://openmessage?user_id={OWNER_ID}>@padukarezz</a> ᴊɪᴋᴀ ᴀᴅᴀ ᴋᴇsᴀʟᴀʜᴀɴ ᴀᴛᴀᴜᴘᴜɴ ᴍᴀsᴀʟᴀʜ ᴅᴍ ᴏᴡɴᴇʀ ʙᴏᴛ ʏᴀɪᴛᴜ: <a href=tg://openmessage?user_id={OWNER_ID}>@padukarezz</a>

ᴛᴏᴛᴀʟ ᴘᴇɴɢɢᴜɴᴀ ᴜʙᴏᴛ: {len(ubot._ubot)} 

ᴏᴡɴᴇʀ ᴜʙᴏᴛ: <a href=tg://openmessage?user_id={OWNER_ID}>Paduka Rezz</a>

<u>ᴋʟɪᴋ ᴛᴏᴍʙᴏʟ ᴅɪʙᴀᴡᴀʜ ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ</u></b></blockquote>

"""

    def TEXT_PAYMENT(harga, total, bulan):

        return f"""

<blockquote><b>💬 sɪʟᴀʜᴋᴀɴ ᴍᴇʟᴀᴋᴜᴋᴀɴ ᴘᴇᴍʙᴀʏᴀʀᴀɴ ᴛᴇʀʟᴇʙɪʜ ᴅᴀʜᴜʟᴜ</b>

<b>🎟️ ʜᴀʀɢᴀ ᴘᴇʀʙᴜʟᴀɴ: {harga}.000</b>

<b>💳 ᴍᴏᴛᴏᴅᴇ ᴘᴇᴍʙᴀʏᴀʀᴀɴ:</b>

 <b>├ Qʀɪꜱ ᴀʟʟ ᴘᴀʏᴍᴇɴᴛ </b>

<b>🔖 ᴛᴏᴛᴀʟ ʜᴀʀɢᴀ: ʀᴘ {total}.000</b>

<b>🗓️ ᴛᴏᴛᴀʟ ʙᴜʟᴀɴ: {bulan}</b> 

OWNER BOT : <a href=tg://openmessage?user_id={OWNER_ID}>@padukarezz</a> 

<blockquote>🛍 ᴋʟɪᴋ ᴛᴏᴍʙᴏʟ ᴋᴏɴꜰɪʀᴍᴀsɪ ᴜɴᴛᴜᴋ ᴋɪʀɪᴍ ʙᴜᴋᴛɪ ᴘᴇᴍʙᴀʏᴀʀᴀɴ ᴀɴᴅᴀ</b></blockquote>

"""

    async def UBOT(count):

        return f"""

<blockquote><b>╭〢 ᴛʜʀᴇᴇʙᴏᴛ ᴋᴇ </b> <code>{int(count) + 1}/{len(ubot._ubot)}</code>

<b> ├〢 ᴀᴄᴄᴏᴜɴᴛ </b> <a href=tg://user?id={ubot._ubot[int(count)].me.id}>{ubot._ubot[int(count)].me.first_name} {ubot._ubot[int(count)].me.last_name or ''}</a> 

<b> ╰〢ᴜsᴇʀ ɪᴅ </b> <code>{ubot._ubot[int(count)].me.id}</code></blockquote>

"""

    def POLICY():

        return """ <blockquote><b>ᴊɪᴋᴀ ᴀᴅᴀ ᴋᴇɴᴅᴀʟᴀ sɪʟᴀʜᴋᴀɴ ʜᴜʙᴜɴɢɪ  <a href=tg://openmessage?user_id={OWNER_ID}>@padukarezz</a></b></blockquote>

"""


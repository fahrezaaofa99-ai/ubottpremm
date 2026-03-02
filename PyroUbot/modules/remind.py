from datetime import datetime, timedelta
from pyrogram import Client, filters
from pytimeparse import parse
from pytz import timezone

from PyroUbot import *


__MODULE__ = "reminders"
__HELP__ = """
<blockquote>
<b>ᴍᴏᴅᴜʟ ɪɴɪ ᴍᴇᴍᴜɴɢᴋɪɴᴋᴀɴ ᴘᴇɴɢɢᴜɴᴀ ᴜɴᴛᴜᴋ ᴍᴇɴɢᴀᴛᴜʀ ᴘᴇɴɢɪɴɢᴀᴛ.</b>

• <b>ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}remind</code> <waktu> <pesan>`
• <b>ᴘᴇɴᴊᴇʟᴀꜱᴀɴ:</b> <i>ᴍᴇɴɢᴀᴛᴜʀ ᴘᴇɴɢɪɴɢᴀᴛ ᴜɴᴛᴜᴋ ᴡᴀᴋᴛᴜ ᴛᴇʀᴛᴇɴᴛᴜ ᴅɪ ᴍᴀꜱᴀ ᴅᴇᴘᴀɴ.</i>

ᴄᴏɴᴛᴏʜ: 
<code>{0}remind 1h30m ʙᴇʟɪ ꜱᴜꜱᴜ</code>
<code>{0}remind 1h30m ᴄᴇᴋ ᴇᴍᴀɪʟ</code>

<b>ᴄᴀᴛᴀᴛᴀɴ:</b> <i>ᴀʀɢᴜᴍᴇɴ ᴡᴀᴋᴛᴜ ᴍᴇɴᴅᴜᴋᴜɴɢ ʙᴇʀʙᴀɢᴀɪ ꜰᴏʀᴍᴀᴛ ꜱᴇᴘᴇʀᴛɪ ᴊᴀᴍ</i> (<code>j</code>), <i>ᴍᴇɴɪᴛ</i> (<code>m</code>), <i>ᴅᴀɴ ʜᴀʀɪ</i> (<code>h</code>).

• <b>ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}listremind</code>
• <b>ᴘᴇɴᴊᴇʟᴀꜱᴀɴ:</b> <i>ᴍᴇɴᴀᴍᴘɪʟᴋᴀɴ ᴅᴀꜰᴛᴀʀ ᴘᴇɴɢɪɴɢᴀᴛ ʏᴀɴɢ ᴛᴇʀꜱɪᴍᴘᴀɴ.</i>
</i>ᴜɴᴛᴜᴋ ᴍᴇɴɢᴀᴛᴜʀ ᴘᴇɴɢɪɴɢᴀᴛ, ɢᴜɴᴀᴋᴀɴ ᴘᴇʀɪɴᴛᴀʜ</i> `<code>{0}remind</code>` <i>ᴅɪɪᴋᴜᴛɪ ᴏʟᴇʜ ᴡᴀᴋᴛᴜ ᴅᴀɴ ᴘᴇꜱᴀɴ ʏᴀɴɢ ᴅɪɪɴɢɪɴᴋᴀɴ. ᴀʀɢᴜᴍᴇɴ ᴡᴀᴋᴛᴜ ʜᴀʀᴜꜱ ᴅɪꜱᴇᴅɪᴀᴋᴀɴ ᴅᴀʟᴀᴍ ꜰᴏʀᴍᴀᴛ ʏᴀɴɢ ᴅɪꜱᴇʙᴜᴛᴋᴀɴ ᴅɪ ᴀᴛᴀꜱ. ᴘᴇɴɢɪɴɢᴀᴛ ᴀᴋᴀɴ ᴅɪᴋɪʀɪᴍ ᴘᴀᴅᴀ ᴡᴀᴋᴛᴜ ʏᴀɴɢ ᴅɪᴛᴇɴᴛᴜᴋᴀɴ ᴅᴇɴɢᴀɴ ᴘᴇꜱᴀɴ ʏᴀɴɢ ᴅɪʙᴇʀɪᴋᴀɴ.  

ᴜɴᴛᴜᴋ ᴍᴇʟɪʜᴀᴛ ᴅᴀꜰᴛᴀʀ ᴘᴇɴɢɪɴɢᴀᴛ ʏᴀɴɢ ᴛᴇʀꜱɪᴍᴘᴀɴ, ɢᴜɴᴀᴋᴀɴ ᴘᴇʀɪɴᴛᴀʜ</i> <code>{0}listremind</code>.
</blockquote>  
"""


# Daftar pengingat yang tersimpan

reminders = []


@PY.UBOT("remind")
@PY.TOP_CMD
async def reminder(client, message):
    gagal = await EMO.GAGAL(client)
    if len(message.command) == 1 or len(message.command) == 2:
        await message.reply(f"{gagal} Penggunaan: `remind <waktu> <pesan>`\n\nContoh:\n`{next((p) for p in prefix)}remind 1j30m Beli susu`\n`{next((p) for p in prefix)}remind 1h30m Cek email`")
    else:
        sukses = await EMO.SUKSES(client)
        time_from_now = message.command[1]
        text_to_remind = message.text.split(" ", 2)[2]
        now = datetime.now(timezone("Asia/Jakarta"))
        delay = parse(time_from_now)
        t = now + timedelta(seconds=delay)

        reminders.append((t, text_to_remind))
        await client.send_message(message.chat.id, text_to_remind, schedule_date=t)
        await message.reply(f"{sukses} Pengingat disimpan, akan dikirim pada {t.strftime('%d/%m/%Y')} pukul {t.strftime('%H:%M:%S')}.")


@PY.UBOT("listremind")
@PY.TOP_CMD
async def listrem(client, message):
    if len(reminders) == 0:
        await message.reply("Tidak ada pengingat yang tersimpan.")
    else:
        response = "• Daftar Pengingat:\n\n"
        for i, reminder in enumerate(reminders, start=1):
            t, text = reminder
            response += f"{i}. {text} - {t.strftime('%d/%m/%Y %H:%M:%S')}\n"
        await message.reply(response)

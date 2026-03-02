from PyroUbot import *
import asyncio
import math
import os
from datetime import timedelta
from time import time

import wget
from pyrogram.errors import FloodWait, MessageNotModified
from yt_dlp import YoutubeDL

__MODULE__ = "ʏᴏᴜᴛᴜʙᴇ"
__HELP__ = """
📚 <b>--Folder Untuk Youtube--</b>

<blockquote><b>🚦 Perintah : <code>{0}song</code>
🦠 Penjelasan : Mendownload Music Yang Di Inginkan.</b></blockquote>
<blockquote><b>🚦 Perintah : <code>{0}vsong</code>
🦠 Penjelasan : Mendownload Video Yang Di Inginkan.</b></blockquote>
"""

# ----------------------
# Helper utils
# ----------------------
def humanbytes(size):
    if not size:
        return ""
    power = 2**10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "kb", 2: "mb", 3: "gb", 4: "tb"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return f"{str(round(size, 2))} {dict_power_n[raised_to_pow]}"


def time_formatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        (f"{str(days)} hari, " if days else "")
        + (f"{str(hours)} jam, " if hours else "")
        + (f"{str(minutes)} menit, " if minutes else "")
        + (f"{str(seconds)} detik, " if seconds else "")
        + (f"{str(milliseconds)} mikrodetik, " if milliseconds else "")
    )
    return tmp[:-2]


async def progress(current, total, message, start, type_of_ps, file_name=None):
    """
    progress callback used by pyrogram send_xxx functions.
    current, total are bytes. message is the Message object to edit.
    """
    try:
        now = time()
        diff = now - start
        # update roughly every 1 second or at completion
        if diff <= 0:
            return
        # reduce frequency of edits: only update when at least 1 sec elapsed or finished
        if round(diff) < 1 and current != total:
            return

        percentage = (current * 100) / total if total else 0
        speed = current / diff if diff else 0
        elapsed_time = round(diff) * 1000
        if elapsed_time == 0:
            return
        time_to_completion = round((total - current) / speed) * 1000 if speed else 0
        estimated_total_time = elapsed_time + time_to_completion
        # simple progress bar text
        filled = math.floor(percentage / 10)
        empty = 10 - filled
        progress_str = "[" + ("█" * filled) + ("░" * empty) + f"] {round(percentage,2)}%\n"
        tmp = progress_str + "{0} of {1}\nestimasi: {2}".format(
            humanbytes(current), humanbytes(total), time_formatter(estimated_total_time)
        )
        if file_name:
            text = f"{type_of_ps}\n\nfile_id: {file_name}\n\n{tmp}"
        else:
            text = f"{type_of_ps}\n{tmp}"

        try:
            await message.edit(text)
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except MessageNotModified:
            pass
        except Exception:
            # ignore other editing errors to avoid crashing progress callback
            pass
    except Exception:
        # defensive: never let progress crash the bot
        return


# ----------------------
# Youtube search pakai yt-dlp (blocking wrapped into thread)
# ----------------------
async def find_first_youtube(query: str):
    """
    Return first entry dict from yt-dlp ytsearch1:<query>
    Runs in a thread to avoid blocking the event loop.
    """
    def sync_search(q):
        ydl_opts = {"quiet": True, "skip_download": True, "nocheckcertificate": True}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{q}", download=False)
            entries = info.get("entries") or []
            return entries[0] if entries else None

    return await asyncio.to_thread(sync_search, query)


# ----------------------
# Utility: safe download thumbnail (blocking) wrapped
# ----------------------
async def download_thumbnail(url: str):
    """
    Download thumbnail via wget.download in a thread and return local path.
    """
    try:
        path = await asyncio.to_thread(wget.download, url)
        return path
    except Exception:
        return None


# ----------------------
# Command vsong
# ----------------------
async def vsong_cmd(client, message):
    # validate arguments
    if len(message.command) < 2:
        return await message.reply_text("❌ Video tidak ditemukan, masukkan judul.")

    infomsg = await message.reply_text("🔍 Pencarian...", quote=False)
    # get query safely
    try:
        query = message.text.split(None, 1)[1]
    except Exception:
        return await infomsg.edit("🔍 Masukkan query yang valid.")

    # search youtube (yt-dlp)
    try:
        search = await find_first_youtube(query)
    except Exception as e:
        await infomsg.edit(f"🔍 Pencarian gagal:\n{e}")
        return

    if not search:
        return await infomsg.edit("🔍 Tidak ada hasil untuk query kamu.")

    link = search.get("webpage_url") or f"https://youtu.be/{search.get('id')}"

    # Download via project's YoutubeDownload (assumed async)
    try:
        # asumsi YoutubeDownload adalah coroutine: await YoutubeDownload(link, as_video=True)
        result = await YoutubeDownload(link, as_video=True)  # gunakan keyword jika signature pakai as_video
        # Jika YoutubeDownload mereturn tuple sesuai order:
        file_name, title, url, duration, views, channel, thumb, data_ytp = result
    except TypeError:
        # fallback jika signature berbeda (positional)
        try:
            file_name, title, url, duration, views, channel, thumb, data_ytp = await YoutubeDownload(link, True)
        except Exception as error:
            return await infomsg.edit(f"🔥 Downloader error:\n{error}")
    except Exception as error:
        return await infomsg.edit(f"🔥 Downloader error:\n{error}")

    # download thumbnail non-blocking
    thumbnail = None
    if thumb:
        thumbnail = await download_thumbnail(thumb)

    # prepare caption (data_ytp should be a format string)
    try:
        caption = data_ytp.format(
            "video",
            title,
            timedelta(seconds=duration),
            views,
            channel,
            url,
            bot.me.mention,
        )
    except Exception:
        # fallback simple caption
        caption = f"{title}\n{url}\n{bot.me.mention}"

    # send video with progress
    try:
        await client.send_video(
            message.chat.id,
            video=file_name,
            thumb=thumbnail,
            file_name=title,
            duration=duration,
            supports_streaming=True,
            caption=caption,
            progress=progress,
            progress_args=(infomsg, time(), "📥 Downloader...", f"{search.get('id')}.mp4"),
            reply_to_message_id=message.id,
        )
    except Exception as e:
        await infomsg.edit(f"❌ Gagal mengirim video:\n{e}")
        # cleanup
        for _f in (thumbnail, file_name):
            try:
                if _f and os.path.exists(_f):
                    os.remove(_f)
            except Exception:
                pass
        return

    # tidy up
    await infomsg.delete()
    for _f in (thumbnail, file_name):
        try:
            if _f and os.path.exists(_f):
                os.remove(_f)
        except Exception:
            pass


@PY.UBOT("vsong")
@PY.TOP_CMD
async def _(client, message):
    await vsong_cmd(client, message)


# ----------------------
# Command song (audio)
# ----------------------
@PY.UBOT("song")
@PY.TOP_CMD
async def song_cmd(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)

    if len(message.command) < 2:
        return await message.reply_text(f"{ggl} Audio tidak ditemukan! Masukkan judul.")

    infomsg = await message.reply_text(f"{prs} Pencarian...", quote=False)
    try:
        query = message.text.split(None, 1)[1]
    except Exception:
        return await infomsg.edit(f"{ggl} Query tidak valid.")

    try:
        search = await find_first_youtube(query)
    except Exception as e:
        await infomsg.edit(f"{prs} Pencarian gagal:\n{e}")
        return

    if not search:
        return await infomsg.edit(f"{prs} Tidak ada hasil.")

    link = search.get("webpage_url") or f"https://youtu.be/{search.get('id')}"

    # Download via project's YoutubeDownload (assumed async)
    try:
        result = await YoutubeDownload(link, as_video=False)
        file_name, title, url, duration, views, channel, thumb, data_ytp = result
    except TypeError:
        try:
            file_name, title, url, duration, views, channel, thumb, data_ytp = await YoutubeDownload(link, False)
        except Exception as error:
            return await infomsg.edit(f"{ggl} Downloader error:\n{error}")
    except Exception as error:
        return await infomsg.edit(f"{ggl} Downloader error:\n{error}")

    # thumbnail download
    thumbnail = None
    if thumb:
        thumbnail = await download_thumbnail(thumb)

    try:
        caption = data_ytp.format(
            "audio",
            title,
            timedelta(seconds=duration),
            views,
            channel,
            url,
            bot.me.mention,
        )
    except Exception:
        caption = f"{title}\n{url}\n{bot.me.mention}"

    try:
        await client.send_audio(
            message.chat.id,
            audio=file_name,
            thumb=thumbnail,
            file_name=title,
            performer=channel,
            duration=duration,
            caption=caption,
            progress=progress,
            progress_args=(infomsg, time(), f"{prs} Processing...", f"{search.get('id')}.mp3"),
            reply_to_message_id=message.id,
        )
    except Exception as e:
        await infomsg.edit(f"❌ Gagal mengirim audio:\n{e}")
        for _f in (thumbnail, file_name):
            try:
                if _f and os.path.exists(_f):
                    os.remove(_f)
            except Exception:
                pass
        return

    await infomsg.delete()
    for _f in (thumbnail, file_name):
        try:
            if _f and os.path.exists(_f):
                os.remove(_f)
        except Exception:
            pass
import os
import requests
from pyrogram import Client, filters
from pyrogram.types import Message

# Ganti dengan API key RapidAPI Anda
RAPIDAPI_KEY = "ad586745a5msh38212dc52683a12p154b2ejsnea80c2b3748d"

async def download_instagram_media(url: str, is_audio: bool = False):
    """Fungsi untuk mendownload media dari Instagram"""
    try:
        api_url = "https://instagram-downloader-download-instagram-videos-stories.p.rapidapi.com/index"
        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": "instagram-downloader-download-instagram-videos-stories.p.rapidapi.com"
        }
        params = {"url": url}
        
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        if is_audio:
            return data.get('media', {}).get('audio_url')
        return data.get('media', {}).get('video_url') or data.get('media', {}).get('url')
    
    except Exception as e:
        print(f"Error: {e}")
        return None

@Client.on_message(filters.command(["ighelp", "instagramhelp"], prefixes=["!", "/", "."]))
async def instagram_help(client: Client, message: Message):
    """Menu bantuan"""
    help_text = """
<b>📚 Bantuan untuk mendownload video dari Instagram</b>

<blockquote>• 🚦 Perintah: <code>{0}dowloadvidio [link vidio]</code>
• 🦠 Penjelasan: Mendownload video dari Instagram</blockquote>

<blockquote>• 🚦 Perintah: <code>{0}dowloadsuara [link lagu]</code>
• 🦠 Penjelasan: Download audio dari Instagram</blockquote>
""".format(message.command[0][0])
    
    await message.reply(help_text, parse_mode="html")

@Client.on_message(filters.command(["dowloadvidio", "downloadvidio"], prefixes=["!", "/", "."]))
async def download_video(client: Client, message: Message):
    """Download video Instagram"""
    if len(message.command) < 2:
        await message.reply("⚠️ Gunakan: <code>.downloadvidio [link_instagram]</code>", parse_mode="html")
        return
    
    url = message.text.split()[1]
    if "instagram.com" not in url:
        await message.reply("❌ Link harus dari Instagram!")
        return
    
    msg = await message.reply("⏳ Memproses video...")
    video_url = await download_instagram_media(url)
    
    if not video_url:
        await msg.edit("❌ Gagal mendapatkan video. Pastikan link valid!")
        return
    
    try:
        await msg.edit("📥 Mengunduh video...")
        video_data = requests.get(video_url).content
        with open("temp_video.mp4", "wb") as f:
            f.write(video_data)
        
        await msg.edit("📤 Mengunggah video...")
        await client.send_video(
            chat_id=message.chat.id,
            video="temp_video.mp4",
            caption="🎥 Video Instagram\n\n✅ Berhasil diunduh"
        )
        await msg.delete()
    except Exception as e:
        await msg.edit(f"❌ Error: {e}")
    finally:
        if os.path.exists("temp_video.mp4"):
            os.remove("temp_video.mp4")

@Client.on_message(filters.command(["dowloadsuara", "downloadsuara"], prefixes=["!", "/", "."]))
async def download_audio(client: Client, message: Message):
    """Download audio Instagram"""
    if len(message.command) < 2:
        await message.reply("⚠️ Gunakan: <code>.downloadsuara [link_instagram]</code>", parse_mode="html")
        return
    
    url = message.text.split()[1]
    if "instagram.com" not in url:
        await message.reply("❌ Link harus dari Instagram!")
        return
    
    msg = await message.reply("⏳ Memproses audio...")
    audio_url = await download_instagram_media(url, is_audio=True)
    
    if not audio_url:
        await msg.edit("❌ Gagal mendapatkan audio. Pastikan link valid!")
        return
    
    try:
        await msg.edit("📥 Mengunduh audio...")
        audio_data = requests.get(audio_url).content
        with open("temp_audio.mp3", "wb") as f:
            f.write(audio_data)
        
        await msg.edit("📤 Mengunggah audio...")
        await client.send_audio(
            chat_id=message.chat.id,
            audio="temp_audio.mp3",
            caption="🎵 Audio Instagram\n\n✅ Berhasil diunduh"
        )
        await msg.delete()
    except Exception as e:
        await msg.edit(f"❌ Error: {e}")
    finally:
        if os.path.exists("temp_audio.mp3"):
            os.remove("temp_audio.mp3")

def register_instagram_module(client):
    """Fungsi untuk mendaftarkan handler"""
    client.add_handler(instagram_help)
    client.add_handler(download_video)
    client.add_handler(download_audio)
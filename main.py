# © BugHunterCodeLabs ™
# © bughunter0
# 2021
# Copyright - https://en.m.wikipedia.org/wiki/Fair_use

import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from bs4 import BeautifulSoup
import requests


bughunter0 = Client(
    "WebScrapperBot",
    bot_token=os.environ["BOT_TOKEN"],
    api_id=int(os.environ["API_ID"]),
    api_hash=os.environ["API_HASH"]
)



@bughunter0.on_message(filters.command(["start"]))
async def start(_, message: Message):
    # Edit Your Start string here
    text = f"اهلا بك بوت ليفاي." \
    "\nاعطني اـٰــيۂ 🙋🏻‍♀💕) “ رابط.\n\nJoin @SIS_fff"
    await message.reply_text(text=text, disable_web_page_preview=True, quote=True)


@bughunter0.on_message((filters.regex("https") | filters.regex("http") | filters.regex("www")) & filters.private)
async def scrapping(bot, message):
    txt = await message.reply_text("التحقق من الارتباط", quote=True)
    try:  # Extracting Raw Data From Webpage ( Unstructured format)
        url = str(message.text)
        request = requests.get(url)
        await txt.edit(text=f"الحصول على بيانات أولية من {url}", disable_web_page_preview=True)
        file_write = open(f'مسودة بيانات-{message.chat.username}.txt', 'a+')
        file_write.write(f"{request.content}")  # Writing Raw Content to Txt file
        file_write.close()
        await message.reply_document(f"مسودة بيانات-{message.chat.username}.txt", caption="©@BugHunterBots", quote=True)
        os.remove(f"RawData-{message.chat.username}.txt")
        await txt.delete()
    except Exception as error:
        print(error)
        await message.reply_text(text=f"{error}", disable_web_page_preview=True, quote=True)
        await txt.delete()
        return
    try:
        txt = await message.reply_text(text=f"الحصول على كود HTML من {url}", disable_web_page_preview=True, quote=True)
        soup = BeautifulSoup(request.content, 'html5lib')  # Extracting Html code in Tree Format
        file_write = open(f'بيانات Html-{message.chat.username}.txt', 'a+')
        soup.data = soup.prettify()  # parsing HTML
        file_write.write(f"{soup.data}")  # writing data to txt
        file_write.close()
        await message.reply_document(f"بيانات Html-{message.chat.username}.txt", caption="©@BugHunterBots", quote=True)
        os.remove(f"بيانات Html-{message.chat.username}.txt")
        await txt.delete()
    except Exception as error:
        await message.reply_text(text=f"{error}", disable_web_page_preview=True, quote=True)
        await txt.delete()
        return
    try:
        txt = await message.reply_text(f"الحصول على كافة الروابط من {url}", disable_web_page_preview=True, quote=True)
        file_write = open(f'الكل-{message.chat.username}.txt', 'a+')
        for link in soup.find_all('a'):  # getting all <a> tags in Html
            links = link.get('href')  # Extracting Href value of <a>
            file_write.write(f"{links}\n\n")  # writing links to txt file
        file_write.close()
        await message.reply_document(
            f"AllLinks-{message.chat.username}.txt",
            caption="©@Q_B_h"
        )
        os.remove(f"كل روابط-{message.chat.username}.txt")
        await txt.delete()
    except Exception as error:
        await message.reply_text(text=f"{error}", disable_web_page_preview=True, quote=True)
        await txt.delete()

    try:
        txt = await message.reply_text(
            f"الحصول على كل فقرة من {url} ...",
            disable_web_page_preview=True,
            quote=True
        )
        file_write = open(f'الكل-{message.chat.username}.txt', 'a+')
        paragraph = ""
        for para in soup.find_all('p'):  # Extracting all <p> tags
            paragraph = para.get_text()  # Getting Text from Paragraphs
            file_write.write(f"{paragraph}\n\n")  # writing to a file
        file_write.close()
        
        await txt.delete()
        await message.reply_document(
            f"الكل-{message.chat.username}.txt",
            caption="©@Q_B_H",
            quote=True
        )
        os.remove(f"الكل-{message.chat.username}.txt")
    except Exception as error:
        await message.reply_text(text=f"لم يتم العثور على فقرات!!", disable_web_page_preview=True, quote=True)
        await txt.delete()
        return




# Use soup.find_all('tag_name') to Extract Specific Tag Details
"""
soup.title
# <title>This is Title</title>

soup.title.name
# u'title'

soup.title.string
# u'This is a string'

soup.title.parent.name
# u'head'
"""

bughunter0.run()

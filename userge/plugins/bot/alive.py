"""Fun plugin"""

import asyncio
from datetime import datetime
from re import search

from pyrogram import filters
from pyrogram.errors import BadRequest, FloodWait, Forbidden
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from userge import Config, Message, get_version, userge, versions
from userge.core.ext import RawClient
from userge.utils import get_file_id, rand_array

CACHED_MEDIA = None


@userge.on_cmd("alive", about={"header": "Just For Fun"}, allow_channels=False)
async def alive_inline(message: Message):
    global CACHED_MEDIA
    if message.client.is_bot:
        if Config.ALIVE_MEDIA:
            url_ = Config.ALIVE_MEDIA.strip()
            if url_.lower() == "false":
                await userge.bot.send_message(
                    message.chat.id,
                    Bot_Alive.alive_info(),
                    reply_markup=Bot_Alive.alive_buttons(),
                    disable_web_page_preview=True,
                )
            else:
                type_, media_ = await Bot_Alive.check_media_link(Config.ALIVE_MEDIA)
                if type_ == "url_gif":
                    await userge.bot.send_animation(
                        message.chat.id,
                        animation=url_,
                        caption=Bot_Alive.alive_info(),
                        reply_markup=Bot_Alive.alive_buttons(),
                    )
                elif type_ == "url_image":
                    await userge.bot.send_photo(
                        message.chat.id,
                        photo=url_,
                        caption=Bot_Alive.alive_info(),
                        reply_markup=Bot_Alive.alive_buttons(),
                    )
                elif type_ == "tg_media" and isinstance(media_, list):
                    if not CACHED_MEDIA:
                        try:
                            CACHED_MEDIA = get_file_id(
                                await userge.bot.get_messages(media_[0], media_[1])
                            )
                        except Exception as er:
                            await message.err(er, del_in=7)
                            return
                    await userge.bot.send_cached_media(
                        message.chat.id,
                        file_id=CACHED_MEDIA,
                        caption=Bot_Alive.alive_info(),
                        reply_markup=Bot_Alive.alive_buttons(),
                    )
        else:
            await userge.bot.send_photo(
                message.chat.id,
                photo=Bot_Alive.alive_default_imgs(),
                caption=Bot_Alive.alive_info(),
                reply_markup=Bot_Alive.alive_buttons(),
            )
    else:
        bot = await userge.bot.get_me()
        try:
            x = await userge.get_inline_bot_results(bot.username, "alive")
            y = await userge.send_inline_bot_result(
                chat_id=message.chat.id, query_id=x.query_id, result_id=x.results[0].id
            )
        except (Forbidden, BadRequest) as ex:
            return await message.err(str(ex), del_in=5)
        await message.delete()
        await asyncio.sleep(200)
        await userge.delete_messages(message.chat.id, y.updates[0].id)


if userge.has_bot:

    @userge.bot.on_callback_query(filters.regex(pattern=r"^settings_btn$"))
    async def alive_cb(_, c_q: CallbackQuery):
        allow = bool(
            c_q.from_user
            and (
                c_q.from_user.id in Config.OWNER_ID
                or c_q.from_user.id in Config.SUDO_USERS
            )
        )
        if allow:
            start = datetime.now()
            try:
                await c_q.edit_message_text(
                    Bot_Alive.alive_info(),
                    reply_markup=Bot_Alive.alive_buttons(),
                    disable_web_page_preview=True,
                )
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except BadRequest:
                pass
            ping = "ριηg:  🐨  {} sec\n"
        alive_s = "➕ єχтяα ρℓυgιηѕ : {}\n".format(
            _parse_arg(Config.LOAD_UNOFFICIAL_PLUGINS)
        )
        alive_s += f"👥 ѕυ∂σ
 : {_parse_arg(Config.SUDO_ENABLED)}\n"
        alive_s += f"🚫 αηтιѕραм : {_parse_arg(Config.ANTISPAM_SENTRY)}\n"
        if Config.HEROKU_APP and Config.RUN_DYNO_SAVER:
            alive_s += "⛽️ ∂уησ ѕανєя :  ✅ αктιƒ\n"
        alive_s += f"💬 вσт ƒσяωαя∂ѕ : {_parse_arg(Config.BOT_FORWARDS)}\n"
        alive_s += f"🛡 ρм gυαя∂
 : {_parse_arg(not Config.ALLOW_ALL_PMS)}\n"
        alive_s += f"📝 ρм ℓσggєя
 : {_parse_arg(Config.PM_LOGGING)}"
        if allow:
            end = datetime.now()
            m_s = (end - start).microseconds / 1000
            await c_q.answer(ping.format(m_s) + alive_s, show_alert=True)
        else:
            await c_q.answer(alive_s, show_alert=True)
        await asyncio.sleep(0.5)


def _parse_arg(arg: bool) -> str:
    return " ✅ αктιƒ" if arg else " ❌ ησηαктιƒ"


class Bot_Alive:
    @staticmethod
    async def check_media_link(media_link: str):
        alive_regex_ = r"http[s]?://(i\.imgur\.com|telegra\.ph/file|t\.me)/(\w+)(?:\.|/)(gif|jpg|png|jpeg|[0-9]+)(?:/([0-9]+))?"
        match = search(alive_regex_, media_link)
        if not match:
            return None, None
        if match.group(1) == "i.imgur.com":
            link = match.group(0)
            link_type = "url_gif" if match.group(3) == "gif" else "url_image"
        elif match.group(1) == "telegra.ph/file":
            link = match.group(0)
            link_type = "url_image"
        else:
            link_type = "tg_media"
            if match.group(2) == "c":
                chat_id = int("-100" + str(match.group(3)))
                message_id = match.group(4)
            else:
                chat_id = match.group(2)
                message_id = match.group(3)
            link = [chat_id, int(message_id)]
        return link_type, link

    @staticmethod
    def alive_info():
        alive_info = f"""
<a href="https://telegram.dog/mixiologist"><b>UsergayKampang</a> SIAP MENUMBUK ASU 🔥.</b>
\n╭▻►▻►▻►▻►▻►◄◅◄◅◄◅◄◅╮
  🐍  • <b>Python :</b>    <code>v{versions.__python_version__}</code>
  🔥  • <b>Pyrogram :</b>    <code>v{versions.__pyro_version__}</code>
  🧬  • <b>𝓚𝓸𝓪𝓵𝓪 🐨 ⁪⁬⁮⁮⁮⁮ :</b>    <code>v{get_version()}</code>
╰▻►▻►▻►▻►▻►◄◅◄◅◄◅◄◅╯\n
<b>{Bot_Alive._get_mode()}</b>    <code>|</code>    🕔  <b>{userge.uptime}</b>
"""
        return alive_info

    @staticmethod
    def _get_mode() -> str:
        if RawClient.DUAL_MODE:
            return "🚀  DUAL"
        if Config.BOT_TOKEN:
            return "🤖  BOT"
        return "👤  USER"

    @staticmethod
    def alive_buttons():
        buttons = [
            [
                InlineKeyboardButton(text="🌐  INFO", callback_data="settings_btn"),
                InlineKeyboardButton(text="🐨  REPO", url=Config.UPSTREAM_REPO),
            ]
        ]
        return InlineKeyboardMarkup(buttons)

    @staticmethod
    def alive_default_imgs():
        alive_imgs = [
            "https://telegra.ph/file/a5f7caf7a0ab68bb6aaa8.jpg",
            "https://telegra.ph/file/661db62b099144e5991c5.jpg",
            
            
            
        ]
        return rand_array(alive_imgs)

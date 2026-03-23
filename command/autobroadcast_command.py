import asyncio
from datetime import datetime, timedelta

import pytz

from database import dB
from helpers import (Emoji, StartAutoBC, StartAutoFW, add_auto_text,
                     add_auto_text_fw, animate_proses)

def extract_type_and_text(message):
    args = message.text.split(None, 2)
    if len(args) < 2:
        return None, None

    type = args[1]
    msg = (
        message.reply_to_message.text
        if message.reply_to_message
        else args[2] if len(args) > 2 else None
    )
    return type, msg
  
async def autobc_cmd(client, message):
    em = Emoji(client)
    await em.get()

    if len(message.command) < 2:
        return await message.reply(
            f"""**{em.block} Invalid usage! Type: {em.net} `.help autobc`**"""
        )

    msg = await animate_proses(message, em.proses)
    cmd, *args = message.command[1:]
    cmd = cmd.lower()
    saved = await dB.get_var(client.me.id, "MSG_AUTOBC")
    value = " ".join(args)

    if cmd == "on":
        if not saved:
            return await msg.edit(
                f"**{em.gagal} Add a message first before enabling auto broadcast.**"
            )

        if await dB.get_var(client.me.id, "AUTOBC_STATUS"):
            return await msg.edit(f"{em.gagal}<b>Auto Broadcast already turned on.</b>")
        else:
            await dB.set_var(client.me.id, "AUTOBC_STATUS", True)
            await dB.set_var(client.me.id, "AUTOBC_ROUNDS", 0)

            asyncio.create_task(StartAutoBC(client, client.me.id, 0))
            return await msg.edit(f"{em.sukses}<b>Auto Broadcast turned on.</b>")

    elif cmd == "off":
        if await dB.get_var(client.me.id, "AUTOBC_STATUS"):
            await dB.set_var(client.me.id, "AUTOBC_STATUS", False)
            return await msg.edit(f"{em.gagal}<b>Auto Broadcast has been stopped.</b>")
        else:
            return await msg.edit(f"{em.sukses}<b>Auto Broadcast already off.</b>")

    elif cmd == "save":
        if not message.reply_to_message:
            return await msg.edit(f"**{em.block} Reply to a message to save it.**")
        await add_auto_text(message)
        await msg.edit(f"**{em.sukses} Message saved to AutoBC.**")

    elif cmd == "list":
        if not saved:
            return await msg.edit(f"**{em.block} No messages saved for broadcast.**")

        text = f"<blockquote><b>{em.klip} Saved Messages:</b>\n\n"
        for i, data in enumerate(saved, 1):
            mid = data.get("message_id")
            try:
                m = await client.get_messages("me", mid)
                preview = (m.caption or m.text or "(Empty)")[:50] + "..."
                jenis = "photo" if m.photo else "video" if m.video else "text"
                text += f"`{i}> {preview} ({jenis})`\n"
            except:
                text += f"`{i}> [Message Not Found]`\n"

        text += f"\n<b>{em.block} To delete: `.autobc remove`</b></blockquote>"
        await msg.edit(text)

    elif cmd == "remove":
        if not saved:
            return await msg.edit(f"**{em.block} No saved messages to remove.**")

        last_data = saved.pop()
        try:
            await client.delete_messages("me", last_data.get("message_id"))
        except:
            pass

        await dB.remove_var(client.me.id, "MSG_AUTOBC")
        await msg.edit(f"**{em.sukses} Saved message removed.**")

    elif cmd == "reset":
        await dB.remove_var(client.me.id, "AUTOBC_STATUS")
        await dB.remove_var(client.me.id, "DELAY_AUTOBC")
        await dB.remove_var(client.me.id, "AUTOBC_ROUNDS")
        await dB.remove_var(client.me.id, "LAST_BROADCAST")
        last_data = saved.pop()
        try:
            await client.delete_messages("me", last_data.get("message_id"))
        except:
            pass

        await dB.remove_var(client.me.id, "MSG_AUTOBC")
        await msg.edit("**{em.sukses} AutoBC Reset**")

    elif cmd == "status":
        status = await dB.get_var(client.me.id, "AUTOBC_STATUS")
        delay = await dB.get_var(client.me.id, "DELAY_AUTOBC") or 60
        rounds = await dB.get_var(client.me.id, "AUTOBC_ROUNDS") or 0
        last = await dB.get_var(client.me.id, "LAST_BROADCAST") or 0
        saved_text = f"{len(saved)}" if saved else "Not Saved Message"

        status_text = f"{em.sukses} Enabled" if status else f"{em.block} Disabled"
        if last:
            last_time = datetime.fromtimestamp(last, tz=pytz.timezone("Asia/Jakarta"))
            last_text = f"<code>{last_time.strftime('%Y-%m-%d %H:%M:%S')} WIB</code>"
            next_time = last_time + timedelta(minutes=delay)
            next_text = f"<code>{next_time.strftime('%Y-%m-%d %H:%M:%S')} WIB</code>"
        else:
            next_text = "Not scheduled"
            last_text = "never broadcasted"

        await msg.edit(
            f"""<blockquote><b>{em.klip} Auto Broadcast Status:</b>

{em.profil} Status: {status_text}
{em.ping} Delay: {delay} Minutes
{em.msg} Save Messages: {saved_text}
{em.robot} Rounds: {rounds} Times
{em.uptime} Last Broadcast: {last_text}
{em.speed} Next Broadcast: {next_text}</blockquote>"""
        )

    elif cmd == "delay":
        if value.isdigit() and int(value) > 0:
            await dB.set_var(client.me.id, "DELAY_AUTOBC", int(value))
            await msg.edit(f"**{em.sukses} Delay set to {value} minutes.**")
        else:
            await msg.edit(f"**{em.block} Use `.autobc delay [number > 0]`**")

    else:
        await msg.edit(
            f"""**{em.block} Invalid command! Type:
{em.net} `.help autobc`**"""
        )


async def autofw_cmd(client, message):
    em = Emoji(client)
    await em.get()

    if len(message.command) < 2:
        return await message.reply(
            f"""**{em.block} Invalid usage! Type: {em.net} `.help autofw`**"""
        )

    msg = await animate_proses(message, em.proses)
    cmd, *args = message.command[1:]
    cmd = cmd.lower()
    saved = await dB.get_var(client.me.id, "MSG_AUTOFW")
    value = " ".join(args)
    rep = message.reply_to_message

    if cmd == "on":
        if not saved:
            return await msg.edit(
                f"**{em.gagal} Add a message first before enabling auto broadcast forward.**"
            )

        if await dB.get_var(client.me.id, "AUTOFW_STATUS"):
            return await msg.edit(
                f"{em.gagal}<b>Auto Broadcast Forward already turned on.</b>"
            )
        else:
            await dB.set_var(client.me.id, "AUTOFW_STATUS", True)
            await dB.set_var(client.me.id, "AUTOFW_ROUNDS", 0)
            asyncio.create_task(StartAutoFW(client, client.me.id, 0))
            return await msg.edit(
                f"{em.sukses}<b>Auto Broadcast Forward turned on.</b>"
            )

    elif cmd == "off":
        if await dB.get_var(client.me.id, "AUTOFW_STATUS"):
            await dB.set_var(client.me.id, "AUTOFW_STATUS", False)
            return await msg.edit(
                f"{em.gagal}<b>Auto Broadcast Forward has been stopped.</b>"
            )
        else:
            return await msg.edit(
                f"{em.sukses}<b>Auto Broadcas Forward already off.</b>"
            )

    elif cmd == "save":
        if not rep:
            return await msg.edit(f"**{em.block} Reply to a message to save it.**")

        if not (rep.forward_from or rep.forward_sender_name or rep.forward_from_chat):
            return await msg.edit(
                f"**{em.block} Only forwarded messages can be saved.**"
            )

        await add_auto_text_fw(message)
        await msg.edit(f"**{em.sukses} Message saved to Auto Forward.**")

    elif cmd == "list":
        if not saved:
            return await msg.edit(f"**{em.block} No messages saved for broadcast.**")

        text = f"<blockquote><b>{em.klip} Saved Messages Forward:</b>\n\n"
        for i, data in enumerate(saved, 1):
            mid = data.get("message_id")
            try:
                m = await client.get_messages("me", mid)
                preview = (m.caption or m.text or "(Empty)")[:50] + "..."
                jenis = "photo" if m.photo else "video" if m.video else "text"
                text += f"`{i}> {preview} ({jenis})`\n"
            except:
                text += f"`{i}> [Message Not Found]`\n"

        text += f"\n<b>{em.block} To delete: `.autofw remove`</b></blockquote>"
        await msg.edit(text)

    elif cmd == "remove":
        if not saved:
            return await msg.edit(f"**{em.block} No saved messages to remove.**")

        last_data = saved.pop()
        try:
            await client.delete_messages("me", last_data.get("message_id"))
        except:
            pass

        await dB.remove_var(client.me.id, "MSG_AUTOFW")
        await msg.edit(f"**{em.sukses} Saved message removed.**")
    
    elif cmd == "reset":
        await dB.remove_var(client.me.id, "AUTOFW_STATUS")
        await dB.remove_var(client.me.id, "AUTOFW_ROUNDS")
        await dB.remove_var(client.me.id, "DELAY_AUTOFW")
        await dB.remove_var(client.me.id, "LAST_FW")
        last_data = saved.pop()
        try:
            await client.delete_messages("me", last_data.get("message_id"))
        except:
            pass

        await dB.remove_var(client.me.id, "MSG_AUTOFW")
        await msg.edit("**{em.sukses} AutoFW Reset**")

    elif cmd == "status":
        status = await dB.get_var(client.me.id, "AUTOFW_STATUS")
        delay = await dB.get_var(client.me.id, "DELAY_AUTOFW") or 60
        rounds = await dB.get_var(client.me.id, "AUTOFW_ROUNDS") or 0
        last = await dB.get_var(client.me.id, "LAST_FW") or 0
        saved_text = f"{len(saved)}" if saved else "Not Saved Message"

        status_text = f"{em.sukses} Enabled" if status else f"{em.block} Disabled"
        if last:
            last_time = datetime.fromtimestamp(last, tz=pytz.timezone("Asia/Jakarta"))
            last_text = f"<code>{last_time.strftime('%Y-%m-%d %H:%M:%S')} WIB</code>"
            next_time = last_time + timedelta(minutes=delay)
            next_text = f"<code>{next_time.strftime('%Y-%m-%d %H:%M:%S')} WIB</code>"
        else:
            next_text = "Not scheduled"
            last_text = "never broadcasted"

        await msg.edit(
            f"""<blockquote><b>{em.klip} Auto Broadcast Forward Status:</b>

{em.profil} Status: {status_text}
{em.ping} Delay: {delay} Minutes
{em.msg} Save Messages: {saved_text}
{em.robot} Rounds: {rounds} Times
{em.uptime} Last Broadcast: {last_text}
{em.speed} Next Broadcast: {next_text}</blockquote>"""
        )

    elif cmd == "delay":
        if value.isdigit() and int(value) > 0:
            await dB.set_var(client.me.id, "DELAY_AUTOFW", int(value))
            await msg.edit(f"**{em.sukses} Delay set to {value} minutes.**")
        else:
            await msg.edit(f"**{em.block} Use `.autofw delay [number > 0]`**")

    else:
        await msg.edit(
            f"""**{em.block} Invalid command! Type:
{em.net} `.help autofw`**"""

        )


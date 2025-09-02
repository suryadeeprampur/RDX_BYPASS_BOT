from FZBypass import Bypass, LOGGER, Config
from pyrogram import idle
from pyrogram.filters import command, user
from os import path as ospath, execl
from asyncio import create_subprocess_exec
from sys import executable
import os
from threading import Thread
from flask import Flask

# =====================
# Flask Web Server (For Render Port Binding)
# =====================
app = Flask(__name__)

@app.route('/')
def home():
    return "FZ Bot is running!"

def run_flask():
    port = int(os.getenv("PORT", 5000))  # Render will inject PORT env
    app.run(host="0.0.0.0", port=port)

Thread(target=run_flask).start()


# =====================
# Restart Command Handler
# =====================
@Bypass.on_message(command("restart") & user(Config.OWNER_ID))
async def restart_command(client, message):
    restart_message = await message.reply("<i>Restarting...</i>")
    await (await create_subprocess_exec("python3", "update.py")).wait()
    with open(".restartmsg", "w") as f:
        f.write(f"{restart_message.chat.id}\n{restart_message.id}\n")
    try:
        execl(executable, executable, "-m", "FZBypass")
    except Exception:
        execl(executable, executable, "-m", "FZBypassBot/FZBypass")


# =====================
# Restart Message Update After Restart
# =====================
async def after_restart():
    if ospath.isfile(".restartmsg"):
        with open(".restartmsg") as f:
            chat_id, msg_id = map(int, f)
        try:
            await Bypass.edit_message_text(
                chat_id=chat_id, message_id=msg_id, text="<i>Restarted !</i>"
            )
        except Exception as e:
            LOGGER.error(e)


# =====================
# Start Bot
# =====================
Bypass.start()
LOGGER.info("FZ Bot Started!")
Bypass.loop.run_until_complete(after_restart())
idle()
Bypass.stop()

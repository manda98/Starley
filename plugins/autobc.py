from command import autobc_cmd
from helpers import CMD


__MODULES__ = "AutoBroad"
__HELP__ = """<blockquote>Command Help **Autobc**</blockquote>
<blockquote expandable>--**Basic Commands**--

    **Add text for autobc**
        `{0}autobc save` (reply text)
    **Set auto gcast on or off, before you set this please add text first**
        `{0}autobc` (on/off)
    **You can set delay for auto gcast**
        `{0}autobc delay` (number)
    **Delete text from list auto gcast**
        `{0}autobc remove` (all delete)
    **You can check all status auto gcast**
        `{0}autobc status`
    **You can check all message text auto gcast**
        `{0}autobc list`
 
**Note**: please add the text first, before enable autobc.</blockquote>
<b>   {1}</b>
"""


@CMD.UBOT("autobc")
async def _(client, message):
    return await autobc_cmd(client, message)


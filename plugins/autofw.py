from command import autofw_cmd
from helpers import CMD

__MODULES__ = "AutoFrwd"
__HELP__ = """<blockquote>Command Help **Autofw**</blockquote>
<blockquote expandable>--**Basic Commands**--

    **Add text for auto gcast forward**
        `{0}autofw save` (reply text)
    **Set auto gcast forward on or off, before you set this please add link first**
        `{0}autofw` (on/off)
    **Delete text from database auto forward gcast**
        `{0}autofw remove (all delete)`
    **You can set delay for auto forward gcast**
        `{0}autofw delay` (number)
    **You can check status auto forward gcast**
        `{0}autofw status`
    **You can check message text auto forward gcast**
        `{0}autofw list`
 
**Note**: please add the link first, before enable autofw.</blockquote>
<b>   {1}</b>
"""


@CMD.UBOT("autofw")
async def _(client, message):
    return await autofw_cmd(client, message)


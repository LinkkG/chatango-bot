import html
import traceback
import ch
import config
from utils import event

class Bot(ch.RoomManager):
    @event
    def onInit(self):
        pass

    @event
    def onConnect(self, room):
        croom = config.get_room(room.name)
        room.channels = tuple(croom["channels"])

    @event
    def onMessage(self, room, user, message):
        if user == self.user: return
        if not message.body.strip(): return

        msgdata = message.body.strip()
        if user.name not in config.users:
            PREFIX = config.default_user["prefix"]
        else:
            PREFIX = config.get_user(user.name)["prefix"]

        if msgdata.startswith(PREFIX):
            msgdata = msgdata[len(PREFIX):].lstrip()
        elif msgdata.startswith("@" + self.name.lower()):
            msgdata = msgdata[len(self.name):].lstrip()

        # partition always returns a 3 items tuple
        cmd, _, msgdata = msgdata.partition(" ")
        args = msgdata.split()
        cmd = cmd.lower()

        if cmd not in config.cmds:
            return

        try:
            exec(config.cmds[cmd], locals())
        except BaseException as e:
            fsize = str(self.user.fontSize).rjust(2, "0")
            fcolor = self.user.fontColor
            etype = e.__class__.__name__
            eargs  = html.escape(str(e))
            msg = '<b>{}</b>: <f x{}{}="8"><i>{}</i>'
            msg = msg.format(etype, fsize, fcolor, eargs)
            traceback.print_exc()
            room.message(msg, html=True)

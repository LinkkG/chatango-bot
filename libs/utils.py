import sys
import time
from . import ch

def arguments(*args, **kwargs):
    args = ", ".join(repr(x) for x in args)
    kwargs = ", ".join(f"{x} = {y}" for x, y in kwargs.items())
    if args and kwargs:
        return "(" + ", ".join(args, kwargs) + ")"
    return "(" + (args or kwargs) + ")"

def event(func):
    def wraper(*args, **kwargs):
        # args[0] is self, the bot
        to_print = time.strftime("%X ")
        for arg in args[1:]:
            if isinstance(arg, ch.PM):
                to_print += "[PM] "
            elif isinstance(arg, ch.Room):
                to_print += "[{}] ".format(arg.name)
            elif isinstance(arg, ch._User):
                to_print += "<{}> ".format(arg.name)
            elif isinstance(arg, ch.Message):
                to_print += repr(arg.body)[1:-1] + " "
            else:
                to_print += repr(arg)
            print(to_print)
            return func(*args, **kwargs)
    return wraper

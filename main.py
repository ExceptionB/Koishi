from v2 import message_loop,message_handlers
from bot_modules import *

# Register handlers below
message_handlers.append(KeywordsBot())
message_handlers.sort()

message_loop()
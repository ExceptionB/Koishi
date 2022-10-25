from json import dumps as jsonify, loads as from_json
from v2 import MessageHandler
from cqhttp_api import *
from RecvContext import RecvContext
from predicates import *
from common import *
from typing import Tuple


class KeywordsBot(MessageHandler):
    def __init__(self) -> None:
        super().__init__()
        self.last_response = unixtime()
        self.priority = 0

    def __eq__(self, context: RecvContext) -> Tuple[bool, bool]:
        if unixtime()- self.last_response<1000:
            return False,False
        print(str(context))
        return isGroupMessage(context) and isBeingAt(context)
    
    def __call__(self,context:RecvContext):
        config = from_json(fread("./keywords.json"))
        templates = config["templates"]
        for template in templates:
            keywords,response = template["keywords"],template["response"]
            for keyword in keywords:
                if keyword in context.raw_message:
                    self.last_response = unixtime()
                    api_send_group_msg(context.group_id,response)
                    return True
        api_send_group_msg(context.group_id,config["catch-all"])
        return True
    
    def __str__(self) -> str:
        return "KeywordsBot"
    
class DiceBot(KeywordsBot):
    def __init__(self) -> None:
        super().__init__()
        self.priority = 1

    def __call__(self, context: RecvContext) -> bool:
        return 
    
    def __eq__(self, context: RecvContext) -> Tuple[bool, bool]:
        return super().__call__(context) and "random" in context.raw_message
        
    def __str__(self) -> str:
        return "DiceBot"
    
    

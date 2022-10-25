from RecvContext import RecvContext,Sender

def isGroupMessage(self:RecvContext):
    return self.post_type == "message" and self.message_type == "group"

def isPrivateMessage(self:RecvContext):
    return  self.post_type == "message" and self.message_type == "private"

def isBeingAt(self:RecvContext):
    return f"[CQ:at,qq={self.self_id}]" in self.raw_message

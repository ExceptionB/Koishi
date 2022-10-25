import socket
import traceback
from typing import Tuple
from common import log
from RecvContext import RecvContext, fromjson

config_adapter_addr = "127.0.0.1"
config_adapter_port = 5701

message_handlers = []

CONST_HTTP_RESPONSE_TEMPALTE = \
"""\
HTTP/1.0 206 OK\r\n\
Server: AkarinAdapter alpha/1.0\r\n\
\r\n\
""".encode("utf-8")

def parse_http_request(rawData:bytes):
    lines = rawData.split(b"\r\n")
    if len(lines) < 3:
        return False,None
    sp = 0
    for x in range(1,len(lines)):
        if lines[x] == b"":
            sp = x
            break
    head = lines[0].decode("utf-8").split(" ")
    if len(head) == 3:
        return True,(head[0].lower(),head[1],lines[1:sp],lines[sp:])
    else:
        return False,None
    
def handle_socket_conn(adapter:socket.socket):
    log("begin receive message",'info')
    connection, remote = adapter.accept()
    log(f"accepted connection from {remote}","info")
    with connection:
        content = connection.recv(8192)
        connection.sendall(CONST_HTTP_RESPONSE_TEMPALTE)
        log("Connection closed",'info')
    success,result = parse_http_request(content)
    if success:
        log("packet was parsed through http protocol","info")
        handle_request(result)
    else:
        log("invaild http request! dropped",'warn')

def handle_request(result):
    method,path,header,body = result
    if method == 'post' and path == "/":
        log("begin handle message",'info')
        handle_message(fromjson("\n".join([line.decode(encoding="utf-8")for line in body])))
    else:
        log("begin handle command",'info')
        handle_command(method,path,header)

def handle_message(context):
    for handler in message_handlers:
        if (handler == context) is True:
            log(f"handler {handler} was fired",'info')
            if handler(context) is True:
                log(f"handler {handler} broke the execution chain",'info')
                break

def handle_command(method,path,headers):
    if method == 'delete':
        raise KeyboardInterrupt()

def message_loop():
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP) as adapter:
        adapter.bind((config_adapter_addr, config_adapter_port))
        adapter.listen(1024)
        log(f"message adapter initialized, listen at {config_adapter_addr}:{config_adapter_port}","info")
        while True:
            try:
                handle_socket_conn(adapter)
            except KeyboardInterrupt:
                log("Bye~",'error')
                break
            except Exception:
                log(f"Unhandled Exception occured!","error")
                traceback.print_exc()
    log("message_loop exited",'info')

class MessageHandler():
    def __init__(self) -> None:
        pass

    def __eq__(self, context: RecvContext) -> Tuple[bool,bool]:
        return False
    
    def __call__(self, context: RecvContext) -> bool:
        return True

    def __str__(self) -> str:
        return "{{name}}"
    
    priority: int = 0

    def __lt__(self,other) -> bool:
        assert other is MessageHandler
        return self.priority > other.priority
config_cqhttp_adapter_url = "http://127.0.0.1:5700/"

# cqhttp interface for python
# Reference to OneBot v11
# https://github.com/botuniverse/onebot-11/blob/master/api/public.md

from common import log
from requests import post

cqhttp_api_params = ["send_private_msg", # 发送私聊消息
"send_group_msg", # 发送群消息
"send_msg", # 发送消息
"delete_msg", # 撤回消息
"get_msg", # 获取消息
"get_forward_msg", # 获取合并转发消息
"send_like", # 发送好友赞
"set_group_kick", # 群组踢人
"set_group_ban", # 群组单人禁言
"set_group_anonymous_ban", # 群组匿名用户禁言
"set_group_whole_ban", # 群组全员禁言
"set_group_admin", # 群组设置管理员
"set_group_anonymous", # 群组匿名
"set_group_card", # 设置群名片（群备注）
"set_group_name", # 设置群名
"set_group_leave", # 退出群组
"set_group_special_title", # 设置群组专属头衔
"set_friend_add_request", # 处理加好友请求
"set_group_add_request", # 处理加群请求／邀请
"get_login_info", # 获取登录号信息
"get_stranger_info", # 获取陌生人信息
"get_friend_list", # 获取好友列表
"get_group_info", # 获取群信息
"get_group_list", # 获取群列表
"get_group_member_info", # 获取群成员信息
"get_group_member_list", # 获取群成员列表
"get_group_honor_info", # 获取群荣誉信息
"get_cookies 获取", # Cookies
"get_csrf_token 获取 CSRF", # Token
"get_credentials 获取 QQ", # 相关接口凭证
"get_record", # 获取语音
"get_image", # 获取图片
"can_send_image", # 检查是否可以发送图片
"can_send_record", # 检查是否可以发送语音
"get_status", # 获取运行状态
"get_version_info", # 获取版本信息
"set_restart 重启 OneBot", # 实现
"clean_cache"] # 清理缓存

def cqhttp_message_send(param,payload):
    log("cqhttp_send begins",'info')
    try:
        url = config_cqhttp_adapter_url+param
        log(f"post message to {url}",'info')
        with post(url,json=payload) as resp:
            if resp.ok:
                data = resp.json()
                log(f"get response from server with code={data['retcode']} status={data['status']}",'info')                
                return data
            else:
                log("failed to get response from server or server returned a error",'warn')
    except Exception as ex:
        log(f"Unhandled Exception occured!","error")
        log(ex,"error")
    log("cqhttp_send exited",'info')

def api_send_private_msg(user_id:int,message,auto_escape:bool = False):
    '''发送私聊消息'''
    return cqhttp_message_send("send_private_msg",{
        "user_id":user_id,
        "message":message,
        "auto_escape":auto_escape
    })

def api_send_group_msg(group_id:int,message,auto_escape:bool = False):
    '''发送群消息'''
    return cqhttp_message_send("send_group_msg",{
        "group_id":group_id,
        "message":message,
        "auto_escape":auto_escape
    })

def api_send_msg(message_type:str,user_id:int,group_id:int,message,auto_escape:bool = False):
    '''发送消息'''
    return cqhttp_message_send("send_msg",{
        "message_type":message_type,
        "user_id":user_id,
        "group_id":group_id,
        "message":message,
        "auto_escape":auto_escape
    })

def api_delete_msg(message_id:int):
    '''撤回消息'''
    return cqhttp_message_send("delete_msg",{
        "message_id":message_id
    })
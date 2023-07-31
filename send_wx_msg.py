import itchat

# 登录微信个人号
itchat.auto_login()

# 发送消息的函数
def send_wechat_message(friend_name, message):
    friend = itchat.search_friends(name=friend_name)  # 根据好友昵称查找好友
    if friend:
        friend_username = friend[0]['UserName']  # 获取好友的UserName
        itchat.send(message, toUserName=friend_username)  # 发送消息
        print("消息发送成功！")
    else:
        print("未找到好友：", friend_name)


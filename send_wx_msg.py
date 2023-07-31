import itchat

# 发送消息的函数
def send_wechat_message(friend_name, message):
    if friend_name:
        itchat.send(message, toUserName=friend_name)  # 发送消息
        print("消息发送成功！")
    else:
        print("未找到好友：", friend_name)


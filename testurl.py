from pyrogram import Client, filters
from pyrogram.errors import RPCError
import streamingtest

# 目标群组id, 机器人只会监听这些目标的信息,请更换这些id

CHAT_TARGET = [-1001601011623, -1001575894417]
USER_TARGET = ["@sea_leaf"]  # 可以是UID 也可以是用户名

# 你的机器人的用户名
USERNAME = "@AirportRoster_bot"

# 如果是在国内环境，则需要代理环境以供程序连接上TG
proxies = {
    "scheme": "socks5",  # "socks4", "socks5" and "http" are supported
    "hostname": "127.0.0.1",
    "port": 1111
}

# 你需要一个TG的session后缀文件，以下是session文件的名字，应形如 my_bot.session 为后缀。这个文件小心保管，不要泄露。
app = Client("my_bot", proxy=proxies)

print("程序已启动!")


@app.on_message(filters.user(USER_TARGET) | filters.chat(CHAT_TARGET))  # 只在指定的群组生效，对应上文的CHAT_TARGET
async def mytest(client, message):
    if "/testurl" in message.text or "/testurl" + USERNAME in message.text:
        back_message = await message.reply("╰(*°▽°*)╯流媒体测试进行中...")  # 发送提示
        try:
            await streamingtest.testurl(client, message, back_message=back_message)

        except RPCError as r:
            print(r)
            await client.edit_message_text(
                chat_id=message.chat.id,
                message_id=back_message.id,
                text="出错啦"
            )


app.run()

import datetime
import time
import hashlib

# hour = 1*60*60
# print(hour)
# print(int(time.time()))
# plushour = int(time.time())+hour
# print(time.ctime(time.time()))
# print(time.ctime(1670879640))
# link = 'https://t.me/SyndicateCryptocomchat'
# link = link.split('/')
# print(link)
# pseudolink = 'https://t.me/ijnsafljsngjn'
# pseudolink = pseudolink.split('/')
# print(pseudolink)

# if link[0]==pseudolink[0] and link[2]==pseudolink[2]:
#     print(link)
from telethon import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest, ImportChatInviteRequest, CheckChatInviteRequest, AddChatUserRequest
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest, GetParticipantsRequest, InviteToChannelRequest,GetFullChannelRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.types import ChannelParticipantsSearch, ChannelParticipantsRecent
import socks
import asyncio

proxy = {
    'proxy_type': 'socks5', # (mandatory) protocol to use (see above)
    'addr': '62.3.23.77',      # (mandatory) proxy IP address
    'port': 64965,           # (mandatory) proxy port number
    'username': 'K6J9L73J',      # (optional) username if the proxy requires auth
    'password': 'wCmQrpVT',      # (optional) password if the proxy requires auth
}

# proxylist = ['proxy_type','addr','port','username','password']
# proxystr = 'socks5:62.3.23.77:64965:K6J9L73J:wCmQrpVT'
# proxystr = proxystr.split(':')
# proxystr[2]=int(proxystr[2])

# proxy = dict(zip(proxylist,proxystr))
# print(proxy)
#aboba = '62.3.23.77:64965:K6J9L73J:wCmQrpVT'
# aboba = aboba.split(':')
#client = TelegramClient('./files/468424685/6281213964523/6281213964523', 8, '7245de8e747a0d6fbe11f7cc14fcc0bb',proxy=proxy)


def test_main(client:TelegramClient):
    client.send_message('@zizzs3228', 'Люто насрал')
    




async def main():
    proxylist = ['proxy_type','addr','port','username','password']
    proxystr = 'socks5:62.3.23.77:64965:K6J9L73J:wCmQrpVT'
    proxystr = proxystr.split(':')
    proxystr[2]=int(proxystr[2])

    proxy = dict(zip(proxylist,proxystr))
    print(proxy)
    client = TelegramClient('./files/468424685/6281213964523/6281213964523', 8, '7245de8e747a0d6fbe11f7cc14fcc0bb',proxy=proxy)
    async with client:
        await client.start()
        await client.send_message('@zizzs3228', 'Люто насрал')




if __name__=="__main__":
    asyncio.run(main()) 
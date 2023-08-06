import requests
from vardxg import Center, Colors, Write
import os
from colorama import init
from zeus import banner

odin = banner()

# The Headers can be changed from me everytime.

def videoStats(link):
    url = "https://bytedance.x10.mx/api/youtube/v2/?link={}".format(link)
    
    headers = {
        "x-vardxg": "1",
        "x-aurora": "0",
        "x-shibo": "0",
        "x-guest": "MQ=="
    }

    response = requests.get(url, headers=headers)
    
    data = response.json()
    videoid = data['videoDetails']['id']
    creationdate = data['videoDetails']['dateCreated']
    liked = data['videoDetails']['likes']
    disliked = data['videoDetails']['dislikes']
    viewed = data['videoDetails']['views']
            
    init(autoreset=True)
    os.system('cls')
    Write.Print(Center.XCenter(odin), Colors.blue, interval=0)

    Write.Print("\n VideoID >>> {}".format(videoid), Colors.green, interval=0)
    Write.Print("\n Created >>> {}".format(creationdate), Colors.green, interval=0)
    Write.Print("\n Likes >>> {}".format(liked), Colors.green, interval=0)
    Write.Print("\n Dislikes >>> {}".format(disliked), Colors.green, interval=0)
    Write.Print("\n Views >>> {}".format(viewed), Colors.green, interval=0)

# Made with <3 by @vardxg on Telegram.
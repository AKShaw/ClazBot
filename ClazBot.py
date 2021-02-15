import os
import json

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    with open("messages.json") as json_file:
        global messages
        messages = {}
        json_data = json.load(json_file)
        for comm in json_data["commands"]:
            messages[str(comm["evoker"])] = [str(comm["response"]["message"]), str(comm["response"]["image"])]
    
    print(f'{client.user} has connected to Discord!')
    
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    message_parts = message.content.split(" ")
    start = message_parts[0].lower()

    if start=="!clazbot":
        #Add, update messages in here, help etc
        if message_parts[1].lower()=="help":
            await message.channel.send("Commands: " + str(messages.keys()))
        else:
            await message.channel.send('Heh-low lez')
    
    if start in messages:
        text = messages[start][0]
        img_path = messages[start][1]
        
        print("Message: ", text)
        print("image: ", img_path)
        embed = discord.Embed()
        embed.set_image(url=img_path)
        await message.channel.send(text, embed=embed)
       
    print(messages.keys())

client.run(TOKEN)
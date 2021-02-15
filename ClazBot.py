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
            messages[str(comm["evoker"])] = str(comm["response"])
    
    print(f'{client.user} has connected to Discord!')
    
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    message_parts = message.content.split(" ")
    start = message_parts[0].lower()

    if start=="!clazbot":
        #Add, update messages in here, help etc
        await message.channel.send('Heh-low lez')
    
    if start in messages:
        await message.channel.send(messages[start])
       
    print(messages.keys())

client.run(TOKEN)
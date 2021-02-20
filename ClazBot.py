import os
import json
import shlex

import discord

is_prod = os.environ.get('IS_HEROKU', None)

if is_prod:
    global TOKEN = os.environ.get('DISCORD_TOKEN')
else:
    from dotenv import load_dotenv
    load_dotenv()
    global TOKEN = os.getenv("DISCORD_TOKEN")



client = discord.Client()

#Build a string of commands from the messages dictionary
def get_commands_string():
    string = "Commands: "
    for key in messages.keys():
        string += "\n\t" + key
        
    string += "\n\t!clazbot add <command> <reply> <image> \t <command> doesn't need a !. <reply> must be in quotes. <image> is optional but must be a URL if provided."
    string += "\n\t!clazbot update <command> <reply> <image> \t Same as !clazbot add."
    string += "\n\t!clazbot delete <command> \t Delete the command."
    return string


#Add a message to the ditionary, return false if it already exists
def add_message(command, reply, image):
    if command in messages:
        return False
    else:
        return update_message(command, reply, image)


#Update a message in the dictionary.
def update_message(command, reply, image):
    messages[command] = [reply, image]
    print(command, " changed to ", reply, " ", str(image))
    save_messages()
    return True

def save_messages():
    with open("messages.json", "w") as outfile:  
        json.dump(messages, outfile) 
    
#Get the command, reply and image from a message and call the appropriate method to add or update it.
def parse_add_update(message_parts, update):
    command = "!"+message_parts[2]
    reply = message_parts[3]
    image = None
    
    if len(message_parts)==5:
        image = message_parts[4]
    
    if update:
        print("Updating ", command, " in dictionary.")
        return update_message(command, reply, image)
    else:
        print("Adding ", command, " to dictionary.")
        return add_message(command, reply, image)
    
@client.event
async def on_ready():
    #Load the messages.json file into a dictionary with the command as the key
    with open("messages.json") as json_file:
        global messages
        messages = json.load(json_file)
    
    print(f'{client.user} has connected to Discord!')
    
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    message_parts = shlex.split(message.content)
    start = message_parts[0].lower()
    second_part = ""
    if len(message_parts)!=1:
        second_part = message_parts[1].lower()

    if start=="!clazbot":
        #Add, update messages in here, help etc
        if second_part=="help":
            await message.channel.send(get_commands_string())
        elif second_part=="add":
            command = "!"+message_parts[2]
        
            #Get the command, reply and image (if applicable) and call the add_message method
            result = parse_add_update(message_parts, False)
            
            if result==False:
                await message.channel.send("Command '" + command + "' is already in use, please use !clazbot update instead.")
            else:
                await message.channel.send("Added '" + command + "' successfully.")
        elif second_part=="update":
            command = "!"+message_parts[2]
            result = parse_add_update(message_parts, True)
            
            await message.channel.send("Updated '" + command + "'.")
        elif second_part=="delete":
            to_delete = "!"+message_parts[2]
            result = messages.pop(to_delete, None)
            save_messages()

            if result is not None:
                print("Deleted ", to_delete)
                await message.channel.send(to_delete + " has been successfully deleted.")
            else:
                await message.channel.send(to_delete + " does not exist.")
        else:
            await message.channel.send('Heh-low lez')
    
    #If the command isnt a clazbot command, look for it in the messages dictionary.
    if start in messages:
        text = messages[start][0]
        img_path = messages[start][1]
        
        if img_path is not None:
            embed = discord.Embed()
            embed.set_image(url=img_path)
            await message.channel.send(text, embed=embed)
        else:
            await message.channel.send(text)

client.run(TOKEN)
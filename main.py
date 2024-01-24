import discord
import requests
import os
import json
import random
from keep_alive import keep_alive

prefix = "?"
client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
  await client.change_presence(activity=discord.Activity(
    type=discord.ActivityType.listening, name=f"{prefix}[message]"))


@client.event
async def on_message(message):
  if message.author != client.user and message.content.startswith(prefix):
    userMessage = message.content
    newString = ""
    finalString = ""
    realString = ""
    words = userMessage.split()
    for x in words:
      url = f"https://api.datamuse.com/words?sl={x}"
      data = json.loads(requests.get(url).content)
      randomizer = random.randint(0, len(data) - 1)
      dict = data[randomizer]
      newString += dict["word"]
      newString += " "
    for i in range(len(newString)):
      if newString[i] == " ":
        finalString += " "
      if newString[i] != "" and "i":
        if (i % 2 == 0):
          finalString += newString[i].upper()
        else:
          finalString += newString[i].lower()

    realString = finalString[0:len(finalString) - 2]
    points = ["!", "!!", "!!!"]
    index = random.randint(0, 2)
    realString += points[index]

    #await message.channel.send(realString)  -> this code used to send the message in the channel itself, but I modified it so that it replies to the original message instead! I also added a checker that makes sure the msg doesn't exceed char limit.

    if (len(realString) > 2000):
      await message.reply(
        "My message exceeded the 2000 character limit. Try again!",
        mention_author=False)
    else:
      await message.reply(realString, mention_author=False)


keep_alive()

try:
  client.run(os.environ['token'])
except:
  os.system("kill 1")

import discord
from discord.ext import commands
import os
import asyncio

intents = discord.Intents.all()
client = commands.Bot(command_prefix='$', intents=intents)


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  # projects dictionary to store all projects from users in server
  projects = {}

  # user id as key
  user_id = message.author.id

  # each user gets a separate dictionary created for them to store their projects
  # project will be organized {number:list}
  if message.author == client.user:
    return

  if message.content.startswith('$'):
    msg = message.content
    if 'commands' in msg.lower():
      await message.channel.send(
          "This bot uses the following commands\n to add a project - $addproject\nshowcase your project in server - $showcase"
      )

    if 'addproject' in msg.lower():

      projects[user_id] = {}

      await message.channel.send("Add project name:")

      def check(author):

        def inner_check(message):
          if message.author != author:
            return False
          try:
            int(message.content)
            return True
          except ValueError:
            return False

        return inner_check

      msg = await client.wait_for('message', check=check)

      name = msg.content
      projects[user_id].update({name:[]})

      
      await message.channel.send("Successfully added name!")

      
      await message.channel.send("Add project type:")
      msg = await client.wait_for('message', check=check)

      type = msg.content
      projects[user_id][name].append(type)
      await message.channel.send("Successfully added type!")

      await message.channel.send("Add project materials:")
      msg = await client.wait_for('message', check=check)

      materials = msg.content
      projects[user_id][name].append(materials)
      await message.channel.send("Successfully added materials!")

      flag = False
      projPer = 0
      while not flag:
        await message.channel.send(
            "How far along are you with the project? (Enter a percentage, without the '%'):"
        )
        msg = await client.wait_for('message', check=check)

        projPer = msg.content

        def is_float(string):
          if string.replace(".", "").isnumeric():
            return True
          else:
            return False
          
        if is_float(projPer):
          await message.channel.send("Successfully added project percentage!")
          projects[user_id][name].append(projPer)
          flag = True
        else:
          await message.channel.send("Please enter a valid number")

      await message.channel.send("Would you like to add personal goals? (y/n)")
      msg = await client.wait_for('message', check=check)

      if 'y' in msg.content.lower():

        #personal goals
        goalNum = 0
        flag = False
        while not flag:
          await message.channel.send("How many goals do you want to set?")

          msg = await client.wait_for('message', check=check)

          goalNum = msg.content

          if goalNum.isnumeric():
            flag = True
          else:
            message.channel.send("Please enter a valid number")

        goals = []
        for x in range(int(goalNum)):
          await message.channel.send("Enter goal")

          # to fix bug where bot input gets stored instead
          flag = False
          while not flag:
            msg = await client.wait_for('message', check=check)
            if msg.author.id == user_id:
              goals.append(msg.content)
              flag = True

        projects[user_id][name].append(goals)
        await message.channel.send("Successfully added goals!")
      # else user sees N/A

      def printGoals(goalsList):
        goals = ""
        if not goals:
          return "N/A"
        for x in goalsList:
          print(goalsList)
          goals+=x+"\n"
        return goals
      
      await message.channel.send("You have added a project!")
      await message.channel.send("Project Name: "+name+"\nProject Type: "+projects[user_id][name][0]+"\nProject Materials: "+projects[user_id][name][1]+"\nProject Percentage Completed: "+projects[user_id][name][2]+"\nProject Goals:\n"+printGoals(projects[user_id][name][3]))

    if 'checkprojects' in msg.lower():
      await message.channel.send(f"<@{user_id}>'s projects")

      allprojs = ""
      projectFound = True
      try:
        projects[user_id]
      except KeyError:
        projectFound = False

      if projectFound:
        for x in projects[user_id]:
          allprojs+=x+"\n"
  
        await message.channel.send("Projects\n"+allprojs)
      else:
        await message.channel.send("No projects found!")

    else:
      await message.channel.send(
          'To read all of the commands, enter "$commands"!')


@client.command()
async def hello(ctx):
  await ctx.send("Hello")


client.run(os.getenv('TOKEN'))

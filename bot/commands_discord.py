import discord

from discord.ext import commands
import random
import numpy as np
import locale
import matplotlib.pyplot as plt
import os
from PIL import Image
from datetime import datetime
import csv
import pandas as pd
from bot.commands_aux import *
import shutil

lang = locale.getdefaultlocale()
if lang[0] == 'fr_FR':
    from lang.fr import *
         
elif lang[0] == 'en_US':
    from lang.en import *
elif lang[0] == 'sr_RS':
    from lang.sr import *
else:
    from lang.template import *


import json
with open('config.json') as f:
    config = json.load(f)

TOKEN = config['token']
PREFIX = config['prefix']
MIN = config['min']
ROLE = config['role']

processed_reactions = {}

class Mybot(commands.Bot):
    async def on_ready(self):
        activity = discord.Game(name='RP', type=discord.ActivityType.playing)
        await bot.change_presence(status=discord.Status.dnd, activity=activity)
        print(login + f'{self.user}  (ID: {self.user.id})')
        print('------')
        for i in bot.guilds:
            print(connected_on + i.name)
        print('------')


intents = discord.Intents.default()
intents.message_content = True
bot = Mybot(command_prefix=PREFIX,intents=intents)

data = {}
cheating_dictionary = {}

@bot.command(
    description='This command rolls a random number between 0 and the specified number (default: 100). For example, to roll a number between 0 and 50, you can use the command "!r 50".',
    help='This command rolls a random number between 0 and the specified number (default: 100). For example, to roll a number between 0 and 50, you can use the command "!r 50".'
)
async def r(ctx, max_: int = 100):
    if max_ < 0:
        max_ *= -1
    if max_ <= MIN:
        x = await ctx.send(f"```Your number cannot be less than the minimum which is {str(MIN)} ...```")
        return
    r_min = MIN
    r_max = max_
    if ctx.author.display_name in cheating_dictionary.keys():
        r_min = int(cheating_dictionary [ctx.author.display_name] [0] / 100 * max_) 
        r_max = int(cheating_dictionary [ctx.author.display_name] [1] / 100 * max_)
    if not os.path.exists(ctx.guild.name):
        os.makedirs(ctx.guild.name)
    value = random.randrange(r_min, r_max+1)
    _value = value / r_max * 100
    user = ctx.author.display_name
    update_csv(ctx, user, _value, loadCSV(ctx))
    x = await ctx.send(f"```{ctx.author.display_name} {made} {str(value)} {on} [{str(max_)}]```")
    await ctx.message.delete()
    if value == MIN:
        await x.add_reaction('\N{CROSS MARK}')
    elif value == max_:
        await x.add_reaction('\N{WHITE HEAVY CHECK MARK}')

@bot.command(
    description = 'Cheating command, This command creates piped dice for the user like this !cheat NAME min max',
    help = 'This command creates piped dice for the user, the command like this !cheat NAME min max',
    hidden=True
)
async def cheat(ctx, name, min:int, max:int):
    if ctx.author.guild_permissions.manage_roles or discord.utils.get(ctx.author.roles, name = ROLE):
        cheating_dictionary [name] = [min, max]
        await ctx.message.delete()
    else:
        await ctx.send("This command do not exist.")
@bot.command(
    name = 'clear_cheat',
    aliases=['cc'],
    description = 'Clear the cheating dictionnary',
    help = 'Clear the cheating dictionnary, like this !clear_cheat NAME, you also can use !cc NAME',
    hidden=True
)
async def clear_cheating_dictionnary(ctx, name):
    if ctx.author.guild_permissions.manage_roles or discord.utils.get(ctx.author.roles, name = ROLE):
        if cheating_dictionary [name] is not None:
            cheating_dictionary.pop(name)
        await ctx.message.delete()
    else:
        await ctx.send("This command do not exist.")

    
@bot.command(
    name='clear',
    aliases=['c'],
    description='Deletes all images generated by !stat command in the current server',
    help='This command deletes all images generated by !stat command in the current server. To use this command, type "!clear"., you also can use !c.'
)
async def clear_image(ctx):
    if ctx.author.guild_permissions.manage_roles or discord.utils.get(ctx.author.roles, name = ROLE):
        # Code pour la commande
        file_list = os.listdir(f"{ctx.guild.name}/users/")
        png_files = [f for f in file_list if f.endswith('.png')]
        for file_name in png_files:
            file_path = os.path.join(f"{ctx.guild.name}/users/", file_name)
            os.remove(file_path)
        os.remove(f"{ctx.guild.name}/statistic.png")
        await ctx.message.delete()
        await ctx.send('Clear successful !')
    else:
        await ctx.send(f"You don't have the permission to use this command, ask admin to do it or {ROLE}.")
    
@bot.command(
    name='save',
    aliases=['sa'],
    description='Saves the current plot data to a folder',
    help='This command saves the current data, you can use the command "!save" or "!sa".'
)
async def save(ctx):
    if ctx.author.guild_permissions.manage_roles or discord.utils.get(ctx.author.roles, name = ROLE):
        now = datetime.now()
        folder_name = now.strftime("%Y-%m-%d %H.%M")
        file_path = ctx.guild.name+"/save/" + folder_name
        # Create the save folder if it doesn't exist
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        try:
            file_list = os.listdir(f"{ctx.guild.name}/users/")
            png_files = [f for f in file_list if f.endswith('.png')]
            for file_name in png_files:
                # Save the png image to a file in the save folder
                with open(ctx.guild.name+ "/users/" + file_name, 'rb') as f:
                    image = f.read()
                with open(os.path.join(file_path, file_name), 'wb') as f:
                    f.write(image)

            with open(ctx.guild.name + "/statistic.png", 'rb') as f:
                image = f.read()
            with open(os.path.join(file_path, "statistic.png"), 'wb') as f:
                f.write(image)
            with open(ctx.guild.name + "/compare.png", 'rb') as f:
                image = f.read()
            with open(os.path.join(file_path, "compare.png"), 'wb') as f:
                f.write(image)
            shutil.copy2(f"{ctx.guild.name}/roll.csv", file_path)
            # Send a message to confirm that the save was successful
            await ctx.send('Files saved to the save folder!')
        except:
            await ctx.send(f'There is no data, try running the {PREFIX}plot, {PREFIX}stat commands for saving all data.')
    else:
        await ctx.send(f"You don't have the permission to use this command, ask admin to do it or {ROLE}.")
    


@bot.command(
    name='plot',
    aliases=['p'],
    description='Plots the data of the current server',
    help='This command plots the data of the current server, you can use the command "!plot" or "!p", you can also specify a user to plot his data, for example "!plot @user".'
)
async def plot(ctx, user : discord.User = None):
    try:
        if not os.path.exists(f"{ctx.guild.name}/users/"):
            os.makedirs(f"{ctx.guild.name}/users/")
        ctx_data = pd.read_csv(f"{ctx.guild.name}/roll.csv", sep=',')
        for names in ctx_data['Name']:
            plot_aux(ctx, names, ctx_data)

        x = send_to_discord(ctx)
        if user is not None:
            await ctx.send(file=discord.File(f"{ctx.guild.name}/users/{user.display_name}_plot.png"))
        else:
            await ctx.send(file = x)
    except FileNotFoundError:
        await ctx.send(f'There is no data, try running the {PREFIX}r command.')

@bot.command(
    name='stat',
    aliases=['s'],
    description='Compare players rolls',
    help='This command compare players rolls, you can use the command "!stat" or "!s".'
)
async def stat(ctx):
    try:
        ctx_data = pd.read_csv(f"{ctx.guild.name}/roll.csv", sep=',')
        x = stat_player_value(ctx, ctx_data)
        await ctx.send(file=discord.File(x))
    except FileNotFoundError:
        await ctx.send(f'There is no data, try running the {PREFIX}r command.')


@bot.event
async def on_command_error(ctx, error):
    command_list = '\n'.join([f'\t{c.name}: {c.description}' for c in bot.commands])

    # Check if the error is a CommandNotFound error
    if isinstance(error, commands.CommandNotFound):
        # If the command is not found, send the help message to the user
        await ctx.send(f'```Sorry, I don\'t recognize that command. Here is a list of the commands that I know:\n{command_list}```')
    else:
        # For other types of errors, print the error to the console
        print(error)


@bot.event
async def on_reaction_add(reaction, user):
    emoji = reaction.emoji
    if reaction.message.id in processed_reactions and user.id in processed_reactions[reaction.message.id]:
        return
    else:        
        if user.bot:
            return
        if emoji == '\N{CROSS MARK}':
            await reaction.message.reply(str(user.display_name) + space + laught)
            if reaction.message.id not in processed_reactions:
                processed_reactions[reaction.message.id] = []
            processed_reactions[reaction.message.id].append(user.id)
        elif emoji == '\N{WHITE HEAVY CHECK MARK}':
            await reaction.message.reply(str(user.display_name) + space + congratulate)
            if reaction.message.id not in processed_reactions:
                processed_reactions[reaction.message.id] = []
            processed_reactions[reaction.message.id].append(user.id)
    print(processed_reactions)


bot.run(TOKEN)
import discord

from discord.ext import commands
import random
import numpy as np
import locale
import matplotlib.pyplot as plt
import os
from PIL import Image
from datetime import datetime

lang = locale.getdefaultlocale()
if lang[0] == 'fr_FR':
    from lang.fr import *
         
elif lang[0] == 'en_US':
    from lang.en import *
elif lang[0] == 'sr_RS':
    from lang.sr import *
else:
    from lang.template import *

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
bot = Mybot(command_prefix='!',intents=intents)


@bot.command(
    description='Rolls a random number between 0 and the specified number',
    help='This command rolls a random number between 0 and the specified number (default: 100). For example, to roll a number between 0 and 50, you can use the command "!r 50".'
)
async def r(ctx, number: int = 100):
    file_path = serveur_path(ctx)
    if not os.path.exists(ctx.guild.name):
        os.makedirs(ctx.guild.name)
    value = random.randrange(1, number+1)
    _value = value/number*100
    user = ctx.author.display_name
    found = False
    random_numbers = load(ctx.guild.name)
    for entry in random_numbers:
        if entry[0] == user:
            entry.append(_value)
            found = True
            break
    if not found:
        random_numbers.append([user, _value])
    x = await ctx.send(f"```{ctx.author.display_name} "+ made + str(value) + space + on + "[" + str(number) + "]```")
    await ctx.message.delete()
    if value == 0:
        await x.add_reaction('\N{CROSS MARK}')
    elif value == number:
        await x.add_reaction('\N{WHITE HEAVY CHECK MARK}')


    with open(file_path, "w") as f:
        for entry in random_numbers:
            f.write(entry[0] + ": " + ", ".join([str(x) for x in entry[1:]]) + "\n")


def load(guild_name):
    random_numbers = []
    # Open the file in read mode
    if not os.path.exists(guild_name + "/roll.txt"):
        f = open(guild_name + "/roll.txt", "x")
    file_path = f"{guild_name}/roll.txt"
    with open(file_path, "r") as f:
        # Read the lines of the file into a list
        lines = f.readlines()

    # Process the lines of the file
    for line in lines:
        # Split the line by the colon and space
        user, numbers = line.strip().split(": ")
        # Convert the string of numbers into a list of integers
        numbers = [float(x) for x in numbers.split(", ")]
        # Add the user and numbers data to the list
        random_numbers.append([user, *numbers])
    return random_numbers


@bot.command(
    description='Send to channel statistics by user',
    help='Send to channel statistics by user'
)
async def stat(ctx):
    await ctx.message.delete()
    file_path = serveur_path(ctx)
    if not os.path.exists(f"{ctx.guild.name}/users/"):
            os.makedirs(f"{ctx.guild.name}/users/")
    try:
        # Open the file in read mode
        with open(file_path, "r") as f:
            # Read the lines of the file into a list
            lines = f.readlines()

        # Initialize a dictionary to store the data
        data = {}

        # Process the lines of the file
        for line in lines:
            # Split the line by the colon and space
            user, numbers = line.strip().split(": ")
            # Convert the string of numbers into a list of integers
            numbers = [float(x) for x in numbers.split(", ")]
            # Add the data to the dictionary
            data[user] = numbers

        # Initialize a dictionary to store the frequency of the numbers by range
        frequencies = {i: 0 for i in range(0, 101, 10)}

        # Process the data to count the frequency of the numbers by range for each user
        for user, numbers in data.items():
            # Reset the frequencies for the current user
            frequencies = {i: 0 for i in range(0, 101, 10)}
            for number in numbers:
                range_start = number // 10 * 10
                frequencies[range_start] += 1

            # Get the names of the ranges
            ranges = list(frequencies.keys())

            # Get the frequencies of the numbers by range
            counts = list(frequencies.values())

            # Plot the data for the current user
            plt.bar(ranges, counts)
            plt.xlabel(value_of_roll)
            plt.ylabel(frequency)
            plt.title(f" {freq_numb} {user} ({total}: {len(numbers)})")
            filename = f"{ctx.guild.name}/users/{user}_plot.png"
            plt.savefig(filename)
            #plt.show()
            plt.clf()
        # Send the file in Discord
        x = send_to_discord(ctx)
        await ctx.send(file=x)

    except:
        await ctx.send("There is no roll data for this server, try : !r") 

def send_to_discord(ctx):
    images = []
    
    file_list = os.listdir(f"{ctx.guild.name}/users/")

    png_files = [f for f in file_list if f.endswith('.png')]

    for file_name in png_files:
        file_path = os.path.join(f"{ctx.guild.name}/users/", file_name)
        image = Image.open(file_path)
        images.append(image)
    
    total_width = sum(image.width for image in images)
    max_height = max(image.height for image in images)

    result_image = Image.new('RGB', (total_width, max_height))
    x_offset = 0
    for image in images:
        result_image.paste(image, (x_offset, 0))
        x_offset += image.width

    result_image.save(f"{ctx.guild.name}/statistic.png")

    result_file = discord.File(f"{ctx.guild.name}/statistic.png")

    return result_file

def serveur_path(ctx):
    guild_name = ctx.guild.name
    file_path = f"{guild_name}/roll.txt"
    return file_path

    
@bot.command(
description='Deletes all images generated by !stat command in the current server',
help='This command deletes all images generated by !stat command in the current server. To use this command, type "!clear_images".'
)
async def clear_image(ctx):
    file_list = os.listdir(f"{ctx.guild.name}/users/")
    png_files = [f for f in file_list if f.endswith('.png')]
    for file_name in png_files:
        file_path = os.path.join(f"{ctx.guild.name}/users/", file_name)
        os.remove(file_path)
    await ctx.message.delete()
    await ctx.send('Clear successful !')


@bot.command(
    description='Send user data to a channel',
    help ='Send user data to a channel'
)
async def affiche(ctx, user : discord.User):
    await ctx.message.delete()
    await ctx.send(file=discord.File(f"{ctx.guild.name}/users/{user.display_name}_plot.png")) 




@bot.command(
    name='save',
    description='Saves the current plot data to a folder',
    help='This command saves the current data, you can use the command "!s".'
)
async def save(ctx):
    now = datetime.now()
    folder_name = now.strftime("%Y-%m-%d %H.%M")

    file_path = ctx.guild.name+"/save/" + folder_name
    
    # Create the save folder if it doesn't exist
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    file_list = os.listdir(f"{ctx.guild.name}/users/")
    try:
    # Calculate the total width and maximum height of the result image
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
        # Send a message to confirm that the save was successful
        await ctx.send('Files saved to the save folder!')
    except:
        await ctx.send('There is no data, try running the !stat command.')



@bot.event
async def on_command_error(ctx, error):
    command_list = '\n'.join([f'{c.name}: {c.description}' for c in bot.commands])
    # Check if the error is a CommandNotFound error
    if isinstance(error, commands.CommandNotFound):
        # If the command is not found, send the help message to the user
        await ctx.send(f'Sorry, I don\'t recognize that command. Here is a list of the commands that I know:\n{command_list}')
    else:
        # For other types of errors, print the error to the console
        print(error)


@bot.event
async def on_reaction_add(reaction, user):
    emoji = reaction.emoji
    if user.bot:
        return

    if emoji == '\N{CROSS MARK}':
        await reaction.message.reply(str(user.display_name) + space + laught)
    elif emoji == '\N{WHITE HEAVY CHECK MARK}':
        await reaction.message.reply(str(user.display_name) + space + congratulate)


bot.run('YOUR-TOKEN')
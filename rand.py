import random #Cette bibilothèque permet de faire du randome
import numpy as np #Numpy (pour "Numeric Python") est une bibliothèque de Python qui fournit des outils avancés pour la manipulation de tableaux et de matrices de données numériques.
import os #permet de lire ecrire ou autre fonction de de système (compatible linux mac et windows)
import matplotlib.pyplot as plt
from PIL import Image
from datetime import datetime

min : int = 1

def serveur_path(nomServ):
    guild_name = nomServ
    file_path = f"{guild_name}/roll.txt"
    return file_path

def load(guild_name):
    random_numbers = []
    # Open the file in read mode
    if not os.path.exists(guild_name + "/roll.txt"):
        f = open(guild_name + "/roll.txt", "x", encoding="utf-8")
    file_path = f"{guild_name}/roll.txt"
    with open(file_path, "r", encoding="utf-8") as f:
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

def rand(max: int = 100):
    if(min < max):
        value = random.randrange(min, max + 1)
    else:
        value = random.randrange(0, max + 1)
    value / (max + 1 - min ) * 100

def ajouterValeur(value : int = 0, nomServ : str = 'erreurNomServ', nomUser = 'erreurNomUser'  ):
    if nomServ == 'erreurNomServ':
        print('Erreur pour ajouter une valeur dans les stats pas de nom serveur indiquer')
        return False
    if nomUser == 'erreurNomUser':
        print('Erreur nom de l\'utilisateur n\'est pas indiquer' )
        return False
    file_path = serveur_path(nomServ)
    if not os.path.exists(nomServ):
        os.makedirs(nomServ)
    random_numbers = load(nomServ)
    for entry in random_numbers:
        if entry[0] == nomUser:
            entry.append(value)
            found = True
            break
    if not found:
        random_numbers.append([nomUser, value])
    with open(file_path, "w", encoding="utf-8") as f:
        for entry in random_numbers:
            f.write(entry[0] + ": " + ", ".join([str(x) for x in entry[1:]]) + "\n")
            
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
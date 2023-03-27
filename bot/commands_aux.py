import discord
import os
from PIL import Image
from datetime import datetime
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def loadCSV(ctx, data):
    try:
        with open(f"{ctx.guild.name}/roll.csv", mode="r", newline="") as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if i == 0:
                    continue
                data[row[0]] = [float(x) for x in row[1:]]
        return data
    except FileNotFoundError:
        print("File not found, creating the file")
        with open(f"{ctx.guild.name}/roll.csv", mode="w", newline=""):
            pass

def update_csv(ctx, name, value, data):
    size = 0
    for _, values in data.items():
        if size < len(values):
            size = len(values)
    if name in data:
        data[name].append(value)
    else:
        data[name] = [value]
    with open(f"{ctx.guild.name}/roll.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name"] + [f"Value_{i}" for i in range(0, size+1)])
        for name, values in data.items():
            writer.writerow([name] + values)
    return data



def stat(name, data):
    name_data = data.loc[data['Name'] == name].iloc[:, 1:].values
    name_values = name_data[~np.isnan(name_data)]
    name_sum = name_values.sum()
    name_mean = name_values.mean()
    name_min = name_values.min()
    name_max = name_values.max()
    name_median = np.median(name_values)
    name_std_dev = name_values.std()
    bins = np.arange(0, 110, 10)
    name_frequency, _ = np.histogram(name_values, bins=bins)
    name_frequency = name_frequency.tolist()
    name_variance = name_values.var()

    name_stats = {
        'Name': name,
        'Sum': name_sum,
        'Mean': name_mean,
        'Min': name_min,
        'Max': name_max,
        'Median': name_median,
        'Standard Deviation': name_std_dev,
        'Frequency': name_frequency,
        'Variance': name_variance,
    }

    return name_stats

def plot_aux(ctx, name, data):
    bins = np.arange(0, 110, 10)
    plot_data = stat(name, data)
    fig, ax = plt.subplots()
    plt.bar(bins[:-1]+5, plot_data['Frequency'], width=10, color='aqua', edgecolor='black', alpha=0.3, label=name + ' Frequency')
    plt.axvline(plot_data['Mean'], color='r', linestyle='--', label=name + ' Mean')
    plt.axvline(plot_data['Median'], color='g', linestyle='-.', label=name + ' Median')
    plt.axvline(plot_data['Min'], color='black', linestyle=':', label=name + ' Min')
    plt.axvline(plot_data['Max'], color='blue' ,linestyle=':', label=name + ' Max')
    plt.legend()
    ax.set_xlabel('Value')
    ax.set_ylabel('Frequency')
    ax.set_xticks(bins)
    ax.set_title(f'{name}_statistics')
    #plt.show()
    fig.savefig(f"{ctx.guild.name}/users/{name}_plot.png")





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

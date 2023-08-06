import subprocess, platform, string
from datetime import datetime
from time import sleep

def has_duplicates(lst):
    if len(lst) == len(set(lst)):
        return False
    else:
        return True

def estimateReadingtime(words_number):
    reading = (0.4615/60) * words_number
    return reading

def print_options(array):
    for index, option in enumerate(array):
        print(str(index+1) + ".", option)

def first_chars(str, chars):
    return(str[:chars])

def last_chars(str, chars):
    return (str[-chars:])

def reverse_string(str):
    return str[::-1]

def clear_terminal():
    if platform.system()=="Windows":
        subprocess.Popen("cls", shell=True).communicate() 
    else:
        print("\033c", end="")

def number_of_words(title):
    text = title.split(" ")
    total_words = len(text)
    return total_words

def hex_to_rgb(hex):
    rgb = []
    for i in (0, 2, 4):
        decimal = int(hex[i:i+2], 16)
        rgb.append(decimal)
    return tuple(rgb)
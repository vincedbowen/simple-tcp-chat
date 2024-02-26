from colorama import Fore
import random


def get_random_color():
    colors = list(vars(Fore).values())
    text_color = random.choice(colors)
    return text_color

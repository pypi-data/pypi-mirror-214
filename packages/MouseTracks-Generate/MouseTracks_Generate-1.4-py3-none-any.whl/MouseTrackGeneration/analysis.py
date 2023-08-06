import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
import random

ana = pd.read_csv('length_analysis.csv')
ana = ana.sort_values(by='distance')
y = ana['length'].values
x = ana['distance'].values
p = np.polyfit(x, y, 6)
fx = np.poly1d(p)


def get_length(startx ,starty, stopx, stopy):
    dx = abs(stopx - startx)
    dy = abs(stopy - starty)
    distance = int(math.sqrt(dx**2 + dy**2))
    length = int(fx(distance))
    length = random.randint(length-10, length+10)
    return length

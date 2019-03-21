import matplotlib.pyplot as plt
import numpy as np
import os
import json

with open('points.json') as json_file:
        players = json.load(json_file)

points = []

for player in players:
    if not player['points'] == 'admin':
        point = int(player['points'])
        points.append(point)

plt.hist(points)
plt.savefig('plot.png')
import matplotlib.pyplot as plt
import pandas as pd
from mplsoccer import Pitch
from mplsoccer import Pitch, FontManager, Sbopen
from mplsoccer.utils import add_image
from urllib.request import urlopen
from PIL import Image
import json

# Read JSON data from file
with open('data/week_7/ahly_benghazi_2023-12-23_akhdar.json') as file:
    json_data = json.load(file)

# Extracting data
passes = [item['data'] for item in json_data['object'] if 'source' in item['data']]
positions = [item for item in json_data['object'] if 'renderedPosition' in item]

# Convert to DataFrame
df_passes = pd.DataFrame(passes)
df_positions = pd.DataFrame([{
    'player_id': position['data']['id'],
    'x': position['renderedPosition']['x'],
    'y': position['renderedPosition']['y'],
    'name': position['data']['NickNameEn']
} for position in positions])

# pitch = Pitch(pitch_type='statsbomb', pitch_color='#151a24', line_color='#c7d5c8')
# fig, ax = pitch.draw(figsize=(16, 11), constrained_layout=True, tight_layout=False)
# fig.set_facecolor("#151a24")

# Define the max values for x and y based on your pitch dimensions
max_x, max_y = 120, 80

# Scale the x and y coordinates
df_positions['x'] = (df_positions['x'] / df_positions['x'].max()) * max_x
df_positions['y'] = (df_positions['y'] / df_positions['y'].max()) * max_y

# Convert to integer format
df_positions['x'] = df_positions['x'].astype(int)
df_positions['y'] = df_positions['y'].astype(int)


# # Plot passes with transparency
# for _, row in df_passes.iterrows():
#     source = df_positions[df_positions['player_id'] == row['source']].iloc[0]
#     target = df_positions[df_positions['player_id'] == row['target']].iloc[0]
#     pitch.lines(source['x'], source['y'], target['x'], target['y'], lw=2, color='white', alpha=0.2, ax=ax)

# # Plot player positions and names with an offset above the circle
# offset = 4  # Adjust this value as needed for better visibility
# for _, row in df_positions.iterrows():
#     pitch.scatter(row['x'], row['y'], s=200, color='red', ax=ax)
#     plt.text(row['x'], row['y'] + offset, row['name'], fontsize=13, ha='center', va='bottom', color='white', zorder=5)

# Create a pitch with a dark background
pitch_color = '#0b132b'  # Deep navy blue
line_color = '#ffffff'   # White

pitch = Pitch(pitch_type='statsbomb', pitch_color=pitch_color, line_color=line_color)
fig, ax = pitch.draw(figsize=(16, 11), constrained_layout=True, tight_layout=False)
fig.set_facecolor(pitch_color)

# Plot passes with neon colors
pass_line_color = '#00ff00'  # Electric green
for _, row in df_passes.iterrows():
    source = df_positions[df_positions['player_id'] == row['source']].iloc[0]
    target = df_positions[df_positions['player_id'] == row['target']].iloc[0]
    pitch.lines(source['x'], source['y'], target['x'], target['y'], lw=2, color=pass_line_color, alpha=0.2, ax=ax)

# Plot player positions with contrasting colors
player_circle_color = '#ff007f'  # Bright pink
offset = 4  # Adjust this value as needed for better visibility
for _, row in df_positions.iterrows():
    pitch.scatter(row['x'], row['y'], s=200, color=player_circle_color, ax=ax)
    plt.text(row['x'], row['y'] + offset, row['name'], fontsize=12, ha='center', va='bottom', color=line_color, zorder=5)

# Adding a title
plt.title("ThirdMan | Ahly Benghazi Passflow vs Al Ahkdar | Round 8", fontsize=20, color=line_color)

plt.show()

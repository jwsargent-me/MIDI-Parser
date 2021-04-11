from PIL import Image
import numpy as np
import json
from pathlib import Path
import array
import os

# GET PATH
file_name = "O Little Town of Bethlehem"
path = "D:/Dropbox/PyCharm Projects/MIDI Parser/JSON/" + file_name + ".json"
path = Path(__file__).parent / path

# GET JSON DATA
with path.open() as f:
    data = json.load(f)

# VARIABLE DEFINITIONS
white = [255, 255, 255]
black = [0, 0, 0]
rows = 64
fps = 30
max_frame = 0

# PREPARE NOTE ARRAYS
prev_val = array.array('i', (0 for i in range(0, 127)))
new_val = array.array('i', (0 for o in range(0, 127)))

note_val = {i: 0 for i in range(0, 127)}
note_offset = 20

# GET FINAL FRAME
for e in data:
    max_frame = data[e]['frame']

# DEFINE IMAGE
img_w, img_h = 88, max_frame
img_data = np.zeros((img_h, img_w, 3), dtype=np.uint8)
frame_image = np.zeros((rows, img_w, 3), dtype=np.uint8)

# PREPARE IMG DATA ARRAY
for e in data:
    if data[e]['type'] == 'note_on':
        n = data[e]['note']
        t = data[e]['frame']
        img_data[t, n - note_offset] = white
        note_val[n] = t
    if data[e]['type'] == 'note_off':
        n = data[e]['note']
        t = note_val[n]
        new_t = data[e]['frame']
        for k in range(t, new_t):
            img_data[k, n - note_offset] = white

        note_len = new_t - t

# SAVE IMAGE
img = Image.fromarray(img_data, 'RGB')
img.save('./RENDERS/' + file_name + '__full_range.png', interpolation='NEAREST')

# ENSURE PROPER DIRECTORY EXISTS
frame_dir = './RENDERS/Frames/' + file_name

if not os.path.isdir(frame_dir):
    os.mkdir(frame_dir)

# EXPORT FRAMES FOR ANIMATED TEXTURE
for frame in range(max_frame):
    if frame + rows < max_frame:
        area = [0, frame, 88, frame + rows]
        img.crop(area).save(frame_dir + '/frames_' + str(frame).zfill(8) + '.jpg', interpolation='NEAREST')

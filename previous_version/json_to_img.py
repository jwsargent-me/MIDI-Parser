from PIL import Image
import numpy as np
import json
from pathlib import Path
import array


def get_ticks_per_frame(bpm, ppq, fps):
    tps = ppq * (bpm / 60)
    tpf = tps / fps
    return tpf


def get_time(t, d):
    new_time = round(t / d)
    return new_time


def get_frame_img(img_data, frame, frame_image, rows):
    for r in range(rows):
        for n in img_data[frame + r]:
            frame_image[r, n] = img_data[frame + r, n]
    return frame_image


path = Path(__file__).parent / "./Still, Still, Still.json"
with path.open() as f:
    data = json.load(f)

white = [255, 255, 255]
black = [0, 0, 0]
rows = 64
ppq = 480
bpm = 120
fps = 60
tpf = get_ticks_per_frame(bpm, ppq, fps)
tick_divisor = tpf

prev_val = array.array('i', (0 for i in range(0, 127)))
new_val = array.array('i', (0 for o in range(0, 127)))

note_val = {i: 0 for i in range(0, 127)}
note_offset = 20

for e in data:
    max_time = data[e]['all_time']

img_w, img_h = 88, round(max_time / tpf)
img_data = np.zeros((img_h, img_w, 3), dtype=np.uint8)
frame_image = np.zeros((rows, img_w, 3), dtype=np.uint8)

for e in data:
    if data[e]['type'] == 'note_on':
        n = data[e]['note']
        t = get_time(data[e]['all_time'], tick_divisor)
        img_data[t, n - note_offset] = white
        note_val[n] = t
    if data[e]['type'] == 'note_off':
        n = data[e]['note']
        t = note_val[n]
        new_t = get_time(data[e]['all_time'], tick_divisor)
        for l in range(t, new_t):
            img_data[l, n - note_offset] = white

        note_len = new_t - t

img = Image.fromarray(img_data, 'RGB')
img.save('full_range.png', interpolation='NEAREST')
img.show()

max_frame = round(max_time / tpf)

for frame in range(max_frame):
    if frame + rows < max_frame:
        area = [0, frame, 88, frame + rows]
        img.crop(area).save('./RENDERS/Frames/frames_' + str(frame) + '.jpg', interpolation='NEAREST')

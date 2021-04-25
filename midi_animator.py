import bpy
import json
from pathlib import Path


def set_blank_keys(n, fr):
    # define animation target object
    obj = bpy.data.objects[str(n)]

    obj.rotation_euler = (obj.rotation_euler[0], obj.rotation_euler[1], obj.rotation_euler[2])

    obj.keyframe_insert(data_path='rotation_euler', frame=fr)
    obj.keyframe_insert(data_path='color', frame=fr)


def set_anim_keys(n, fr, v, m, vel):
    # define animation target object
    obj = bpy.data.objects[str(n)]

    col = v * (vel / 127)

    # set animation keyframes
    obj.color = (v, v, v, 1)
    obj.rotation_euler = (v, obj.rotation_euler[1], obj.rotation_euler[2])
    obj.keyframe_insert(data_path='rotation_euler', frame=fr)
    obj.keyframe_insert(data_path='color', frame=fr)


def note_on(note, value, frame, mult):
    ease_frames = round((127 / value) * mult)

    note = str(note).zfill(3)

    n = anim_series + note

    set_blank_keys(n, frame - ease_frames)
    set_anim_keys(n, frame, 1, velocity_multiplier, value)


def note_off(note, frame):
    note = str(note).zfill(3)

    n = anim_series + note

    set_blank_keys(n, frame)
    set_anim_keys(n, frame + 4, 0, velocity_multiplier, 0)


# Global variables
file_name = 'Revive Us Again'
path = 'D:/Dropbox/PyCharm Projects/MIDI Parser/JSON/' + file_name + '.json'
path = Path(__file__).parent / path

anim_series = 'Fac - Note '
ease_multiplier = 3
velocity_multiplier = 45

# Open json data file
with path.open() as f:
    data = json.load(f)

for e in data:
    if data[e]['type'] == 'note_on':
        note_on(data[e]['note'], data[e]['value'], data[e]['frame'], ease_multiplier)
    if data[e]['type'] == 'note_off':
        note_off(data[e]['note'], data[e]['frame'])

'''
Potential issues:
 - It appears that midi notes may be slightly early, but consistently so
 - Some notes may be getting dropped/garbled. Part of this is how blank frames are set, 
    and part of this is how they are generated. When writing to frames, we lose a lot of data. 
    Might be worth saving to 60fps and then rendering out every other frame
    For example, a note on and a note off event could potentially occur on the same frame
 -  
'''

import bpy
import json
from pathlib import Path


def set_blank_keys(n, fr):
    obj = bpy.data.objects[str(n)]
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
    ease_frames = mult  # - round((value / 127) * mult)

    note = str(note).zfill(3)

    n = 'Fac - Note ' + note

    set_blank_keys(n, frame - ease_frames)
    set_anim_keys(n, frame, 1, velocity_multiplier, value)


def note_off(note, value, frame, mult):
    ease_frames = mult - round((value / 127) * mult)

    note = str(note).zfill(3)

    n = 'Fac - Note ' + note

    set_blank_keys(n, frame)
    set_anim_keys(n, frame + ease_frames, 0, velocity_multiplier, 0)


# def pedal_change(v, t):
#     frame = get_frame(t, ticks_per_frame)


# Global variables
path = Path(__file__).parent / "D:\Dropbox\PyCharm Projects\MIDI Parser\JSON\Angels We Have Heard On High b.json"

ease_multiplier = 1
velocity_multiplier = 45

# Open json data file
with path.open() as f:
    data = json.load(f)

for e in data:
    if data[e]['type'] == 'note_on':
        note_on(data[e]['note'], data[e]['value'], data[e]['frame'], ease_multiplier)
    if data[e]['type'] == 'note_off':
        note_off(data[e]['note'], data[e]['value'], data[e]['frame'], ease_multiplier)

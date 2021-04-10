import bpy
import json
from pathlib import Path


def get_ticks_per_frame(bpm, ppq, fps):
    tps = ppq * (bpm / 60)
    tpf = tps / fps
    return tpf


def add_time(c, t):
    c += t
    return c


def get_frame(t, tf):
    frame = (t / tf)
    return round(frame)


def set_blank_keys(n, f):
    obj = bpy.data.objects[str(n)]
    obj.keyframe_insert(data_path='rotation_euler', frame=f)
    obj.keyframe_insert(data_path='color', frame=f)


def set_anim_keys(n, f, v, m, vel):
    # define animation target object
    obj = bpy.data.objects[str(n)]

    # set amplitude of motion
    amp = v * (0.075)
    col = v * (vel / 127)

    # set animation keyframes
    obj.color = (v, v, v, 1)
    obj.rotation_euler = (obj.rotation_euler[0], amp, obj.rotation_euler[2])
    obj.keyframe_insert(data_path='rotation_euler', frame=f)
    obj.keyframe_insert(data_path='color', frame=f)


def note_on(n, v, e, t):
    ease_frames = e - round((v / 127) * e)
    frame = get_frame(t, ticks_per_frame)

    set_blank_keys(n, frame - ease_frames)
    set_anim_keys(n, frame, 1, velocity_multiplier, v)


def note_off(n, v, e, t):
    ease_frames = e - round((v / 127) * e)
    frame = get_frame(t, ticks_per_frame)

    set_blank_keys(n, frame)
    set_anim_keys(n, frame + ease_frames, 0, velocity_multiplier, 0)


def pedal_change(v, t):
    frame = get_frame(t, ticks_per_frame)


# Global variables
path = Path(__file__).parent / "../midi_json_ver2_2.json"

ppq = 480
bpm = 120
fps = 60

c_time = 0
ease_multiplier = 6
velocity_multiplier = 4
ticks_per_frame = get_ticks_per_frame(bpm, ppq, fps)

# Open json data file
with path.open() as f:
    data = json.load(f)

for e in data:
    # Increase global tick count
    if 'time' in data[e]:
        c_time = add_time(c_time, data[e]['time'])
    # Check if event is note_on, note_off, or control_change (pedal)
    if data[e]['type'] == 'note_on':
        note_on(data[e]['note'], data[e]['velocity'], ease_multiplier, c_time)
    if data[e]['type'] == 'note_off':
        note_off(data[e]['note'], data[e]['velocity'], ease_multiplier, c_time)
    if data[e]['type'] == 'control_change' and data[e]['control'] == 64:
        pedal_change(data[e]['value'], c_time)
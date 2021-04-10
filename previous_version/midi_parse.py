from mido import MidiFile, tick2second, second2tick, tempo2bpm
import json


def get_rate(ppq, t):
    ms_per_tick = 60000 / (t * ppq)
    tick_per_sec = (ms_per_tick * 1000)
    return ms_per_tick, tick_per_sec


mid = MidiFile('YOUR_MIDI.mid', clip=True)

data = {}
json_data = {}
ppq = mid.ticks_per_beat
quarter_duration = tick2second(ppq, ppq, 500000)
ticks_per_second = second2tick(1, ppq, 500000)
tempo = 120
c_time = 0
abs_time = 0

for z, t in enumerate(mid.tracks):
    for i, m in enumerate(t):
        print(m)
        i_pad = str(i).rjust(4, '0')
        event = 'event_' + i_pad
        data[event] = {}
        d = data[event]

        if m.type in ("note_on", "note_off"):
            c_time += m.time
            d['type'] = m.type
            d['note'] = m.note
            d['velocity'] = m.velocity
            d['time'] = m.time
            d['all_time'] = c_time

        elif m.type == "control_change":
            c_time += m.time
            d['type'] = m.type
            d['control'] = m.control
            d['value'] = m.value
            d['time'] = m.time
            d['all_time'] = c_time

        elif m.type == "set_tempo":
            c_time += m.time
            TEMPO = tempo2bpm(m.tempo)
            d['type'] = m.type
            d['tempo'] = TEMPO
            d['all_time'] = c_time
            print(d['tempo'])

        else:
            d['type'] = 'empty'
            d['time'] = 0
            d['all_time'] = c_time

    json_data[str(z)] = data

tickrate = get_rate(ppq, TEMPO)

with open('YOUR_JSON.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)
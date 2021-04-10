import os
import mido
import time
import json


def get_time_info(md):      # md = input_midi
    tr = 0.0

    for t in md.tracks:
        if t.name == file_name:
            tempo = 0
            for m in t:
                if 'set_tempo' in str(m):
                    tempo = m.tempo

            # define the tick multiplier to get seconds
            if tempo > 0:
                tr = get_tick_ratio(tempo, md.ticks_per_beat)

            else:
                print('ERROR: Tempo data not found!')

    return tr


def get_tick_ratio(t, ppq):     # t = tempo, ppq = pulse per quarter
    ticks_per_quarter = ppq
    us_per_quarter = t
    us_per_tick = us_per_quarter / ticks_per_quarter
    seconds_per_tick = us_per_tick / 1000000

    return seconds_per_tick


def msg_time(gt, t, tr):    # gt = global_tick, t = msg.time, tr = tick_ratio
    gt = gt + t
    sec = gt * tr
    fr = round(sec * frame_rate)
    tm = time.strftime('%H:%M:%S', time.gmtime(round(sec)))

    return gt, sec, fr, tm


def process_msg(m, m_note, m_val, p):
    if p:
        msg_print(m, m_note, m_val)

    msg_dict = msg_to_dict(m, m_note, m_val)

    return msg_dict


def msg_print(m, m_note, m_val):        # m = msg and m_val is the message value
    print('Tick: ' + str(global_tick) +
          ' - Frame: ' + str(msg_frame) +
          ' - Time: ' + str(msg_timestamp) +
          ' - ' + str(m.type) + ':  note - ' + str(m_note) + '  value - ' + str(m_val))


def msg_to_dict(m, n, v):       # d = data, f = msg_frame, v = values
    data[global_tick] = {}
    d = data[global_tick]
    d['type'] = m.type
    d['frame'] = msg_frame
    d['note'] = n
    d['value'] = v

    return data[global_tick]


def json_print(d):
    json_object = json.dumps(d, indent=4)
    print(json_object)

    return json_object


def json_write(d):
    with open('./JSON/' + file_name + '.json', 'w') as outfile:
        json.dump(d, outfile, indent=4)


# Global Variables
data = {}

global_tick = 0
frame_rate = 30

will_msg_print = False

directory = os.fsencode('./MIDI/')

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".mid") or filename.endswith(".midi"):
        # print(os.path.join(directory, filename))
        continue
    else:
        continue

file_name = 'Away In A Manger'
input_midi = mido.MidiFile('./MIDI/' + file_name + '.mid')
# maybe cycle through all MIDI files in the repository? Should be easy to add
#
# - tempo data is extracted from the file per tempo event I believe, at least per file
# - json is printed based on midi file name
# - basically all data necessary is derived, no hard coded inputs

# Get the tick ratio
tick_ratio = get_time_info(input_midi)

# go through all recorded data events and pull desired messages
for tracks in input_midi.tracks:
    if tracks.name == 'Record':
        for msg in tracks:
            # Get message time elements
            global_tick, msg_sec, msg_frame, msg_timestamp = msg_time(global_tick, msg.time, tick_ratio)

            # print note events to console
            if msg.type in ['note_on', 'note_off']:
                process_msg(msg, msg.note, msg.velocity, will_msg_print)

            # print pedal control events to console
            if msg.type in ['control_change']:
                if msg.control == 64:
                    process_msg(msg, msg.control, msg.value, will_msg_print)

json_print(data)
json_write(data)

'''

Currently, 
 - my script will import a MIDI file
 - get the tempo/tick data from the file 
 - generate a list of entries with frame and time info
 - this includes sustain and note events (do I need any others for piano animation?)

What I need to implement
 - save data to a .json
 - save data to a .csv
 - plan how animations will work
 - create a method to generate scrolling tiles like I had before from the csv or json file
 
IDEAS:
 - Have the json file only register actual events for animation purposes. 
 This will save file size and make animation curves much cleaner
 
 - Have the csv fill in cells until a note turns back off so it is a continuous stream per row.
 This could make it easier to generate scrolling textures which could be very useful.
    One CONCERN: This solution will take a ton of data for larger midi files, 
    and I think this could potentially be completely mitigated with an elegant system
     during the texture generation stage 
  
  - 
  
  Other Goals:
   - Clean up functions and variables, this structure needs some work
   - Make sure this will play nicely with external execution
   - 
  
'''

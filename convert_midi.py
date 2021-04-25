import os
import mido
import time
import json


def get_time_info(md):  # md = input_midi
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


def get_tick_ratio(t, ppq):  # t = tempo, ppq = pulse per quarter
    ticks_per_quarter = ppq
    us_per_quarter = t
    us_per_tick = us_per_quarter / ticks_per_quarter
    seconds_per_tick = us_per_tick / 1000000

    return seconds_per_tick


def msg_time(gt, t, tr):  # gt = global_tick, t = msg.time, tr = tick_ratio
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


def msg_print(m, n, v):  # m = msg, n = note, v = value
    print('Tick: ' + str(global_tick) +
          ' - Frame: ' + str(msg_frame) +
          ' - Time: ' + str(msg_timestamp) +
          ' - ' + str(m.type) + ':  note - ' + str(n) + '  value - ' + str(v))


def msg_to_dict(m, n, v):  # m = msg, n = note, v = value
    msg_id = str(message_num + 1).zfill(6)
    data[msg_id] = {}
    d = data[msg_id]
    d['type'] = m.type
    d['frame'] = msg_frame
    d['note'] = n
    d['value'] = v

    return data[msg_id]


def json_print(d):
    json_object = json.dumps(d, indent=4)
    print(json_object)

    return json_object


def json_write(d):
    json_path = './JSON/'
    if not os.path.isdir(json_path):
        os.mkdir(json_path)

    with open(json_path + file_name + '.json', 'w') as outfile:
        json.dump(d, outfile, indent=4)


# Global Variables
frame_rate = 60             # this determines how frame values are generated
will_msg_print = False      # temporary bool to control console printing of data dict

directory = os.fsencode('./MIDI/')

for file in os.listdir(directory):
    input_midi = None
    data = {}
    global_tick = 0
    message_num = 0

    filename = os.fsdecode(file)

    if filename.endswith(".mid") or filename.endswith(".midi"):
        file_name = os.path.splitext(filename)[0]

        input_midi = mido.MidiFile('./MIDI/' + filename)

        # get the tick ratio
        tick_ratio = get_time_info(input_midi)

        # go through all recorded data events and pull desired messages
        for tracks in input_midi.tracks:
            if tracks.name == 'Piano':      # Make sure to update this to match recorded channel name
                for msg in tracks:
                    message_num = message_num + 1
                    # Get message time elements
                    global_tick, msg_sec, msg_frame, msg_timestamp = msg_time(global_tick, msg.time, tick_ratio)

                    # print note events to console
                    if msg.type in ['note_on', 'note_off']:
                        process_msg(msg, msg.note, msg.velocity, will_msg_print)

                    # print pedal control events to console
                    if msg.type in ['control_change']:
                        if msg.control == 64:
                            process_msg(msg, msg.control, msg.value, will_msg_print)

        json_write(data)

'''

Notes:
 -
  
'''

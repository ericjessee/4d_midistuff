import mido
import threading
import time

#iterate through all of the midi messages in the track, and build a big list.
#each list index corresponds to one midi tick.
#only supporting one note for now. for multiple notes, timeline can be a nested array, or a dict.
#also only support for note on/off with velocity
def create_timeline_single(track):
    tick_count=0
    timeline = []
    for message in track:
        print(f'got {message.type}')
        if message.type == 'note_on':
            for i in range(0, message.time):
                timeline.append(message.velocity / 127) #scale to a weight between 0 and 1
        elif message.type == 'note_off':
            for i in range(0, message.time):
                timeline.append(0)
        tick_count += message.time
    return timeline, tick_count

#directly mapping frames to ticks for now. can potentially scale
def midi_callback(frame, timeline, outfile):
    #this print statement is a stand in for the API call to output the weight from the
    #xpresso node
    print(f'{timeline[frame]}', file=outfile)

#essentially a standin for the frame increment coming from
#cinema4d. This is will obviously block the main thread,
#so might need to create a seperate thread to handle the 
#frame events.
def frame_counter(num_frames, timeline):
    with open('output.txt', 'x') as outfile:
        for frame in range(0, num_frames):
            midi_callback(frame, timeline, outfile)

if __name__ == "__main__":
    #replace the filename with any midi file
    testfile = mido.MidiFile('mixed_velocities.mid')
    track = testfile.tracks[1]
    timeline, tick_count = create_timeline_single(track)
    frame_counter(tick_count, timeline)
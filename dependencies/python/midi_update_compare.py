import mido
import sys
from collections import defaultdict
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Define the note name maps for different tracks
note_name_maps = {
    'PART GUITAR': {
        127: "LANE MARKER",
        126: "LANE MARKER",
        124: "BRE",
        123: "BRE",
        122: "BRE",
        121: "BRE",
        120: "BRE (use all 5)",
        116: "OVERDRIVE",
        105: "h2h note",
        106: "h2h note",
        103: "Solo Marker",
        102: "Force HOPO Off",
        101: "Force HOPO On",
        100: "EXPERT Orange",
        99: "EXPERT Blue",
        98: "EXPERT Yellow",
        97: "EXPERT Red",
        96: "EXPERT Green",
        90: "Force HOPO Off",
        89: "Force HOPO On",
        88: "HARD Orange",
        87: "HARD Blue",
        86: "HARD Yellow",
        85: "HARD Red",
        84: "HARD Green",
        76: "MEDIUM Orange",
        75: "MEDIUM Blue",
        74: "MEDIUM Yellow",
        73: "MEDIUM Red",
        72: "MEDIUM Green",
        64: "EASY Orange",
        63: "EASY Blue",
        62: "EASY Yellow",
        61: "EASY Red",
        60: "EASY Green",
        59: "Left Hand Highest",
        40: "Left Hand Lowest"
    },
    'PART BASS': {
        127: "LANE MARKER",
        126: "LANE MARKER",
        124: "BRE",
        123: "BRE",
        122: "BRE",
        121: "BRE",
        120: "BRE (use all 5)",
        116: "OVERDRIVE",
        102: "Force HOPO Off",
        101: "Force HOPO On",
        100: "EXPERT Orange",
        99: "EXPERT Blue",
        98: "EXPERT Yellow",
        97: "EXPERT Red",
        96: "EXPERT Green",
        90: "Force HOPO Off",
        89: "Force HOPO On",
        88: "HARD Orange",
        87: "HARD Blue",
        86: "HARD Yellow",
        85: "HARD Red",
        84: "HARD Green",
        76: "MEDIUM Orange",
        75: "MEDIUM Blue",
        74: "MEDIUM Yellow",
        73: "MEDIUM Red",
        72: "MEDIUM Green",
        64: "EASY Orange",
        63: "EASY Blue",
        62: "EASY Yellow",
        61: "EASY Red",
        60: "EASY Green",
        59: "Left Hand Highest",
        40: "Left Hand Lowest"
    },
    'BEAT': {
        13: "Up Beats",
        12: "Downbeat"
    },
    'HARM1': {
        116: "OVERDRIVE",
        105: "Phrase Marker",
        83: "Highest Note B4",
        82: "A#4",
        81: "A4",
        80: "G#4",
        79: "G4",
        78: "F#4",
        77: "F4",
        76: "E4",
        75: "D#4",
        74: "D4",
        73: "C#4",
        72: "C4",
        71: "B3",
        70: "A#3",
        69: "A3",
        68: "G#3",
        67: "G3",
        66: "F#3",
        65: "F3",
        64: "E3",
        63: "D#3",
        62: "D3",
        61: "C##",
        60: "C3",
        59: "B2",
        58: "A#2",
        57: "A2",
        56: "G#2",
        55: "G2",
        54: "F#2",
        53: "F2",
        52: "E2",
        51: "D#2",
        50: "D2",
        49: "C#2",
        48: "C2",
        47: "B1",
        46: "A#1",
        45: "A1",
        44: "G#1",
        43: "G1",
        42: "F#1",
        41: "F1",
        40: "E1",
        39: "D#1",
        38: "D1",
        37: "C#1",
        36: "Lowest Note C1",
        1: "Lyric Shift"
    },
    'PART REAL_KEYS_X': {
        127: "LANE MARKER",
        126: "GLISSANDO MARKER",
        116: "OVERDRIVE",
        115: "SOLO",
        72: "Highest playable note B#3",
        71: "B3",
        70: "A#3",
        69: "A3",
        68: "G#3",
        67: "G3",
        66: "F#3",
        65: "F3",
        64: "E3",
        63: "D#3",
        62: "D3",
        61: "C#3",
        60: "C3",
        59: "B2",
        58: "A#2",
        57: "A2",
        56: "G#2",
        55: "G2",
        54: "F#2",
        53: "F2",
        52: "E2",
        51: "D#2",
        50: "D2",
        49: "C#2",
        48: "Lowest playable note C2",
        9: "Range A2-C4",
        5: "Range F2-A3",
        0: "Range C2-E3"
    },
    'PART KEYS': {
        127: "LANE MARKER",
        124: "BRE",
        123: "BRE",
        122: "BRE",
        121: "BRE",
        120: "BRE (use all 5)",
        116: "OVERDRIVE",
        103: "Solo Marker",
        100: "EXPERT Orange",
        99: "EXPERT Blue",
        98: "EXPERT Yellow",
        97: "EXPERT Red",
        96: "EXPERT Green",
        88: "HARD Orange",
        87: "HARD Blue",
        86: "HARD Yellow",
        85: "HARD Red",
        84: "HARD Green",
        76: "MEDIUM Orange",
        75: "MEDIUM Blue",
        74: "MEDIUM Yellow",
        73: "MEDIUM Red",
        72: "MEDIUM Green",
        64: "EASY Orange",
        63: "EASY Blue",
        62: "EASY Yellow",
        61: "EASY Red",
        60: "EASY Green"
    },
    'PART VOCALS': {
        116: "OVERDRIVE",
        105: "Phrase Marker",
        97: "Non-Displayed Percussion",
        96: "Displayed Percussion",
        83: "Highest Note B5",
        82: "A#4",
        81: "A4",
        80: "G#4",
        79: "G4",
        78: "F#4",
        77: "F4",
        76: "E4",
        75: "D#4",
        74: "D4",
        73: "C#4",
        72: "C4",
        71: "B3",
        70: "A#3",
        69: "A3",
        68: "G#3",
        67: "G3",
        66: "F#3",
        65: "F3",
        64: "E3",
        63: "D#3",
        62: "D3",
        61: "C#3",
        60: "C3",
        59: "B2",
        58: "A#2",
        57: "A2",
         56: "G#2",
        55: "G2",
        54: "F#2",
        53: "F2",
        52: "E2",
        51: "D#2",
        50: "D2",
        49: "C#2",
        48: "C2",
        47: "B1",
        46: "A#1",
        45: "A1",
        44: "G#1",
        43: "G1",
        42: "F#1",
        41: "F1",
        40: "E1",
        39: "D#1",
        38: "D1",
        37: "C#1",
        36: "Lowest Note C1",
        1: "Lyric Shift",
        0: "Range Shift"
    },
    'PART DRUMS': {
        127: "CYMBAL SWELLS",
        126: "DRUM ROLL",
        124: "DRUM FILL",
        123: "DRUM FILL",
        122: "DRUM FILL",
        121: "DRUM FILL",
        120: "DRUM FILL (use all 5)",
        116: "OVERDRIVE",
        112: "TOM GEMS PAD 4",
        111: "TOM GEMS PAD 3",
        110: "TOM GEMS PAD 2",
        103: "Solo Marker",
        100: "EXPERT Green",
        99: "EXPERT Blue",
        98: "EXPERT Yellow",
        97: "EXPERT Red",
        96: "EXPERT Kick",
        95: "EXPERT 2xKick",
        88: "HARD Green",
        87: "HARD Blue",
        86: "HARD Yellow",
        85: "HARD Red",
        84: "HARD Kick",
        76: "MEDIUM Green",
        75: "MEDIUM Blue",
        74: "MEDIUM Yellow",
        73: "MEDIUM Red",
        72: "MEDIUM Kick",
        64: "EASY Green",
        63: "EASY Blue",
        62: "EASY Yellow",
        61: "EASY Red",
        60: "EASY Kick",
        52: "DRUM ANIMATION",
        51: "FLOOR TOM RH",
        50: "FLOOR TOM LH",
        49: "TOM2 RH",
        48: "TOM2 LH",
        47: "TOM1 RH",
        46: "TOM1 LH",
        45: "SOFT CRASH 2 LH",
        44: "CRASH 2 LH",
        43: "RIDE LH",
        42: "RIDE CYM RH",
        41: "CRASH2 CHOKE",
        40: "CRASH1 CHOKE",
        39: "CRASH2 SOFT RH",
        38: "CRASH2 HARD RH",
        37: "CRASH1 SOFT RH",
        36: "CRASH1 HARD RH",
        35: "CRASH1 SOFT LH",
        34: "CRASH1 HARD LH",
        32: "PERCUSSION RH",
        31: "HI-HAT RH",
        30: "HI-HAT LH",
        29: "SOFT SNARE RH",
        28: "SOFT SNARE LH",
        27: "SNARE RH",
        26: "SNARE LH",
        25: "HI-HAT OPEN",
        24: "KICK RF"
    }
}

# Time window for grouping events
TIME_WINDOW = 1
# Threshold for considering minor timing differences as insignificant
TIME_THRESHOLD = 1

# Define the notes to ignore for specific tracks
IGNORED_NOTES = {
    'NONE': {95}
}

# Define the tracks to ignore
IGNORED_TRACKS = {'NONE'}

def load_midi_tracks(file_path):
    mid = mido.MidiFile(file_path)
    tracks = {}
    for track in mid.tracks:
        for msg in track:
            if msg.type == 'track_name':
                tracks[msg.name] = track
                break
    return tracks

def extract_note_events(track, note_range, ignore_notes=None):
    note_events = defaultdict(list)
    current_time = 0
    for msg in track:
        current_time += msg.time
        if msg.type == 'note_on' or msg.type == 'note_off':
            if msg.note in note_range and (ignore_notes is None or msg.note not in ignore_notes):
                note_events[current_time].append(msg.note)
    return note_events

def group_events_by_time_window(events, time_window):
    grouped_events = defaultdict(list)
    for time, notes in events.items():
        grouped_time = min(grouped_events.keys(), key=lambda t: abs(t - time) if abs(t - time) <= time_window else float('inf'), default=time)
        if abs(grouped_time - time) <= time_window:
            grouped_events[grouped_time].extend(notes)
        else:
            grouped_events[time].extend(notes)
    return grouped_events

def compare_tracks(track1_events, track2_events, time_window, time_threshold):
    differences = []

    grouped_track1 = group_events_by_time_window(track1_events, time_window)
    grouped_track2 = group_events_by_time_window(track2_events, time_window)

    all_times = sorted(set(grouped_track1.keys()).union(grouped_track2.keys()))

    for time in all_times:
        base_set = set(grouped_track1.get(time, []))
        update_set = set(grouped_track2.get(time, []))
        if base_set != update_set:
            added = update_set - base_set
            removed = base_set - update_set

            if added or removed:
                # Check for corresponding events within the time threshold
                close_matches = False
                for other_time in all_times:
                    if time != other_time and abs(time - other_time) <= time_threshold:
                        other_base_set = set(grouped_track1.get(other_time, []))
                        other_update_set = set(grouped_track2.get(other_time, []))
                        if (removed & other_update_set) or (added & other_base_set):
                            close_matches = True
                            break

                if not close_matches:
                    differences.append((time, list(removed), list(added)))
                else:
                    # Check if removed notes have corresponding added notes within the threshold
                    for note in removed:
                        if not any(note in set(grouped_track2.get(t, [])) for t in all_times if abs(time - t) <= time_threshold):
                            differences.append((time, [note], []))
                    
                    # Check if added notes have corresponding removed notes within the threshold
                    for note in added:
                        if not any(note in set(grouped_track1.get(t, [])) for t in all_times if abs(time - t) <= time_threshold):
                            differences.append((time, [], [note]))

    return differences

def format_comparison(removed, added, note_name_map):
    messages = []
    if removed:
        removed_str = ', '.join(note_name_map.get(note, f"Unknown Note ({note})") for note in removed)
        messages.append(f"removed: {removed_str}")
    if added:
        added_str = ', '.join(note_name_map.get(note, f"Unknown Note ({note})") for note in added)
        messages.append(f"added: {added_str}")
    return ', '.join(messages)

def main(shortname, note_range=range(60, 128)):
    midi_file1 = os.path.join(REPO_ROOT, '_ark', 'songs', 'vanilla', shortname, f'{shortname}_update.mid')
    midi_file2 = os.path.join(REPO_ROOT, '_ark', 'songs', 'updates', shortname, f'{shortname}_update.mid')
    output_file = os.path.join(REPO_ROOT, '_ark', 'songs', 'updates', shortname, f'{shortname}_update.txt')

    if not os.path.exists(midi_file1):
        #missing_output_file = os.path.join(REPO_ROOT, '_ark', 'songs', 'updates', shortname, f'{shortname}_missingupdate.txt')
        #with open(missing_output_file, 'w') as f:
        #    f.write("MISSING")
        print(f"Update file '{midi_file1}' is missing.")
        return

    if not os.path.exists(midi_file2):
        #missing_output_file = os.path.join(REPO_ROOT, '_ark', 'songs', 'updates', shortname, f'{shortname}_missingupdate.txt')
        #with open(missing_output_file, 'w') as f:
        #    f.write("MISSING")
        print(f"Update file '{midi_file2}' is missing.")
        return

    tracks1 = load_midi_tracks(midi_file1)
    tracks2 = load_midi_tracks(midi_file2)
    
    new_tracks = sorted(t for t in tracks2 if t not in tracks1 and shortname not in t and not t.endswith('_plus') and t not in IGNORED_TRACKS)
    no_update_tracks = sorted(t for t in tracks1 if t not in tracks2 and shortname not in t and not t.endswith('_plus') and t not in IGNORED_TRACKS)

    for track_name in new_tracks:
        print(f"New track in update: '{track_name}'")
    for track_name in no_update_tracks:
        print(f"No update track for existing: '{track_name}'")

    if no_update_tracks:
        missing_output_file = os.path.join(REPO_ROOT, '_ark', 'songs', 'vanilla', shortname, f'{shortname}_missingupdate.txt')
        with open(missing_output_file, 'w') as f:
            for track_name in no_update_tracks:
                f.write(f"No update track for existing: '{track_name}'\n")

    significant_changes = False
    output_lines = []

    common_tracks = sorted(set(tracks1) & set(tracks2) - IGNORED_TRACKS)
    for track_name in common_tracks:
        ignore_notes = IGNORED_NOTES.get(track_name, None)
        track1_events = extract_note_events(tracks1[track_name], note_range, ignore_notes)
        track2_events = extract_note_events(tracks2[track_name], note_range, ignore_notes)
        
        differences = compare_tracks(track1_events, track2_events, TIME_WINDOW, TIME_THRESHOLD)
        note_name_map = note_name_maps.get(track_name, {})
        
        if differences:
            significant_changes = True
            print(f"Differences found in track '{track_name}':")
            output_lines.append(f"Differences found in track '{track_name}':")
            sorted_differences = sorted(differences, key=lambda x: x[0])
            for time, removed, added in sorted_differences:
                comparison = format_comparison(removed, added, note_name_map)
                message = f"Time: {time}, {comparison}"
                print(message)
                output_lines.append(message)
        else:
            print(f"No significant changes in track '{track_name}'.")

    #if significant_changes:
    #    with open(output_file, 'w') as f:
    #        for line in output_lines:
    #            f.write(line + '\n')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python midi_update_compare.py <shortname>")
    else:
        shortname = sys.argv[1]
        main(shortname)

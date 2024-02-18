import random
#from fuzzywuzzy import process
import os
import configparser
import json
from pathlib import Path
import sys
#import pprint
import json

# removes any comments from a RB dta, and then returns a nice, tokenized list to parse
def clean_dta(dta_path: Path) -> list:
    with open(dta_path, encoding="latin1") as f:
        lines = [line.lstrip() for line in f]
    reduced_lines = [x.split(";", 1)[0] for x in lines]
    dta_as_str = ''.join(reduced_lines)
    dta_as_list = dta_as_str.replace("(", " ( ").replace(")", " ) ").split()
    return dta_as_list

# parse, read_from_tokens, and atom have all been originally written by Peter Norvig
# parse and atom have been tweaked for the purposes of parsing RB dtas
# explanations of his functions can be found here: http://norvig.com/lispy.html
def parse(program: list):
    "Read a Scheme expression from a string."
    program.insert(0, "(")
    program.append(")")
    return read_from_tokens(program)

def read_from_tokens(tokens: list):
    "Read an expression from a sequence of tokens."
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF')
    token = tokens.pop(0)
    if token == '(':
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0)  # pop off ')'
        return L
    elif token == ')':
        raise SyntaxError('unexpected )')
    else:
        return atom(token)

def atom(token: str):
    "Numbers become numbers; every other token is a symbol."
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return (str(token)).strip("'").strip('"')

# clean up name entry in case there are parentheses in the song title (i.e. (Don't Fear) The Reaper)
def dict_from_name(parsed_name) -> str:
    new_song_name_list = []
    for s in range(len(parsed_name)):
        if s > 0:
            if type(parsed_name[s]) == list:
                new_song_name_list.append("(" + " ".join(str(x) for x in parsed_name[s]) + ")")
            elif parsed_name[s] != "":
                new_song_name_list.append(str(parsed_name[s]))
    return " ".join(new_song_name_list)

# parse song part difficulties and return a dict
def dict_from_rank(parsed_rank: list):
    rank_dict = {}
    for rank in parsed_rank:
        if type(rank) == list:
            rank_dict[rank[0]] = rank[1]
    return rank_dict

# parse song info (pans, vols, etc) and return a dict
def dict_from_song(parsed_song: list):
    song_info_dict = {}
    try:
        for info in parsed_song:
            if type(info) == list:
                if "drum_" in info[0]:
                    song_info_dict[info[0]] = {}
                    song_info_dict[info[0]][info[1][0]] = info[1][1]
                elif info[0] == "name":
                    song_info_dict[info[0]] = dict_from_name(info[1])
                # elif info[0] == "song":
                #    song_info_dict[info[0]] = dict_from_song(info[1])
                elif info[0] == "rank":
                    song_info_dict[info[0]] = dict_from_rank(info[1])
                elif info[0] in ["crowd_channels"]:
                    song_info_dict[info[0]] = info[1:]
                elif info[0] not in ["tracks", "pans", "vols", "preview", "anim_tempo", "bank",
                                     "song_scroll_speed", "midi_file", "drum_freestyle", "drum_solo",
                                     "solo", "version", "format", "album_art", "tuning_offset_cents",
                                     "ugc", "context", "downloaded", "base_points", "cores", "seqs", "hopo_threshold", "song"]:
                    song_info_dict[info[0]] = info[1]
    except Exception as e:
        print_color_text(f"Error processing song info: {e}", "1;31")  # Red text
    return song_info_dict

# convert the list of lists that parse returns into a big song dictionary
def dict_from_parsed(parsed: list):
    keys_to_ignore = ["song", "master", "context", "bank", "anim_tempo", "preview", 
                      "decade", "unlockable", "song_location", "downloaded", "exported",
                      "album_art", "version", "format", "song_id", "tuning_offset_cents",
                      "game_origin", "encoding", "song_tonality", "real_guitar_tuning", "real_bass_tuning",
                      "album_track_number", "song_scroll_speed", "guide_pitch_volume", "ugc"]

    big_songs_dict = {}
    for song in parsed:
        song_dict = {}
        shortname = None  # Initialize shortname variable
        skip_entry = False  # Flag to skip processing

        for a in range(len(song)):
            if skip_entry:
                skip_entry = False
                continue

            if a == 0:  # the shortname
                shortname = song[0]
                song_dict["shortname"] = shortname  # Include shortname in the entry
            elif song[a][0] == "name":
                song_dict["name"] = dict_from_name(song[a])
            elif song[a][0] == "rank":
                song_dict["rank"] = dict_from_rank(song[a])
            elif song[a][0] in keys_to_ignore:
                skip_entry = True
            else:
                val = []
                for b in range(len(song[a])):
                    if b == 0:
                        key = song[a][b]
                    else:
                        val.append(song[a][b])
                if all(isinstance(item, str) for item in val):
                    song_dict[key] = (" ".join(x for x in val)).strip('"')
                else:
                    song_dict[key] = val if len(val) > 1 else val[0]

        if shortname is not None:  # Check if shortname is not empty
            big_songs_dict[shortname] = song_dict

    return big_songs_dict

# the main parse function - supply a path to a dta, and it will return a big song dictionary
def parse_dta(dta_path: Path, rpcs3_path: Path) -> dict:
    #print(dta_path)
    parsed = parse(clean_dta(dta_path))
    parsed_dta_dict = dict_from_parsed(parsed)
    #pprint.pprint(parsed_dta_dict, sort_dicts=False)
    return parsed_dta_dict

def parse_updates_dta(updates_dta_path: Path, existing_data: dict) -> dict:
    #print(f"Attempting to load RB3DX Metadata from: {updates_dta_path}")
    try:
        updates_parsed = parse(clean_dta(updates_dta_path))
        updates_dict = dict_from_parsed(updates_parsed)
        for shortname, updates in updates_dict.items():
            if shortname in existing_data:
                existing_data[shortname].update(updates)
                #print(f"Applying Updated Metadata for: {shortname}")
        return existing_data
    except Exception as e:
        print_color_text(f"Error processing songs_updates.dta: {e}", "1;31")  # Red text
        return existing_data

def read_json(json_file_path):
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print_color_text(f"Error: JSON file '{json_file_path}' not found. Please make sure the file exists.", "1;31")  # Red text
        return None
    except json.JSONDecodeError as e:
        print_color_text(f"Error decoding JSON file '{json_file_path}': {e}", "1;31")  # Red text
        return None

localized_genre_lookup = {
    'acapella': 'A Capella', 'acidjazz': 'Acid Jazz', 'acoustic': 'Acoustic',
    'alternative': 'Alternative', 'alternativerap': 'Alternative Rap',
    'ambient': 'Ambient', 'arena': 'Arena', 'black': 'Black Metal',
    'bluegrass': 'Bluegrass', 'blues': 'Blues', 'breakbeat': 'Breakbeat',
    'chicago': 'Chicago', 'chiptune': 'Chiptune', 'classic': 'Classic',
    'classical': 'Classical', 'classicrock': 'Classic Rock',
    'college': 'College', 'contemporary': 'Contemporary',
    'contemporaryfolk': 'Contemporary Folk', 'core': 'Core',
    'country': 'Country', 'dance': 'Dance', 'dancepunk': 'Dance Punk',
    'darkwave': 'Dark Wave', 'death': 'Death Metal', 'delta': 'Delta',
    'disco': 'Disco', 'downtempo': 'Downtempo', 'drumandbass': 'Drum and Bass',
    'dub': 'Dub', 'electric': 'Electric', 'electroclash': 'Electroclash',
    'electronica': 'Electronica', 'emo': 'Emo', 'experimental': 'Experimental',
    'folkrock': 'Folk Rock', 'funk': 'Funk', 'fusion': 'Fusion',
    'gangsta': 'Gangsta', 'garage': 'Garage', 'glam': 'Glam', 'goth': 'Goth',
    'grunge': 'Grunge', 'hair': 'Hair', 'hardcore': 'Hardcore',
    'hardcoredance': 'Hardcore Dance', 'hardcorerap': 'Hardcore Rap',
    'hardrock': 'Hard Rock', 'hiphop': 'Hip Hop', 'honkytonk': 'Honky Tonk',
    'house': 'House', 'indierock': 'Indie Rock', 'inspirational': 'Inspirational',
    'industrial': 'Industrial', 'lofi': 'Lo-fi', 'mathrock': 'Math Rock',
    'metal': 'Metal', 'motown': 'Motown', 'new_wave': 'New Wave',
    'noise': 'Noise', 'novelty': 'Novelty', 'numetal': 'Nu-Metal',
    'oldies': 'Oldies', 'oldschoolhiphop': 'Old School Hip Hop', 'other': 'Other',
    'outlaw': 'Outlaw', 'pop': 'Pop', 'poprock': 'Pop Rock',
    'postrock': 'Post Rock', 'power': 'Power', 'prog': 'Prog',
    'progrock': 'Prog Rock', 'psychadelic': 'Psychedelic', 'ragtime': 'Ragtime',
    'rap': 'Rap', 'reggae': 'Reggae', 'rhythmandblues': 'Rhythm and Blues',
    'rock': 'Rock', 'rockabilly': 'Rockabilly', 'rockandroll': 'Rock and Roll',
    'shoegazing': 'Shoegazing', 'ska': 'Ska', 'smooth': 'Smooth',
    'softrock': 'Soft Rock', 'soul': 'Soul', 'southernrock': 'Southern Rock',
    'speed': 'Speed', 'surf': 'Surf', 'synth': 'Synthpop', 'techno': 'Techno',
    'teen': 'Teen', 'thrash': 'Thrash', 'traditionalfolk': 'Traditional Folk',
    'trance': 'Trance', 'triphop': 'Trip Hop', 'undergroundrap': 'Underground Rap',
    'subgenre_acapella': 'A Capella', 'subgenre_acidjazz': 'Acid Jazz',
    'subgenre_acoustic': 'Acoustic', 'subgenre_alternative': 'Alternative',
    'subgenre_alternativerap': 'Alternative Rap', 'subgenre_ambient': 'Ambient',
    'subgenre_arena': 'Arena', 'subgenre_black': 'Black Metal',
    'subgenre_bluegrass': 'Bluegrass', 'subgenre_blues': 'Blues',
    'subgenre_breakbeat': 'Breakbeat', 'subgenre_chicago': 'Chicago',
    'subgenre_chiptune': 'Chiptune', 'subgenre_classic': 'Classic',
    'subgenre_classical': 'Classical', 'subgenre_classicrock': 'Classic Rock',
    'subgenre_college': 'College', 'subgenre_contemporary': 'Contemporary',
    'subgenre_contemporaryfolk': 'Contemporary Folk', 'subgenre_core': 'Core',
    'subgenre_country': 'Country', 'subgenre_dance': 'Dance',
    'subgenre_dancepunk': 'Dance Punk', 'subgenre_darkwave': 'Dark Wave',
    'subgenre_death': 'Death Metal', 'subgenre_delta': 'Delta',
    'subgenre_disco': 'Disco', 'subgenre_downtempo': 'Downtempo',
    'subgenre_drumandbass': 'Drum and Bass', 'subgenre_dub': 'Dub',
    'subgenre_electric': 'Electric', 'subgenre_electroclash': 'Electroclash',
    'subgenre_electronica': 'Electronica', 'subgenre_emo': 'Emo',
    'subgenre_experimental': 'Experimental', 'subgenre_folkrock': 'Folk Rock',
    'subgenre_funk': 'Funk', 'subgenre_fusion': 'Fusion',
    'subgenre_gangsta': 'Gangsta', 'subgenre_garage': 'Garage',
    'subgenre_glam': 'Glam', 'subgenre_goth': 'Goth', 'subgenre_grunge': 'Grunge',
    'subgenre_hair': 'Hair', 'subgenre_hardcore': 'Hardcore',
    'subgenre_hardcoredance': 'Hardcore Dance', 'subgenre_hardcorerap': 'Hardcore Rap',
    'subgenre_hardrock': 'Hard Rock', 'subgenre_hiphop': 'Hip Hop',
    'subgenre_honkytonk': 'Honky Tonk', 'subgenre_house': 'House',
    'subgenre_indierock': 'Indie Rock', 'subgenre_inspirational': 'Inspirational',
    'subgenre_industrial': 'Industrial', 'subgenre_lofi': 'Lo-fi',
    'subgenre_mathrock': 'Math Rock', 'subgenre_metal': 'Metal',
    'subgenre_motown': 'Motown', 'subgenre_new_wave': 'New Wave',
    'subgenre_noise': 'Noise', 'subgenre_novelty': 'Novelty',
    'subgenre_numetal': 'Nu-Metal', 'subgenre_oldies': 'Oldies',
    'subgenre_oldschoolhiphop': 'Old School Hip Hop', 'subgenre_other': 'Other',
    'subgenre_outlaw': 'Outlaw', 'subgenre_pop': 'Pop',
    'subgenre_postrock': 'Post Rock', 'subgenre_power': 'Power',
    'subgenre_prog': 'Prog', 'subgenre_progrock': 'Prog Rock',
    'subgenre_psychadelic': 'Psychedelic', 'subgenre_ragtime': 'Ragtime',
    'subgenre_rap': 'Rap', 'subgenre_reggae': 'Reggae',
    'subgenre_rhythmandblues': 'Rhythm and Blues', 'subgenre_rbsoulfunk': 'R&B/Soul/Funk',
    'subgenre_rock': 'Rock', 'subgenre_rockabilly': 'Rockabilly',
    'subgenre_rockandroll': 'Rock and Roll', 'subgenre_shoegazing': 'Shoegazing',
    'subgenre_ska': 'Ska', 'subgenre_smooth': 'Smooth',
    'subgenre_softrock': 'Soft Rock', 'subgenre_soul': 'Soul',
    'subgenre_southernrock': 'Southern Rock', 'subgenre_speed': 'Speed',
    'subgenre_surf': 'Surf', 'subgenre_synth': 'Synthpop', 'subgenre_techno': 'Techno',
    'subgenre_teen': 'Teen', 'subgenre_thrash': 'Thrash',
    'subgenre_traditionalfolk': 'Traditional Folk', 'subgenre_trance': 'Trance',
    'subgenre_triphop': 'Trip Hop', 'subgenre_undergroundrap': 'Underground Rap',
}

def get_random_genre(data):
    all_genres = {song["genre"] for song in data.values() if "genre" in song}
    all_subgenres = {song["sub_genre"] for song in data.values() if "sub_genre" in song}

    combined_genres = all_genres.union(all_subgenres)
    #print_color_text(f"{combined_genres}", "1;31")  # Red text
    random_genre_internal = random.choice(list(combined_genres)) if combined_genres else None
    
    # Map the internal genre name to the localized string
    random_genre_localized = localized_genre_lookup.get(random_genre_internal, random_genre_internal)

    return random_genre_internal, random_genre_localized

def get_random_artist(data):
    artists = {song["artist"] for song in data.values() if "artist" in song and isinstance(song["artist"], str)}
    return random.choice(list(artists)) if artists else None

def get_random_year(data):
    years = {song.get("year", song.get("year_released")) for song in data.values() if "year" in song or "year_released" in song}
    #print("All years:", years)  # Add this line to print all years
    return random.choice(list(years)) if years else None

def get_random_song(data):
    song = random.choice(list(data.values()))
    return song["name"], song["artist"]

def eval_random_song(data):
    song = random.choice(list(data.values()))
    return song["name"], song["artist"], song["shortname"]

def get_random_song_from_artist(data, artist):
    artist_songs = [song for song in data.values() if "artist" in song and isinstance(song["artist"], str) and song["artist"] == artist]

    if not artist_songs:
        print_color_text(f"No songs found for the artist '{artist}'.", "1;31")  # Red text
        return None

    song = random.choice(artist_songs)
    return song["name"], song["artist"]

def fuzzy_search(data, config_file, target_title, rpcs3_path):
    output_file_path = rpcs3_path / "dev_hdd0" / "game" / "BLUS30463" / "USRDIR" / "dx_playlist.dta"
    clear_screen()
    if target_title.startswith('genre:'):
        genre_to_search = target_title[len('genre:'):].strip()
        genre_matches = [
            (song["name"], song["artist"], song["shortname"])
            for song in data.values()
            if ("genre" in song and genre_to_search.lower() == song["genre"].lower()) or
               ("sub_genre" in song and genre_to_search.lower() == song["sub_genre"].lower())
        ]

        if genre_matches:
            random_song_title, random_artist, random_short_name = random.choice(genre_matches)
            #print_color_text(f"Random song matching genre '{genre_to_search}': '{random_song_title}' by '{random_artist}'", "1;38;5;77")  # Light Green text
            print_color_text(f"'{random_song_title}' by '{random_artist}' added to playlist.", "1;38;5;77")  # Light Green text
            append_short_name_to_output(output_file_path, random_short_name, rpcs3_path)
        else:
            print(f"No songs found in the genre '{genre_to_search}'.")
    elif target_title.startswith('year:'):
        year_to_search = target_title[len('year:'):].strip()
        year_matches = [
            (song["name"], song["artist"], song["shortname"]) 
            for song in data.values() 
            if ("year_released" in song and str(year_to_search) == str(song["year_released"])) or ("year" in song and year_to_search == song["year"])
        ]

        if year_matches:
            random_song_title, random_artist, random_short_name = random.choice(year_matches)
            #print_color_text(f"Random song from the year '{year_to_search}': '{random_song_title}' by '{random_artist}'", "1;38;5;77")  # Light Green text
            print_color_text(f"'{random_song_title}' by '{random_artist}' added to playlist.", "1;38;5;77")  # Light Green text
            append_short_name_to_output(output_file_path, random_short_name, rpcs3_path)
        else:
            print_color_text(f"No songs found in the year '{year_to_search}'.", "1;31")  # Red text
    elif target_title.startswith('artist:'):
        artist_to_search = target_title[len('artist:'):].strip()
        artist_matches = [
            (song.get("name", ""), song.get("artist", ""), song.get("shortname", ""))
            for song in data.values()
            if "artist" in song and isinstance(song["artist"], str) and artist_to_search.lower() == song["artist"].lower()
        ]

        if artist_matches:
            random_song_title, random_artist, random_short_name = random.choice(artist_matches)
            #print_color_text(f"Random song by artist '{artist_to_search}': '{random_song_title}' by '{random_artist}'", "1;38;5;77")  # Light Green text
            print_color_text(f"'{random_song_title}' by '{random_artist}' added to playlist.", "1;38;5;77")  # Light Green text
            append_short_name_to_output(output_file_path, random_short_name, rpcs3_path)
        else:
            print_color_text(f"No songs found for the artist '{artist_to_search}'.", "1;31")  # Red text

def append_short_name_to_output(output_file, short_name, rpcs3_path):
    output_file = str(output_file).strip('\"')  # Convert to string before stripping
    with open(output_file, 'r') as output:
        existing_content = output.read().strip()

    existing_short_names = [s.strip('()') for s in existing_content.split()]

    existing_short_names.append(short_name)

    with open(output_file, 'w') as output:
        output.write(f"({' '.join(existing_short_names)})")

    #print_color_text(f"Short Name '({short_name})' appended to dx_playlist.dta", "1;38;5;140")  # Darker Purple text

def refresh_options(data):
    year = get_random_year(data)
    artist = get_random_artist(data)
    song_title, _ = get_random_song(data)
    random_song_name = {get_random_song(data)}
    # Extracting unique genres and sub-genres from the data
    genres = {song["genre"] for song in data.values() if "genre" in song}
    subgenres = {song["sub_genre"] for song in data.values() if "sub_genre" in song}
    
    # Combine genres and subgenres
    all_genres = genres.union(subgenres)

    #print("Available Genres and Subgenres:", all_genres)
    
    genre = get_random_genre(data)
    song_title_direct, artist_direct, short_name_direct = eval_random_song(data)
    print(" ")
    return year, artist, song_title, genre, song_title_direct, artist_direct, short_name_direct

def get_rpcs3_path():
    rpcs3_path = input("\033[1;33mEnter the path for RPCS3: \033[0m")
    rpcs3_path = Path(rpcs3_path)
    
    if not rpcs3_path.is_dir():
        print_color_text(f"Invalid RPCS3 path provided.", "1;31")  # Red text
        exit()

    return rpcs3_path

def save_rpcs3_path(config_path: Path, rpcs3_path: Path):
    config = configparser.ConfigParser()
    config['Paths'] = {'RPCS3Folder': f'"{str(rpcs3_path)}"'}
    with open(config_path, 'w') as configfile:
        config.write(configfile)

def load_rpcs3_path(config_path: Path):
    config = configparser.ConfigParser()
    config.read(config_path)
    if 'Paths' in config and 'RPCS3Folder' in config['Paths']:
        return Path(config['Paths']['RPCS3Folder'].strip('"'))
    else:
        return None

def clear_playlist(output_file):
    clear_screen()
    with open(output_file, 'w') as output:
        output.write("")
    print_color_text(f"Playlist cleared in dx_playlist.dta", "1;31")  # Red text

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def print_color_text(*args):
    text = ' '.join(map(str, args[:-1]))
    color_code = args[-1]
    print(f"\033[{color_code}m{text}\033[0m")

def input_colorized(prompt, color_code):
    print_color_text(prompt, color_code)
    return input()

def parse_and_export_to_json():
    config_path = Path.cwd() / 'dx_play_a_show_config.ini'
    rpcs3_path = load_rpcs3_path(config_path)

    if rpcs3_path is None:
        rpcs3_path = get_rpcs3_path()
        save_rpcs3_path(config_path, rpcs3_path)

    # Assuming rpcs3_path is a pathlib.Path object
    output_file_path = rpcs3_path / "dev_hdd0" / "game" / "BLUS30463" / "USRDIR" / "dx_playlist.dta"
    output_json_path = Path.cwd() / "dx_songs.json"
    output_json_path_str = str(output_json_path)

    # Check if the directory exists
    if not os.path.exists(output_file_path.parent):
        print_color_text(f"Error: Directory {output_file_path.parent} does not exist.", "1;31")  # Red text
        sys.exit()

    # Check if the file exists
    output_file_path_str = str(output_file_path)
    if not os.path.isfile(output_file_path_str):
        print_color_text(f"Error: File {output_file_path_str} does not exist.", "1;31")  # Red text
        sys.exit()

    # Define the folders to search
    target_folders = [rpcs3_path / "dev_hdd0" / "game" / "BLUS30050",
                      rpcs3_path / "dev_hdd0" / "game" / "BLUS30463"]

    print_color_text("Finding and reading 'songs.dta' files in specified RPCS3 folder. This may take some time.", "1;36")  # Cyan text
    print_color_text("Make sure you have run Rock Band 3 Deluxe first to generate needed files.", "1;38;5;226")  # Magenta text


    # Filter the dta_files list based on the target folders
    dta_files = [dta_file for folder in target_folders
                 for dta_file in folder.rglob("songs.dta")]

    if not dta_files:
        print_color_text("No 'songs.dta' files found in the specified RPCS3 folders.", "1;31")  # Red text
        exit()

    all_parsed_dicts = {}

    for dta_file in dta_files:
        parsed_dict = parse_dta(dta_file, rpcs3_path)
        all_parsed_dicts.update(parsed_dict)

    # Parse and apply updates from songs_updates.dta
    updates_dta_path = rpcs3_path / "dev_hdd0" / "game" / "BLUS30463" / "USRDIR" / "songs_updates.dta"
    all_parsed_dicts = parse_updates_dta(updates_dta_path, all_parsed_dicts)

    # Export the output JSON to the working directory
    with open(output_json_path_str, 'w') as json_file:
        json.dump(all_parsed_dicts, json_file, indent=2)

    # Check if the JSON file already exists
    if not output_json_path.is_file():
        with open(output_json_path, 'w') as json_file:
            json.dump(all_parsed_dicts, json_file, indent=2)

    # Read the JSON file
    data = read_json(output_json_path)

    if data:
        song_title_index = "name"
        artist_index = "artist"
        year_index = "year"
        genre_index = "genre"
        short_name_index = "shortname"
        year, artist, song_title, genre, song_title_direct, artist_direct, short_name_direct = refresh_options(data)
        genre_internal, genre_display = get_random_genre(data)
        clear_screen()
        while True:
            print_color_text(f"▛▀▖      ▌   ▛▀▖        ▌ ▞▀▖ ▛▀▖   ▜          ", "1;36")  # Cyan text
            print_color_text(f"▙▄▘▞▀▖▞▀▖▌▗▘ ▙▄▘▝▀▖▛▀▖▞▀▌  ▄▘ ▌ ▌▞▀▖▐ ▌ ▌▚▗▘▞▀▖", "1;36")  # Cyan text
            print_color_text(f"▌▚ ▌ ▌▌ ▖▛▚  ▌ ▌▞▀▌▌ ▌▌ ▌ ▖ ▌ ▌ ▌▛▀ ▐ ▌ ▌▗▚ ▛▀ ", "1;36")  # Cyan text
            print_color_text(f"▘ ▘▝▀ ▝▀ ▘ ▘ ▀▀ ▝▀▘▘ ▘▝▀▘ ▝▀  ▀▀ ▝▀▘ ▘▝▀▘▘ ▘▝▀▘", "1;36")  # Cyan text
            print_color_text(f"Welcome to RB3DX Play A Show! {len(all_parsed_dicts)} songs loaded!", "1;36")  # Cyan text
            print_color_text("Choose an option:", "1;37")  # White text
            print_color_text(f"1. A random song from {str(year)}", "1;32;40")  # Red text
            print_color_text(f"2. A random song by '{artist}'", "1;38;5;196")  # Green text
            print_color_text(f"3. '{song_title_direct}' by '{artist_direct}'", "1;38;5;226")  # Yellow text
            print_color_text(f"4. A random {genre_display} song", "1;34")  # Blue text
            print_color_text("5. Refresh options", "1;38;5;208")  # Magenta text
            # print_color_text("6. Random song by search", "1;35")  # Magenta text
            print_color_text("6. Clear the playlist", "1;31")  # Red text
            print_color_text("0. Exit", "1;38;5;93")  # Magenta text



            choice = input_colorized("Enter the number of your choice: ", "1;37")  # You can choose a color code

            if choice == '1':
                fuzzy_search(data, output_file_path, f'year:{year}', rpcs3_path)
                year, artist, song_title, genre, song_title_direct, artist_direct, short_name_direct = refresh_options(data)
            elif choice == '2':
                fuzzy_search(data, output_file_path, f'artist:{artist}', rpcs3_path)
                year, artist, song_title, genre, song_title_direct, artist_direct, short_name_direct = refresh_options(data)
            elif choice == '3':
                clear_screen()
                print_color_text(f"'{song_title_direct}' by '{artist_direct}' added to playlist.", "1;38;5;77")
                append_short_name_to_output(output_file_path, short_name_direct, rpcs3_path)
                year, artist, song_title, genre, song_title_direct, artist_direct, short_name_direct = refresh_options(data)
            elif choice == '4':
                fuzzy_search(data, output_file_path, f'genre:{genre_internal}', rpcs3_path)
                genre_internal, genre_display = get_random_genre(data)
                year, artist, song_title, genre, song_title_direct, artist_direct, short_name_direct = refresh_options(data)
            elif choice == '5':
                clear_screen()
                print_color_text("Options refreshed.", "1;34")  # Blue text
                genre_internal, genre_display = get_random_genre(data)
                year, artist, song_title, genre, song_title_direct, artist_direct, short_name_direct = refresh_options(data)
            elif choice == '6':
                clear_playlist(output_file_path)
                year, artist, song_title, genre, song_title_direct, artist_direct, short_name_direct = refresh_options(data)
            elif choice == '0':
                clear_screen()
                print_color_text("Exiting Play A Show. Goodbye!", "1;31")  # Red text
                break
            else:
                clear_screen()
                print_color_text("Invalid choice.", "1;31")  # Red text
                print(" ")

# Call the new function to run both parts
if __name__ == "__main__":
    parse_and_export_to_json()
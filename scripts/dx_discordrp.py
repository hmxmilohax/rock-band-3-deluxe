#!/usr/bin/env python3
import sys
import subprocess
import json
import time
import os
import configparser
import logging
from pathlib import Path
import requests
from datetime import datetime
import pylast
import re
import argparse
import pypresence
import platform

def get_rpcs3_path():
    os_system = platform.system()
    default_data_path = None

    if os_system == 'Darwin':  # macOS
        default_data_path = Path.home() / "Library/Application Support/rpcs3"
    elif os_system == 'Windows':
        default_data_path = None
    elif os_system == 'Linux':
        default_data_paths = [
            Path.home() / ".config/rpcs3",
            Path.home() / ".rpcs3",
            Path("/usr/share/rpcs3"),
            Path("/usr/local/share/rpcs3")
        ]
        for path in default_data_paths:
            if path.exists():
                default_data_path = path
                break
    else:
        default_data_path = None

    while True:
        if default_data_path and default_data_path.exists():
            print(f"Default RPCS3 data directory detected: {default_data_path}")
            print(f"RPCS3 Directory must contain 'dev_hdd0' folder.\nWhere Rock Band 3 Deluxe is installed in /dev_hdd0/game/BLUS30463/.")
            rpcs3_path_str = input(f"Enter the path for RPCS3 data directory (leave empty to use default): ").strip()
            if not rpcs3_path_str:
                rpcs3_path = default_data_path
            else:
                rpcs3_path = Path(rpcs3_path_str)
        else:
            print(f"RPCS3 Directory must contain 'dev_hdd0' folder.\nWhere Rock Band 3 Deluxe is installed in /dev_hdd0/game/BLUS30463/.")
            rpcs3_path_str = input("Enter the path for RPCS3 base directory (e.g. C:\\games\\rpcs3): ").strip()
            rpcs3_path = Path(rpcs3_path_str)

        if rpcs3_path.exists() and rpcs3_path.is_dir():
            return rpcs3_path
        else:
            print("Invalid RPCS3 data directory path provided.")

def save_config(config_path: Path, rpcs3_path, xbox_console_ip, ps3_console_ip, never_setup_rpcs3=False, never_setup_xbox=False, never_setup_ps3=False, lastfm_config=None, never_setup_lastfm=False):
    config = configparser.ConfigParser()
    if config_path.exists():
        config.read(config_path)

    # Save Paths
    if 'Paths' not in config:
        config['Paths'] = {}
    config['Paths']['rpcs3_path'] = str(rpcs3_path) if rpcs3_path else ''
    config['Paths']['xbox_console_ip'] = xbox_console_ip
    config['Paths']['ps3_console_ip'] = ps3_console_ip

    # Save Settings for "Never" flags
    if 'Settings' not in config:
        config['Settings'] = {}
    config['Settings']['never_setup_rpcs3'] = str(never_setup_rpcs3)
    config['Settings']['never_setup_xbox'] = str(never_setup_xbox)
    config['Settings']['never_setup_ps3'] = str(never_setup_ps3)
    config['Settings']['never_setup_lastfm'] = str(never_setup_lastfm)

    # Save LastFM
    if lastfm_config:
        if 'LastFM' not in config:
            config['LastFM'] = {}
        config['LastFM']['api_key'] = lastfm_config.get('API_KEY', '')
        config['LastFM']['api_secret'] = lastfm_config.get('API_SECRET', '')
        config['LastFM']['username'] = lastfm_config.get('USERNAME', '')
        config['LastFM']['password_hash'] = lastfm_config.get('PASSWORD_HASH', '')

    with config_path.open('w') as configfile:
        config.write(configfile)

def load_config(config_path: Path):
    config = configparser.ConfigParser()
    if config_path.is_file():
        config.read(config_path)
    else:
        # Configuration file doesn't exist
        # Return default values
        return None, '', '', False, False, False, None, False  # Added never_setup_lastfm

    rpcs3_path = None
    xbox_console_ip = ''
    ps3_console_ip = ''
    lastfm_config = None
    never_setup_rpcs3 = False
    never_setup_xbox = False
    never_setup_ps3 = False
    never_setup_lastfm = False  # Initialize never_setup_lastfm

    # Read Paths
    if 'Paths' in config:
        rpcs3_path_str = config['Paths'].get('rpcs3_path', '').strip('"')
        if rpcs3_path_str:
            rpcs3_path = Path(rpcs3_path_str)
        xbox_console_ip = config['Paths'].get('xbox_console_ip', '').strip()
        ps3_console_ip = config['Paths'].get('ps3_console_ip', '').strip()

    # Read Settings for "Never" flags
    if 'Settings' in config:
        never_setup_rpcs3 = config['Settings'].getboolean('never_setup_rpcs3', fallback=False)
        never_setup_xbox = config['Settings'].getboolean('never_setup_xbox', fallback=False)
        never_setup_ps3 = config['Settings'].getboolean('never_setup_ps3', fallback=False)
        never_setup_lastfm = config['Settings'].getboolean('never_setup_lastfm', fallback=False)  # Read never_setup_lastfm

    # Read LastFM
    if 'LastFM' in config:
        api_key = config['LastFM'].get('api_key', '').strip()
        api_secret = config['LastFM'].get('api_secret', '').strip()
        username = config['LastFM'].get('username', '').strip()
        password_hash = config['LastFM'].get('password_hash', '').strip()

        if api_key and api_secret and username and password_hash:
            lastfm_config = {
                'API_KEY': api_key,
                'API_SECRET': api_secret,
                'USERNAME': username,
                'PASSWORD_HASH': password_hash
            }

    return rpcs3_path, xbox_console_ip, ps3_console_ip, never_setup_rpcs3, never_setup_xbox, never_setup_ps3, lastfm_config, never_setup_lastfm

def setup_lastfm_network(lastfm_config):
    if lastfm_config and all(key in lastfm_config for key in ['API_KEY', 'API_SECRET', 'USERNAME', 'PASSWORD_HASH']):
        return pylast.LastFMNetwork(
            api_key=lastfm_config['API_KEY'],
            api_secret=lastfm_config['API_SECRET'],
            username=lastfm_config['USERNAME'],
            password_hash=lastfm_config['PASSWORD_HASH'],
        )
    else:
        return None

def setup_lastfm_config():
    print("\nTo set up Last.fm scrobbling, you need a Last.fm account.")
    print("You also need a Last.fm API key and secret.")
    print("You can learn how to create one here - https://www.last.fm/api/authentication")
    print("Please enter your Last.fm API key and secret.")

    while True:
        api_key = input("API Key: ").strip()
        api_secret = input("API Secret: ").strip()
        print("\nIn order to properly scrobble with Last.fm")
        print("You will also need to enter your username and password")
        print("This is NOT sent ANYWHERE, and is stored hashed in config.ini locally.")
        print("I don't like it either....")
        username = input("Last.fm Username: ").strip()
        password = input("Last.fm Password: ").strip()
        password_hash = pylast.md5(password)

        # Verify the credentials
        try:
            network = pylast.LastFMNetwork(
                api_key=api_key,
                api_secret=api_secret,
                username=username,
                password_hash=password_hash,
            )
            # Test authentication by fetching user info
            user = network.get_authenticated_user()
            user.get_image()
            print("Last.fm authentication successful.")
            lastfm_config = {
                'API_KEY': api_key,
                'API_SECRET': api_secret,
                'USERNAME': username,
                'PASSWORD_HASH': password_hash
            }
            return lastfm_config
        except pylast.WSError as e:
            print(f"\nError authenticating with Last.fm: {e}")
            print("Please check your API key, API secret, username, and password.")
            print("Do you want to try again?")
            print("1. Yes")
            print("2. No (Skip Last.fm setup)")
            choice = input("Enter your choice (1-2): ").strip()
            if choice == '1':
                # Loop back to re-enter credentials
                continue
            elif choice == '2':
                # User chooses to skip Last.fm setup
                return None
            else:
                print("Invalid choice. Please try again.")
                continue

def load_or_create_scrobble_data(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            logger.error("Error loading scrobble data. Starting fresh.")
            return {}
    else:
        # Create the file if it doesn't exist
        with open(file_path, 'w') as file:
            json.dump({}, file)
        return {}

def save_scrobble_data(file_path, scrobble_data):
    with open(file_path, 'w') as file:
        json.dump(scrobble_data, file, indent=4)

def scrobble_track(network, artist, title, timestamp, scrobble_file, additional_data, active_instrument_name=None):
    scrobble_data = load_or_create_scrobble_data(scrobble_file)
    key = f"{artist} - {title}"
    instrument_text = {
        'GUITAR': 'Guitar',
        'REAL_GUITAR': 'Pro Guitar',
        'KEYS': 'Keys',
        'DRUMS': 'Drums',
        'REAL_KEYS': 'Pro Keys',
        'REAL_BASS': 'Pro Bass',
        'BASS': 'Bass',
        'VOCALS': 'Vocals'
    }
    # Increment the count for the active instrument in the JSON if it's a solo performance
    if active_instrument_name:
        instrument_key = active_instrument_name
        if 'instrument_counts' not in scrobble_data:
            scrobble_data['instrument_counts'] = {instrument: 0 for instrument in instrument_text.values()}

        if instrument_key in scrobble_data['instrument_counts']:
            scrobble_data['instrument_counts'][instrument_key] += 1
        else:
            scrobble_data['instrument_counts'][instrument_key] = 1

    if key in scrobble_data:
        entry = scrobble_data[key]
        entry['count'] += 1
        entry['last_scrobbled'] = timestamp
        entry['scrobble_times'].append(timestamp)
    else:
        scrobble_data[key] = {
            'artist': artist,
            'title': title,
            'first_scrobbled': timestamp,
            'last_scrobbled': timestamp,
            'count': 1,
            'scrobble_times': [timestamp],
            'songname': title,
            'year': additional_data.get('Year', ''),
            'album': additional_data.get('Album', ''),
            'genre': additional_data.get('Genre', ''),
            'subgenre': additional_data.get('Subgenre', ''),
            'source': additional_data.get('Source', ''),
            'author': additional_data.get('Author', '')
        }

    save_scrobble_data(scrobble_file, scrobble_data)

    if network is not None:
        try:
            album = additional_data.get('Album', '')
            if album:
                network.scrobble(artist=artist, title=title, timestamp=timestamp, album=album)
                logger.info(f"Scrobbled: {artist} - {title} (Album: {album}, {timestamp})")
            else:
                network.scrobble(artist=artist, title=title, timestamp=timestamp)
                logger.info(f"Scrobbled: {artist} - {title} ({timestamp})")
        except pylast.WSError as e:
            logger.error(f"Scrobble error: {e}")
    else:
        logger.debug("Scrobbling is disabled due to incomplete Last.fm configuration.")

def configure_logging(debug_mode):
    if debug_mode:
        logging_level = logging.DEBUG
    else:
        logging_level = logging.CRITICAL

    logging.basicConfig(level=logging_level, format='[%(levelname)s] %(message)s')
    logger = logging.getLogger(__name__)

    if not debug_mode:
        # Suppress logging from external libraries in non-debug mode
        logging.getLogger('urllib3').setLevel(logging.CRITICAL)
        logging.getLogger('requests').setLevel(logging.CRITICAL)
        logging.getLogger('asyncio').setLevel(logging.CRITICAL)
        logging.getLogger('pylast').setLevel(logging.CRITICAL)
        logging.getLogger('httpcore').setLevel(logging.CRITICAL)
        logging.getLogger('httpx').setLevel(logging.CRITICAL)
    else:
        # In debug mode, set them to INFO level
        logging.getLogger('urllib3').setLevel(logging.INFO)
        logging.getLogger('requests').setLevel(logging.INFO)
        logging.getLogger('asyncio').setLevel(logging.INFO)
        logging.getLogger('pylast').setLevel(logging.INFO)
        logging.getLogger('httpcore').setLevel(logging.INFO)
        logging.getLogger('httpx').setLevel(logging.INFO)

# Initialize logger
logger = logging.getLogger(__name__)

# Function to parse the raw input data
def parse_raw_input(raw_input, from_web=False):
    try:
        if isinstance(raw_input, dict):
            return raw_input

        # Extract JSON-like content
        start_idx = raw_input.find("{")
        end_idx = raw_input.rfind("}") + 1
        if start_idx == -1 or end_idx == 0:
            logger.error("No JSON-like content found in raw input.")
            return None
        parsed_input = raw_input[start_idx:end_idx]

        result = []
        inside_string = False
        i = 0
        length = len(parsed_input)

        while i < length:
            if parsed_input[i] == '\\' and i + 1 < length and parsed_input[i + 1] == 'q':
                if not inside_string:
                    result.append('"')
                    inside_string = True
                else:
                    next_i = i + 2
                    if next_i < length:
                        next_char = parsed_input[next_i]
                        if next_char in [',', '}', ':']:
                            result.append('"')
                            inside_string = False
                    else:
                        result.append('"')
                        inside_string = False
                i += 2  # Skip the \q
            else:
                result.append(parsed_input[i])
                i += 1

        final_json_str = ''.join(result)

        result = json.loads(final_json_str)
        return result
    except json.JSONDecodeError as e:
        logger.exception("Invalid JSON data after parsing: %s", e)
        return None
    except Exception as e:
        logger.exception("Error parsing raw input: %s", e)
        return None

# Function to load JSON data from parsed input
def load_json(parsed_input):
    try:
        if isinstance(parsed_input, str):
            data = json.loads(parsed_input)
            return data
        elif isinstance(parsed_input, dict):
            return parsed_input
        else:
            return None
    except json.JSONDecodeError as e:
        logger.exception("Invalid JSON data: %s", e)
        return None

# Function to simplify instrument names
def simplify_instrument_name(instrument_name):
    instrument_mapping = {
        'GUITAR': 'Guitar',
        'REAL_GUITAR': 'Pro Guitar',
        'KEYS': 'Keys',
        'DRUMS': 'Drums',
        'REAL_KEYS': 'Pro Keys',
        'REAL_BASS': 'Pro Bass',
        'BASS': 'Bass',
        'VOCALS': 'Vocals'
    }
    return instrument_mapping.get(instrument_name.upper(), instrument_name)

# Function to map instrument names to small_image names
def map_instrument_to_small_image(instrument_name):
    instrument_mapping = {
        'GUITAR': 'guitar',
        'REAL_GUITAR': 'real_guitar',
        'KEYS': 'keys',
        'DRUMS': 'drums',
        'REAL_KEYS': 'real_keys',
        'REAL_BASS': 'real_bass',
        'BASS': 'bass',
        'VOCALS': 'vocals'
    }
    return instrument_mapping.get(instrument_name.upper(), 'default_small_image_name')

# Function to clean up difficulty levels
def clean_difficulty(difficulty):
    difficulty_mapping = {
        '0': 'Warmup',
        '1': 'Apprentice',
        '2': 'Solid',
        '3': 'Moderate',
        '4': 'Challenging',
        '5': 'Nightmare',
        '6': 'Impossible'
    }
    return difficulty_mapping.get(difficulty, difficulty)

# Function to fetch JSON data from a web address
def fetch_json_from_web(address):
    try:
        response = requests.get(address, timeout=5)
        if response.status_code == 200:
            return response.text
        else:
            logger.error(f"Failed to fetch data from {address}, status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        if logger.getEffectiveLevel() <= logging.DEBUG:
            logger.debug(f"Exception when fetching data from {address}: {e}")
        else:
            logger.error(f"Could not connect to {address}")
        return None

# Initialize static variables
def init_update_presence():
    update_presence.initial_mode_set = False
    update_presence.previous_mode = ''
    update_presence.start_time = None  # Set to None initially
    update_presence.current_song_start_time = None
    update_presence.current_song_scrobbled = False
    update_presence.previous_screen = ''
    update_presence.current_song_name = ''
    update_presence.current_artist_name = ''
    update_presence.last_presence_data = None  # For data change detection
    update_presence.last_now_playing_update_time = None  # For tracking Now Playing updates
    update_presence.scrobble_in_seconds = None
    update_presence.reached_endgame_screen = False

# Function to normalize data for comparison
def normalize_data(data):
    # Create a copy to avoid modifying the original
    data_copy = data.copy()
    # Remove dynamic fields that change every time
    dynamic_fields = ['timestamp', 'last_updated']  # Add any dynamic fields here
    for field in dynamic_fields:
        data_copy.pop(field, None)
    return data_copy

def extract_song_artist(loaded_song):
    if loaded_song and loaded_song != 'No song loaded':
        song_artist_parts = loaded_song.split(' - ', 1)
        if len(song_artist_parts) == 2:
            song_name = song_artist_parts[0].strip()
            artist_year = song_artist_parts[1].strip()
            artist_parts = artist_year.split(',', 1)
            artist_name = artist_parts[0].strip()
            return song_name, artist_name
        else:
            return loaded_song.strip(), ''
    else:
        return '', ''

# Function to handle scrobbling logic
def handle_scrobbling(parsed_input, network, active_instrument_name, active_instrument_text):
    if network is None:
        # Last.fm is not configured; skip scrobbling logic
        return
    loaded_song = parsed_input.get('Loaded Song', '')
    scrobble_song = parsed_input.get('Songname', '')
    scrobble_artist = parsed_input.get('Artist', '')
    scrobble_album = parsed_input.get('Album', '')
    timestamp = int(time.time())

    current_screen = parsed_input.get('Current Screen', '')

    # Capture previous screen before updating it
    previous_screen = update_presence.previous_screen

    # Check if song has ended (transition from song screen to endgame screen)
    reached_endgame_screen = (previous_screen != 'coop_endgame_screen' and current_screen == 'coop_endgame_screen')
    update_presence.reached_endgame_screen = reached_endgame_screen

    # If song is loaded, update song tracking variables
    if loaded_song and loaded_song != 'No song loaded':
        # If 'Songname' or 'Artist' is missing, try to parse from 'Loaded Song'
        if not scrobble_song or not scrobble_artist:
            scrobble_song, scrobble_artist = extract_song_artist(loaded_song)

        logger.debug(f"Loaded song: {loaded_song}")
        logger.debug(f"Scrobble song: {scrobble_song}, Artist: {scrobble_artist}")

        # If song has changed
        if scrobble_song != update_presence.current_song_name or scrobble_artist != update_presence.current_artist_name:
            # Song has changed
            logger.debug("Song has changed. Updating song tracking variables.")
            update_presence.current_song_name = scrobble_song
            update_presence.current_artist_name = scrobble_artist
            update_presence.current_song_start_time = datetime.now()
            update_presence.current_song_scrobbled = False  # Reset scrobble flag for new song
            update_presence.now_playing_updated = False
            update_presence.last_now_playing_update_time = None

        # Update 'Now Playing' status if not already updated
        if not update_presence.now_playing_updated and network is not None:
            if scrobble_artist and scrobble_song:
                try:
                    album = scrobble_album if scrobble_album else None
                    network.update_now_playing(artist=scrobble_artist, title=scrobble_song, album=album)
                    logger.info(f"Updated Now Playing: {scrobble_artist} - {scrobble_song}")
                    update_presence.now_playing_updated = True
                    update_presence.last_now_playing_update_time = datetime.now()
                except pylast.WSError as e:
                    logger.error(f"Now Playing update error: {e}")
            else:
                logger.warning("Cannot update Now Playing: Artist or Songname is missing.")
    else:
        # No song loaded
        logger.debug("No song loaded.")

    # Check if we need to scrobble the song
    if update_presence.current_song_name and not update_presence.current_song_scrobbled:
        time_since_song_started = None
        if update_presence.current_song_start_time:
            time_since_song_started = datetime.now() - update_presence.current_song_start_time
            scrobble_in_seconds = max(180 - time_since_song_started.total_seconds(), 0)
            update_presence.scrobble_in_seconds = scrobble_in_seconds
        else:
            scrobble_in_seconds = None

        if reached_endgame_screen:
            logger.debug("Reached endgame screen. Will scrobble the song.")
            scrobble = True
        elif time_since_song_started and time_since_song_started.total_seconds() >= 180:
            logger.debug("Song has been playing for at least 3 minutes. Will scrobble the song.")
            scrobble = True
        else:
            scrobble = False

        if scrobble:
            # Scrobble the song
            if network is not None:
                if update_presence.current_artist_name and update_presence.current_song_name:
                    additional_data = {
                        'Songname': update_presence.current_song_name,
                        'Artist': update_presence.current_artist_name,
                        'Year': parsed_input.get('Year', ''),
                        'Album': parsed_input.get('Album', ''),
                        'Genre': parsed_input.get('Genre', ''),
                        'Subgenre': parsed_input.get('Subgenre', ''),
                        'Source': parsed_input.get('Source', ''),
                        'Author': parsed_input.get('Author', '')
                    }
                    # Pass the active instrument name if it's a solo performance
                    if active_instrument_text == "Solo":
                        active_instrument_name = simplify_instrument_name(active_instrument_name)
                    else:
                        active_instrument_name = None

                    scrobble_track(network, update_presence.current_artist_name, update_presence.current_song_name, timestamp, 'dx_playdata.json', additional_data, active_instrument_name)
                    update_presence.current_song_scrobbled = True  # Mark as scrobbled
                    update_presence.scrobble_in_seconds = None  # Reset countdown
                    logger.info(f"Scrobbled: {update_presence.current_artist_name} - {update_presence.current_song_name}")
                else:
                    logger.warning("Cannot scrobble track: Artist or Songname is missing.")
            else:
                logger.debug("Scrobbling is disabled due to incomplete Last.fm configuration.")
        else:
            # Continue waiting to scrobble
            pass
    else:
        # Already scrobbled, do not scrobble again
        pass

    # If the user navigated away from the song before scrobbling
    song_screens = [
        'practice_game_screen',
        'game_screen'
    ]

    if current_screen not in song_screens and not reached_endgame_screen and not update_presence.current_song_scrobbled:
        logger.debug(f"User navigated to {current_screen} before completing the song. Resetting song tracking variables.")
        # Reset song tracking variables
        update_presence.current_song_name = ''
        update_presence.current_artist_name = ''
        update_presence.current_song_start_time = None
        update_presence.current_song_scrobbled = False
        update_presence.now_playing_updated = False
        update_presence.last_now_playing_update_time = None
        update_presence.scrobble_in_seconds = None
        update_presence.reached_endgame_screen = False

    # Update previous screen at the end
    update_presence.previous_screen = current_screen

# Function to update Discord Rich Presence
def update_presence(client_id, parsed_input, RPC, network, large_text):
    try:
        loaded_song = parsed_input.get('Loaded Song', 'No song loaded')
        scrobble_song = parsed_input.get('Songname', '')
        scrobble_artist = parsed_input.get('Artist', '')
        timestamp = int(time.time())

        current_screen = parsed_input.get('Current Screen', '')

        # Map 'Game mode' values to better verbiage
        game_mode = parsed_input.get('Game mode', '')
        game_mode_mapping = {
            'defaults': 'In the Menus',
            'audition': 'Audition Mode',
            'qp_coop': 'Quickplay',
            'party_shuffle': 'Party Shuffle',
            'tour': 'Tour',
            'trainer': 'Instrument Training',
            'practice': 'Practice',
            'career': 'Road Challenges',
            'autoplay': 'Autoplay',
            'jukebox': 'Jukebox',
            'dx_play_a_show': 'Play a Show'
        }
        game_mode = game_mode_mapping.get(game_mode, game_mode)

        # Set start_time if it's None (only once)
        if update_presence.start_time is None:
            update_presence.start_time = int(time.time())

        # Do not reset start_time when game mode changes
        update_presence.previous_mode = game_mode

        # Get active instruments
        active_instruments = parsed_input.get('SelectedInstruments', [])
        active_instrument_count = sum(1 for instrument in active_instruments if instrument.get('active', False))

        # Initialize active_instrument_name
        active_instrument_name = None

        # Set instrument details
        active_instrument_text = ""
        active_instrument_small_image = 'default_small_image_name'
        active_instrument_small_text = ""

        if active_instrument_count > 1:
            active_instrument_text = f"{active_instrument_count} Player"
            active_instrument_small_image = 'band'
            active_instrument_small_text = f"{active_instrument_count} players"
        elif active_instrument_count == 1:
            active_instrument_text = "Solo"
            for instrument in active_instruments:
                if instrument.get('active', False):
                    instrument_name = instrument.get('instrument', '')
                    instrument_difficulty = instrument.get('difficulty', '')
                    instrument_name = simplify_instrument_name(instrument_name)
                    instrument_difficulty = clean_difficulty(instrument_difficulty)
                    active_instrument_small_text = f"{instrument_name}, {instrument_difficulty}"
                    active_instrument_small_image = map_instrument_to_small_image(instrument.get('instrument', ''))
                    active_instrument_name = instrument_name  # Assign active_instrument_name here
                    break
        else:
            # No active instruments
            active_instrument_text = ""
            active_instrument_small_image = 'default_small_image_name'
            active_instrument_small_text = None

        if parsed_input.get('Online', '') == "true":
            game_mode = "Online " + game_mode

        activity = {
            'details': f"{active_instrument_text} {game_mode}",
            'state': loaded_song,
            'large_image': 'banner',
            'large_text': large_text,
            'small_image': active_instrument_small_image,
            'small_text': active_instrument_small_text if active_instrument_small_text else None,
            'start': update_presence.start_time
        }

        # Update the presence only if data has changed
        if activity != update_presence.last_presence_data:
            RPC.update(**activity)
            update_presence.last_presence_data = activity.copy()
        else:
            pass

    except pypresence.InvalidPipe:
        logger.error("Discord client not detected. Make sure Discord is running.")

    return active_instrument_name, active_instrument_text

# Initialize static variables after function definition
init_update_presence()
update_presence.now_playing_updated = False

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_current_status(presence_data, debug_mode, network, should_clear_screen=True, screen_clear_delay_counter=0):
    if screen_clear_delay_counter == 0:
        if not debug_mode and should_clear_screen:
            clear_screen()

    loaded_song = presence_data.get('Loaded Song', 'No song loaded')
    scrobble_song = presence_data.get('Songname', '')
    scrobble_artist = presence_data.get('Artist', '')
    timestamp = int(time.time())

    current_screen = presence_data.get('Current Screen', 'Unknown Screen')

    # Map 'Game mode' values to better verbiage
    game_mode = presence_data.get('Game mode', '')
    game_mode_mapping = {
            'defaults': 'In the Menus',
            'audition': 'Audition Mode',
            'qp_coop': 'Quickplay',
            'party_shuffle': 'Party Shuffle',
            'tour': 'Tour',
            'trainer': 'Instrument Training',
            'practice': 'Practice',
            'career': 'Road Challenges',
            'autoplay': 'Autoplay',
            'jukebox': 'Jukebox',
            'dx_play_a_show': 'Play a Show'
        }
    game_mode = game_mode_mapping.get(game_mode, game_mode)

    # Get active instruments
    active_instruments = presence_data.get('SelectedInstruments', [])
    active_instrument_count = sum(1 for instrument in active_instruments if instrument.get('active', False))

    active_instrument_text = ""
    if active_instrument_count > 1:
        active_instrument_text = f"{active_instrument_count} Player"
    elif active_instrument_count == 1:
        active_instrument_text = "Solo"
    else:
        active_instrument_text = "No instruments"

    # Additional song information
    song_year = presence_data.get('Year', '')
    song_album = presence_data.get('Album', '')
    song_genre = presence_data.get('Genre', '')
    song_subgenre = presence_data.get('Subgenre', '')
    song_source = presence_data.get('Source', '')
    song_author = presence_data.get('Author', '')

    # Display current status
    print("Current Status (You must keep this window open):")

    print(f"  Game Mode: {game_mode}")

    if loaded_song == 'No song loaded':
        print(f"  Current Screen: {current_screen}")

    if scrobble_artist and scrobble_song:
        print(f"  Now Playing: {scrobble_artist} - {scrobble_song}")

        # Only print these lines if the field is not '0' and not empty
        if song_album and song_album != '0':
            print(f"    Album: {song_album}")
        if song_year and song_year != '0':
            print(f"    Year: {song_year}")
        if song_genre and song_genre != '0':
            print(f"    Genre: {song_genre}")
        if song_subgenre and song_subgenre != '0':
            print(f"    Subgenre: {song_subgenre}")
        if song_source and song_source != '0':
            print(f"    Source: {song_source}")
        if song_author and song_author != '0':
            print(f"    Author: {song_author}")

    print(f"  Players: {active_instrument_text}")

    if update_presence.current_song_start_time and loaded_song != 'No song loaded':
        # Only display scrobble countdown if Last.fm is configured
        if network is not None:
            time_since_song_started = datetime.now() - update_presence.current_song_start_time
            minutes, seconds = divmod(time_since_song_started.total_seconds(), 60)
            if debug_mode:
                print(f"  Time Since Song Started: {int(minutes)}:{int(seconds):02d}")

            # Display scrobble countdown
            if not update_presence.current_song_scrobbled:
                if update_presence.reached_endgame_screen:
                    print("  Scrobble in: Endgame screen reached, scrobbling soon.")
                elif update_presence.scrobble_in_seconds is not None:
                    scrobble_in_seconds = int(update_presence.scrobble_in_seconds)
                    minutes_left, seconds_left = divmod(scrobble_in_seconds, 60)
                    print(f"  Scrobble In: {int(minutes_left)}m {int(seconds_left)}s")
        else:
            # Do not display scrobble countdown if Last.fm is not configured
            pass

    # Display the current screen for debugging
    if debug_mode:
        print(f"  Current Screen: {current_screen}")
        print(f"  Previous Screen: {update_presence.previous_screen}")

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Discord Rich Presence and Last.fm Scrobbler for Rock Band 3 Deluxe")
    parser.add_argument('--debug', action='store_true', help='Enable debug mode with detailed logging')
    args = parser.parse_args()

    debug_mode = args.debug  # Store debug mode flag

    # Configure logging based on debug mode
    configure_logging(debug_mode)

    # Configurable parameters
    client_id = "1125571051607298190"
    idle_timeout = 900  # 15 minutes

    config_path = Path.cwd() / 'dx_config.ini'
    rpcs3_path, xbox_console_ip, ps3_console_ip, never_setup_rpcs3, never_setup_xbox, never_setup_ps3, lastfm_config, never_setup_lastfm = load_config(config_path)

    # Initial setup prompts based on existing configurations and "never" flags
    if (not rpcs3_path and not xbox_console_ip and not ps3_console_ip) and not (never_setup_rpcs3 and never_setup_xbox and never_setup_ps3):
        print("No RPCS3 data path or consoles configured.")
        print("You will now be asked in order if you wish to configure RPCS3, Xbox, and/or PlayStation 3 console sources.")

    # Check if any are missing and prompt accordingly, considering "never" flags
    if not rpcs3_path and not never_setup_rpcs3:
        print("\nRPCS3 data path not configured.")
        print("Do you want to set it up now?")
        print("1. Yes")
        print("2. Not Now")
        print("3. Never")
        choice = input("Enter your choice (1-3): ").strip()
        if choice == '1':
            rpcs3_path = get_rpcs3_path()
            save_config(config_path, rpcs3_path or '', xbox_console_ip or '', ps3_console_ip or '', never_setup_rpcs3, never_setup_xbox, never_setup_ps3, lastfm_config, never_setup_lastfm)
        elif choice == '2':
            pass
        elif choice == '3':
            never_setup_rpcs3 = True
            save_config(config_path, rpcs3_path or '', xbox_console_ip or '', ps3_console_ip or '', never_setup_rpcs3, never_setup_xbox, never_setup_ps3, lastfm_config, never_setup_lastfm)
            print("RPCS3 setup will not be prompted again.")
        else:
            print("Invalid choice. Please try again.")

    if not xbox_console_ip and not never_setup_xbox:
        print("\nXbox console IP not configured.")
        print("Do you want to set it up now?")
        print("1. Yes")
        print("2. Not Now")
        print("3. Never")
        choice = input("Enter your choice (1-3): ").strip()
        if choice == '1':
            xbox_console_ip = input("Enter the IP address of the Xbox console: ").strip()
            save_config(config_path, rpcs3_path or '', xbox_console_ip or '', ps3_console_ip or '', never_setup_rpcs3, never_setup_xbox, never_setup_ps3, lastfm_config, never_setup_lastfm)
        elif choice == '2':
            pass
        elif choice == '3':
            never_setup_xbox = True
            save_config(config_path, rpcs3_path or '', xbox_console_ip or '', ps3_console_ip or '', never_setup_rpcs3, never_setup_xbox, never_setup_ps3, lastfm_config, never_setup_lastfm)
            print("Xbox setup will not be prompted again.")
        else:
            print("Invalid choice. Please try again.")

    if not ps3_console_ip and not never_setup_ps3:
        print("\nPlayStation 3 console IP not configured.")
        print("Do you want to set it up now?")
        print("1. Yes")
        print("2. Not Now")
        print("3. Never")
        choice = input("Enter your choice (1-3): ").strip()
        if choice == '1':
            ps3_console_ip = input("Enter the IP address of the PlayStation 3 console: ").strip()
            save_config(config_path, rpcs3_path or '', xbox_console_ip or '', ps3_console_ip or '', never_setup_rpcs3, never_setup_xbox, never_setup_ps3, lastfm_config, never_setup_lastfm)
        elif choice == '2':
            pass
        elif choice == '3':
            never_setup_ps3 = True
            save_config(config_path, rpcs3_path or '', xbox_console_ip or '', ps3_console_ip or '', never_setup_rpcs3, never_setup_xbox, never_setup_ps3, lastfm_config, never_setup_lastfm)
            print("PlayStation 3 setup will not be prompted again.")
        else:
            print("Invalid choice. Please try again.")

    # Save the updated configuration
    save_config(config_path, rpcs3_path or '', xbox_console_ip or '', ps3_console_ip or '', never_setup_rpcs3, never_setup_xbox, never_setup_ps3, lastfm_config, never_setup_lastfm)

    # Check Last.fm configuration
    if not lastfm_config and not never_setup_lastfm:
        while True:
            print("\nLast.fm configuration not found.")
            print("Do you want to set up Last.fm scrobbling?")
            print("1. Yes")
            print("2. Not Now")
            print("3. Never")
            choice = input("Enter your choice (1-3): ").strip()
            if choice == '1':
                # Proceed to set up Last.fm configuration
                lastfm_config = setup_lastfm_config()
                if lastfm_config:
                    # Save the configuration
                    save_config(config_path, rpcs3_path or '', xbox_console_ip or '', ps3_console_ip or '',
                                never_setup_rpcs3, never_setup_xbox, never_setup_ps3, lastfm_config, never_setup_lastfm)
                    break  # Exit the loop since setup is complete
                else:
                    # User chose to skip Last.fm setup after failed authentication
                    print("Proceeding without Last.fm scrobbling.")
                    break
            elif choice == '2':
                # Do not set up now, do not set 'never_setup_lastfm'
                print("Proceeding without Last.fm scrobbling.")
                break
            elif choice == '3':
                # Do not ask again
                never_setup_lastfm = True
                save_config(config_path, rpcs3_path or '', xbox_console_ip or '', ps3_console_ip or '',
                            never_setup_rpcs3, never_setup_xbox, never_setup_ps3, lastfm_config, never_setup_lastfm)
                print("Last.fm setup will not be prompted again.")
                break
            else:
                print("Invalid choice. Please try again.")

    # Initialize other configurations
    network = setup_lastfm_network(lastfm_config)

    large_text = "Rock Band 3 Deluxe"  # Default value for large_text

    # Connect to Discord RPC
    try:
        RPC = pypresence.Presence(client_id)
        RPC.connect()
    except pypresence.exceptions.DiscordNotFound:
        logger.error("Discord client not detected. Make sure Discord is running.")
        return

    try:
        presence_cleared = False
        previous_data = None
        last_data_change_time = time.time()
        last_data_receive_time = time.time()
        last_json_content = None
        console_connection_error_displayed = False
        screen_clear_delay_counter = 0  # Initialize the screen clear delay counter

        while True:
            current_time = time.time()
            data_changed = False
            json_data = None
            from_web = False
            data_source = None  # Initialize data_source variable

            # Determine whether to clear the screen
            should_clear_screen = screen_clear_delay_counter == 0

            # Attempt to fetch data from consoles if configured
            if xbox_console_ip and not never_setup_xbox:
                web_address = f"http://{xbox_console_ip}:21070/jsonrpc"
                json_data = fetch_json_from_web(web_address)
                if json_data:
                    data_source = 'xbox'
                    from_web = True
                    console_connection_error_displayed = False  # Reset the error flag
                    screen_clear_delay_counter = 0  # Reset the counter when connection is successful
                else:
                    if not console_connection_error_displayed:
                        print(f"Error: Could not connect to Xbox at {xbox_console_ip}.")
                        print("Please ensure the IP is correct and the console is powered on.")
                        print("Rich Presence on Xbox requires Nightly RB3Enhanced installed and configured")
                        print("Consult the MiloHax Discord or online setup guide https://rb3pc.milohax.org/adv_discordrp")
                        print("Attempting to reconnect...")
                        console_connection_error_displayed = True

                        # Set the screen clear delay counter to delay clearing the screen
                        screen_clear_delay_counter = 1  # Number of cycles to delay
                    else:
                        # We can choose whether to reset the counter on subsequent failures
                        # For now, we'll only set the counter on the first failure
                        pass

                    # Xbox data not available, fall back to RPCS3 if configured
                    if rpcs3_path and not never_setup_rpcs3:
                        json_path = rpcs3_path / "dev_hdd0" / "game" / "BLUS30463" / "USRDIR" / "discordrp.json"
                        json_file = Path(json_path)
                        if json_file.is_file():
                            with json_file.open('r', encoding='utf-8') as file:
                                json_data = file.read()
                            if json_data:
                                data_source = 'local'
                                from_web = False
            if ps3_console_ip and not never_setup_ps3:
                web_address = f"http://{ps3_console_ip}/dev_hdd0/game/BLUS30463/USRDIR/discordrp.json"
                json_data = fetch_json_from_web(web_address)
                if json_data:
                    data_source = 'ps3'
                    from_web = True
                    console_connection_error_displayed = False  # Reset the error flag
                    screen_clear_delay_counter = 0  # Reset the counter when connection is successful
                else:
                    if not console_connection_error_displayed:
                        print(f"Error: Could not connect to PlayStation 3 at {ps3_console_ip}.")
                        print("Please ensure the IP is correct and the console is powered on.")
                        print("Rich Presence on PlayStation 3 requires webMAN installed and enabled")
                        print("Consult the MiloHax Discord or online setup guide https://rb3pc.milohax.org/adv_discordrp")
                        print("Attempting to reconnect...")
                        console_connection_error_displayed = True

                        # Set the screen clear delay counter to delay clearing the screen
                        screen_clear_delay_counter = 1  # Number of cycles to delay
                    else:
                        # We can choose whether to reset the counter on subsequent failures
                        # For now, we'll only set the counter on the first failure
                        pass

                    # PS3 data not available, fall back to RPCS3 if configured
                    if rpcs3_path and not never_setup_rpcs3:
                        json_path = rpcs3_path / "dev_hdd0" / "game" / "BLUS30463" / "USRDIR" / "discordrp.json"
                        json_file = Path(json_path)
                        if json_file.is_file():
                            with json_file.open('r', encoding='utf-8') as file:
                                json_data = file.read()
                            if json_data:
                                data_source = 'local'
                                from_web = False
            else:
                # Xbox not configured or opted out, try RPCS3
                if rpcs3_path and not never_setup_rpcs3:
                    json_path = rpcs3_path / "dev_hdd0" / "game" / "BLUS30463" / "USRDIR" / "discordrp.json"
                    json_file = Path(json_path)
                    if json_file.is_file():
                        with json_file.open('r', encoding='utf-8') as file:
                            json_data = file.read()
                        if json_data:
                            data_source = 'local'
                            from_web = False

            # Set interval based on data source
            if data_source == 'xbox' or data_source == 'ps3':
                interval = 5  # Check every 5 seconds when using remote consoles
            else:
                interval = 2  # Check every 2 seconds when fetching from the local machine

            # If no data from any source, wait and retry
            if not json_data:
                # Check for idle timeout
                if current_time - last_data_receive_time > idle_timeout and previous_data:
                    if not presence_cleared:
                        RPC.clear()
                        presence_cleared = True
                        previous_data = None
                time.sleep(interval)
                continue

            # Process the fetched data
            parsed_input_data = parse_raw_input(json_data, from_web)
            if not parsed_input_data:
                logger.error("Failed to parse raw input data.")
                time.sleep(interval)
                continue

            presence_data = load_json(parsed_input_data)
            if presence_data is not None:
                # Normalize data for comparison
                normalized_data = normalize_data(presence_data)
                # Compare normalized data
                if normalized_data != previous_data:
                    previous_data = normalized_data
                    data_changed = True
                    last_data_change_time = time.time()  # Reset idle timer
                else:
                    data_changed = False

                last_data_receive_time = time.time()

                if data_changed or presence_cleared:
                    if presence_cleared:
                        update_presence.start_time = None  # Reset start_time to reset the timer
                        presence_cleared = False
                    # Update Discord Rich Presence
                    active_instrument_name, active_instrument_text = update_presence(client_id, presence_data, RPC, network, large_text)

                # Call scrobbling logic only if Last.fm is configured
                if network is not None:
                    handle_scrobbling(presence_data, network, active_instrument_name, active_instrument_text)

                # Display current status in every iteration
                display_current_status(presence_data, debug_mode, network, should_clear_screen, screen_clear_delay_counter)

            else:
                logger.error("Failed to load presence data from parsed input.")
                time.sleep(interval)
                continue

            # Decrement the screen clear delay counter if it's greater than zero
            if screen_clear_delay_counter > 0:
                screen_clear_delay_counter -= 1

            # Wait before checking again
            time.sleep(interval)

    except KeyboardInterrupt:
        print("Disconnecting from Discord...", end="", flush=True)
        RPC.clear()
        RPC.close()
        print("\nDisconnected. Goodbye!", flush=True)

if __name__ == '__main__':
    main()

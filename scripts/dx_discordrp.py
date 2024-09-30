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

# Check if the system is running on macOS
is_macos = sys.platform == "darwin"

def get_rpcs3_path():
    while True:
        rpcs3_path_str = input("\033[1;33mEnter the path for RPCS3: \033[0m")
        if rpcs3_path_str.strip():  # Check if the input is not empty after stripping whitespace
            rpcs3_path = Path(rpcs3_path_str)
            
            if not rpcs3_path.is_dir():
                print(f"Invalid RPCS3 path provided.")
                continue  # Prompt again for valid input
            
            return rpcs3_path
        else:
            print(f"Invalid RPCS3 path provided.")

def save_config(config_path: Path, rpcs3_path, xbox_console_ip, never_setup_rpcs3=False, never_setup_xbox=False, lastfm_config=None):
    config = configparser.ConfigParser()
    if config_path.exists():
        config.read(config_path)
    
    # Save Paths
    if 'Paths' not in config:
        config['Paths'] = {}
    config['Paths']['rpcs3_path'] = str(rpcs3_path) if rpcs3_path else ''
    config['Paths']['xbox_console_ip'] = xbox_console_ip
    
    # Save Settings for "Never" flags
    if 'Settings' not in config:
        config['Settings'] = {}
    config['Settings']['never_setup_rpcs3'] = str(never_setup_rpcs3)
    config['Settings']['never_setup_xbox'] = str(never_setup_xbox)
    
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
        # Return default values: No paths, no "never" flags, and no LastFM config
        return None, '', False, False, None  # rpcs3_path, xbox_console_ip, never_setup_rpcs3, never_setup_xbox, lastfm_config

    rpcs3_path = None
    xbox_console_ip = ''
    lastfm_config = None
    never_setup_rpcs3 = False
    never_setup_xbox = False

    # Read Paths
    if 'Paths' in config:
        rpcs3_path_str = config['Paths'].get('rpcs3_path', '').strip('"')
        if rpcs3_path_str:
            rpcs3_path = Path(rpcs3_path_str)
        xbox_console_ip = config['Paths'].get('xbox_console_ip', '').strip()

    # Read Settings for "Never" flags
    if 'Settings' in config:
        never_setup_rpcs3 = config['Settings'].getboolean('never_setup_rpcs3', fallback=False)
        never_setup_xbox = config['Settings'].getboolean('never_setup_xbox', fallback=False)

    # Read LastFM
    if 'LastFM' in config:
        api_key = config['LastFM'].get('api_key', '').strip()
        api_secret = config['LastFM'].get('api_secret', '').strip()
        username = config['LastFM'].get('username', '').strip()
        password = config['LastFM'].get('password', '').strip()

        if api_key and api_secret and username and password:
            lastfm_config = {
                'API_KEY': api_key,
                'API_SECRET': api_secret,
                'USERNAME': username,
                'PASSWORD_HASH': pylast.md5(password)
            }

    return rpcs3_path, xbox_console_ip, never_setup_rpcs3, never_setup_xbox, lastfm_config

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

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('asyncio').setLevel(logging.WARNING)
logging.getLogger('pylast').setLevel(logging.WARNING)
logging.getLogger('httpcore').setLevel(logging.WARNING)
logging.getLogger('httpx').setLevel(logging.WARNING)

# Now you can import the required packages
import pypresence

# Function to parse the raw input data
def parse_raw_input(raw_input, from_web=False):
    try:
        if isinstance(raw_input, dict):
            # If the input is already a dictionary (from web), return it as is
            return raw_input  # Return as is, since it's already a dict

        #logger.debug(f"Raw input: {raw_input}")

        # Extract JSON-like content
        start_idx = raw_input.find("{")
        end_idx = raw_input.rfind("}") + 1
        if start_idx == -1 or end_idx == 0:
            logger.error("No JSON-like content found in raw input.")
            return None
        parsed_input = raw_input[start_idx:end_idx]

        #logger.debug(f"Extracted JSON-like string: {parsed_input}")

        result = []
        inside_string = False
        i = 0
        length = len(parsed_input)

        while i < length:
            if parsed_input[i] == '\\' and i + 1 < length and parsed_input[i + 1] == 'q':
                if not inside_string:
                    # Start of a new string
                    result.append('"')
                    inside_string = True
                else:
                    # Inside a string, determine if \q is closing quote or embedded quote
                    next_i = i + 2
                    if next_i < length:
                        next_char = parsed_input[next_i]
                        if next_char in [',', '}', ':']:
                            # Closing quote
                            result.append('"')
                            inside_string = False
                    else:
                        # At the end of the string
                        result.append('"')
                        inside_string = False
                i += 2  # Skip the \q
            else:
                # Regular character
                result.append(parsed_input[i])
                i += 1

        # No extra " appended after the loop

        final_json_str = ''.join(result)

        #logger.debug(f"After custom parsing: {final_json_str}")

        # Parse JSON
        data = json.loads(final_json_str)
        return data
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
            #logger.debug(f"Attempting to parse JSON: {parsed_input}")
            data = json.loads(parsed_input)  # Parse the JSON data
            return data
        elif isinstance(parsed_input, dict):
            #logger.debug("Parsed input is already a dictionary. Returning as is.")
            return parsed_input
        else:
            #logger.error("Parsed input is neither a string nor a dictionary.")
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
        response = requests.get(address, timeout=5)  # Added timeout
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch data from {address}, status code: {response.status_code}", flush=True)
            return None
    except requests.RequestException as e:
        #print(f"Error fetching data from {address}: {str(e)}", flush=True)
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
    loaded_song = parsed_input.get('Loaded Song', 'No song loaded')
    scrobble_song = parsed_input.get('Songname', '')
    scrobble_artist = parsed_input.get('Artist', '')
    scrobble_album = parsed_input.get('Album', '')  # Get album from parsed input
    timestamp = int(time.time())

    current_screen = parsed_input.get('Current Screen', '')

    if loaded_song == 'No song loaded':
        # Reset current song tracking variables
        update_presence.current_song_name = ''
        update_presence.current_artist_name = ''
        update_presence.current_song_start_time = None
        update_presence.current_song_scrobbled = False
        update_presence.now_playing_updated = False
        update_presence.last_now_playing_update_time = None
    else:
        # If 'Songname' or 'Artist' is missing, try to parse from 'Loaded Song'
        if not scrobble_song or not scrobble_artist:
            scrobble_song, scrobble_artist = extract_song_artist(loaded_song)

        # If song has changed
        if scrobble_song != update_presence.current_song_name or scrobble_artist != update_presence.current_artist_name:
            # Song has changed
            update_presence.current_song_name = scrobble_song
            update_presence.current_artist_name = scrobble_artist
            update_presence.current_song_start_time = datetime.now()
            update_presence.current_song_scrobbled = False
            update_presence.now_playing_updated = False
            update_presence.last_now_playing_update_time = None

        # Check if we should reset now_playing_updated due to time elapsed
        if update_presence.last_now_playing_update_time:
            time_since_last_update = datetime.now() - update_presence.last_now_playing_update_time
            if time_since_last_update.total_seconds() >= 900:  # 15 minutes
                update_presence.now_playing_updated = False

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
        #elif network is None:
        #    logger.debug("Now Playing update skipped due to incomplete Last.fm configuration.")

        # Check if we need to scrobble the song
        if update_presence.current_song_name and not update_presence.current_song_scrobbled:
            time_since_song_started = datetime.now() - update_presence.current_song_start_time
            if time_since_song_started.total_seconds() >= 180 or (update_presence.previous_screen != 'coop_endgame_screen' and current_screen == 'coop_endgame_screen'):
                # Either 3 minutes have passed, or we reached endgame screen
                if network is not None:
                    if scrobble_artist and scrobble_song:
                        additional_data = {
                            'Songname': scrobble_song,
                            'Artist': scrobble_artist,
                            'Year': parsed_input.get('Year', ''),
                            'Album': scrobble_album,  # Use scrobble_album here
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

                        scrobble_track(network, scrobble_artist, scrobble_song, timestamp, 'dx_playdata.json', additional_data, active_instrument_name)
                        update_presence.current_song_scrobbled = True
                    else:
                        logger.warning("Cannot scrobble track: Artist or Songname is missing.")
                else:
                    logger.debug("Scrobbling is disabled due to incomplete Last.fm configuration.")

    # Update previous screen
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
                    active_instrument_small_image = map_instrument_to_small_image(instrument_name)
                    active_instrument_name = instrument_name  # Assign active_instrument_name here
                    break
        else:
            # No active instruments
            active_instrument_text = ""
            active_instrument_small_image = 'default_small_image_name'
            active_instrument_small_text = None

        # Update previous screen
        update_presence.previous_screen = current_screen

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
            logger.debug(f"Updating Presence: {loaded_song}, {active_instrument_text} {game_mode}")
        else:
            # Data hasn't changed
            pass

    except pypresence.InvalidPipe:
        logger.error("Discord client not detected. Make sure Discord is running.")

    return active_instrument_name, active_instrument_text

# Initialize static variables after function definition
init_update_presence()
update_presence.now_playing_updated = False

def main():
    # Check if Discord is installed and running
    try:
        import pypresence
    except ImportError:
        logger.error("pypresence module not found. Discord is either not installed or not accessible.")
        return

    # Configurable parameters
    client_id = "1125571051607298190"
    interval = 10  # Check for updates every 10 seconds
    idle_timeout = 900  # 15 minutes

    config_path = Path.cwd() / 'dx_config.ini'
    rpcs3_path, xbox_console_ip, never_setup_rpcs3, never_setup_xbox, lastfm_config = load_config(config_path)

    # Function to prompt setup with "Never" option
    def prompt_setup():
        nonlocal rpcs3_path, xbox_console_ip, never_setup_rpcs3, never_setup_xbox

        while True:
            print("\nNo RPCS3 path or Xbox console IP configured.")
            print("Please select your setup:")
            print("1. Set up RPCS3")
            print("2. Set up Xbox")
            print("3. Set up both")
            choice = input("Enter the number corresponding to your setup (1-6): ").strip()

            if choice == '1':
                rpcs3 = get_rpcs3_path()
                if rpcs3:
                    rpcs3_path = rpcs3
                save_config(config_path, rpcs3_path or '', xbox_console_ip or '', never_setup_rpcs3, never_setup_xbox, lastfm_config)
                return
            elif choice == '2':
                xbox_console_ip_input = input("Enter the IP address of the Xbox console: ").strip()
                if xbox_console_ip_input:
                    xbox_console_ip = xbox_console_ip_input
                save_config(config_path, rpcs3_path or '', xbox_console_ip or '', never_setup_rpcs3, never_setup_xbox, lastfm_config)
                return
            elif choice == '3':
                rpcs3 = get_rpcs3_path()
                if rpcs3:
                    rpcs3_path = rpcs3
                xbox_console_ip_input = input("Enter the IP address of the Xbox console: ").strip()
                if xbox_console_ip_input:
                    xbox_console_ip = xbox_console_ip_input
                save_config(config_path, rpcs3_path or '', xbox_console_ip or '', never_setup_rpcs3, never_setup_xbox, lastfm_config)
                return
            else:
                print("Invalid choice. Please try again.")


    # Initial setup prompts based on existing configurations and "never" flags
    while (not rpcs3_path and not xbox_console_ip) and not (never_setup_rpcs3 and never_setup_xbox):
        prompt_setup()

    # Check if only one is missing and prompt accordingly, considering "never" flags
    if not rpcs3_path and not never_setup_rpcs3:
        print("\nRPCS3 path not configured.")
        print("Do you want to set it up now?")
        print("1. Yes")
        print("2. Never")
        choice = input("Enter your choice (1-2): ").strip()
        if choice == '1':
            rpcs3 = get_rpcs3_path()
            if rpcs3:
                rpcs3_path = rpcs3
                save_config(config_path, rpcs3_path or '', xbox_console_ip or '', never_setup_rpcs3, never_setup_xbox, lastfm_config)
        elif choice == '2':
            never_setup_rpcs3 = True
            save_config(config_path, rpcs3_path or '', xbox_console_ip or '', never_setup_rpcs3, never_setup_xbox, lastfm_config)
            print("RPCS3 setup will not be prompted again.")

    if not xbox_console_ip and not never_setup_xbox:
        print("\nXbox console IP not configured.")
        print("Do you want to set it up now?")
        print("1. Yes")
        print("2. Never")
        choice = input("Enter your choice (1-2): ").strip()
        if choice == '1':
            xbox_console_ip = input("Enter the IP address of the Xbox console: ").strip()
            save_config(config_path, rpcs3_path or '', xbox_console_ip or '', never_setup_rpcs3, never_setup_xbox, lastfm_config)
        elif choice == '2':
            never_setup_xbox = True
            save_config(config_path, rpcs3_path or '', xbox_console_ip or '', never_setup_rpcs3, never_setup_xbox, lastfm_config)
            print("Xbox setup will not be prompted again.")

    # Save the updated configuration
    save_config(config_path, rpcs3_path or '', xbox_console_ip or '', never_setup_rpcs3, never_setup_xbox, lastfm_config)

    # Initialize other configurations
    network = setup_lastfm_network(lastfm_config)

    # Define the JSON path based on RPCS3 path
    if rpcs3_path:
        json_path = Path(rpcs3_path) / "dev_hdd0" / "game" / "BLUS30463" / "USRDIR" / "discordrp.json"
    else:
        json_path = None  # RPCS3 not configured

    large_text = "Rock Band 3 Deluxe"  # Default value for large_text

    # Connect to Discord RPC
    try:
        RPC = pypresence.Presence(client_id)
        RPC.connect()
        logger.debug("Connected to Discord RPC successfully.")
    except pypresence.exceptions.DiscordNotFound:
        logger.error("Discord client not detected. Make sure Discord is running.")
        return

    try:
        presence_cleared = False  # Initialize presence_cleared flag
        previous_data = None  # Initialize previous_data
        last_data_change_time = time.time()  # Initialize last_data_change_time
        last_data_receive_time = time.time()  # Initialize last_data_receive_time

        while True:
            # Determine available sources based on configuration and "never" flags
            data_source = None  # 'xbox' or 'local'
            json_data = None
            from_web = False

            logger.debug("Attempting to fetch data from available sources.")

            # Try fetching from Xbox if configured and not opted out
            if xbox_console_ip and not never_setup_xbox:
                web_address = f"http://{xbox_console_ip}:21070/jsonrpc"
                json_data = fetch_json_from_web(web_address)
                if json_data:
                    last_data_receive_time = time.time()
                    data_source = 'xbox'
                    from_web = True
                    #logger.debug("Data fetched from Xbox.")
                #else:
                    #logger.debug("Failed to fetch data from Xbox.")

            # Try fetching from RPCS3 if configured and not opted out
            if not json_data and rpcs3_path and not never_setup_rpcs3:
                json_path = Path(rpcs3_path) / "dev_hdd0" / "game" / "BLUS30463" / "USRDIR" / "discordrp.json"
                json_file = Path(json_path)
                if json_file.is_file():
                    with json_file.open('r', encoding='utf-8') as file:
                        json_data = file.read()
                    if json_data:
                        data_source = 'local'
                        from_web = False
                        #logger.debug("Data fetched from local file.")
                        # Delete the JSON file after reading it
                        try:
                            json_file.unlink()
                            #logger.debug(f"Deleted local JSON file: {json_file}")
                        except Exception as e:
                            logger.error(f"Failed to delete local JSON file: {e}")
                        last_data_receive_time = time.time()  # Update last_data_receive_time
                    else:
                        logger.debug("No data in local file.")
                #else:
                #    logger.debug("Local JSON file not found.")

            # If no data from any source, wait and retry
            if not json_data:
                logger.debug("No data available from any source. Waiting before retrying.")
                # Check for idle timeout
                current_time = time.time()
                if current_time - last_data_receive_time > idle_timeout and previous_data:
                    logger.debug("Idle timeout reached. Clearing presence and resetting Last.fm Now Playing status.")
                    if not presence_cleared:
                        RPC.clear()
                        presence_cleared = True
                        previous_data = None
                        # Reset any other tracking variables if necessary
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
                else:
                    pass  # No change in data and not idle

                # Call scrobbling logic regardless of data change
                handle_scrobbling(presence_data, network, active_instrument_name, active_instrument_text)

            else:
                logger.error("Failed to load presence data from parsed input.")
                time.sleep(interval)
                continue

            # Now start monitoring the data source
            while True:
                current_time = time.time()
                data_changed = False
                json_data = None  # Reset json_data

                # Fetch data from current data source
                if data_source == 'xbox':
                    json_data = fetch_json_from_web(web_address)
                    if not json_data:
                        logger.debug("Lost connection to Xbox.")
                        break  # Go back to initial data source check
                    else:
                        from_web = True
                        #logger.debug("Data fetched from Xbox.")
                elif data_source == 'local':
                    if json_file.is_file():
                        with json_file.open('r', encoding='utf-8') as file:
                            json_data = file.read()
                        from_web = False
                        #logger.debug("Data fetched from local file.")
                        # Delete the JSON file after reading it
                        try:
                            json_file.unlink()
                            #logger.debug(f"Deleted local JSON file: {json_file}")
                        except Exception as e:
                            logger.error(f"Failed to delete local JSON file: {e}")
                    else:
                        # No new data; do not reset last_data_receive_time
                        #logger.debug("Local file not found.")
                        pass  # Do not break; continue looping

                if json_data:
                    parsed_input_data = parse_raw_input(json_data, from_web)
                    if parsed_input_data:
                        presence_data = load_json(parsed_input_data)
                        if presence_data is not None:
                            # Normalize data for comparison
                            normalized_data = normalize_data(presence_data)
                            # Compare data
                            if normalized_data != previous_data:
                                previous_data = normalized_data
                                data_changed = True
                                last_data_change_time = current_time  # Reset idle timer
                            else:
                                data_changed = False

                            last_data_receive_time = current_time  # Update last data receive time

                            if data_changed:
                                # If we were previously idle, reset start_time
                                if presence_cleared:
                                    update_presence.start_time = None  # Reset start_time to reset the timer
                                    presence_cleared = False
                                update_presence(client_id, presence_data, RPC, network, large_text)
                            else:
                                pass  # No change in data

                            handle_scrobbling(presence_data, network, active_instrument_name, active_instrument_text)

                        else:
                            logger.error("Failed to load presence data from parsed input.")
                    else:
                        logger.error("Failed to parse raw input data.")

                # Check for idle timeout
                if current_time - last_data_receive_time > idle_timeout and previous_data:
                    logger.debug("Idle timeout reached. Clearing presence.")
                    if not presence_cleared:
                        RPC.clear()
                        presence_cleared = True
                        previous_data = None
                        # Reset any other tracking variables if necessary
                    break  # Go back to initial data source check

                # Wait before checking again
                time.sleep(interval)

    except KeyboardInterrupt:
        print("Disconnecting from Discord...", flush=True)
        RPC.clear()
        RPC.close()
        print("Disconnected. Goodbye!", flush=True)

if __name__ == '__main__':
    main()

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

# Check if the system is running on macOS
is_macos = sys.platform == "darwin"

def get_rpcs3_path():
    while True:
        rpcs3_path_str = input("\033[1;33mEnter the path for RPCS3: \033[0m")
        if rpcs3_path_str.strip():  # Check if the input is not empty after stripping whitespace
            rpcs3_path = Path(rpcs3_path_str)
            
            if not rpcs3_path.is_dir():
                print_color_text(f"Invalid RPCS3 path provided.", "1;31")  # Red text
                continue  # Prompt again for valid input
            
            return rpcs3_path
        else:
            print_color_text(f"Invalid RPCS3 path provided.", "1;31")  # Red text

def save_rpcs3_path(config_path: Path, rpcs3_path: Path, xbox_console_ip: str):
    config = configparser.ConfigParser()
    config['Paths'] = {
        'rpcs3_path': f'"{str(rpcs3_path)}"',
        'xbox_console_ip': xbox_console_ip
    }
    with open(config_path, 'w') as configfile:
        config.write(configfile)

def load_config(config_path: Path):
    config = configparser.ConfigParser()
    config.read(config_path)
    if 'Paths' in config and 'rpcs3_path' in config['Paths']:
        rpcs3_path = Path(config['Paths']['rpcs3_path'].strip('"'))
        xbox_console_ip = config['Paths'].get('xbox_console_ip', '')
        return rpcs3_path, xbox_console_ip
    else:
        return None, ''

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('asyncio').setLevel(logging.WARNING)

# List of required packages
required_packages = ["pypresence", "json", "time", "os", "logging", "pathlib", "requests"]

# Check if each package is installed, and if not, install it
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"{package} not found. Installing...")
        
        # Use "pip3" on macOS and Linux, and "pip" on Windows
        pip_command = "pip3" if is_macos or sys.platform.startswith("linux") else "pip"
        
        subprocess.check_call([pip_command, "install", package])

# Now you can import the required packages
import pypresence

# Function to parse the raw input data
def parse_raw_input(raw_input, from_web=False):
    try:
        if isinstance(raw_input, dict):
            # If the input is already a dictionary (from web), return it as JSON string
            return json.dumps(raw_input)
        start_idx = raw_input.index("{")
        end_idx = raw_input.rindex("}") + 1
        parsed_input = raw_input[start_idx:end_idx]
        parsed_input = parsed_input.replace("\\q", "\"")
        parsed_input = parsed_input.replace("'", "\'")
        if from_web:
            parsed_input = parsed_input[:-1] if parsed_input.endswith('"') else parsed_input
        return parsed_input
    except ValueError:
        logger.exception("Error parsing raw input")
        return ""

# Function to load JSON data from parsed input
def load_json(parsed_input):
    try:
        data = json.loads(parsed_input)  # Parse the JSON data
        return data
    except json.JSONDecodeError as e:
        logger.exception("Invalid JSON data.")
        return None

# Function to prompt for JSON file path
def prompt_json_path(suffix):
    json_path = rpcs3_path / "dev_hdd0" / "game" / "BLUS30463" / "USRDIR" / "discordrp.json"
    return json_path.strip()

# Connect to Discord RPC and update rich presence
def connect_and_update(client_id, interval, RPC, json_data, large_text="", from_web=False):
    try:
        # Parse the raw input data
        parsed_input_data = parse_raw_input(json_data, from_web)
        #logger.debug(f"Parsed Input Data: {parsed_input_data}")

        # Load the JSON data from parsed input
        presence_data = load_json(parsed_input_data)

        # Check if the JSON data was loaded successfully
        if presence_data is not None:
            # Update Discord Rich Presence
            update_presence(client_id, presence_data, RPC, large_text)
        else:
            logger.error("Failed to load presence data. Check the JSON input.")

    except Exception as e:
        logger.exception(f"An error occurred: {str(e)}")

# Function to update Discord Rich Presence
def update_presence(client_id, parsed_input, RPC, large_text):
    try:
        # Perform the necessary actions based on the updated data
        # ...

        # Set default values if 'Loaded Song' is empty or missing
        loaded_song = parsed_input.get('Loaded Song', 'No song loaded')

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
        if game_mode in game_mode_mapping:
            game_mode = game_mode_mapping[game_mode]

        # Get the current timestamp
        current_time = datetime.now()

        # Check if the 'Game mode' has changed
        if update_presence.start_time is None:
            # If this is the initial mode setting, just set the mode without resetting the timer
            update_presence.initial_mode_set = True
            update_presence.previous_mode = game_mode
            update_presence.start_time = current_time
            #logger.debug(f"Initial game mode set to {game_mode}.")
        elif game_mode != update_presence.previous_mode:
            # If the mode has changed, reset the timer and update the previous mode
            update_presence.previous_mode = game_mode
            update_presence.start_time = current_time
            update_presence.last_printed_minute = None
            #logger.debug(f"Game mode changed to {game_mode}. Timer reset.")

        # Calculate the elapsed time
        elapsed_time_string = get_elapsed_time(update_presence.start_time)
        #logger.debug(f"Elapsed time: {elapsed_time_string}")

        # Get the active instruments and count the number of active instruments
        active_instruments = parsed_input.get('SelectedInstruments', [])
        active_instrument_count = sum(1 for instrument in active_instruments if instrument.get('active', False))

        # Check if there are more than 1 active instruments
        if active_instrument_count > 1:
            active_instrument_text = f"{active_instrument_count} player band"
        elif active_instrument_count == 1:
            active_instrument_text = "1 player band"
        else:
            active_instrument_text = ""

        # Set a default value for active_instrument_small_image
        active_instrument_small_image = 'default_small_image_name'

        active_instrument_count = sum(1 for instrument in active_instruments if instrument.get('active', False))

        # ...

        # Set a default value for active_instrument_small_text
        active_instrument_small_text = ""

        if active_instrument_count > 1:
            active_instrument_text = f"{active_instrument_count} Player"
            active_instrument_small_image = 'default_small_image_name'
        else:
            for instrument in active_instruments:
                if instrument.get('active', False):
                    instrument_name = instrument.get('instrument', '')
                    instrument_small_text_name = instrument.get('instrument', '')
                    instrument_difficulty = instrument.get('difficulty', '')
                    instrument_name = simplify_instrument_name(instrument_name)
                    instrument_difficulty = clean_difficulty(instrument_difficulty)
                    active_instrument_text = "Solo"
                    active_instrument_small_text = f"{instrument_name}, {instrument_difficulty}"
                    active_instrument_small_image = map_instrument_to_small_image(instrument_small_text_name)
                    break
            else:
                active_instrument_text = ""
                
        if parsed_input.get('Online', '') == "true":
            game_mode = "Online " + game_mode

        activity = {
            'details': f"{active_instrument_text} {game_mode} {elapsed_time_string}",
            'state': loaded_song,
            'large_image': 'banner',
            'large_text': large_text,
            'small_image': active_instrument_small_image,
            'small_text': active_instrument_small_text if active_instrument_small_text else None
        }

        # Update the presence
        RPC.update(**activity)

        # Print activity details if a new minute has passed
        current_minute = current_time.minute
        if current_minute != update_presence.last_printed_minute:
            print(f"Updating Presence: {loaded_song}, {active_instrument_text} {game_mode} {elapsed_time_string}")
            update_presence.last_printed_minute = current_minute

    except pypresence.InvalidPipe:
        logger.error("Discord client not detected. Make sure Discord is running.")

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
    return instrument_mapping.get(instrument_name, instrument_name)

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
        response = requests.get(address)
        if response.status_code == 200:
            raw_data = response.text
            sanitized_data = raw_data.replace('\\', '\\\\')
            return json.loads(sanitized_data)
        else:
            logger.error(f"Failed to fetch data from {address}, status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        logger.error(f"Error fetching data from {address}: {str(e)}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON data from {address}: {str(e)}")
        return None

# Function to get elapsed time in a user-friendly format
def get_elapsed_time(start_time):
    elapsed = datetime.now() - start_time
    days, remainder = divmod(elapsed.total_seconds(), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, _ = divmod(remainder, 60)
    
    if days > 0:
        return f"for {int(days)} day{'s' if days > 1 else ''}, {int(hours)} hour{'s' if hours != 1 else ''}, and {int(minutes)} minute{'s' if minutes != 1 else ''}"
    elif hours > 0:
        return f"for {int(hours)} hour{'s' if hours != 1 else ''} and {int(minutes)} minute{'s' if minutes != 1 else ''}"
    else:
        return f"for {int(minutes)} minute{'s' if minutes != 1 else ''}"

# Initialize static variables
update_presence.initial_mode_set = False
update_presence.previous_mode = ''
update_presence.start_time = None  # Set to None initially
update_presence.last_printed_minute = None

def main():
    # Check if Discord is installed and running
    try:
        import pypresence
    except ImportError:
        logger.error("pypresence module not found. Discord is either not installed or not accessible.")
        return

    # Configurable parameters
    client_id = "1125571051607298190"
    interval = 10  # Check for updates every 15 seconds

    config_path = Path.cwd() / 'dx_config.ini'
    rpcs3_path, xbox_console_ip = load_config(config_path)

    if rpcs3_path is None:
        rpcs3_path = get_rpcs3_path()
        xbox_console_ip = input("Enter the IP address of the Xbox console (leave empty if not applicable): ").strip()
        save_rpcs3_path(config_path, rpcs3_path, xbox_console_ip)

    json_path = rpcs3_path / "dev_hdd0" / "game" / "BLUS30463" / "USRDIR" / f"discordrp.json"

    json_file = Path(json_path)
    if not json_file.is_file() and not xbox_console_ip:
        logger.error(f"JSON file does not exist: {json_path} and no Xbox console IP provided.")
        return

    large_text = "Rock Band 3 Deluxe"  # Default value for large_text

    # Connect to Discord RPC
    try:
        RPC = pypresence.Presence(client_id)
        RPC.connect()
        logger.debug("Connected to Discord RPC successfully.")
    except pypresence.exceptions.DiscordNotFound:
        logger.error("Discord client not detected. Make sure Discord is running.")
        return

    json_data = None
    from_web = False
    if xbox_console_ip:
        logger.debug("Attempting to connect to Xbox 360.")
        web_address = f"http://{xbox_console_ip}:21070/jsonrpc"
        json_data = fetch_json_from_web(web_address)
        from_web = True

    if not json_data and json_file.is_file():
        with json_file.open('r') as file:
            json_data = file.read()
        from_web = False

    if json_data:
        # Parse the raw input data
        parsed_input_data = parse_raw_input(json_data, from_web)

        # Load the JSON data from parsed input
        presence_data = load_json(parsed_input_data)

        if presence_data is not None:
            # Initial update to Discord Rich Presence
            connect_and_update(client_id, interval, RPC, presence_data, large_text)
        else:
            logger.error("Failed to load presence data. Check the JSON input.")
    else:
        logger.error("No valid JSON data available from either web address or local file.")
        return

    try:
        while True:
            if from_web:
                # Fetch JSON data from web address
                json_data = fetch_json_from_web(web_address)
                if json_data:
                    # Parse the raw input data
                    parsed_input_data = parse_raw_input(json_data, from_web)
                    # Load the JSON data from parsed input
                    presence_data = load_json(parsed_input_data)
                    if presence_data is not None:
                        # Update Discord Rich Presence
                        connect_and_update(client_id, interval, RPC, presence_data, large_text)
                    else:
                        logger.error("Failed to load presence data. Check the JSON input.")
            elif json_file.is_file():
                with json_file.open('r') as file:
                    json_data = file.read()

                if json_data:
                    # Parse the raw input data
                    parsed_input_data = parse_raw_input(json_data, from_web)

                    # Load the JSON data from parsed input
                    presence_data = load_json(parsed_input_data)

                    if presence_data is not None:
                        # Update Discord Rich Presence
                        connect_and_update(client_id, interval, RPC, presence_data, large_text)
                    else:
                        logger.error("Failed to load presence data. Check the JSON input.")
                else:
                    logger.error("No valid JSON data available from local file.")
            
            # Wait for the specified interval before checking again
            time.sleep(interval)

    except KeyboardInterrupt:
        print("Disconnecting from Discord...")
        RPC.clear()
        RPC.close()
        print("Disconnected. Goodbye!")

if __name__ == '__main__':
    main()

import sys
import subprocess
import json
import time
import os
import logging
from pathlib import Path

# Check if the system is running on macOS
is_macos = sys.platform == "darwin"

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# List of required packages
required_packages = ["pypresence", "json", "time", "os", "logging", "pathlib"]

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
def parse_raw_input(raw_input):
    #logger.debug("Parsing raw input data...")
    parsed_input = raw_input.replace("\\q", "\"")
    parsed_input = parsed_input.replace("'", "'")  # Replace single quotes with double quotes
    parsed_input = parsed_input[1:-2]  # Remove first quote and extra double quote at the end
    #logger.debug("Raw input data parsed successfully.")
    return parsed_input

# Function to load JSON data from parsed input
def load_json(parsed_input):
    #logger.debug("Loading JSON data...")
    try:
        data = json.loads(parsed_input)  # Parse the JSON data
        #logger.debug("JSON data loaded successfully.")
        return data
    except json.JSONDecodeError as e:
        logger.exception("Invalid JSON data.")
        return None

# Function to prompt for JSON file path
def prompt_json_path(suffix):
    json_path = input(f"Enter the path to the JSON file{suffix}: ")
    return json_path.strip()

# Connect to Discord RPC and update rich presence
def connect_and_update(client_id, interval, RPC, json_path_suffix="", large_text=""):
    try:
        # Try to read JSON file path from the text file
        json_path_file = Path(f"json_path{json_path_suffix}.txt")
        if not json_path_file.is_file():
            logger.error(f"JSON file path text file not found{json_path_suffix}.")
            json_path = prompt_json_path(json_path_suffix)
            json_path_file.write_text(json_path)
        else:
            json_path = json_path_file.read_text().strip()
            #logger.debug(f"JSON file path read from the text file: {json_path}")

        json_file = Path(json_path)
        if not json_file.is_file():
            logger.error(f"JSON file does not exist: {json_path}")
            return

        try:
            # Read the raw input data from the stored file
            with json_file.open('r') as file:
                raw_input_data = file.read()

            # Print the parsed raw input
            #logger.debug("Parsed Raw Input:")
            #logger.debug(raw_input_data)

            # Parse the raw input data
            parsed_input_data = parse_raw_input(raw_input_data)

            # Print the parsed JSON
            #logger.debug("Parsed JSON:")
            #logger.debug(parsed_input_data)

            # Load the JSON data from parsed input
            presence_data = load_json(parsed_input_data)

            # Check if the JSON data was loaded successfully
            if presence_data is not None:
                # Update Discord Rich Presence
                #logger.debug(f"Presence data: {presence_data}")
                update_presence(client_id, presence_data, RPC, large_text)
            else:
                logger.error("Failed to load presence data. Check the JSON input.")

        except Exception as e:
            logger.exception(f"An error occurred: {str(e)}")

    except FileNotFoundError:
        # If the text file doesn't exist, prompt for JSON file path
        json_path = prompt_json_path()
        logger.error(f"JSON file path text file not found: {json_path}")
# Update Discord Rich Presence
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
            'jukebox': 'Jukebox'
        }
        if game_mode in game_mode_mapping:
            game_mode = game_mode_mapping[game_mode]

        # Get the current timestamp
        current_time = int(time.time())

        # Check if the 'Game mode' has changed
        if game_mode != update_presence.previous_mode:
            # If the mode has changed, reset the timer and update the previous mode
            update_presence.previous_mode = game_mode
            update_presence.start_time = current_time

        # Calculate the duration in seconds
        elapsed_time = current_time - update_presence.start_time

        # Format the elapsed time into a user-friendly string
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        elapsed_time_string = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

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

        #logger.debug(f"Large text: {large_text}")

        activity = {
            'details': f"{active_instrument_text} {game_mode} (Elapsed: {elapsed_time_string})",
            'state': loaded_song,
            'large_image': 'banner',
            'large_text': large_text,
            'small_image': active_instrument_small_image,
            'small_text': active_instrument_small_text if active_instrument_small_text else None
        }

        # Update the presence
        RPC.update(**activity)
        #logger.debug("Rich Presence updated.")

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

# Initialize static variables
update_presence.previous_mode = ''
update_presence.start_time = 0

# Main function
def main(suffix=None):
    # Check if Discord is installed and running
    try:
        import pypresence
    except ImportError:
        logger.error("pypresence module not found. Discord is either not installed or not accessible.")
        return

    # Configurable parameters
    client_id = "1125571051607298190"
    interval = 1  # Check for updates every 10 seconds

    # Set the JSON path suffix based on the provided argument
    json_path_suffix = ""
    large_text = "Rock Band 3 Deluxe"  # Default value for large_text

    if suffix == "_xenia":
        json_path_suffix = suffix
        large_text = "Rock Band 3 Deluxe Xenia"
    elif suffix == "_rpcs3":
        json_path_suffix = suffix
        large_text = "Rock Band 3 Deluxe RPCS3"

    # Connect to Discord RPC
    try:
        RPC = pypresence.Presence(client_id)
        RPC.connect()
        logger.debug("Connected to Discord RPC successfully.")
    except pypresence.exceptions.DiscordNotFound:
        logger.error("Discord client not detected. Make sure Discord is running.")
        return

    try:
        while True:
            # Pass the json_path_suffix and large_text to connect_and_update function
            connect_and_update(client_id, interval, RPC, json_path_suffix, large_text)
            # Wait for the specified interval before checking again
            time.sleep(interval)

    except KeyboardInterrupt:
        pass

    # Disconnect from Discord RPC before exiting
    RPC.close()

if __name__ == '__main__':
    # Check for the script argument and pass it to the main function
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()

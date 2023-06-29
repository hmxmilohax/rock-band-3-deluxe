import json
import time
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Check if currentsonglocation.txt file exists
if os.path.isfile('currentsonglocation.txt'):
    # If the file exists, load the path from it
    with open('currentsonglocation.txt', 'r') as file:
        currentsong_path = file.read()
        logging.info("Loaded file location from currentsonglocation.txt.")
else:
    # Ask the user to input the location of currentsong.json
    currentsong_path = input("Enter the location of currentsong.json: ")
    
    # Save the path to currentsonglocation.txt file
    with open('currentsonglocation.txt', 'w') as file:
        file.write(currentsong_path)
    logging.info("File location saved to currentsonglocation.txt.")

# Function to monitor currentsong.json
def monitor_currentsong():
    while True:
        try:
            # Read the content of the file
            with open(currentsong_path, 'r') as file:
                content = file.read()

            if content and content[0] == '"':
                # Remove all quotes
                content = content.replace('"', '')

                # Replace "\qPlaylist\q:\q" with "\qPlaylist\q:\q\q"
                content = content.replace('\\qPlaylist\\q:\\q', '\\qPlaylist\\q:\\q\\q')

                # Replace "\qSubPlaylist\q:\q" with "\qSubPlaylist\q:\q\q"
                content = content.replace('\\qSubPlaylist\\q:\\q', '\\qSubPlaylist\\q:\\q\\q')

                # Replace "\qLoadingPhrase\q:\q" with "\qLoadingPhrase\q:\q\q"
                content = content.replace('\\qLoadingPhrase\\q:\\q', '\\qLoadingPhrase\\q:\\q\\q')

                # Replace "\q" with an actual double quote
                content = content.replace('\\q', '"')

                # Write the modified content back to the file
                with open(currentsong_path, 'w') as file:
                    file.write(content)

                logging.info("Modification completed. The modified content is saved in 'currentsong.json'.")
        except IOError:
            logging.error("An error occurred while reading or writing the file.")

        time.sleep(2)  # Wait for 2 seconds before probing again

# Call the function to monitor currentsong.json
monitor_currentsong()

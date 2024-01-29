import csv
import random
from fuzzywuzzy import process
import os
import configparser

def get_csv_and_config_file_paths():
    config = configparser.ConfigParser()
    config_file_path = "config.ini"

    if not os.path.exists(config_file_path):
        print("Configuration file not found. Creating a new one.")
        config.add_section("Paths")
        csv_file_path = input("Enter the path for the CSV file (e.g., A:/games/RPCS3/dev_hdd0/game/BLUS30463/USRDIR/jnacks_setlist.csv): ")
        config.set("Paths", "csv_file_path", csv_file_path)

        output_file_path = input("Enter the path for the output file (e.g., A:/games/RPCS3/dev_hdd0/game/BLUS30463/USRDIR/dx_playlist.dta): ")
        config.set("Paths", "output_file_path", output_file_path)

        with open(config_file_path, "w") as config_file:
            config.write(config_file)
    else:
        config.read(config_file_path)
        csv_file_path = config.get("Paths", "csv_file_path")
        output_file_path = config.get("Paths", "output_file_path")

    return csv_file_path, output_file_path, config_file_path

def read_csv(csv_file_path):
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t', quotechar='"', escapechar='\\')
        header = next(reader)  # Read the header row

        # Find the index of the 'Song Title', 'Artist', 'Year', 'Genre', and 'Short Name' columns
        song_title_index = next((i for i, col in enumerate(header) if "Song Title" in col), None)
        artist_index = next((i for i, col in enumerate(header) if "Artist" in col), None)
        year_index = next((i for i, col in enumerate(header) if "Year" in col), None)
        genre_index = next((i for i, col in enumerate(header) if "Genre" in col), None)
        short_name_index = next((i for i, col in enumerate(header) if "Short Name" in col), None)

        if song_title_index is None or artist_index is None:
            print("Error: 'Song Title' or 'Artist' column not found.")
            return None

        # Read all data from the CSV file and store it in memory
        data = list(reader)

    return data, song_title_index, artist_index, year_index, genre_index, short_name_index

def get_random_year(data, year_index):
    years = set(row[year_index] for row in data)
    return random.choice(list(years))

def get_random_artist(data, artist_index):
    artists = set(row[artist_index] for row in data)
    return random.choice(list(artists))

def get_random_genre(data, genre_index):
    genres = set(row[genre_index] for row in data)
    return random.choice(list(genres))

def get_random_song(data, song_title_index, artist_index):
    song = random.choice(data)
    return song[song_title_index], song[artist_index]

def eval_random_song(data, song_title_index, artist_index, short_name_index):
    song = random.choice(data)
    return song[song_title_index], song[artist_index], song[short_name_index]

def clear_playlist(output_file):
    with open(output_file, 'w') as output:
        output.write("")
    print(f"Playlist cleared in {output_file}")

def get_random_song_from_artist(data, artist, song_title_index, artist_index):
    # Filter songs by the specified artist
    artist_songs = [song for song in data if song[artist_index] == artist]

    if not artist_songs:
        print(f"No songs found for the artist '{artist}'.")
        return None

    # Choose a random song from the filtered list
    song = random.choice(artist_songs)
    return song[song_title_index], song[artist_index]


def fuzzy_search(data, song_title_index, artist_index, year_index, genre_index, short_name_index, config_file, target_title):
    config = configparser.ConfigParser()
    config.read(config_file)

    output_file_path = config.get("Paths", "output_file_path")

    # Check if it's a genre search
    if target_title.startswith('genre:'):
        genre_to_search = target_title[len('genre:'):].strip()
        genre_matches = [(row[song_title_index], row[artist_index], row[short_name_index]) for row in data if genre_to_search.lower() in row[genre_index].lower()]

        if genre_matches:
            # Randomly select a matching song title, artist, and short name
            random_song_title, random_artist, random_short_name = random.choice(genre_matches)
            print(f"Random song matching genre '{genre_to_search}': '{random_song_title}' by '{random_artist}'")

            append_short_name_to_output(output_file_path, random_short_name)
        else:
            print(f"No songs found in the genre '{genre_to_search}'.")
    # Check if it's a year search
    elif target_title.startswith('year:'):
        year_to_search = target_title[len('year:'):].strip()
        year_matches = [(row[song_title_index], row[artist_index], row[short_name_index]) for row in data if year_to_search == row[year_index]]

        if year_matches:
            # Randomly select a matching song title, artist, and short name
            random_song_title, random_artist, random_short_name = random.choice(year_matches)
            print(f"Random song from the year '{year_to_search}': '{random_song_title}' by '{random_artist}'")

            append_short_name_to_output(output_file_path, random_short_name)
        else:
            print(f"No songs found in the year '{year_to_search}'.")
    elif target_title == 'csv':
        # Choose a random song from the CSV file
        song_title, artist = get_random_song(data, song_title_index, artist_index)
        print(f"Random song title from the CSV file: '{song_title}' by '{artist}'")
    else:
        # Perform fuzzy search on the 'Song Title' and 'Artist' columns
        matches = [(row[song_title_index], row[artist_index], row[short_name_index], score) for row in data for _, score in [process.extractOne(target_title, [row[song_title_index], row[artist_index]])]]

        # Get the top 5 matches
        top_matches = sorted(matches, key=lambda x: x[3], reverse=True)[:5]

        # Print the top 5 matches
        for i, (match_title, match_artist, _, score) in enumerate(top_matches, start=1):
            print(f"{i}. '{match_title}' by '{match_artist}' (Score: {score})")

        # Ask the user for confirmation
        confirmation = input("Enter the number (1-5), 'n' to abort: ")

        if confirmation.lower() == 'y':
            # Extract the best match and its index
            best_match, best_artist, best_short_name, _ = max(top_matches, key=lambda x: x[3])

            append_short_name_to_output(output_file_path, best_short_name)
        elif confirmation.lower() == 'n':
            print("Operation aborted.")
        elif confirmation.isdigit() and 1 <= int(confirmation) <= 5:
            # Extract the selected match and its index
            selected_match, _, selected_short_name, _ = top_matches[int(confirmation) - 1]

            append_short_name_to_output(output_file_path, selected_short_name)
        else:
            print("Invalid input. Please enter 'y', 'n', 'genre:GenreName', 'year:Year', 'csv', or a number (1-5).")

def append_short_name_to_output(output_file, short_name):
    # Open the dx_playlist.dta file and read the existing content
    with open(output_file, 'r') as output:
        existing_content = output.read().strip()

    # Extract short names from existing content
    existing_short_names = [s.strip('()') for s in existing_content.split()]

    # Add the new short name to the list
    existing_short_names.append(short_name)
    # Write back to the dx_playlist.dta file
    with open(output_file, 'w') as output:
        output.write(f"({' '.join(existing_short_names)})")

    print(f"Short Name '({short_name})' appended to {output_file}")

def refresh_options(data, song_title_index, artist_index, year_index, genre_index, short_name_index):
    year = get_random_year(data, year_index)
    artist = get_random_artist(data, artist_index)
    song_title, _ = get_random_song(data, song_title_index, artist_index)
    random_song_name = {get_random_song(data, song_title_index, artist_index)}
    genre = get_random_genre(data, genre_index)
    song_title_raw, artist2, short_name2 = eval_random_song(data, song_title_index, artist_index, short_name_index)
    print(" ")
    return year, artist, song_title, genre, song_title_raw, artist2, short_name2

def main():
    csv_file_path, output_file_path, config_file_path = get_csv_and_config_file_paths()
    data = read_csv(csv_file_path)

    if data:
        data, song_title_index, artist_index, year_index, genre_index, short_name_index = data
        year, artist, song_title, genre, song_title_raw, artist2, short_name2 = refresh_options(data, song_title_index, artist_index, year_index, genre_index, short_name_index)
        while True:
            print("Welcome to Rock Band 3 Deluxe Play A Show!")
            print("Choose an option:")
            print(f"1. A random song from {year}")
            print(f"2. A random song by {artist}")
            print(f"3. '{song_title_raw}' by '{artist2}'")
            print(f"4. A random {genre} song")
            print("5. Refresh options")
            print("6. Manual fuzzy search")
            print("7. Clear the playlist")
            print("0. Exit")

            choice = input("Enter the number of your choice: ")

            if choice == '1':
                fuzzy_search(data, song_title_index, artist_index, year_index, genre_index, short_name_index, config_file_path, f'year:{year}')
                year, artist, song_title, genre, song_title_raw, artist2, short_name2 = refresh_options(data, song_title_index, artist_index, year_index, genre_index, short_name_index)
            elif choice == '2':
                song_title, _ = get_random_song_from_artist(data, artist, song_title_index, artist_index)
                if song_title:
                    short_name = [song[short_name_index] for song in data if song[song_title_index] == song_title][0]
                    print(f"Random song from {artist}: '{song_title}'")
                    append_short_name_to_output(output_file_path, short_name)
                year, artist, song_title, genre, song_title_raw, artist2, short_name2 = refresh_options(data, song_title_index, artist_index, year_index, genre_index, short_name_index)
            elif choice == '3':
                append_short_name_to_output(output_file_path, short_name2)
                year, artist, song_title, genre, song_title_raw, artist2, short_name2 = refresh_options(data, song_title_index, artist_index, year_index, genre_index, short_name_index)
            elif choice == '4':
                fuzzy_search(data, song_title_index, artist_index, year_index, genre_index, short_name_index, config_file_path, f'genre:{genre}')
                year, artist, song_title, genre, song_title_raw, artist2, short_name2 = refresh_options(data, song_title_index, artist_index, year_index, genre_index, short_name_index)
            elif choice == '5':
                print("Options refreshed.")
                year, artist, song_title, genre, song_title_raw, artist2, short_name2 = refresh_options(data, song_title_index, artist_index, year_index, genre_index, short_name_index)
            elif choice == '6':
                search_string = input("Enter a Song Title or Artist to search for: ")
                fuzzy_search(data, song_title_index, artist_index, year_index, genre_index, short_name_index, config_file_path, search_string)
                print(" ")
            elif choice == '7':
                clear_playlist(output_file_path)
                year, artist, song_title, genre, song_title_raw, artist2, short_name2 = refresh_options(data, song_title_index, artist_index, year_index, genre_index, short_name_index)
            elif choice == '0':
                print("Exiting Play A Show. Goodbye!")
                break
            else:
                print("Invalid choice.")

if __name__ == "__main__":
    main()

# takes a song dict (ideally returned from parse_song_dta), and converts it back into dta
# returns a list of dta lines for the user to write out to a dta file
def song_dict_to_dta(song_dict: dict, indent=0):
    lines = []
    for song_k,song_v in song_dict.items():
        if isinstance(song_v, dict):
            lines.append(f"{'    '*indent}({song_k}")
            if song_k == "tracks":
                lines.append(f"{'    '*indent}{'  '}(")
            lines.extend(song_dict_to_dta(song_v, indent+1))
            if song_k == "tracks":
                lines.append(f"{'    '*indent}{'  '})")
            lines.append(f"{'    '*indent})")
        else:
            if isinstance(song_v, str) and song_k in ["name", "artist", "album_name", "midi_file"]:
                lines.append(f"{'    '*(indent)}({song_k} \"{song_v}\")")
            elif isinstance(song_v, list):
                if song_k == "preview" or song_k == "crowd_channels":
                    lines.append(f"{'    '*(indent)}({song_k} {' '.join(str(a) for a in song_v)})")
                else:
                    lines.append(f"{'    '*(indent)}({song_k} ({' '.join(str(a) for a in song_v)}))")
            else:
                lines.append(f"{'    '*(indent)}({song_k} {song_v})")
    return lines

# def main():
#     if len(sys.argv) != 2:
#         print("no dta provided")
#         exit()
#     big_song_dict = parse_dta(sys.argv[1])

#     print("Dict to dta...")
#     dict_to_dta(big_song_dict["songs"])

#     # print(song_dict_to_dta(big_song_dict["songs"]))
#     for line in song_dict_to_dta(big_song_dict["songs"]):
#         print(line)

    
# if __name__ == "__main__":
#     main()

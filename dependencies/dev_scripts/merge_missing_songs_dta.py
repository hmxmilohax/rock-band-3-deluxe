from pathlib import Path
from add_rb3_plus_pro_strings import *
from add_rb3_plus_keys import *
from parse_song_dta import parse_song_dta
from song_dict_to_dta import song_dict_to_dta
import argparse

# use -k if you want to add keys
# use -o if you want to restore every song to how it originally was in RB3 (that is to say, no harmonies or RB4 chart upgrades)
parser = argparse.ArgumentParser(prog = 'missing_songs_dta_merger', description="merges separate dtas to make one big missing_songs_dta")
parser.add_argument("-k", "--keys", action="store_true")
parser.add_argument("-o", "--original", action="store_true")

args = parser.parse_args()

# get the current working directory (where this script resides)
cwd = Path().absolute()
# get the root directory of the repo
root_dir = Path(__file__).parents[2]

dta_dir = root_dir.joinpath("dependencies/dta_sections")
# vanilla.dta
# vanilla_pro_upgrades.dta
# custom_sources_official.dta
# custom_sources_rbn.dta
# custom_sources_unofficial.dta
# harms_and_updates.dta
# keys.dta

grand_total_dta_dict = {}

# TODO: merge all of these dicts together, and then output THAT big combined dict as a nice, clean, merged dta
# vanilla = parse_song_dta(dta_dir.joinpath("vanilla.dta"))["songs"]
# vanilla_pro = parse_song_dta(dta_dir.joinpath("vanilla_pro_upgrades.dta"))["songs"]
# cs_official = parse_song_dta(dta_dir.joinpath("custom_sources_official.dta"))["songs"]
# cs_rbn = parse_song_dta(dta_dir.joinpath("custom_sources_rbn.dta"))["songs"]
# cs_unofficial = parse_song_dta(dta_dir.joinpath("custom_sources_unofficial.dta"))["songs"]
# rb3_plus_strings = integrate_rb3_plus()
# keys_dict = integrate_rb3_plus_keys() if args.keys else {}
# harms_dict = parse_song_dta(dta_dir.joinpath("harms_and_updates.dta")) if not args.original else {}

with open(dta_dir.joinpath("vanilla.dta"),"r", encoding="ISO-8859-1") as f:
    vanilla = [line for line in f.readlines()]

with open(dta_dir.joinpath("vanilla_pro_upgrades.dta"),"r", encoding="ISO-8859=1") as f:
    vanilla_pro = [line for line in f.readlines()]

with open(dta_dir.joinpath("custom_sources_official.dta"),"r", encoding="ISO-8859=1") as f:
    cs_official = [line for line in f.readlines()]

with open(dta_dir.joinpath("custom_sources_rbn.dta"),"r", encoding="ISO-8859=1") as f:
    cs_rbn = [line for line in f.readlines()]

with open(dta_dir.joinpath("custom_sources_unofficial.dta"),"r", encoding="ISO-8859=1") as f:
    cs_unofficial = [line for line in f.readlines()]

with open(dta_dir.joinpath("misc.dta"),"r", encoding="ISO-8859=1") as f:
    misc = [line for line in f.readlines()]

rb3_plus_dta = [s + "\n" for s in song_dict_to_dta(integrate_rb3_plus())]

if args.keys:
    keys_dta = [s + "\n" for s in song_dict_to_dta(integrate_rb3_plus_keys())]
else:
    keys_dta = []

if not args.original:
    with open(dta_dir.joinpath("harms_and_updates.dta"),"r", encoding="ISO-8859=1") as f:
        harms_dta = [line for line in f.readlines()]
else:
    harms_dta = []

grand_total_dta = []
if args.keys:
    grand_total_dta.extend(keys_dta)
    grand_total_dta.append("\n")
grand_total_dta.extend(vanilla)
grand_total_dta.append("\n")
grand_total_dta.extend(cs_official)
grand_total_dta.append("\n")
grand_total_dta.extend(cs_rbn)
grand_total_dta.append("\n")
grand_total_dta.extend(cs_unofficial)
grand_total_dta.append("\n")
grand_total_dta.extend(misc)
grand_total_dta.append("\n")
if not args.original:
    grand_total_dta.extend(harms_dta)
    grand_total_dta.append("\n")
grand_total_dta.extend(vanilla_pro)
grand_total_dta.append("\n")
grand_total_dta.extend(rb3_plus_dta)

with open(root_dir.joinpath("_ark/songs/missing_song_data.dta"),"w",encoding="ISO-8859-1") as dta_output:
        dta_output.writelines(grand_total_dta)

print(f"missing song dta written to {root_dir.joinpath('_ark/songs/missing_song_data.dta')}.")
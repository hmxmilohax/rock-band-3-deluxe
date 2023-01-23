# enable_stock_pad.py
from pathlib import Path

def main():

    # get the current working directory (where this script resides)
    cwd = Path().absolute()
    # get the root directory of the repo
    root_dir = Path(__file__).parents[2]

    with open(root_dir.joinpath("_ark/config/macros.dta"), "r", encoding="ISO-8859=1") as f:
        the_macros = [line for line in f.readlines()]

    for i in range(len(the_macros)):
        if ";#define STOCK_PAD" in the_macros[i]:
            the_macros[i] = the_macros[i].replace(";#define STOCK_PAD", "#define STOCK_PAD")
            break

    with open(root_dir.joinpath("_ark/config/macros.dta"), "w", encoding="ISO-8859=1") as ff:
        ff.writelines(the_macros)

if __name__ == "__main__":
    main()
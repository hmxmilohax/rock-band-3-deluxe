# add_devbuild.py
from pathlib import Path
import sys

def main():
    if len(sys.argv) != 2:
        print("no devbuild provided")
    else:
        commit = sys.argv[1]
        print(f"Commit: {commit}")
        # get the current working directory (where this script resides)
        cwd = Path().absolute()
        # get the root directory of the repo
        root_dir = Path(__file__).parents[2]
        print(root_dir)
        # sed -i -e "s/devbuild/"$GITHUB_SHA_SHORT"/g" _ark/ui/locale/*/locale_updates_keep.dta
        for locale in root_dir.joinpath("_ark/ui/locale").glob("*/locale_updates_keep.dta"):
            print(locale)
            with open(locale, "r", encoding="ISO-8859=1") as f:
                the_locale = [line for line in f.readlines()]

            for i in range(len(the_locale)):
                if "devbuild" in the_locale[i]:
                    the_locale[i] = the_locale[i].replace("devbuild", f"devbuild {commit}")

            with open(locale, "w", encoding="ISO-8859=1") as ff:
                ff.writelines(the_locale)


if __name__ == "__main__":
    main()
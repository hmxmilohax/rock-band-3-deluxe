import sys

# Check if correct number of arguments are provided
if len(sys.argv) != 2:
    print("Usage: python filter_file.py <input_file>")
    sys.exit(1)

# Input file name
input_file = sys.argv[1]

# Function to check if a line starts with "Shortname="
def line_starts_with_shortname(line):
    return line.startswith("ShortName=")

# Function to extract the shortname value
def extract_shortname(line):
    return line.split("ShortName=")[1].strip()

# Read input file, filter lines, and write to output file
with open(input_file, 'r') as f_in, open('playashow.dta', 'w') as f_out:
    for line in f_in:
        if line_starts_with_shortname(line.strip()):
            shortname_value = extract_shortname(line)
            f_out.write(f"({shortname_value})\n")

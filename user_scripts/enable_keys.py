# enable_keys.py
import subprocess
from sys import platform

# copy the add_rb3_plus_keys.py code
# or better yet, just call it
cmd_xenia = "python dependencies\\dev_scripts\\add_rb3_plus_keys.py"
subprocess.run(cmd_xenia, shell=(platform == "win32"), cwd="..")
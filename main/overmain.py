import subprocess
import shlex

subprocess.call(shlex.split('sudo PYTHONPATH=".:build/lib.linux-armv7l-2.7" python main.py'))

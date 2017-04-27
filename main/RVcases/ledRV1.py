import subprocess
import shlex

subprocess.call(shlex.split('sudo PYTHONPATH="../LEDs/python/build/lib.linux-armv7l-2.7" python ../ledRV1_part2.py'))
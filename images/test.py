import numpy
import os
from shutil import move as move_file

source_file = '/input/001.jpg'
os.makedirs('processed', exist_ok=True)
destination_dir = '/processed'

# Move the file
shutil.move(source_file, destination_dir)

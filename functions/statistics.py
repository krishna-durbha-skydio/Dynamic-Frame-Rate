"""
Compute Statistics
"""
# Importing Libraries
import numpy as np
import matplotlib.pyplot as plt

import os,pathlib,sys,warnings
warnings.filterwarnings('ignore')
sys.path.append("/home/krishnasrikardurbha/Desktop/Dynamic-Frame-Rate")
import subprocess, shlex
import functions.software_commands as software_commands
import defaults


def get_statistics(
	video_path:str,
	quality_dir:str
):
	"""
	Args:
		input_path (str): List of video path
	"""
	# File
	filename, ext = os.path.splitext(os.path.basename(video_path))
	original = filename.split("_")

	# Resolution, Bitrate and fps
	cmd = software_commands.get_metadata(
		input_path=video_path
	)
	output = subprocess.getoutput(cmd)
	output = output.split(",")
	
	# Resolution
	w, h = int(output[1]), int(output[2])
	resolution = (w,h)
	
	# fps
	fps = output[3].split("/")
	fps = float(fps[0])/float(fps[1])
		
	# Bitrate
	b = int(output[-1])/1e6

	# Quality Score
	quality_file_path = os.path.join(quality_dir, filename+".npy")
	try:
		q = np.load(quality_file_path, allow_pickle=True)[()][0]
	except:
		q = np.load(quality_file_path, allow_pickle=True)[()]

	return resolution, fps, b, q
"""
Creating and Analyzing Video Segments
"""
# Importing Libraries
import numpy as np
np.set_printoptions(suppress=True)
import matplotlib.pyplot as plt
import seaborn as sns
import multiprocessing

import os,pathlib,sys,warnings
warnings.filterwarnings('ignore')
sys.path.append("/home/krishnasrikardurbha/Desktop/Dynamic-Frame-Rate")
from tqdm import tqdm
import subprocess, shlex, joblib
import functions.software_commands as software_commands
import functions.quality_metrics as quality_metrics
import functions.statistics as statistics
import functions.utils as utils
import defaults

# Paths
streamed_videos_dir = "/home/krishnasrikardurbha/Desktop/Dynamic-Frame-Rate/dataset/real_time/streamed_videos"
streamed_videos_segments_dir = "/home/krishnasrikardurbha/Desktop/Dynamic-Frame-Rate/dataset/real_time/streamed_videos_segments"
streamed_videos_segments_quality_scores_dir = "/home/krishnasrikardurbha/Desktop/Dynamic-Frame-Rate/dataset/real_time/streamed_videos_segments_quality_scores"


# Splitting Videos that are streamed videos
time_length = 1
for video_file in os.listdir(streamed_videos_dir):
	# Command
	cmd = software_commands.split_video_fixed_time(
		input_path=os.path.join(streamed_videos_dir, video_file),
		time_length=time_length,
		output_dir=os.path.join(streamed_videos_segments_dir)
	)

	# Execute
	subprocess.run(shlex.split(cmd))


# Loading CONVIQT Model
CONVIQT = quality_metrics.CONVIQT()

# Function to save scores
def save_scores(videos_dir, quality_scores_dir, filename, replace=False):
    if os.path.exists(os.path.join(quality_scores_dir, os.path.splitext(filename)[0] + ".npy")) == False or replace == True:
        quality = CONVIQT.compute_quality(os.path.join(videos_dir, filename))
        np.save(os.path.join(quality_scores_dir, filename[:-4]+".npy"), quality)


# Calculating quality of streamed video segments i.e 1s segments of each flights
for video_file in tqdm(os.listdir(streamed_videos_segments_dir)):
    save_scores(streamed_videos_segments_dir, streamed_videos_segments_quality_scores_dir, video_file)


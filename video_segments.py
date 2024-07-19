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

# Compressing Video to simulate at intermediate bitrates
Bitrate2Filenames_Maps = [
    ((2.75, 2.5, 2.25), (1,2,3,13,14,15,25,26,27,37,38,39)),
    ((1.75, 1.5, 1.25), (4,5,6,16,17,18,28,29,30,40,41,42))
]

streamed_videos_path = "/home/krishnasrikardurbha/Desktop/Dynamic-Frame-Rate/dataset/streamed_videos"
for bitrates, FlightIDs in Bitrate2Filenames_Maps:
    for b in bitrates:
        for id in FlightIDs:
            # Video Path and Save Path
            video_path = os.path.join(streamed_videos_path, "flight{}.mp4".format(id))
            save_path = os.path.join(streamed_videos_path, "flight{}_{}.mp4".format(id,b))

            # Command to Compress Videos
            cmd = software_commands.simulate_compress_video(
                input_path=video_path,
                video_codec="libx265",
                output_bitrate=b,
                output_path=save_path,
                threads=8
            )

            # Execute
            subprocess.run(shlex.split(cmd))


# # Splitting Videos that are streamed videos
# time_length = 1
# for video_file in os.listdir(defaults.streamed_videos):
# 	# Command
# 	cmd = software_commands.split_video_fixed_time(
# 		input_path=os.path.join(defaults.streamed_videos, video_file),
# 		time_length=time_length,
# 		output_dir=os.path.join(defaults.video_segments)
# 	)

# 	# Execute
# 	subprocess.run(shlex.split(cmd))


# Saving Scores
# Loading CONVIQT Model
CONVIQT = quality_metrics.CONVIQT()

def save_scores(videos_dir, quality_scores_dir, filename, replace=False):
	if os.path.exists(os.path.join(quality_scores_dir, filename[:-4]+".npy")) == False or replace == True:
		quality = CONVIQT.compute_quality(os.path.join(videos_dir, filename))
		np.save(os.path.join(quality_scores_dir, filename[:-4]+".npy"), quality)


# Streamed Videos Parallel
videos_dir = defaults.streamed_videos
quality_scores_dir = os.path.join(defaults.quality_scores, "CONVIQT")
for filename in tqdm(os.listdir(videos_dir)):
	save_scores(videos_dir, quality_scores_dir, filename)
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


for gop_size in [10,30]:
    # Creating Synthetic Dataset
    stored_videos_dir = "/home/krishnasrikardurbha/Desktop/Dynamic-Frame-Rate/dataset/simulations/stored_videos"
    compressed_videos_dir = "/home/krishnasrikardurbha/Desktop/Dynamic-Frame-Rate/dataset/simulations/gop_size={}/compressed_videos".format(int(gop_size))

    # Compressed videos for different resolution, fps and bitrates
    for resolution in [(1920,1080), (1280,720)]:
        resolution_string = "{}x{}".format(resolution[0], resolution[1])
        for fps in [30,20,10]:
            for bitrate in reversed([4, 3.5, 3, 2.75, 2.5, 2.25, 2, 1.75, 1.5, 1.25, 1, 0.75, 0.5, 0.25]):
                # For each file in stored-videos
                for flight_name in os.listdir(stored_videos_dir):
                    # Creating directories
                    os.makedirs(os.path.join(compressed_videos_dir, resolution_string, str(fps), str(bitrate)), exist_ok=True)

                    # Video Path and Save Path
                    video_path = os.path.join(stored_videos_dir, flight_name)
                    save_dir = os.path.join(compressed_videos_dir, resolution_string, str(fps), str(bitrate))

                    if os.path.exists(os.path.join(save_dir, os.path.splitext(flight_name)[0] + ".mp4")):
                        print ("File {} Exists. Skipping".format(os.path.join(save_dir, os.path.splitext(flight_name)[0] + ".mp4")))
                        print ()
                        continue

                    # Command to Compress Videos
                    cmd = software_commands.compress_video(
                        input_path=video_path,
                        output_resolution=resolution,
                        output_bitrate=bitrate,
                        output_fps=fps,
                        output_gop_size=gop_size,
                        output_dir=save_dir,
                        threads=16
                    )

                    # Execute
                    subprocess.run(shlex.split(cmd))


    # Splitting Videos
    time_length = 3

    compressed_videos_dir = "/home/krishnasrikardurbha/Desktop/Dynamic-Frame-Rate/dataset/simulations/gop_size={}/compressed_videos".format(int(gop_size))
    compressed_videos_segments_dir = "/home/krishnasrikardurbha/Desktop/Dynamic-Frame-Rate/dataset/simulations/gop_size={}/compressed_videos_segments".format(int(gop_size))


    for resolution in [(1920,1080), (1280,720)]:
        resolution_string = "{}x{}".format(resolution[0], resolution[1])
        for fps in [30,20,10]:
            for bitrate in [4, 3.5, 3, 2.75, 2.5, 2.25, 2, 1.75, 1.5, 1.25, 1, 0.75, 0.5, 0.25]:
                # For each compressed video
                compressed_videos_setting_dir = os.path.join(compressed_videos_dir, resolution_string, str(fps), str(bitrate))
                compressed_videos_segments_setting_dir = os.path.join(compressed_videos_segments_dir, resolution_string, str(fps), str(bitrate))
                os.makedirs(compressed_videos_segments_setting_dir, exist_ok=True)

                for flight_name in os.listdir(compressed_videos_setting_dir):
                    cmd = software_commands.split_video_fixed_time(
                        input_path=os.path.join(compressed_videos_setting_dir, flight_name),
                        time_length=time_length,
                        output_dir=compressed_videos_segments_setting_dir
                    )

                    # Execute
                    subprocess.run(shlex.split(cmd))


    # Saving Scores
    # Loading CONVIQT Model
    CONVIQT = quality_metrics.CONVIQT()

    def save_scores(videos_dir, quality_scores_dir, filename, replace=False):
        if os.path.exists(os.path.join(quality_scores_dir, filename[:-4]+".npy")) == False or replace == True:
            quality = CONVIQT.compute_quality(os.path.join(videos_dir, filename))
            np.save(os.path.join(quality_scores_dir, filename[:-4]+".npy"), quality)


    # Calculating Scores
    quality_scores_dir = "/home/krishnasrikardurbha/Desktop/Dynamic-Frame-Rate/dataset/simulations/gop_size={}/compressed_videos_segments_quality_scores".format(int(gop_size))

    for resolution in [(1920,1080), (1280,720)]:
        resolution_string = "{}x{}".format(resolution[0], resolution[1])
        for fps in [30,20,10]:
            for bitrate in [4, 3.5, 3, 2.75, 2.5, 2.25, 2, 1.75, 1.5, 1.25, 1, 0.75, 0.5, 0.25]:
                # For each compressed video
                compressed_videos_segments_setting_dir = os.path.join(compressed_videos_segments_dir, resolution_string, str(fps), str(bitrate))
                quality_scores_setting_dir = os.path.join(quality_scores_dir, resolution_string, str(fps), str(bitrate))
                os.makedirs(quality_scores_setting_dir, exist_ok=True)

                for flight_name in tqdm(os.listdir(compressed_videos_segments_setting_dir)):
                    save_scores(compressed_videos_segments_setting_dir, quality_scores_setting_dir, flight_name)
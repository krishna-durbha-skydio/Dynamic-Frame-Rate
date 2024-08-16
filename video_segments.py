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
streamed_videos_dir = "/home/krishnasrikardurbha/Desktop/Dynamic-Frame-Rate/dataset/human_study/streamed_videos"
streamed_videos_quality_scores_dir = "/home/krishnasrikardurbha/Desktop/Dynamic-Frame-Rate/dataset/human_study/streamed_videos_quality_scores"


# Loading CONVIQT Model
CONVIQT = quality_metrics.CONVIQT()

# Function to save scores
def save_scores(videos_dir, quality_scores_dir, filename, replace=False):
    if os.path.exists(os.path.join(quality_scores_dir, os.path.splitext(filename)[0] + ".npy")) == False or replace == True:
        quality = CONVIQT.compute_quality(os.path.join(videos_dir, filename))
        np.save(os.path.join(quality_scores_dir, filename[:-4]+".npy"), quality)


# Calculating quality of stream videos i.e entire flights
for video_file in tqdm(os.listdir(streamed_videos_dir)):
    save_scores(streamed_videos_dir, streamed_videos_quality_scores_dir, video_file)
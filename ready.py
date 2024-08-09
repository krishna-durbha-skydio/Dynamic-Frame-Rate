# Importing Libraries
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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

# Calculating stream videos stats
for i in range(len(os.listdir(streamed_videos_dir))):
    video_file = "flight{}.mp4".format(i+1)
    print (video_file)
    stats = statistics.get_statistics(
        video_path=os.path.join(streamed_videos_dir,video_file),
        quality_dir=None
    )
    print (stats[0], np.round(stats[1]), np.round(stats[2], decimals=2))
    print ()
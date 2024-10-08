import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

import os, sys, warnings
warnings.filterwarnings("ignore")
import functions.software_commands as software_commands
import subprocess, shlex


def pict_type_info(
    video_path:str
):
    # Execute Command
    cmd = "ffprobe -v error -select_streams v:0 -show_entries frame=pkt_pts_time,pkt_size,pict_type -of csv=p=0 {}".format(video_path)
    Output = subprocess.getoutput(cmd)

    # Read Output
    temp = Output.split("\n")
    Output = []
    for i in range(len(temp)):
        if temp[i].__contains__("Could not find ref with POC") or temp[i].__contains__("Last message repeated"):
            continue
        Output.append(temp[i].split(","))

    Output = np.asarray(Output)

    presentation_times = Output[:,0].astype("float")
    bits = Output[:,1].astype(int) * 8
    frame_type = Output[:,2]

    return frame_type, presentation_times, bits


frame_type, presentation_times, bits = pict_type_info(video_path="/home/krishnasrikardurbha/Desktop/Dynamic-Frame-Rate/dataset/gop_size=10/compressed_videos/1920x1080/20/3/mode3_1.mp4")
N = len(presentation_times)//4 + 5

frame_type = frame_type[N:N+30]
presentation_times = presentation_times[N:N+30]
bits = bits[N:N+30]

# Plotting
plt.figure(figsize=(10,6))
plt.ylabel("Bitrate")
plt.xlabel('Presentation Time')
plt.grid()

# Plot I-frames
mask = np.where(frame_type == "I")
plt.stem(presentation_times[mask], bits[mask]/1e6, label="I-frames", markerfmt="r.")

# Plot P-frames
mask = np.where(frame_type == "P")
plt.stem(presentation_times[mask], bits[mask]/1e6, label="P-frames", markerfmt="b.")

# Save
plt.legend()
plt.savefig("{}.png".format("flight"))

for i in range(0,len(frame_type),10):
    print (bits[i]/1e6, np.mean(bits[i+1:i+10])/1e6, np.sum(bits[i+1:i+10])/1e6, np.sum(bits[i:i+10])/1e6, 3/3)
print ()
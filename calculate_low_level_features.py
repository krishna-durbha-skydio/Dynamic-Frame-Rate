"""
Calculating SI-TI of uncompressed videos
"""
# Importing Libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import os, sys, warnings
warnings.filterwarnings("ignore")
import subprocess, shlex

# Calculating SITI features using executable
def calculate_SITI(
    input_video_path:str
):
    """
    Args:
        input_video_path (str): Input Video Path.
    """

    # Command
    cmd = "/home/krishnasrikardurbha/Desktop/SITI/src/SITI/siti -i {}".format(input_video_path)

    # GetOutput
    subprocess.run(shlex.split(cmd))
    assert False, ""
    output = subprocess.getoutput(cmd)

    return output

# Convert Logs to csv
def logs_2_csv(
    output:str,
    csv_path:str
):
    """
    Args:
        output (str): Output of calculate_SITI
        csv_path (str): Path to csv file
    """
    # Post-processing output
    output = output.split("\n")

    # Data
    data = []
    for i in range(len(output)):
        if i==0 or i==len(output)-1:
            continue
        s = output[i]
        s = s.split(",")

        if len(s) == 5:
            data.append(s)

    # Creating and Saving a dataframe
    df = pd.DataFrame(data = np.asarray(data), columns = ["frame_number", "meanSI", "stdSI", "meanTI", "stdTI"])
    df.to_csv(csv_path, index=False)


# for filename in os.listdir("dataset/stored_videos"):
#     output = calculate_SITI(input_video_path="dataset/stored_videos/{}".format(filename))
#     logs_2_csv(output, "dataset/features_temp/{}.csv".format(os.path.splitext(filename)[0]))

res_3840p = "/home/krishnasrikardurbha/Desktop/Dynamic-Frame-Rate/dataset/stored_videos/mode0_1.mp4"
res_1080p = "/home/krishnasrikardurbha/Desktop/Dynamic-Frame-Rate/dataset/gop_size=30/compressed_videos/1920x1080/30/3/mode0_1.mp4"
calculate_SITI(input_video_path=res_1080p)
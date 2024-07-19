
import os,pathlib,sys,warnings
warnings.filterwarnings('ignore')
sys.path.append("/home/krishnasrikardurbha/Desktop/Dynamic-Frame-Rate")
import functions.utils as utils
import functions.software_commands as software_commands
import subprocess, shlex

# Paths
reference_path = "/home/krishnasrikardurbha/Desktop/Dynamic-Frame-Rate/dataset/Examples/subject_cam_1/S1000103.mp4"
distorded_path = "/home/krishnasrikardurbha/Desktop/Dynamic-Frame-Rate/dataset/Examples/subject_cam_1/stream_1716504234206036_bbe9fac15d3f44edb2923ca04b449c17.mp4"

last_reference_path =  "/home/krishnasrikardurbha/Desktop/Dynamic-Frame-Rate/dataset/Examples/subject_cam_1/last_S1000103.mp4"
last_distorded_path = "/home/krishnasrikardurbha/Desktop/Dynamic-Frame-Rate/dataset/Examples/subject_cam_1/last_stream_1716504234206036_bbe9fac15d3f44edb2923ca04b449c17.mp4"


# Reverse
# cmd = "ffmpeg -sseof -5 -i {} -c copy {}".format(reference_path, last_reference_path)
# subprocess.run(shlex.split(cmd))
# print ("-"*1000)

# cmd = "ffmpeg -sseof -5 -i {} -c copy {}".format(distorded_path, last_distorded_path)
# subprocess.run(shlex.split(cmd))
# print ("-"*1000)


# Frame Comparisions
# cmd = "ffmpeg -i {} -vf fps=30 -threads 8 /home/krishnasrikardurbha/Desktop/Dynamic-Frame-Rate/dataset/temp/Images/reference/%d.png".format(last_reference_path)
# subprocess.run(shlex.split(cmd))
# print ("-"*1000)

# cmd = "ffmpeg -i {} -vf fps=30 -threads 8 /home/krishnasrikardurbha/Desktop/Dynamic-Frame-Rate/dataset/temp/Images/distorted/%d.png".format(last_distorded_path)
# subprocess.run(shlex.split(cmd))


# Software Commands
cmd = software_commands.get_metadata(distorded_path)
subprocess.run(shlex.split(cmd))
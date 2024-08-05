# Importing Libraries
import numpy as np
import matplotlib.pyplot as plt

import os,pathlib,sys,warnings
warnings.filterwarnings('ignore')
sys.path.append("/home/krishnasrikardurbha/Desktop/Dynamic-Frame-Rate")
import subprocess, shlex
import defaults


def split_video_fixed_time(
	input_path:str,
	time_length:float,
	output_dir:str
):
	"""
	Splitting video into multiple parts with exactly same amount of time.

	Args:
		input_path (str): Path to input video.
		time_length (float): Time length (in seconds) of each part of split.
		output_dir (str): Directory to save parts of videos.
	"""
	# File
	filename, ext = os.path.splitext(os.path.basename(input_path))
	
	# Assertions
	assert ext != ".yuv", "Invalid input video format i.e .yuv file."
	os.makedirs(output_dir, exist_ok=True)

	# Command
	cmd = defaults.ffmpeg_path
	cmd_split = "-i {} -acodec copy -f segment -segment_time {} -vcodec copy -reset_timestamps 1 -map 0 {}/{}_%d{}".format(input_path, time_length, output_dir, filename, ext)

	cmd = " ".join([cmd, cmd_split])
	
	return cmd


def get_metadata(
	input_path:str
):
	"""
	Get video metadata

	Args:
		input_path (str): Path to input video.
	"""
	cmd = defaults.ffprobe_path
	# cmd_stats = "-v error -show_format -show_streams {}".format(input_path)
	# cmd_stats = "-v error -hide_banner -select_streams v:0 -show_packets {}".format(input_path)
	cmd_stats = "-v error -select_streams v:0 -show_entries stream=width,height,bit_rate,avg_frame_rate,duration -of csv {}".format(input_path)

	# Final Command
	cmd = " ".join([cmd, cmd_stats])

	return cmd


def compress_video(
	input_path:str,
	output_resolution:tuple,
	output_bitrate:float,
	output_fps:float,
	output_gop_size:int,
	output_dir:str,
	threads:int
):
	"""
	Splitting video into multiple parts with exactly same amount of time.

	Args:
		input_path (str): Path to input video.
		output_resolution (tuple): Output resolution.
		output_bitrate (float): Output bitrate in (Mbps).
		output_fps (float): Output fps.
		output_dir (str): Directory to save parts of videos.
		output_gop_size (int): GoP size of output video.
		threads (int): No.of threads used for compression.
	"""
	# File
	filename, ext = os.path.splitext(os.path.basename(input_path))
	
	# Assertions
	assert ext != "yuv", "Invalid input video format i.e .yuv file."
	os.makedirs(output_dir, exist_ok=True)

	# Command
	cmd = defaults.ffmpeg_path

	# Input File
	cmd_input = "-i {}".format(input_path)
	
	# Codec and Settings
	cmd_codec_settings = "-codec:v libx265 -profile:v main -x265-params level-idc=50:keyint={} -bf 0".format(output_gop_size)
	cmd_resolution = "-vf 'scale={}x{}:flags=lanczos'".format(output_resolution[0], output_resolution[1])
	
	# Constant Bitrate and Constant Frame-Rate
	bitrate = output_bitrate * 1000 # (Converting to kbps)
	cmd_bitrate = "-r {} -b:v {}k -minrate {}k -maxrate {}k -bufsize {}k".format(output_fps, bitrate, bitrate, bitrate, 2*bitrate)

	# Output File
	cmd_output = "-threads {} -y {}".format(threads, os.path.join(output_dir, filename + ext))

	# Final Command
	cmd = " ".join([cmd, cmd_input, cmd_codec_settings, cmd_resolution, cmd_bitrate, cmd_output])
	
	return cmd


def simulate_compress_video(
	input_path:str,
	video_codec:str,
	output_fps:float,
	output_bitrate:float,
	output_path:str,
	threads:int
):
	"""
	Splitting video into multiple parts with exactly same amount of time.

	Args:
		input_path (str): Path to input video.
		video_codec (str): Video codec used for compression.
		output_fps (float): Output fps.
		output_bitrate (float): Output bitrate in (Mbps).
		output_path (str): Path to save compressed video.
		threads (int): No.of threads used for compression.
	"""
	# Command
	cmd = defaults.ffmpeg_path

	# Input File
	cmd_input = "-i {}".format(input_path)
	
	# Fps, Codec and Resolution
	cmd_fps_codec_resolution = "-codec:v {}".format(video_codec)
	
	# Bitrate
	bitrate = int(output_bitrate * 1000) # (Converting to kbps)
	cmd_bitrate = "-r {} -b:v {}k -minrate {}k -maxrate {}k -bufsize {}k".format(output_fps, bitrate, bitrate, bitrate, bitrate)

	# Output File
	cmd_output = "-threads {} -y {}".format(threads, output_path)

	# Final Command
	cmd = " ".join([cmd, cmd_input, cmd_fps_codec_resolution, cmd_bitrate, cmd_output])
	
	return cmd
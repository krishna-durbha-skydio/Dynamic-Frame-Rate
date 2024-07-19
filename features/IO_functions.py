"""
Functions for IO operations
"""
# Importing Libraries
import numpy as np
import cv2

import os
import json

def read_rgb_video(video_path):
	"""
	Args:
		video_path (str): Video path.
	Returns:
		frames (np.array): Numpy array of frames.
	"""
	video = cv2.VideoCapture(video_path)
	success,image = video.read()

	frames = []
	while success:
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		frames.append(image)

		success,image = video.read()

	video.release()
	return np.array(frames, dtype=np.uint8)
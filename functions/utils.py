# Importing Libraries
import numpy as np
import cv2
from PIL import Image

import os,pathlib,sys,warnings
warnings.filterwarnings('ignore')
sys.path.append("/home/krishnasrikardurbha/Desktop/Dynamic-Frame-Rate")
os.environ["OPENCV_FFMPEG_READ_ATTEMPTS"] = "1000000"
from tqdm import tqdm
import contextlib
import joblib

# Allows to use tqdm when extracting features for multiple images in parallel.
@contextlib.contextmanager
def tqdm_joblib(tqdm_object):
	"""
	- Allows to use tqdm when extracting features for multiple images in parallel.
	- Useful when multi-threading on CPUs with joblib.
	- Context manager to patch joblib to report into tqdm progress bar given as argument
	"""
	class TqdmBatchCompletionCallback(joblib.parallel.BatchCompletionCallBack):
		def __call__(self, *args, **kwargs):
			tqdm_object.update(n=self.batch_size)
			return super().__call__(*args, **kwargs)

	old_batch_callback = joblib.parallel.BatchCompletionCallBack
	joblib.parallel.BatchCompletionCallBack = TqdmBatchCompletionCallback
	try:
		yield tqdm_object
	finally:
		joblib.parallel.BatchCompletionCallBack = old_batch_callback
		tqdm_object.close()


# Plot Frames
def plot_frames(frames, save_dir):
	for i in range(frames.shape[0]):
		img = frames[i]
		img = Image.fromarray(np.uint8(img))
		img.save(os.path.join(save_dir, str(i)+".png"))


# Extract Frames
def extract_frames(video_path):
	"""
	Args:
		video_path (string): Video path.
	Returns:
		frames (np.array): Numpy array of frames.
	"""
	video = cv2.VideoCapture(video_path)
	length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
	print (video, video_path, length)
	success,image = video.read()

	frames = []
	while success:
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		print (image.shape)
		frames.append(image)

		success,image = video.read()

	frames = np.asarray(frames)
	print (frames.shape)
	return frames


# Save Frames to Video
def save_video(frames,video_path):
	"""
	Args:
		frames (np.array): Numpy array of frames.
		video_path (string): Video path.
	"""
	size = frames.shape[1:3]
	frames = list(frames)

	video = cv2.VideoWriter(video_path,cv2.VideoWriter_fourcc(*'mp4v'), 24, (size[1], size[0]))
	for frame in frames:
		video.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
	video.release()
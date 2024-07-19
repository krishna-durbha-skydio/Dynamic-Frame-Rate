"""
No-Reference Quality Estimation
"""
# Importing Libraries
import numpy as np
import skvideo
import pickle
from PIL import Image
import torch
from torchvision import transforms

import os, pathlib, sys, warnings
sys.path.append("/home/krishnasrikardurbha/Desktop/Dynamic-Frame-Rate")
import CONVIQT.demo_score as demo_score
from CONVIQT.modules.network import get_network
from CONVIQT.modules.CONTRIQUE_model import CONTRIQUE_model
from CONVIQT.modules.GRUModel import GRUModel
from joblib import load
import cv2


class CONVIQT():
	def __init__(self,
		contrique_path:str = "/home/krishnasrikardurbha/Desktop/Dynamic-Frame-Rate/CONVIQT/models/CONTRIQUE_checkpoint25.tar",
		conviqt_path:str = "/home/krishnasrikardurbha/Desktop/Dynamic-Frame-Rate/CONVIQT/models/CONVIQT_checkpoint10.tar",
		regressor_path:str = "/home/krishnasrikardurbha/Desktop/Dynamic-Frame-Rate/CONVIQT/models/YouTube_UGC.save"
	):
		# Parameters
		self.num_frames = 8
		self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

		# Load CONTRIQUE Model
		encoder = get_network('resnet50', pretrained=False)
		model = CONTRIQUE_model(None, encoder, 2048)
		model.load_state_dict(torch.load(contrique_path, map_location=self.device.type))
		self.model = model.to(self.device)
		self.model.eval()

		# Load CONVIQT model
		temporal_model = GRUModel(c_in = 2048, hidden_size = 1024, projection_dim = 128, normalize = True, num_layers = 1)
		temporal_model.load_state_dict(torch.load(conviqt_path, map_location=self.device.type))
		self.temporal_model = temporal_model.to(self.device)
		self.temporal_model.eval()

		# Load Regressor Model
		self.regressor = pickle.load(open(regressor_path, 'rb'))
		

	# Extract Frames
	def extract_frames(self, video_path):
		"""
		Args:
			video_path (string): Video path.
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

		return np.array(frames)
		
	
	def compute_quality(self, input_video_path):
		# load video
		video = self.extract_frames(input_video_path)
		T, height, width, C = video.shape
		
		# Define torch transform for 2 spatial scales
		transform = demo_score.torch_transform((height, width))
		
		# Define arrays to store frames
		frames = torch.zeros((T,3,height,width), dtype=torch.float16)
		frames_2 = torch.zeros((T,3,height// 2,width// 2), dtype=torch.float16)
		
		# Read every video frame
		for frame_ind in range(T):
			inp_frame = Image.fromarray(video[frame_ind])
			inp_frame, inp_frame_2 = transform(inp_frame)
			frames[frame_ind], frames_2[frame_ind] = inp_frame.type(torch.float16), inp_frame_2.type(torch.float16)
		
		# Convert to torch tensors
		if T < self.num_frames:
			batch_size = T
		else:
			batch_size = self.num_frames
		loader = demo_score.create_data_loader(frames, frames_2, batch_size)
		
		# Extract CONTRIQUE features
		video_feat = demo_score.extract_features(None, self.model, loader)

		
		# Extract CONVIQT features
		feat_frames = torch.from_numpy(video_feat[:,:2048])
		feat_frames_2 = torch.from_numpy(video_feat[:,2048:])
		loader = demo_score.create_data_loader(feat_frames, feat_frames_2, batch_size)
		video_feat = demo_score.extract_features_temporal(None, self.temporal_model, loader)
		
		# Predicting Score using regressor model
		score = self.regressor.predict(video_feat)[0]
		
		return score

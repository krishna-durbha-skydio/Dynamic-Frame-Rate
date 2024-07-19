"""
Calculating Low-Level features of uncompressed videos
"""
# Importing Libraires
import numpy as np
import pandas as pd

import os, sys
import time
import argparse
import features.GLCM as GLCM
import features.TC as TC
import features.SI as SI
import features.TI as TI
import features.CF as CF
import features.CI as CI
import features.CTI as CTI
import features.Texture_DCT as Texture_DCT
import features.IO_functions as IO_functions


# Fexture Extraction Modules
cf = CF.CF_Features()
ci = CI.CI_Features(rgb=True, WR=5)
cti = CTI.CTI_Features(rgb=True)
glcm = GLCM.GLCM_Features(descriptors=["contrast","correlation","energy","homogeneity"],angles=[0],distance=1,levels=256,block_size=(64,64),rgb=True)
tc = TC.TC_Features(rgb=True)
si = SI.SI_Features(rgb=True)
ti = TI.TI_Features(rgb=True)
texture_dct_features = Texture_DCT.Texture_DCT_Features(block_size=(32,32),rgb=True)


# Feature Extraction from Video
class generate_low_level_features():
	def __init__(self,
		video:np.array
	):
		# Video
		self.video = video

		# Features
		self.features = {}

		# Generate
		self.generate_glcm_features()
		self.generate_tc_features()
		self.generate_si_features()
		self.generate_ti_features()
		self.generate_cti_features()
		self.generate_cf_features()
		self.generate_ci_features()
		self.generate_texture_dct_features()


	def generate_low_level_features(self):
		return self.features


	def generate_glcm_features(self):
		# GLCM Features
		print ("GLCM Features:\n",flush=True)

		# Stats
		spatial_stats = np.sort(["mean", "std"])
		temporal_stats = np.sort(["mean", "std", "skew", "kurt"])
		stats = []
		for t in temporal_stats:
			for s in spatial_stats:
				stats.append([t,s])

		# Feature Names
		features_names = []
		for f in ["GLCM_contrast", "GLCM_correlation", "GLCM_energy", "GLCM_homogeneity"]:
			for t in temporal_stats:
				for s in spatial_stats:
					features_names.append(t+"_"+f+"_"+s)
		
		# Compute
		time_instant = time.time()
		_, features = glcm.compute_video_glcm_features(video=np.copy(self.video), stats=stats)
		compute_time = time.time() - time_instant

		# Assertions
		assert len(features_names) == features.shape[0], "Dimensions of frame features do not match."

		for i,name in enumerate(features_names):
			self.features[name] = features[i]
		self.features["GLCM_compute_time"] = np.round(compute_time, decimals=6)


	def generate_tc_features(self):
		# TC Features
		print ("TC Features:\n",flush=True)

		# Stats
		spatial_stats = np.sort(["mean", "std", "skew", "kurt"])
		temporal_stats = np.sort(["mean", "std"])
		stats = []
		for t in temporal_stats:
			for s in spatial_stats:
				stats.append([t,s])

		# Feature Names
		features_names = []
		for f in ["TC"]:
			for t in temporal_stats:
				for s in spatial_stats:
					features_names.append(t+"_"+f+"_"+s)

		# Compute
		time_instant = time.time()
		_, features = tc.compute_video_tc_features(video=np.copy(self.video), stats=stats)
		compute_time = time.time() - time_instant

		# Assertions
		assert len(features_names) == features.shape[0], "Dimensions of frame features do not match."

		for i,name in enumerate(features_names):
			self.features[name] = features[i]
		self.features["TC_compute_time"] = np.round(compute_time, decimals=6)

	
	def generate_si_features(self):
		# SI Features
		print ("SI Features:\n",flush=True)

		# Stats
		spatial_stats = np.sort(["mean", "std"])
		temporal_stats = np.sort(["mean", "std", "skew", "kurt"])
		stats = []
		for t in temporal_stats:
			for s in spatial_stats:
				stats.append([t,s])

		# Feature Names
		features_names = []
		for f in ["SI"]:
			for t in temporal_stats:
				for s in spatial_stats:
					features_names.append(t+"_"+f+"_"+s)

		# Compute
		time_instant = time.time()
		_, features = si.compute_video_spatial_information(video=np.copy(self.video), stats=stats)
		compute_time = time.time() - time_instant

		# Assertions
		assert len(features_names) == features.shape[0], "Dimensions of frame features do not match."

		for i,name in enumerate(features_names):
			self.features[name] = features[i]
		self.features["SI_compute_time"] = np.round(compute_time, decimals=6)


	def generate_ti_features(self):
		# TI Features
		print ("TI Features:\n",flush=True)

		# Stats
		spatial_stats = np.sort(["mean", "std"])
		temporal_stats = np.sort(["mean", "std", "skew", "kurt"])
		stats = []
		for t in temporal_stats:
			for s in spatial_stats:
				stats.append([t,s])

		# Feature Names
		features_names = []
		for f in ["TI"]:
			for t in temporal_stats:
				for s in spatial_stats:
					features_names.append(t+"_"+f+"_"+s)

		# Compute
		time_instant = time.time()
		_, features = ti.compute_video_temporal_information(video=np.copy(self.video), stats=stats)
		compute_time = time.time() - time_instant

		# Assertions
		assert len(features_names) == features.shape[0], "Dimensions of frame features do not match."

		for i,name in enumerate(features_names):
			self.features[name] = features[i]
		self.features["TI_compute_time"] = np.round(compute_time, decimals=6)


	def generate_cti_features(self):
		# CTI Features
		print ("CTI Features:\n",flush=True)

		# Stats
		spatial_stats = np.sort(["mean", "std"])
		temporal_stats = np.sort(["mean", "std", "skew", "kurt"])
		stats = []
		for t in temporal_stats:
			for s in spatial_stats:
				stats.append([t,s])

		# Feature Names
		features_names = []
		for f in ["CTI"]:
			for t in temporal_stats:
				for s in spatial_stats:
					features_names.append(t+"_"+f+"_"+s)

		# Compute
		time_instant = time.time()
		_, features = cti.compute_video_contrast_information(video=np.copy(self.video), stats=stats)
		compute_time = time.time() - time_instant

		# Assertions
		assert len(features_names) == features.shape[0], "Dimensions of frame features do not match."

		for i,name in enumerate(features_names):
			self.features[name] = features[i]
		self.features["CTI_compute_time"] = np.round(compute_time, decimals=6)


	def generate_cf_features(self):
		# CF Features
		print ("CF Features:\n",flush=True)

		# Stats
		temporal_stats = np.sort(["mean", "std", "skew", "kurt"])
		stats = temporal_stats

		# Feature Names
		features_names = []
		for f in ["CF"]:
			for t in temporal_stats:
				features_names.append(t+"_"+f)

		# Compute
		time_instant = time.time()
		_, features = cf.compute_video_colorfulness(video=np.copy(self.video), stats=stats)
		compute_time = time.time() - time_instant

		# Assertions
		assert len(features_names) == features.shape[0], "Dimensions of frame features do not match."

		for i,name in enumerate(features_names):
			self.features[name] = features[i]
		self.features["CF_compute_time"] = np.round(compute_time, decimals=6)


	def generate_ci_features(self):
		# CI Features
		print ("CI Features:\n",flush=True)

		# Stats
		spatial_stats = np.sort(["mean", "std"])
		temporal_stats = np.sort(["mean", "std", "skew", "kurt"])
		stats = []
		for t in temporal_stats:
			for s in spatial_stats:
				stats.append([t,s])

		# Feature Names
		features_names = []
		for f in ["CI_U"]:
			for t in temporal_stats:
				for s in spatial_stats:
					features_names.append(t+"_"+f+"_"+s)

		# Compute
		time_instant = time.time()
		_, features = ci.compute_video_chroma_information(video=np.copy(self.video), component="U", stats=stats)
		compute_time = time.time() - time_instant

		# Assertions
		assert len(features_names) == features.shape[0], "Dimensions of frame features do not match."

		for i,name in enumerate(features_names):
			self.features[name] = features[i]
		self.features["CI_U_compute_time"] = np.round(compute_time, decimals=6)

		# Feature Names
		features_names = []
		for f in ["CI_V"]:
			for t in temporal_stats:
				for s in spatial_stats:
					features_names.append(t+"_"+f+"_"+s)

		# Compute
		time_instant = time.time()
		_, features = ci.compute_video_chroma_information(video=np.copy(self.video), component="V", stats=stats)
		compute_time = time.time() - time_instant

		# Assertions
		assert len(features_names) == features.shape[0], "Dimensions of frame features do not match."

		for i,name in enumerate(features_names):
			self.features[name] = features[i]
		self.features["CI_V_compute_time"] = np.round(compute_time, decimals=6)
		

	def generate_texture_dct_features(self):
		# Texture-DCT Features
		print ("Texture-DCT Features:\n",flush=True)

		# Feature Names
		features_names = ["mean_E_Y", "mean_h_Y", "mean_L_Y"]

		# Compute
		time_instant = time.time()
		_, features = texture_dct_features.compute_video_features(video=np.copy(self.video), component="Y")
		compute_time = time.time() - time_instant

		# Assertions
		assert len(features_names) == features.shape[0], "Dimensions of frame features do not match."

		for i,name in enumerate(features_names):
			self.features[name] = features[i]
		self.features["EhL_Y_compute_time"] = np.round(compute_time, decimals=6)


		# Feature Names
		features_names = ["mean_E_U", "mean_h_U", "mean_L_U"]

		# Compute
		time_instant = time.time()
		_, features = texture_dct_features.compute_video_features(np.copy(self.video), component="U")
		compute_time = time.time() - time_instant

		# Assertions
		assert len(features_names) == features.shape[0], "Dimensions of frame features do not match."

		for i,name in enumerate(features_names):
			self.features[name] = features[i]
		self.features["EhL_U_compute_time"] = np.round(compute_time, decimals=6)


		# Feature Names
		features_names = ["mean_E_V", "mean_h_V", "mean_L_V"]

		# Compute
		time_instant = time.time()
		_, features = texture_dct_features.compute_video_features(video=np.copy(self.video), component="V")
		compute_time = time.time() - time_instant

		# Assertions
		assert len(features_names) == features.shape[0], "Dimensions of frame features do not match."

		for i,name in enumerate(features_names):
			self.features[name] = features[i]
		self.features["EhL_V_compute_time"] = np.round(compute_time, decimals=6)


def main(args):	
	# Path Assertions
	assert os.path.exists(args.videos_path), "Invalid path to videos"
	assert os.path.exists(args.features_information_path), "Invalid path to save features"

	# Filenames
	filenames = os.listdir(args.videos_path)
	
	# Save Path
	save_path = os.path.join(args.features_information_path, "features.csv")
	Feature_Info = pd.DataFrame()

	for filename in sorted(filenames):
		print ("-"*75 + "\n" + filename[:-4] + "\n" + "-"*75, flush=True)

		# Reading Video 
		file_path = os.path.join(args.videos_path, filename)
		video = IO_functions.read_rgb_video(file_path)
		
		# Trimming Video
		num_frames = video.shape[0]		
		if num_frames < 5:
			continue
		elif num_frames == 5:
			None
		elif num_frames == 6:
			video = video[1:]
		else:
			video = video[int(num_frames * 0.25): int(num_frames * 0.25) + 5]

		# Calculating Low-Level Features
		F = generate_low_level_features(video)
		data = F.generate_low_level_features()

		# Saving computed features
		data = pd.DataFrame([{**{"filename":filename[:-4]}, **data}])
		Feature_Info = pd.concat([Feature_Info, data], ignore_index=True)
		Feature_Info.to_csv(save_path, index=False)

	Feature_Info.to_csv(save_path, index=False)



# Calling Main function
if __name__ == '__main__':
	root_dir = os.path.dirname(os.path.realpath(__file__))

	# Get Arguments
	parser = argparse.ArgumentParser(description='Estimating compressed video information')

	# Dataset Paths
	parser.add_argument('--videos_path', default='/home/krishnasrikardurbha/Desktop/Dynamic-Frame-Rate/dataset/video_segments/streamed_videos', help='Path to dataset.')
	parser.add_argument('--features_information_path', default='/home/krishnasrikardurbha/Desktop/Dynamic-Frame-Rate/dataset/features', help='Path to information of features extracted from videos.')
	
	# Main Path
	parser.add_argument('--main_path', default='/home/krishnasrikardurbha/Desktop/Dynamic-Frame-Rate', type=str, help='Path to main folder')

	# Parse Arguments
	args = parser.parse_args()

	main(args)
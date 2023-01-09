import os
import cv2
import requests
import json

class CheckCamOnline:
	def __init__(self, site_base_url):
		self.site_base_url = site_base_url
		self.cameras_info = self.retrieve_save_cam_map()
		self.max_cameras = len(self.cameras_info)
		

	def retrieve_save_cam_map(self):
		print("Sending GET request to site...")
		response = requests.get(self.site_base_url)
		html = response.text.replace("'", "\"")
		html_sub = html[response.text.find("camMarker"):]
		camMarkerString = html_sub[html_sub.find("["):html_sub.find("]")]
		json_str = camMarkerString + "]"
		camMarkerDict = json.loads(json_str)

		if not os.path.isdir("data/"):
		    os.makedirs("data/")

		with open('data/cam_data.json', 'w') as f:
			json.dump(camMarkerDict, f)
		print("Saved camera data info JSON file.\n")
		return self.get_cam_name_map()


	def get_cam_name_map(self):
		print("Loading camera info JSON file.")
		camMarkerDict = None
		with open('data/cam_data.json', 'r') as f:
			camMarkerDict = json.load(f)
		print("Sucessfully loaded camera info dict.\n")
		return camMarkerDict


	def get_all_online_cams(self):
		print("Checking available cameras...")
		available_streams = []
		for idx, cam in enumerate(self.cameras_info):
			cap = cv2.VideoCapture(cam['hls'])
			if (cap.isOpened() == True):
				print(f"Camera {cam['description']} found.")
				available_streams.append(cam)
			else: 
				print(f"Camera {cam['description']} NOT found. (down for maintainence, probably)")
		print("Finished checking cameras.")
		print("\tOnline: \t" + len(available_streams))
		print("\tOffline:\t" + str(len(self.cameras_info)-len(available_streams)) + "\n")
		return availible_streams

	
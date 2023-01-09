import cv2
import sys
from check_cam_online import *
import random
from threaded_camera import ThreadedCamera
import time
import yolov5.detect as yolo
from os import listdir
from os.path import isfile, join
import shutil

CLASS_MAP = {'1': 'bicycle', '2': 'car', '3': 'motorcycle', '5': 'bus'}

if __name__ == '__main__':
	opts = yolo.parse_opt()

	SITE_URL = "https://trafficvid.lexingtonky.gov/publicmap/"
	# CAM_URL_FORMATTED = "https://5723acd20ffa9.streamlock.net:1935/lexington-live/lex-cam-{}.stream/playlist.m3u8"

	cam_check = CheckCamOnline(SITE_URL) # Initializing will download the list of cams and check which are online

	for stream in cam_check.cameras_info:
		print("Reading: " + stream['description'])
		# print(stream['hls'])

		cap = cv2.VideoCapture(stream['hls'])
		if cap.isOpened() == False:
			continue
			# print('Unable to open URL, re-rolling in 2 secs.')
			# time.sleep(2)
			# random_stream = random.choice(cam_check.cameras_info)
			# print(random_stream['description'])
			# print(random_stream['hls'])
		
		_, image = cap.read()
		path = os.path.join("images", stream['description'] + ".jpg").replace("/", "+")
		save_success = cv2.imwrite(path, image)
		if save_success:
			print("Saved: " + path)
		else:
			print("Failed to save: " + path)

	random_stream = random.choice(cam_check.cameras_info)
	cap = cv2.VideoCapture(random_stream['hls'])
	print(random_stream)
	threaded_camera = ThreadedCamera(cap, random_stream['description'])
	while True:
		try:
			threaded_camera.show_frame()
		except AttributeError:
			pass

	# python .\stream.py --weights yolov5x.pt --classes 1 2 3 5 --device 0 --line-thickness 1 --conf-thres 0.50 --save-txt
	#  python .\yolov5\detect.py --classes 1 2 3 5 --weights yolov5x.pt --source https://5723acd20ffa9.streamlock.net:1935/lexington-live/lex-cam-050.stream/playlist.m3u8
	
	# see options in yolov5/detect.py
	# this is using data/coco128.yml, class 2 = car, 5 = bus
		
	opts.source = './images' #path
	s = yolo.main(opts)
	label_dir = s[s.find("to")+3:]
	if len(os.listdir(label_dir)) > 0:
		for label in os.listdir(label_dir):
			label_path = os.path.join(label_dir, label)
			name = label.replace("+", "/")[:-4]
			with open(label_path, 'r') as f:
				lines=f.read().splitlines()
				print("Traffic Density @ "+ name + ": " + str(len(lines)) + " vehicle(s).")
				# add vehicle types here
	run_dir = label_dir[:-6]
	shutil.rmtree(run_dir)
	


from threading import Thread
import time, cv2

class ThreadedCamera(object):
	def __init__(self, stream, window_name):
		self.capture = stream
		self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 2)
		self.window_name = window_name
	   
		# FPS = 1/X
		# X = desired FPS
		self.FPS = 1/30
		self.FPS_MS = int(self.FPS * 1000)
		
		# Start frame retrieval thread
		self.thread = Thread(target=self.update, args=())
		self.thread.daemon = True
		self.thread.start()
		
	def update(self):
		while True:
			if self.capture.isOpened():
				(self.status, self.frame) = self.capture.read()
			time.sleep(self.FPS)
			
	def show_frame(self):
		cv2.imshow(self.window_name, self.frame)
		cv2.waitKey(self.FPS_MS)

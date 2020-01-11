import cv2
import numpy as np
from app.config import video_src


"""
An example class of how to implement openCV and how it can communicate with the
wxPython layer.
"""

class WebcamFeed(object):

	""" Starts a webcam feed """
	def __init__(self):

		self.webcam = cv2.VideoCapture(video_src)

	def has_webcam(self):
		_, frame = self.webcam.read()
		if(isinstance(frame, np.ndarray)):
			return True
		return False

	""" Retrieves a frame from the webcam and converts it to an RGB - Image """
	def get_image(self, w=None, h=None):
		_, frame = self.webcam.read()
		if w != None and h != None:
			frame = cv2.resize(frame, (w, h))
		return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

	""" Retrieves a frame to get the size """
	def size(self):
		_, frame = self.webcam.read()
		return frame.shape[:2]
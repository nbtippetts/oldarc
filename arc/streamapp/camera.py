from imutils.video import VideoStream
from django.conf import settings
import threading
import argparse
import datetime
import imutils
import time
import cv2


class VideoCamera(object):
	def __init__(self):
		print('Starting webcam video.')
		self.video = cv2.VideoCapture(0)

	def __del__(self):
		print('Shutting down webcam video.')
		self.video.release()

	def get_frame(self):
		success, image = self.video.read()
		# We are using Motion JPEG, but OpenCV defaults to capture raw images,
		# so we must encode it into JPEG in order to correctly display the
		# video stream.
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		frame_flip = cv2.flip(image,1)
		ret, jpeg = cv2.imencode('.jpg', frame_flip)
		return jpeg.tobytes()

class CaptureFrame(object):
	def __init__(self):
		self.video = cv2.VideoCapture(0)

	def __del__(self):
		self.video.release()

	def get_frame(self):
		success, image = self.video.read()
		cv2.imshow("Capturing",image)
		key = cv2.waitKey(1)
		write_image = cv2.imwrite("/static/images/room.jpg",image)
		print(write_image)
		return write_image

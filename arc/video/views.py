import logging
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
# from picamera import PiCamera
from time import sleep 

def video(request):
	# if request.method == 'POST':
	# 	duration = request.POST.get('duration')
	# 	with PiCamera() as camera:
	# 		camera.resolution = (640, 480)
	# 		camera.start_preview()
	# 		sleep(2)
	# 		sleep(int(duration))
	# 		camera.stop_preview()
	return render(request, 'video/video.html')


# def screenshot(request):
	# if request.method == 'POST':
	# 	with PiCamera() as camera:
	# 		camera.resolution = (640, 480)
	# 		camera.start_preview()
	# 		sleep(2)
	# 		camera.capture('/home/pi/Desktop/image.jpg')
	# 		camera.stop_preview()
	# return render(request, 'video/video.html')
	# camera.start_preview()
	# for i in range(5):
	# 	sleep(5)
	# 	camera.capture('/home/pi/Desktop/image%s.jpg' % i)
	# camera.stop_preview()

# def record():
# 	camera.start_preview()
# 	camera.start_recording('/home/pi/Desktop/video.h264')
# 	sleep(5)
# 	camera.stop_recording()
# 	camera.stop_preview()

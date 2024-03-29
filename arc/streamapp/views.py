from django.shortcuts import render
from django.http.response import StreamingHttpResponse
# from streamapp.camera import VideoCamera

def index(request):
	return render(request, 'video_view.html')


def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def video_feed(request):
	try:
		return #StreamingHttpResponse(gen(VideoCamera()),content_type='multipart/x-mixed-replace; boundary=frame')
	except HttpResponseServerError as e:
		print("aborted")

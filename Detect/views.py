
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from django.db.models import *
from datetime import datetime
from .models import Detections
import sys
from io import StringIO
from Detect.yolo1 import *
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
from django.shortcuts import render


@gzip.gzip_page
def Dect(request): 
    return render(request, 'index.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def live_feed(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        pass


# views.py


def detection(request):
    detections = Detections.objects.all()
    output = StringIO()
    sys.stdout = output  # Redirect the standard output to the StringIO object

    
    # Your console code here
    
    print("Tracking Objects")
    obj = VideoCamera()
    # print(obj.text)
    
    # for mhd in obj.outputLayer: 
    #     print(mhd) 
    # print(obj)
    # # Rest of your code...

        
    print("Hello, console!" )
    # Get the console output as a string
    console_output = output.getvalue()

    # Reset the standard output
    sys.stdout = sys.__stdout__

    # Pass the console output to the template
    context = {
        'console_output': console_output,
        'detections': detections,
        
    }           
    
    return render(request, 'detections.html', context)


def Data(request):
    detections = Detections.objects.all()
    # detections = [
    #    
    # ]

    # Parse timestamps and sort detections by hour
    for dta in detections:
        # Adjust this based on your timestamp format
        dta['timestamp'] = datetime.strptime(
            dta['timestamp'], '%Y-%m-%d %H:%M:%S')
    detections.sort(key=lambda dta: dta['timestamp'].hour)

    return render(request, 'chart.html', {'detections': detections})


class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        return ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    def get_providers(self):
        return ['Early Morning', 'Morning', 'Afternoon', 'Evening', 'Night', 'Midnight']


    def get_data(self):
        data = []
        labels = self.get_labels()
        detections = Detections.objects.annotate(count=Count('pk'))

        # Group data by time range
        grouped_data = {label: {} for label in labels}

        for detection in detections:
            day_of_week = detection.get_day_of_week()
            day_group = grouped_data[day_of_week]

            # Group data by time range
            time_range = detection.get_time_range()
            time_group = day_group.setdefault(
                time_range, {label: 0 for label in labels})
            time_group[day_of_week] += detection.count

        # Prepare data for Chart.js
        for label in labels:
            chart_data = []

            # Group data by days
            for time_group in grouped_data[label].values():
                chart_data.append(sum(time_group[label] for label in labels))

            data.append(chart_data)

        return data
    
    def get_options(self):
        return {}


line_chart = TemplateView.as_view(template_name='line_chart.html')
line_chart_json = LineChartJSONView.as_view()


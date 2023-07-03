import cv2
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
from .yolo1 import *
from io import StringIO
import sys
from .models import Detections
from datetime import datetime
from django.db.models import Count
from chartjs.views.lines import BaseLineChartView
from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from user.models import Profile as Profiles


@login_required(login_url='Login')
def intro(request):
    profiles = Profiles.objects.all()
    context = {
        "profiles": profiles,
    }
    return render(request, 'pages/intropage.html', context)


@login_required(login_url='Login')
def Home(request):
    profiles=Profiles.objects.all()
    context={
        "profiles":profiles
    }
    return render(request, 'pages/index.html', context)


@login_required(login_url='Login')
def Site(request):
    profiles=Profiles.objects.all()
    context={
        "profiles":profiles,
    }
    return render(request, 'pages/site.html', context)



@login_required(login_url="Login")
def Reports(request):
    profiles = Profiles.objects.all()
    context = {
        "profiles": profiles,
    }
    return render(request, "pages/reports.html", context)


@gzip.gzip_page
def Hmmm(request):
    return render(request, 'Live_stream.html')


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

    print("Hello, console!")

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
        """Return 7 labels for the x-axis."""
        return ['Early Morning', 'Morning', 'Afternoon', 'Evening', 'Night', 'Midnight',]

    def get_providers(self):
        """Return names of datasets."""
        # return ["Central", "Eastside", "Westside"]
        return ["Count_str", "text"]

    def get_data(self):
        """Return 3 datasets to plot."""
        data = []
        detections = Detections.objects.annotate(count=Count('pk'))
        grouped_data = {}

        for detection in detections:
            time_range = detection.get_time_range()
            grouped_data[time_range] = grouped_data.get(
                time_range, 0) + detection.count

        for label in self.get_labels():
            data.append(grouped_data.get(label, 0))

        return [data]
    # def get_data(self):
    #     data = []
    #     labels = self.get_labels()
    #     detections = Detections.objects.annotate(count=Count('pk'))

    #     # Group data by time range
    #     grouped_data = {label: {} for label in labels}

    #     for detection in detections:
    #         time_range = detection.get_time_range()
    #         time_group = grouped_data[time_range]

    #         # Group data by day
    #         day = detection.get_date()
    #         day_group = time_group.setdefault(
    #             day, {label: 0 for label in labels})
    #         day_group[time_range] += detection.count

    #     # Prepare data for Chart.js
    #     for label in labels:
    #         chart_data = []

    #         # Group data by days, weeks, months, or years
    #         for time_group in grouped_data[label].values():
    #             chart_data.append(sum(time_group[label] for label in labels))

    #         data.append(chart_data)

    #     return data

    # def get_options(self):
    #     return {}

    # def get_providers(self):
    #     return self.get_labels()


line_chart = TemplateView.as_view(template_name='line_chart.html')
line_chart_json = LineChartJSONView.as_view()

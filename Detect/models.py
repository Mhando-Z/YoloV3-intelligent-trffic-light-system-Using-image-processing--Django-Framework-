

from django.db import models

class Detections(models.Model):
    # tracking_objects = models.JSONField()
    text = models.CharField(max_length=200, blank=True, null=True)
    count_str = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True) 
    

    def get_time_range(self):
        hour = self.timestamp.hour

        if 4 <= hour < 6:
            return 'Early Morning'
        elif 6 <= hour < 12:
            return 'Morning'
        elif 12 <= hour < 16:
            return 'Afternoon'
        elif 16 <= hour < 19:
            return 'Evening'
        elif 19 <= hour <= 23:
            return 'Night'
        elif 0 <= hour < 4:
            return 'Midnight'
        else:
            return 'Invalid'


    def get_day_of_week(self):
        return self.timestamp.strftime('%A')

    def get_week(self):
        return self.timestamp.strftime('%Y-%U')

    def get_month(self):
        return self.timestamp.strftime('%Y-%m')

    def get_year(self):
        return self.timestamp.year
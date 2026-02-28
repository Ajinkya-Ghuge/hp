from django.db import models

class Submission(models.Model):
    answer = models.TextField()
    keystroke_data = models.JSONField()
    start_time = models.BigIntegerField()
    end_time = models.BigIntegerField()
    risk_score = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
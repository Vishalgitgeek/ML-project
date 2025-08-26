from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class BatchPrediction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    filename = models.CharField(max_length=255)
    upload_time = models.DateTimeField(auto_now_add=True)
    total_records = models.IntegerField()
    processed_records = models.IntegerField(default=0)
    failed_records = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=[
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ], default='PROCESSING')
    
    def __str__(self):
        return f"Batch {self.filename} - {self.status}"


class PredictionRecord(models.Model):
    batch = models.ForeignKey(BatchPrediction, on_delete=models.CASCADE, related_name='predictions')
    row_number = models.IntegerField()
    
    # Input features
    gender = models.CharField(max_length=10)
    race_ethnicity = models.CharField(max_length=20)
    parental_level_of_education = models.CharField(max_length=50)
    lunch = models.CharField(max_length=20)
    test_preparation_course = models.CharField(max_length=20)
    reading_score = models.IntegerField()
    writing_score = models.IntegerField()
    
    # Output
    predicted_math_score = models.FloatField(null=True, blank=True)
    
    # Status
    is_successful = models.BooleanField(default=True)
    error_message = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Prediction {self.batch.filename} - Row {self.row_number}"


class SinglePrediction(models.Model):
    """Store individual predictions from the web form"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)  # For anonymous users
    
    # Input features
    gender = models.CharField(max_length=10)
    race_ethnicity = models.CharField(max_length=20)
    parental_level_of_education = models.CharField(max_length=50)
    lunch = models.CharField(max_length=20)
    test_preparation_course = models.CharField(max_length=20)
    reading_score = models.IntegerField()
    writing_score = models.IntegerField()
    
    # Output
    predicted_math_score = models.FloatField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Prediction: {self.predicted_math_score:.2f} at {self.created_at}"

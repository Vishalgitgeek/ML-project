from django.contrib import admin
from .models import BatchPrediction, PredictionRecord, SinglePrediction

# Register your models here.

@admin.register(BatchPrediction)
class BatchPredictionAdmin(admin.ModelAdmin):
    list_display = ['filename', 'user', 'status', 'total_records', 'processed_records', 'failed_records', 'upload_time']
    list_filter = ['status', 'upload_time']
    search_fields = ['filename', 'user__username']
    readonly_fields = ['id', 'upload_time']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

@admin.register(PredictionRecord)
class PredictionRecordAdmin(admin.ModelAdmin):
    list_display = ['batch', 'row_number', 'predicted_math_score', 'is_successful', 'created_at']
    list_filter = ['is_successful', 'created_at', 'gender', 'lunch']
    search_fields = ['batch__filename']
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('batch')

@admin.register(SinglePrediction)
class SinglePredictionAdmin(admin.ModelAdmin):
    list_display = ['user', 'predicted_math_score', 'reading_score', 'writing_score', 'created_at']
    list_filter = ['created_at', 'gender', 'lunch']
    search_fields = ['user__username']
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
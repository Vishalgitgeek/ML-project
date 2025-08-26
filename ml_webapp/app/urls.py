from django.urls import path
from . import views

urlpatterns = [
    # Single prediction
    path('', views.predict_view, name='index'),
    
    # Batch predictions
    path('batch/', views.batch_predict_view, name='batch_predict'),
    path('batch/result/<uuid:batch_id>/', views.batch_result_view, name='batch_result'),
    path('batch/download/<uuid:batch_id>/', views.download_batch_results, name='download_batch_results'),
    path('batch/status/<uuid:batch_id>/', views.ajax_batch_status, name='batch_status'),
    
    # History
    path('history/batch/', views.batch_history_view, name='batch_history'),
    path('history/predictions/', views.prediction_history_view, name='prediction_history'),
    
    # Utilities
    path('sample-csv/', views.sample_csv_download, name='sample_csv'),
]
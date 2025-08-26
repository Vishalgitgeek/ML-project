from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
import os, sys
from django.core.paginator import Paginator

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.pipeline.predict_pipeline import PredictPipeline

from src.pipeline.predict_pipeline import PredictPipeline
from .forms import PredictionForm, BatchPredictionForm
from .models import BatchPrediction, PredictionRecord, SinglePrediction
from .services import BatchPredictionService
import logging

logger = logging.getLogger(__name__)


# Create your views here.

# def predict_view(request):
#     # return HttpResponse("Hello, world")
#     return render(request, 'app/home.html')


from .forms import PredictionForm
from src.pipeline.predict_pipeline import PredictPipeline  

def predict_view(request):
    """Single prediction view"""
    prediction = None
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            try:
                input_data = {
                    'gender': [form.cleaned_data['gender']],
                    'race/ethnicity': [form.cleaned_data['race_ethnicity']],
                    'parental level of education': [form.cleaned_data['parental_level_of_education']],
                    'lunch': [form.cleaned_data['lunch']],
                    'test preparation course': [form.cleaned_data['test_preparation_course']],
                    'reading score': [form.cleaned_data['reading_score']],
                    'writing score': [form.cleaned_data['writing_score']]
                }
                
                pipeline = PredictPipeline()
                prediction = pipeline.predict(input_data)[0]
                
                # Store prediction in database
                SinglePrediction.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    session_key=request.session.session_key if not request.user.is_authenticated else None,
                    gender=form.cleaned_data['gender'],
                    race_ethnicity=form.cleaned_data['race_ethnicity'],
                    parental_level_of_education=form.cleaned_data['parental_level_of_education'],
                    lunch=form.cleaned_data['lunch'],
                    test_preparation_course=form.cleaned_data['test_preparation_course'],
                    reading_score=form.cleaned_data['reading_score'],
                    writing_score=form.cleaned_data['writing_score'],
                    predicted_math_score=float(prediction)
                )
                
                messages.success(request, f"Prediction successful! Math score: {prediction:.2f}")
                
            except Exception as e:
                messages.error(request, f"Error making prediction: {str(e)}")
                logger.error(f"Prediction error: {str(e)}")
    else:
        form = PredictionForm()
    
    return render(request, 'app/home.html', {'form': form, 'prediction': prediction})

def batch_predict_view(request):
    """Batch prediction view"""
    if request.method == 'POST':
        form = BatchPredictionForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                csv_file = form.cleaned_data['csv_file']
                filename = csv_file.name
                
                # Process the batch
                service = BatchPredictionService()
                batch = service.process_csv_file(
                    csv_file, 
                    filename, 
                    user=request.user if request.user.is_authenticated else None
                )
                
                messages.success(request, f"Batch processing completed! Batch ID: {batch.id}")
                return redirect('batch_result', batch_id=batch.id)
                
            except Exception as e:
                messages.error(request, f"Error processing batch: {str(e)}")
                logger.error(f"Batch processing error: {str(e)}")
    else:
        form = BatchPredictionForm()
    
    return render(request, 'app/batch_predict.html', {'form': form})

def batch_result_view(request, batch_id):
    """View batch prediction results"""
    batch = get_object_or_404(BatchPrediction, id=batch_id)
    
    # Get predictions with pagination
    predictions = batch.predictions.all().order_by('row_number')
    paginator = Paginator(predictions, 50)  # Show 50 predictions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get batch summary
    service = BatchPredictionService()
    summary = service.get_batch_summary(batch)
    
    context = {
        'batch': batch,
        'predictions': page_obj,
        'summary': summary,
        'page_obj': page_obj
    }
    
    return render(request, 'app/batch_result.html', context)

def download_batch_results(request, batch_id):
    """Download batch results as CSV"""
    batch = get_object_or_404(BatchPrediction, id=batch_id)
    
    try:
        service = BatchPredictionService()
        csv_content = service.generate_results_csv(batch)
        
        response = HttpResponse(csv_content, content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{batch.filename}_results.csv"'
        
        return response
        
    except Exception as e:
        messages.error(request, f"Error generating CSV: {str(e)}")
        return redirect('batch_result', batch_id=batch_id)

def batch_history_view(request):
    """View batch prediction history"""
    if request.user.is_authenticated:
        batches = BatchPrediction.objects.filter(user=request.user).order_by('-upload_time')
    else:
        batches = BatchPrediction.objects.filter(user=None).order_by('-upload_time')[:10]  # Last 10 for anonymous users
    
    paginator = Paginator(batches, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'app/batch_history.html', {'page_obj': page_obj})

def prediction_history_view(request):
    """View single prediction history"""
    if request.user.is_authenticated:
        predictions = SinglePrediction.objects.filter(user=request.user).order_by('-created_at')
    else:
        # For anonymous users, show predictions from current session
        session_key = request.session.session_key
        if session_key:
            predictions = SinglePrediction.objects.filter(session_key=session_key).order_by('-created_at')
        else:
            predictions = SinglePrediction.objects.none()
    
    paginator = Paginator(predictions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'app/prediction_history.html', {'page_obj': page_obj})

def ajax_batch_status(request, batch_id):
    """AJAX endpoint to check batch processing status"""
    batch = get_object_or_404(BatchPrediction, id=batch_id)
    
    data = {
        'status': batch.status,
        'processed_records': batch.processed_records,
        'failed_records': batch.failed_records,
        'total_records': batch.total_records,
        'progress': (batch.processed_records + batch.failed_records) / batch.total_records * 100
    }
    
    return JsonResponse(data)

def sample_csv_download(request):
    """Download sample CSV template"""
    sample_data = '''gender,race/ethnicity,parental level of education,lunch,test preparation course,reading score,writing score
female,group B,bachelor's degree,standard,none,72,74
male,group C,some college,standard,completed,69,73
female,group B,master's degree,standard,none,90,88
male,group A,associate's degree,free/reduced,none,47,57
female,group C,some college,standard,completed,76,78'''
    
    response = HttpResponse(sample_data, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sample_student_data.csv"'
    
    return response
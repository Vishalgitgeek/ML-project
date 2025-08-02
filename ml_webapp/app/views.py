from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# def predict_view(request):
#     # return HttpResponse("Hello, world! This is the index page of the ML web app.")
#     return render(request, 'app/home.html')


from django.shortcuts import render
from .forms import PredictionForm
from src.pipeline.predict_pipeline import PredictPipeline  # Update path as needed

def predict_view(request):
    prediction = None
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
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
    else:
        form = PredictionForm()
    return render(request, 'app/home.html', {'form': form, 'prediction': prediction})


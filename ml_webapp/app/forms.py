from django import forms
import pandas as pd
from io import StringIO

class PredictionForm(forms.Form):
    gender = forms.ChoiceField(
        choices=[('male', 'Male'), ('female', 'Female')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    race_ethnicity = forms.ChoiceField(
        choices=[
            ('group A', 'Group A'), ('group B', 'Group B'),
            ('group C', 'Group C'), ('group D', 'Group D'), ('group E', 'Group E')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    parental_level_of_education = forms.ChoiceField(
        choices=[
            ("some high school", "Some High School"),
            ("high school", "High School"),
            ("some college", "Some College"),
            ("associate's degree", "Associate's Degree"),
            ("bachelor's degree", "Bachelor's Degree"),
            ("master's degree", "Master's Degree")
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    lunch = forms.ChoiceField(
        choices=[('standard', 'Standard'), ('free/reduced', 'Free/Reduced')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    test_preparation_course = forms.ChoiceField(
        choices=[('none', 'None'), ('completed', 'Completed')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    reading_score = forms.IntegerField(
        min_value=0, max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter reading score (0-100)'
        })
    )
    writing_score = forms.IntegerField(
        min_value=0, max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter writing score (0-100)'
        })
    )

class BatchPredictionForm(forms.Form):
    csv_file = forms.FileField(
        help_text="Upload a CSV file with student data. Maximum file size: 5MB",
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.csv',
            'id': 'csv-file-input'
        })
    )
    
    def clean_csv_file(self):
        csv_file = self.cleaned_data['csv_file']
        
        # Check file size (5MB limit)
        if csv_file.size > 5 * 1024 * 1024:  # 5MB
            raise forms.ValidationError("File size cannot exceed 5MB")
        
        # Check file extension
        if not csv_file.name.endswith('.csv'):
            raise forms.ValidationError("Please upload a CSV file")
        
        # Validate CSV structure
        try:
            # Read the file content
            file_content = csv_file.read().decode('utf-8')
            csv_file.seek(0)  # Reset file pointer
            
            # Parse CSV
            df = pd.read_csv(StringIO(file_content))
            
            # Required columns
            required_columns = [
                'gender', 'race/ethnicity', 'parental level of education',
                'lunch', 'test preparation course', 'reading score', 'writing score'
            ]
            
            # Check if all required columns exist
            missing_columns = set(required_columns) - set(df.columns)
            if missing_columns:
                raise forms.ValidationError(
                    f"Missing required columns: {', '.join(missing_columns)}"
                )
            
            # Check if file has data
            if len(df) == 0:
                raise forms.ValidationError("CSV file is empty")
            
            # Check maximum number of rows (limit to 1000 for performance)
            if len(df) > 1000:
                raise forms.ValidationError("CSV file cannot have more than 1000 rows")
            
            # Validate data types and values
            errors = []
            
            # Check gender values
            valid_genders = ['male', 'female']
            invalid_genders = df[~df['gender'].isin(valid_genders)]['gender'].unique()
            if len(invalid_genders) > 0:
                errors.append(f"Invalid gender values: {', '.join(invalid_genders)}")
            
            # Check race/ethnicity values
            valid_races = ['group A', 'group B', 'group C', 'group D', 'group E']
            invalid_races = df[~df['race/ethnicity'].isin(valid_races)]['race/ethnicity'].unique()
            if len(invalid_races) > 0:
                errors.append(f"Invalid race/ethnicity values: {', '.join(invalid_races)}")
            
            # Check score ranges
            for score_col in ['reading score', 'writing score']:
                if score_col in df.columns:
                    invalid_scores = df[(df[score_col] < 0) | (df[score_col] > 100)]
                    if len(invalid_scores) > 0:
                        errors.append(f"Invalid {score_col} values (must be 0-100)")
            
            if errors:
                raise forms.ValidationError("; ".join(errors))
        
        except pd.errors.EmptyDataError:
            raise forms.ValidationError("CSV file is empty or corrupted")
        except pd.errors.ParserError:
            raise forms.ValidationError("Invalid CSV format")
        except UnicodeDecodeError:
            raise forms.ValidationError("File encoding not supported. Please use UTF-8 encoding")
        
        return csv_file


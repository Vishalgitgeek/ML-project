from django import forms

class PredictionForm(forms.Form):
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female')])
    race_ethnicity = forms.ChoiceField(choices=[
        ('group A', 'Group A'), ('group B', 'Group B'),
        ('group C', 'Group C'), ('group D', 'Group D'), ('group E', 'Group E')
    ])
    parental_level_of_education = forms.ChoiceField(choices=[
        ("some high school", "Some High School"),
        ("high school", "High School"),
        ("some college", "Some College"),
        ("associate's degree", "Associate's Degree"),
        ("bachelor's degree", "Bachelor's Degree"),
        ("master's degree", "Master's Degree")
    ])
    lunch = forms.ChoiceField(choices=[('standard', 'Standard'), ('free/reduced', 'Free/Reduced')])
    test_preparation_course = forms.ChoiceField(choices=[('none', 'None'), ('completed', 'Completed')])
    reading_score = forms.IntegerField()
    writing_score = forms.IntegerField()


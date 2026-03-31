from django import forms
from .models import UserDietLog, DietSuggestion, MealPlan

class DietLogForm(forms.ModelForm):
    class Meta:
        model = UserDietLog
        fields = ['diet_suggestion', 'meal_name', 'portion_size', 'calories_consumed', 'notes']
        widgets = {
            'meal_name': forms.TextInput(attrs={'class': 'form-control'}),
            'portion_size': forms.TextInput(attrs={'class': 'form-control'}),
            'calories_consumed': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['diet_suggestion'].queryset = DietSuggestion.objects.all()
        self.fields['diet_suggestion'].required = False
        self.fields['diet_suggestion'].widget.attrs['class'] = 'form-control'

class MealPlanForm(forms.ModelForm):
    class Meta:
        model = MealPlan
        fields = ['breakfast', 'lunch', 'dinner', 'snacks']
        widgets = {
            'breakfast': forms.Select(attrs={'class': 'form-control'}),
            'lunch': forms.Select(attrs={'class': 'form-control'}),
            'dinner': forms.Select(attrs={'class': 'form-control'}),
            'snacks': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].empty_label = "None"
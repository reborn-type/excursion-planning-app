from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Route, Excursion

class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(label="Имя", max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Фамилия", max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    age = forms.IntegerField(label="Возраст", min_value=18, max_value=100, widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name']

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 18 or age > 100:
            raise forms.ValidationError("Возраст должен быть от 18 до 100 лет.")
        return age

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = f"user_{User.objects.count() + 1}"
        if commit:
            user.save()
            UserProfile.objects.create(user=user, age=self.cleaned_data['age'])
        return user
    
class IDLoginForm(forms.Form):
    login_input = forms.CharField(
        label="Введите Ваш ID или admin", 
        max_length=50, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: 123 или admin'})
    )
    

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['title', 'description', 'length_km']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'length_km': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ExcursionForm(forms.ModelForm):
    class Meta:
        model = Excursion
        fields = ['title', 'route', 'price', 'min_age', 'max_age', 'max_persons']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'route': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'min_age': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_age': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_persons': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
from django.forms import ModelForm
from django import forms
from .models import Profile

class ProfileForm(ModelForm):
    class Meta:
        model = Profile 
        fields="__all__"  
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)   
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})
        
        # self.fields['Full_name'].widget.attrs.update({'class':'input'})
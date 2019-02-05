from django.forms import ModelForm, TextInput
from .models import Site

class PilotForm(ModelForm):
    class Meta:
        model = Site
        fields = ['url']
        widgets = {'url' : TextInput(attrs={'class' : 'input', 'placeholder' : 'Url Address'})}

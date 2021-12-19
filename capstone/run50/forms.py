from django import forms


class ActivityForm(forms.Form):
    distance = forms.FloatField(label='Distance (km)', min_value=0.0)
    duration = forms.IntegerField(label='Duration (min)', min_value=0)
    date = forms.DateField(label='Date', widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(label='Time', widget=forms.TimeInput(attrs={'type': 'time'}))
    image = forms.ImageField(label='Image', required=False)
    # location = forms.CharField(label='Location', max_length=200, required=False, widget=forms.TextInput(attrs={'id': 'location-input'}))
    elevation = forms.FloatField(label='Elevation (m)', min_value=0.0)

    def __init__(self, *args, **kwargs):
        super(ActivityForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control w-75'


class EditProfileForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    profile_picture = forms.ImageField(label='Profile Picture', required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    share_preference = forms.BooleanField(label='Share my profile with others', required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), initial=True)

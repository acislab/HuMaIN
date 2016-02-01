from django import forms

class cropLabelForm(forms.Form):
    srcFile = forms.CharField( max_length=200 )
    x = forms.IntegerField()
    y = forms.IntegerField()
    width = forms.IntegerField()
    height = forms.IntegerField()
    duration = forms.FloatField()
    
    
class cropFieldForm(forms.Form): 
    srcFile = forms.CharField( max_length=200 )
    # Country
    x_country = forms.IntegerField()
    y_country = forms.IntegerField()
    width_country = forms.IntegerField()
    height_country = forms.IntegerField()
    duration_country = forms.IntegerField()
    # Event Date
    x_date = forms.IntegerField()
    y_date = forms.IntegerField()
    width_date = forms.IntegerField()
    height_date = forms.IntegerField()
    duration_date = forms.IntegerField()
    # Latitude
    x_latitude = forms.IntegerField()
    y_latitude = forms.IntegerField()
    width_latitude = forms.IntegerField()
    height_latitude = forms.IntegerField()
    duration_latitude = forms.IntegerField()
    # Longitude
    x_longitude = forms.IntegerField()
    y_longitude = forms.IntegerField()
    width_longitude = forms.IntegerField()
    height_longitude = forms.IntegerField()
    duration_longitude = forms.IntegerField()
    # Scientific Name
    x_name = forms.IntegerField()
    y_name = forms.IntegerField()
    width_name = forms.IntegerField()
    height_name = forms.IntegerField()
    duration_name = forms.IntegerField()
    
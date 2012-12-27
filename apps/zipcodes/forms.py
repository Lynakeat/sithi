from django import forms

from activebuys.apps.zipcodes.models import ZipCode

class ZipCodeForm(forms.Form):
    """
    Form that tries to find a ZipCode instance whose `code` matches the input
    """
    zip_code = forms.CharField(
                        max_length=5, 
                        required=True,
                        label=u'My ZIP Code',
                        initial=u'Enter ZIP code',
                        widget=forms.TextInput(attrs={'class':'blink','title':'Enter ZIP code'}))
    
    def clean_zip_code(self):
        """ Find a ZipCode instance corresponding to the input data """
        data = self.cleaned_data['zip_code']
        if not data:
            raise forms.ValidationError(u'Please enter your ZIP code.')
        else:
            try:
                data = ZipCode.objects.get(code=data)
            except:
                raise forms.ValidationError(u'Zip code not found.  Please try another.')
        return data
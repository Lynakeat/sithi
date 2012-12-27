from django import forms
from activebuys.apps.utils.forms import EmErrorList
from activebuys.apps.business.models import Feature


class FeatureForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'blink', 'title': "Email Address"}))

    class Meta:
        model = Feature
        widgets = {
            'business_name': forms.TextInput(attrs={'class': 'blink', 'title': "Business Name"}),
            'contact_name': forms.TextInput(attrs={'class': 'blink', 'title': "Contact Name"}),
            'phone': forms.TextInput(attrs={'class': 'blink', 'title': "Phone"}),
            'website': forms.TextInput(attrs={'class': 'blink', 'title': "Website"}),
            'city': forms.TextInput(attrs={'class': 'blink', 'title': "City"}),
        }

    def __init__(self, *args, **kwargs):
        kwargs['error_class'] = EmErrorList
        super(FeatureForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            if field not in ['form_type', ]:
                self.fields[field].initial = self.fields[field].widget.attrs['title']
                if field in ['phone', 'website']:
                    setattr(self, 'clean_' + field, self.base_clean_blank_field(field))
                else:
                    setattr(self, 'clean_' + field, self.base_clean_field(field))

    def base_clean_field(self, field_name, *args, **kwargs):
        """
            Raise error is user value == initial value
        """
        def clean():
            message = 'Required Field'
            data = self.cleaned_data[field_name]
            initial = self.fields[field_name].initial
            if initial == data:
                raise forms.ValidationError(message)
            return data
        return clean

    def base_clean_blank_field(self, field_name, *args, **kwargs):
        """
            Return `None` for blank field if user value == initial value
        """
        def clean():
            data = self.cleaned_data[field_name]
            initial = self.fields[field_name].initial
            if initial == data:
                return None
            return data
        return clean

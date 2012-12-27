from django import forms

from activebuys.apps.utils.forms import EmErrorList
from activebuys.apps.contacts.models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        widgets = {
            'name': forms.TextInput(attrs={"class":"blink", "title":"Name"}),
            'email': forms.TextInput(attrs={"class":"blink", "title":"Email Address"}),
            'phone': forms.TextInput(attrs={"class":"blink", "title":"Phone Number"}),
            'subject': forms.TextInput(attrs={"class":"blink", "title":"Subject"}),
            'message': forms.Textarea(attrs={"class":"blink", "title":"Thoughts"})
        }

    def __init__(self, *args, **kwargs):
        kwargs['error_class'] = EmErrorList
        super(MessageForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].initial = self.fields[field].widget.attrs['title']

        for field_name in ['name', 'email', 'subject', 'message']:
            setattr(self, 'clean_'+field_name, self.base_clean_field(field_name))

    def base_clean_field(self, field_name, *args, **kwargs):
        def clean():
            message = 'Required Field'
            data = self.cleaned_data[field_name]
            initial = self.fields[field_name].initial
            if initial == data:
                raise forms.ValidationError(message)
            return data
        return clean

    def clean_phone(self):
        data = self.cleaned_data['phone']
        initial = self.fields['phone'].initial
        if initial == data:
            return None
        return data
from django import forms
from activebuys.apps.companies.models import NonProfit, CompanyAddress 


class BasePartnerForm(forms.ModelForm):
    logo = forms.ImageField(help_text="180 x 140")

    class Meta:
        abstract = True
        
        
class NonProfitForm(BasePartnerForm):
    class Meta:
        model = NonProfit


class CompanyAdminForm(forms.ModelForm):
    class Meta:
        model = CompanyAddress
        widgets = {
            'hours': forms.Textarea(attrs={'cols':30, 'rows':3})
        }
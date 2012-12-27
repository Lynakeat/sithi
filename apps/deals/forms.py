from django import forms

from activebuys.apps.utils.forms import EmErrorList
from activebuys.apps.accounts.models import AccountDeal
from activebuys.apps.companies.models import NonProfit


def get_build_deal_form(deal, user, session):
    if deal.nonprofit:
        nonprofit_initial = deal.nonprofit
    else:
        try:
            nonprofit_initial = NonProfit.objects.filter(featured=True)[0]
        except IndexError:
            nonprofit_initial = NonProfit.objects.all()[0]
            
    widget_key = session.get('wid', '')

    class FormClass(forms.ModelForm):
        quantity = forms.IntegerField(
            widget=forms.TextInput(attrs={'class': 'fc_cart_item_quantity fc_text fc_text_short'}),
            initial=1
        )
        location = forms.ModelChoiceField(queryset=deal.locations.all(), empty_label=None)
        nonprofit = forms.ModelChoiceField(
            widget=forms.Select(attrs={"class":"profit-select"}),
            queryset=NonProfit.objects.all(), required=False,
            initial=nonprofit_initial
        )
        is_gift = forms.BooleanField(
                widget=forms.RadioSelect(
                    attrs={'class':"radio gift-option"},
                    choices=((False, "No"),(True, "Yes"))
                ),
                required=False, initial=False
            )
        name_to = forms.CharField(required=False)
        name_from = forms.CharField(required=False)
        message = forms.CharField(widget=forms.Textarea(), required=False)
        email_to = forms.CharField(required=False)
        surprise = forms.BooleanField(
                widget=forms.RadioSelect(choices=((False, "No"),(True, "Yes"))),
                required=False, initial='False'
            )

        class Meta:
            model = AccountDeal
            exclude = ('status', 'deal', 'account')
            widgets = {
                'fcc_session_id': forms.HiddenInput()
            }

        def __init__(self, *args, **kwargs):
            kwargs['error_class'] = EmErrorList
            super(FormClass, self).__init__(*args, **kwargs)
            is_surprise = self.fields['surprise'].initial
            if args:
                is_gift = args[0].get('is_gift') == 'True'
                is_surprise = args[0].get('surprise') == 'True'

                gift_fields = ['name_to', 'name_from', 'email_to']
                if is_gift:
                    for field in gift_fields:
                        self.fields[field].required = True
                self.fields['email_to'].required = is_gift and not is_surprise

        def clean_is_gift(self):
            return self.cleaned_data['is_gift'] and deal.allow_gifts

        def clean(self):
            is_gift = self.cleaned_data.get('is_gift', False)
            q = self.cleaned_data.get('quantity', 0)
            
            # Check for existing purchases
            try:
                already_bought = user.accountdeal_set.\
                                filter(deal=deal, is_gift=is_gift).count()
            except AttributeError:
                already_bought = 0
            
            # Check cart
            try:
                in_cart = user.accountdeal_set.all_new().\
                                filter(deal=deal, is_gift=is_gift).count()
            except AttributeError:
                in_cart = 0
                
            limit =  is_gift and deal.gift_limit or deal.per_user
            sold = deal.sold
            errors = None

            if q <= 0:
                errors = self.error_class(["Quantity should be more then 0"])
            
            # Check user limits
            elif limit:
                # requested quantity is greater than limit
                if limit < q or q > (limit - already_bought):
                    if is_gift:
                        errors = self.error_class(['You may only purchase %d gift vouchers' % limit])
                    else:
                        errors = self.error_class(['You may only purchase %d vouchers' % limit])
                
                # check against total limits
                if deal.total_number and (sold + q + in_cart) > deal.total_number and not errors:
                    if q == 1:
                        errors = self.error_class(['Sorry, this deal has sold out.'])
                    else:
                        errors = self.error_class(['There are only %d vouchers remaining' %\
                            (deal.total_number - sold - in_cart)
                        ])
                
                if errors:
                    self.errors['quantity'] = errors
                
            return self.cleaned_data

        def save(self, commit=True):
            instance = super(FormClass, self).save(commit=False)
            instance.account = user
            instance.deal = deal
            instance.widget_id = widget_key
            if commit:
                instance.save()
            return instance

        def save_all(self):
            """ Create Account Deals according quantity """
            obj = self.save(True)
            for i in xrange(self.cleaned_data['quantity']-1):
                obj.id = None
                obj.save()

    return FormClass


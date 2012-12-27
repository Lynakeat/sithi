from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect
from django.contrib.localflavor.us.us_states import STATE_CHOICES
from django.contrib.localflavor.us.forms import USStateField
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404

from activebuys.apps.utils.views import render_to, render_json

from activebuys.apps.accounts.models import (
        Account, RestorePasswordRequest, AccountDeal, SubscribeLocation, GENDER_CHOICES, LEVEL_CHOICES
    )
from activebuys.apps.accounts.forms import (
        RegistrationForm, LoginForm, RestorePasswordForm, build_change_form
    )
from activebuys.apps.accounts.mails import send_confirm_email, send_restore_password_email, send_gift_vouchers
from activebuys.apps.utils import cmonitor
from activebuys.apps.foxycart import customer_save_command

from activebuys.apps.reviews.models import Review
from django.core.mail import send_mail
from activebuys.apps.companies.models import CompanyAddress, SubCategory, Category
from activebuys.apps.follow.models import Follow
from django.forms.models import modelformset_factory
import datetime
from django.db.models import Count

@render_to('accounts/registration.html')
def registration(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            # create customer account on foxycart for SSO authentication
            account.foxycart_customer_id = customer_save_command(account.email,
                                      customer_password_hash=account.password)
            account.save()
            form.save_m2m()
            cmonitor.subscribe(account)
            return {}, 'accounts/registration_complete.html'
    return {'form': form}

@render_to('accounts/login.html')
def login(request):
    form = LoginForm()
    r_next = request.REQUEST.get('next', '/')

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            if request.COOKIES.get('fcsid'):
                # clean previous user's cart
                # cart should be empty on each login to prevent limit cheating
                AccountDeal.clean_by_fcid(request.COOKIES.get('fcsid'))
            auth_login(request, form.get_user())
            return redirect(r_next)

    if request.GET.get('_popup'):
        return {
                'form':form,
                'next': r_next,
            }, 'accounts/login-popup.html'

    return {'form': form, 'next': r_next}

@render_to('accounts/registration_confirm.html')
def confirm(request):
    """ Account activation """
    if not request.GET.get('code'):
        raise Http404('code required')
    count = Account.objects.filter(is_active=False, confirm_email_code=request.GET.get('code')).update(is_active=True)
    return {'form':LoginForm(), 'is_validcode': bool(count)}

@render_to('accounts/restore_password.html')
def restore_password(request):
    """ Restore password form """
    code = request.REQUEST.get('code')
    if not code:
        raise Http404('code required')
    form = RestorePasswordForm()
    if request.method == "POST":
        form = RestorePasswordForm(request.POST)
        if form.is_valid():
            form.change_password()
            return redirect('account-login')
    return {'form': form, 'code':code}

@render_json
def resend_confirmation(request):
    """ Send account activation url to user """
    email = request.GET.get('email')
    success = True
    try:
        user = Account.objects.get(email=email, is_active=False)
        send_confirm_email(user)
    except Account.DoesNotExist:
        success = False
    return {'success': success}

@render_json
def send_restore_code(request):
    """ Send url to restore password form """
    email = request.GET.get('email')
    success = True
    try:
        user = Account.objects.get(email=email)
        # create restore pass request
        RestorePasswordRequest.objects.create(account=user)
        # send restore url to user
        send_restore_password_email(user)
    except Account.DoesNotExist:
        success = False
    return {'success': success}

@login_required
@render_to('accounts/profile.html')
def profile(request):
    user = Account.objects.get(pk=request.user.id)
    reviews = Review.objects.filter(user=request.user)
    follows = Follow.objects.filter(user=request.user)
    gender_choices = GENDER_CHOICES
    level_choices = LEVEL_CHOICES
    active_interests = Category.objects.all()
    
    return {
        'subscribe_locations': SubscribeLocation.objects.all(),
        'reviews': reviews,
        'follows': follows,  
        'gender_choices': gender_choices,
        'states': STATE_CHOICES,
        'account': user,
        'active_interests': active_interests,
        'level_choices': level_choices
    }

@render_to('accounts/profile.html')
def profile_view(request, id):
    account =   Account.objects.get(id=id)
    reviews = Review.objects.filter(user=account)
    follows = Follow.objects.filter(user=account)
    gender_choices = GENDER_CHOICES    
    active_interests = Category.objects.all()
    return {
        'subscribe_locations': SubscribeLocation.objects.all(),
        'reviews': reviews,
        'follows': follows,  
        'gender_choices': gender_choices,
        'states': STATE_CHOICES,
        'account': account,     
        'active_interests': active_interests,
        'level_choices': level_choices
    }

@login_required
@render_json
def profile_edit(request):
    """ ajax profile editting """
    context = {
        'success':False,
        'messages': "post method required"
    }

    if request.method == "POST":
        old_email = request.user.email
        form_class = build_change_form(request.POST.keys())
        form = form_class(request.POST,  instance=request.user)
        if form.is_valid():
            account = form.save(commit=False)
            account.save()
            form.save_m2m()
            cmonitor.update(old_email, account)
            context['success'] = True
            context['messages'] = {}
        else:
            context['messages'] = dict((key,value) for key, value in form.errors.items())
    return context

@login_required
@render_json
def mark_as_used(request):
    """ mark user deal as used """
    try:
        accdeal = request.user.accountdeal_set.get(id=request.POST.get('id'))
        accdeal.status = AccountDeal.USED
        accdeal.save() # use `save` to allow use signals 
    except AccountDeal.DoesNotExist:
        pass
    return {}

@login_required
@render_json
def resend_gift(request):
    try:
        accdeal = request.user.accountdeal_set.get(id=request.POST.get('id'))
        send_gift_vouchers(accdeal.email_to, accdeal.name_to,
                           accdeal.name_from, [accdeal])
    except AccountDeal.DoesNotExist:
        pass
    return {}


@render_json
def remove_accountdeal(request):
    """ api call from foxycart cart to remove user deal """
    AccountDeal.objects.all_new().\
        filter(deal__id=request.GET.get('id'),
               fcc_session_id='&fcsid='+request.GET.get('fcc_session_id')).delete()
    return {}


@login_required
@render_to('accounts/purchase.html')
def purchase(request):
    reviews = Review.objects.filter(user=request.user)
    follows = Follow.objects.filter(user=request.user)    
    account =   Account.objects.get(id=request.user.id)
    return {
        'reviews': reviews,
        'follows': follows,
        'account': account
    }

@login_required
@render_to('accounts/review.html')
def review(request):
    sort = request.GET.get('sort', 'date')
    sort_by = 'Date'
    if sort == 'rating':
        reviews = Review.objects.filter(user=request.user).order_by('-score')
        sort_by = 'Rating'
    elif sort == 'most-helpful':
        sort_by = 'Most Helpful'
        reviews = Review.objects.extra(
            select={'yes_count': 'select count(*) from reviews_vote where reviews_vote.review_id = reviews_review.id and vote_type =1 and active=true'}
            ).filter(user=request.user).order_by('-yes_count')
    elif sort == 'least-helpful':
        sort_by = 'Least Helpful'
        reviews = Review.objects.extra(
            select={'no_count': 'select count(*) from reviews_vote where reviews_vote.review_id = reviews_review.id and vote_type =2 and active=true'}
            ).filter(user=request.user).order_by('-no_count')
    else:
        sort_by = 'Date'
        reviews = Review.objects.filter(user=request.user) 
        
    follows = Follow.objects.filter(user=request.user)    
    account =   Account.objects.get(id=request.user.id)

    return {
        'reviews': reviews,
        'follows': follows,
        'account': account,
        'sort_by':sort_by
    }


@login_required
@render_to('accounts/follow.html')
def follow(request):
    follows = Follow.objects.filter(user=request.user)
    companies = CompanyAddress.objects.filter(follow_companyaddress=follows)
    categories = Category.objects.filter(companyaddress=companies)
    subcategories = SubCategory.objects.filter(category=categories).distinct()  
    account =   Account.objects.get(id=request.user.id)
    return { 
        'follows': follows,
        'companies':companies,
        'categories': categories,
        'subcategories': get_subcategories(companies),
        'account': account,
    }

@login_required
@render_to('accounts/follow.html')
def resource_subcategory(request, slug):
    follows = Follow.objects.filter(user=request.user)
    subcategories = SubCategory.objects.filter(slug=slug)
    companies = CompanyAddress.objects.filter(follow_companyaddress=follows, subcategories=subcategories)
    categories = Category.objects.filter(companyaddress=companies)  
    account =   Account.objects.get(id=request.user.id)
    return { 
        'follows': follows,
        'companies':companies,
        'categories': categories,
        'subcategories': get_subcategories(companies),        
        'account': account
    }

#Get month list in one year
def get_subcategories(companies):
    if not CompanyAddress.objects.count(): return []
    categories = Category.objects.filter(companyaddress=companies)    
    subcategories = SubCategory.objects.filter(category=categories).distinct()
    result = []
    for m in subcategories:
        if CompanyAddress.objects.filter(subcategories=m, id=companies).count() > 0:
            result.append((m, CompanyAddress.objects.filter(subcategories=m, id=companies).count))
    return result






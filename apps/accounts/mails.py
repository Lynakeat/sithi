import urllib
from django.conf import settings
from django.contrib.sites.models import Site
from django.core import mail
from django.template import loader

from activebuys.apps.companies.models import Company

def base_code_sending(user, code, body_template, subject):
    site_name = Site.objects.get_current().domain
    context = {
        'domain': site_name,
        'code': code,
        'user': user
    }
    if '%s' in subject:
        subject = subject % site_name
    # create mail message and send it
    email = mail.EmailMessage(
        to=[user.email],
        subject = subject,
        body=loader.render_to_string(body_template, context)
    )
    #email.content_subtype = "html"
    email.send()

def send_confirm_email(user):
    subject = getattr(settings, 'CONFIRM_EMAIL_SUBJECT', 'Confirm email for %s')
    body_template = 'accounts/confirm_email_body.txt'
    code = user.confirm_email_code
    base_code_sending(user, code, body_template, subject)

def send_restore_password_email(user):
    subject = getattr(settings, 'RESTORE_PASSWORD_EMAIL_SUBJECT', 'Restore password for %s')
    body_template = 'accounts/restore_pass_email_body.txt'
    code = user.get_restore_pass_code()
    base_code_sending(user, code, body_template, subject)


def regroup_accdeal_list(acc_deals):
    """ regroup account deals list by deal """
    output = {}
    for deal in acc_deals:
        try:
            output[deal.deal.id]['quantity']+=1
        except KeyError:
            output[deal.deal.id] = {
                'quantity': 1,
                'deal': deal.deal,
                'nonprofit': deal.nonprofit,
                'location': deal.location,
                'company': deal.deal.company
            }
    return output

def send_order_receipt(order):
    """ send receipt mail to user how buy a vouchers
        with all vouchers in attach
    """
    site = Site.objects.get_current()
    deals_list = regroup_accdeal_list(order.deals.all()).values()
    context = {
        'order': order,
        'deals_list': deals_list,
        'site': site,
        'MEDIA_URL': settings.MEDIA_URL
    }
    
    # create mail message and send it
    email = mail.EmailMessage(
        to=[order.account.email],
        subject = u"ACTIVEBUYS Receipt",
        body=loader.render_to_string('accounts/receipt_email.html', context)
    )

    email.content_subtype = "html"
    for deal in order.deals.all():
        email.attach_file(deal.voucher.pdf.path)
    email.send()

def send_order_notifications(order):
    """ send notification mail to companies related to voucher
     - only include data relevant to each company in the email
    """
    site = Site.objects.get_current()
    # find each Company associated with the order
    companies = Company.objects.filter(companyaddress__deal__accountdeal__order=order).distinct()
    # for each Company:
    for company in companies:
        # add Company and relevant deals only to context
        #deals_list = order.deals.filter(deal__company=company)
        deals_list = regroup_accdeal_list(order.deals.filter(deal__company=company)).values()
        context = {
            'order': order,
            'company': company,
            'deals_list': deals_list,
            'site': site,
            'MEDIA_URL': settings.MEDIA_URL
        }
        # create and send a notification email
        # TODO: mail managers when notification email is missing
        if company.notification_email:
            # recipients = [a[1] for a in settings.MANAGERS]
            recipients = [company.notification_email]
            email = mail.EmailMessage(
                to=recipients,
                subject = u"ACTIVEBUYS Notification",
                body=loader.render_to_string('accounts/notification_email.html', context)
            )

            email.content_subtype = "html"
            # for deal in order.deals.all():
            #     email.attach_file(deal.voucher.pdf.path)
            email.send()

def send_gift_vouchers(email, name_to, name_from, acc_deals):
    """ send Gift email with vouchers
        with all vouchers in attach
    """
    deals_list = regroup_accdeal_list(acc_deals).values()
    site = Site.objects.get_current()
    context = {
        'name_to': name_to,
        'name_from': name_from,
        'deals_list': deals_list,
        'site': site,
        'MEDIA_URL': settings.MEDIA_URL
    }

    # create mail message and send it
    email = mail.EmailMessage(
        to=[email],
        subject = u"ACTIVEBUYS Receipt",
        body=loader.render_to_string('accounts/gift_email.html', context)
    )
    email.content_subtype = "html"
    for deal in acc_deals:
        email.attach_file(deal.voucher.pdf.path)
    email.send()

def send_emails_on_order_creation(instance):
    send_order_receipt(instance)
    send_order_notifications(instance)
    # send email for each gift reciever
    gifts = instance.get_gifts()
    for email, values in gifts.items():
        send_gift_vouchers(email, values['name_to'],
                           values['name_from'], values['deals'])


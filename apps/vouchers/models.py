from random import random
from django.db import models
from django.core.files.base import ContentFile
from django.dispatch import receiver
from django.core.files.storage import FileSystemStorage

from activebuys.apps.vouchers.pdf import generate_voucher

AccountDeal = models.get_model('accounts', 'AccountDeal')

voucher_storage = FileSystemStorage()

CODE_LENGTH = 10

class Voucher(models.Model):
    accountdeal = models.OneToOneField(AccountDeal)
    is_used = models.BooleanField(default=False)
    pdf = models.FileField(upload_to='assets/vouchers/%y/%m', storage=voucher_storage)
    code = models.CharField(unique=True, max_length=CODE_LENGTH)
    
    def __unicode__(self):
        return self.code

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_unique_code()
        super(Voucher, self).save(*args, **kwargs)
        if not self.pdf:
            self.pdf.save(self.code+'.pdf', ContentFile(generate_voucher(self).getvalue()))

    def generate_unique_code(self):
        code = None
        while True:
            code = str(random())[2:CODE_LENGTH+2] # trim "0." and and take 10 numbers after  
            try:
                self.__class__.objects.get(code=code)
            except self.__class__.DoesNotExist:
                break
            continue
        return code


@receiver(models.signals.post_save, sender=AccountDeal, dispatch_uid="create_voucher_on_success_payment")
def create_voucher_on_success_payment(sender, **kwargs):
    inst = kwargs['instance']
    if not kwargs['raw'] == True: # 'raw' flag is for when loaddata is running
        if inst.is_paid and not Voucher.objects.filter(accountdeal=inst).count():
            voucher = Voucher(accountdeal=inst)
            voucher.save()

@receiver(models.signals.post_save, sender=AccountDeal, dispatch_uid="mark_voucher_as_used")
def mark_voucher_as_used(sender, **kwargs):
    inst = kwargs['instance']
    if inst.is_used and not kwargs['raw'] == True: # 'raw' flag is for when loaddata is running
        Voucher.objects.filter(accountdeal=inst).update(is_used=True)

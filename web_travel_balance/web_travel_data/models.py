from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Member(models.Model):
    """A member of team"""
    name = models.CharField(max_length=200, verbose_name=_('Name'))

    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    contribute = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    return_to_close = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    email = models.EmailField(default='', verbose_name=_('E-mail'))
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return a string representation of the model"""
        return self.name


class Contribution(models.Model):
    """What is amount was given per time"""
    member = models.ForeignKey(
        Member, null=True, on_delete=models.CASCADE, verbose_name=_('Member'))
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name=_('Amount'))
    date_added = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Date'))
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.CharField(max_length=255, default='', verbose_name=_('Note'))

    def __str__(self):
        """Return a string representation of the model"""
        return f"{self.amount}"


class Expence(models.Model):
    """What is amount was spent and why"""
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name=_('Amount'))
    purpose = models.CharField(max_length=200, verbose_name=_('Purpose'))
    date_added = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Date'))
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.CharField(max_length=255, default='', verbose_name=_('Note'))

    def __str__(self):
        """Return a string representation of the model"""
        return f"{self.purpose}: {self.amount}"


class Exeption(models.Model):
    """ Exeptions for spendings and members"""
    name = models.CharField(max_length=200, verbose_name=_('Exeption'))
    member = models.ManyToManyField(Member, verbose_name=_('Member'))
    expence = models.ManyToManyField(Expence, verbose_name=_('Expence'))
    expences = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.CharField(max_length=255, default='', verbose_name=_('Note'))

    def __str__(self):
        """Return a string representation of the model"""
        return self.name

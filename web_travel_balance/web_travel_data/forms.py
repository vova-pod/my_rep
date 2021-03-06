from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Member, Contribution, Expence, Exeption, Team
from .balance_data import *


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'email']

    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = False


class ContributionForm(forms.ModelForm):
    class Meta:
        model = Contribution
        fields = ['amount', 'member', 'note']
        widgets = {'member': forms.Select}

    def __init__(self, team, *args, **kwargs):
        super(ContributionForm, self).__init__(*args, **kwargs)
        self.fields['member'].queryset = Member.objects.filter(owner=team)
        self.fields['note'].required = False


class ExpenceForm(forms.ModelForm):
    class Meta:
        model = Expence
        fields = ['amount', 'purpose', 'note']

    def __init__(self, team, expence_id, *args, **kwargs):
        self.team = team
        self.expence_id = expence_id
        super(ExpenceForm, self).__init__(*args, **kwargs)
        self.fields['note'].required = False

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if self.expence_id is not None:
            expence = Expence.objects.get(id=self.expence_id)
            expence_amount = expence.amount
        else:
            expence_amount = 0
        if (all_balance(self.team) + expence_amount - amount) < 0:
            err = _('Not enough money in TeamWallet. Make contribution.')
            raise forms.ValidationError(err)
        return amount


class ExeptionForm(forms.ModelForm):
    class Meta:
        model = Exeption
        fields = ['name', 'note', 'member', 'expence']
        widgets = {'member': forms.CheckboxSelectMultiple,
                   'expence': forms.CheckboxSelectMultiple,
                   'name': forms.TextInput(attrs={'placeholder': 'Exception'})}

    def __init__(self, team, exeption_id, *args, **kwargs):
        self.team = team
        self.exeption_id = exeption_id
        super(ExeptionForm, self).__init__(*args, **kwargs)
        self.fields['member'].queryset = Member.objects.filter(owner=team)
        self.fields['expence'].queryset = Expence.objects.filter(owner=team)
        self.fields['note'].required = False

    def clean(self):

        members = self.cleaned_data['member']
        expences = self.cleaned_data['expence']

        repetition = {}
        for exeption in Exeption.objects.filter(owner=self.team).exclude(id=self.exeption_id):
            for member in members:
                if member in exeption.member.all():
                    for expence in expences:
                        if expence in exeption.expence.all():
                            repetition[member.name] = (
                                expence.purpose, str(expence.amount))

        if repetition:
            err = _(
                'Exeption you are trying to add already was established with ' + str(repetition))
            raise forms.ValidationError(err)

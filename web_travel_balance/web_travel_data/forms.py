from django import forms

from .models import Member, Contribution, Expence


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name']


class ContributionForm(forms.ModelForm):
    class Meta:
        model = Contribution
        fields = ['member', 'amount']
        widgets = {'member': forms.Select}


class ExpenceForm(forms.ModelForm):
    class Meta:
        model = Expence
        fields = ['purpose', 'amount']

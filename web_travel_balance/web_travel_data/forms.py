from django import forms

from .models import Member, Contribution, Expence, Exeption


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'email']


class ContributionForm(forms.ModelForm):
    class Meta:
        model = Contribution
        fields = ['amount', 'member', 'note']
        labels = {'amount': 'Amount', 'member': 'Member', 'note': 'Note'}
        widgets = {'member': forms.Select}

    def __init__(self, user, *args, **kwargs):
        super(ContributionForm, self).__init__(*args, **kwargs)
        self.fields['member'].queryset = Member.objects.filter(owner=user)
        self.fields['note'].required = False


class ExpenceForm(forms.ModelForm):
    class Meta:
        model = Expence
        fields = ['amount', 'purpose']


class ExeptionForm(forms.ModelForm):
    class Meta:
        model = Exeption
        fields = ['name', 'member', 'expence']
        widgets = {'member': forms.CheckboxSelectMultiple,
                   'expence': forms.CheckboxSelectMultiple}

    def __init__(self, user, *args, **kwargs):
        super(ExeptionForm, self).__init__(*args, **kwargs)
        self.fields['member'].queryset = Member.objects.filter(owner=user)
        self.fields['expence'].queryset = Expence.objects.filter(owner=user)

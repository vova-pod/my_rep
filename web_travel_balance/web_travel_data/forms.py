from django import forms

from .models import Member, Contribution, Expence, Exeption, Team


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

    def __init__(self, *args, **kwargs):
        super(ExpenceForm, self).__init__(*args, **kwargs)
        self.fields['note'].required = False


class ExeptionForm(forms.ModelForm):
    class Meta:
        model = Exeption
        fields = ['name', 'note', 'member', 'expence']
        widgets = {'member': forms.CheckboxSelectMultiple,
                   'expence': forms.CheckboxSelectMultiple,
                   'name': forms.TextInput(attrs={'placeholder': 'Exception'})}

    def __init__(self, team, *args, **kwargs):
        self.team = team
        super(ExeptionForm, self).__init__(*args, **kwargs)
        self.fields['member'].queryset = Member.objects.filter(owner=team)
        self.fields['expence'].queryset = Expence.objects.filter(owner=team)
        self.fields['note'].required = False

    def clean(self):

        members = self.cleaned_data["member"]
        expences = self.cleaned_data["expence"]

        repetition = {}
        for exeption in Exeption.objects.filter(owner=self.team):
            for member in members:
                if member in exeption.member.all():
                    for expence in expences:
                        if expence in exeption.expence.all():
                            repetition[member] = expence

        if repetition:
            raise forms.ValidationError(
                "Exeption you are trying to add already was established with")

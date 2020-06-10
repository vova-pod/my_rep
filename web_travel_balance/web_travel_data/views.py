from django.shortcuts import render
from .models import Member, Contribution, Expence


def balance():
    """Calculate total balance"""
    contributions = 0
    expences = 0
    for contribution in Contribution.objects.all():
        contributions += contribution.amount
    for expence in Expence.objects.all():
        expences += expence.amount
    return contributions - expences


def all_contributions():
    """Calculate all contributions"""
    contributions = 0
    for contribution in Contribution.objects.all():
        contributions += contribution.amount
    return contributions


def all_expences():
    """Calculate all expences"""
    expences = 0
    for expence in Expence.objects.all():
        expences += expence.amount
    return expences


def contributions_per_member():
    """Calculate contributions per member"""
    for member in Member.objects.all():
        contributions = 0
        for contribution in Contribution.objects.filter(member=member.id):
            contributions += contribution.amount
        member.contribute = contributions
        member.save()


def balance_per_member():
    """Calculate if member owes and how much"""
    for member in Member.objects.all():
        member.balance = all_contributions() / len(Member.objects.all()) - \
            member.contribute
        member.save()


def index(request):
    """The home page for Web Travel Balance"""
    contributions_per_member()
    balance_per_member()
    members = Member.objects.all()
    context = {'balance': balance(), 'contributed': all_contributions(), 'spent': all_expences(),
               'members': members, }
    return render(request, 'web_travel_data/index.html', context)

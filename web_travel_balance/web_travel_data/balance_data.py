from .models import Member, Contribution, Expence, Exeption
from django.db import connection
from prettytable import PrettyTable
from datetime import datetime


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


def expences_per_exeption():
    """Calculate expences per exeption"""
    for exeption in Exeption.objects.all():
        expences = 0
        for expence in Expence.objects.filter(exeption=exeption.id):
            expences += expence.amount
        exeption.expences = expences
        exeption.save()


def all_exeption_expences():
    """Calculate all exeption expences"""
    exeption_expences = 0
    for exeption_expence in Exeption.objects.all():
        exeption_expences += exeption_expence.expences
    return exeption_expences


def base_expences_per_member():
    if balance() <= 0:
        return (all_expences() - all_exeption_expences()) / len(Member.objects.all())
    else:
        return (all_contributions() - all_exeption_expences()) / len(Member.objects.all())


def balance_per_member():
    """Calculate if member owes and how much"""
    for member in Member.objects.all():
        member_owe = base_expences_per_member()
        for exeption in Exeption.objects.all():
            for expence in Expence.objects.filter(exeption=exeption.id):
                if exeption not in member.exeption_set.all():
                    member_owe += expence.amount / \
                        (len(Member.objects.all()) -
                         len(Member.objects.filter(exeption=exeption.id)))
        member.balance = member.contribute - member_owe
        member.save()


def return_to_close():
    """How much shell we return to member to close balance or take"""
    for member in Member.objects.all():
        member.return_to_close = member.balance + \
            (balance() / len(Member.objects.all()))
        member.save()


def create_member_report(id):
    """Create member report string table"""
    member = Member.objects.get(id=id)
    contributions = member.contribution_set.order_by('date_added')
    member_report = PrettyTable()
    member_report.field_names = ["Date", "Amount"]
    for contribution in contributions:
        member_report.add_row(
            [contribution.date_added.strftime("%d/%m/%Y"), contribution.amount])
    return str(member_report)

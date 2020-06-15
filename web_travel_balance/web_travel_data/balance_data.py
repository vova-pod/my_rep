from .models import Member, Contribution, Expence, Exeption
from django.db import connection
from prettytable import PrettyTable
from datetime import datetime
import decimal


def balance(request_user):
    """Calculate total balance"""
    contributions = 0
    expences = 0
    for contribution in Contribution.objects.filter(owner=request_user):
        contributions += contribution.amount
    for expence in Expence.objects.filter(owner=request_user):
        expences += expence.amount
    return contributions - expences


def all_contributions(request_user):
    """Calculate all contributions"""
    contributions = 0
    for contribution in Contribution.objects.filter(owner=request_user):
        contributions += contribution.amount
    return contributions


def all_expences(request_user):
    """Calculate all expences"""
    expences = 0
    for expence in Expence.objects.filter(owner=request_user):
        expences += expence.amount
    return expences


def contributions_per_member(request_user):
    """Calculate contributions per member"""
    for member in Member.objects.filter(owner=request_user):
        contributions = 0
        for contribution in Contribution.objects.filter(member=member.id):
            contributions += contribution.amount
        member.contribute = contributions
        member.save()


def expences_per_exeption(request_user):
    """Calculate expences per exeption"""
    for exeption in Exeption.objects.filter(owner=request_user):
        expences = 0
        for expence in Expence.objects.filter(exeption=exeption.id):
            expences += expence.amount
        exeption.expences = expences
        exeption.save()


def all_exeption_expences(request_user):
    """Calculate all exeption expences"""
    exeption_expences = 0
    for exeption_expence in Exeption.objects.filter(owner=request_user):
        exeption_expences += exeption_expence.expences
    return exeption_expences


def base_expences_per_member(request_user):
    if len(Member.objects.filter(owner=request_user)) != 0:
        if balance(request_user) <= 0:
            return (all_expences(request_user) - all_exeption_expences(request_user)) / len(Member.objects.filter(owner=request_user))
        else:
            return (all_contributions(request_user) - all_exeption_expences(request_user)) / len(Member.objects.filter(owner=request_user))


def balance_per_member(request_user):
    """Calculate if member owes and how much"""
    if len(Member.objects.filter(owner=request_user)) != 0:
        for member in Member.objects.filter(owner=request_user):
            member_owe = base_expences_per_member(request_user)
            for exeption in Exeption.objects.filter(owner=request_user):
                for expence in Expence.objects.filter(exeption=exeption.id):
                    if exeption not in member.exeption_set.all():
                        member_owe += expence.amount / (len(Member.objects.filter(owner=request_user)) -
                                                        len(Member.objects.filter(owner=request_user).filter(exeption=exeption.id)))
            member.balance = member.contribute - decimal.Decimal(member_owe)
            member.save()


def return_to_close(request_user):
    """How much shell we return to member to close balance or take"""
    if len(Member.objects.filter(owner=request_user)) != 0:
        for member in Member.objects.filter(owner=request_user):
            member.return_to_close = member.balance + \
                decimal.Decimal(balance(request_user) /
                                len(Member.objects.filter(owner=request_user)))
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

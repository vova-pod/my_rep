from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Member, Contribution, Expence, Exeption
from .forms import MemberForm, ContributionForm, ExpenceForm, ExeptionForm
from .balance_data import *


def index(request):
    """The home page for Web Travel Balance"""
    all_expences()
    balance()
    all_contributions()
    contributions_per_member()
    expences_per_exeption()
    all_exeption_expences()
    base_expences_per_member()
    balance_per_member()
    return_to_close()
    members = Member.objects.order_by('date_added')
    exeptions = Exeption.objects.all()
    context = {'balance': balance(), 'contributed': all_contributions(), 'spent': all_expences(),
               'members': members, 'exeptions': exeptions, 'all_exeption_expences': all_exeption_expences()}
    return render(request, 'web_travel_data/index.html', context)


def members(request):
    """Show all members"""
    members = Member.objects.order_by('date_added')
    context = {'members': members}
    return render(request, 'web_travel_data/members.html', context)


def new_member(request):
    """Add new member."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = MemberForm()
    else:
        # POST data submitted, process data
        form = MemberForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('web_travel_data:members')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'web_travel_data/new_member.html', context)


def new_contribution(request):
    """ Add new contribution for particular member"""

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = ContributionForm()
    else:
        # POST data submitted, process data
        form = ContributionForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('web_travel_data:index')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'web_travel_data/new_contribution.html', context)


def new_expence(request):
    """ Add new expence"""

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = ExpenceForm()
    else:
        # POST data submitted, process data
        form = ExpenceForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('web_travel_data:index')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'web_travel_data/new_expence.html', context)


def member_contribution(request, member_id):
    """Show a single member all his contributions"""

    member = Member.objects.get(id=member_id)
    contributions = member.contribution_set.order_by('date_added')
    context = {'member': member, 'contributions': contributions}
    return render(request, 'web_travel_data/member_contribution.html', context)


def expences(request):
    """ Show all expences"""

    expences = Expence.objects.order_by('date_added')
    context = {'expences': expences}
    return render(request, 'web_travel_data/expences.html', context)


def contributions(request):
    """ Show all contributions"""

    contributions = Contribution.objects.order_by('date_added')
    context = {'contributions': contributions}
    return render(request, 'web_travel_data/contributions.html', context)


def edit_member(request, member_id):
    """Edit an existing member"""

    member = Member.objects.get(id=member_id)

    if request.method != 'POST':
        # Initial request; prefill form with current entry.
        form = MemberForm(instance=member)
    else:
        # POST data submitted, process data
        form = MemberForm(instance=member, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('web_travel_data:members')

    context = {'member': member, 'form': form}
    return render(request, 'web_travel_data/edit_member.html', context)


def exeptions(request):
    """Show all exeptions"""
    exeptions = Exeption.objects.all()
    context = {'exeptions': exeptions}
    return render(request, 'web_travel_data/exeptions.html', context)


def new_exeption(request):
    """Add new exeption"""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = ExeptionForm()
    else:
        # POST data submitted, process data
        form = ExeptionForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('web_travel_data:exeptions')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'web_travel_data/new_exeption.html', context)


def edit_exeption(request, exeption_id):
    """Edit an exeption"""
    exeption = Exeption.objects.get(id=exeption_id)

    if request.method != 'POST':
        # Initial request; prefill form with current entry.
        form = ExeptionForm(instance=exeption)
    else:
        # POST data submitted, process data
        form = ExeptionForm(instance=exeption, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('web_travel_data:exeptions')

    context = {'exeption': exeption, 'form': form}
    return render(request, 'web_travel_data/edit_exeption.html', context)


def delete_exeption(request, exeption_id):
    """Delete an exeption"""
    exeption = Exeption.objects.get(id=exeption_id)

    if request.method == 'POST':
        exeption.delete()
        messages.success(request, "Exeption has been successfully deleted.")
        return redirect('web_travel_data:exeptions')

    context = {'exeption': exeption}
    return render(request, 'web_travel_data/delete_exeption.html', context)

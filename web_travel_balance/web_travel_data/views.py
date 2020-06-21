from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Member, Contribution, Expence, Exeption
from .forms import MemberForm, ContributionForm, ExpenceForm, ExeptionForm
from .balance_data import *


@login_required
def index(request):
    """The home page for Web Travel Balance"""

    contributions_per_member(request.user)
    expences_per_exeption(request.user)
    aee = all_exeption_expences(request.user)
    base_expences_per_member(request.user)
    balance_per_member(request.user)
    return_to_close(request.user)

    members = Member.objects.filter(owner=request.user).order_by('date_added')
    context = {'members': members}
    return render(request, 'web_travel_data/index.html', context)


@login_required
def new_member(request):
    """Add new member."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = MemberForm()
    else:
        # POST data submitted, process data
        form = MemberForm(data=request.POST)
        if form.is_valid():
            new_member = form.save(commit=False)
            new_member.owner = request.user
            form.save()
            return redirect('web_travel_data:index')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'web_travel_data/new_member.html', context)


@login_required
def contributions(request):
    """ Add new contribution for particular member"""

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = ContributionForm(user=request.user)
    else:
        # POST data submitted, process data
        form = ContributionForm(data=request.POST, user=request.user)
        if form.is_valid():
            new_contribution = form.save(commit=False)
            new_contribution.owner = request.user
            form.save()
            return redirect('web_travel_data:contributions')

    # Display a blank or invalid form.
    contributions = Contribution.objects.filter(
        owner=request.user).order_by('-date_added')

    context = {'form': form, 'contributions': contributions}
    return render(request, 'web_travel_data/contributions.html', context)


@login_required
def expences(request):
    """ Add new expence"""

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = ExpenceForm()
    else:
        # POST data submitted, process data
        form = ExpenceForm(data=request.POST)
        if form.is_valid():
            new_expence = form.save(commit=False)
            new_expence.owner = request.user
            form.save()
            return redirect('web_travel_data:expences')

    # Display a blank or invalid form.
    expences = Expence.objects.filter(
        owner=request.user).order_by('-date_added')

    context = {'form': form, 'expences': expences}
    return render(request, 'web_travel_data/expences.html', context)


@login_required
def member(request, member_id):
    """ Show all member contributions"""
    member = Member.objects.get(id=member_id)
    # Make sure the member belongs to the current user.
    if member.owner != request.user:
        raise Http404
    contributions = member.contribution_set.order_by('date_added')

    context = {'member': member, 'contributions': contributions}
    return render(request, 'web_travel_data/member.html', context)


@login_required
def edit_member(request, member_id):
    """Edit an existing member """

    member = Member.objects.get(id=member_id)
    if member.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request; prefill form with current entry.
        form = MemberForm(instance=member)
    else:
        # POST data submitted, process data
        form = MemberForm(instance=member, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Member info has been updated.")
            return redirect('web_travel_data:member', member_id)

    context = {'member': member, 'form': form}
    return render(request, 'web_travel_data/edit_member.html', context)


@login_required
def exeptions(request):
    """Show all exeptions"""
    aee = all_exeption_expences(request.user)
    exeptions = Exeption.objects.filter(owner=request.user)

    context = {'exeptions': exeptions, 'all_exeption_expences': aee}
    return render(request, 'web_travel_data/exeptions.html', context)


@login_required
def new_exeption(request):
    """Add new exeption"""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = ExeptionForm(user=request.user)
    else:
        # POST data submitted, process data
        form = ExeptionForm(data=request.POST, user=request.user)
        if form.is_valid():
            new_exeption = form.save(commit=False)
            new_exeption.owner = request.user
            form.save()
            return redirect('web_travel_data:exeptions')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'web_travel_data/new_exeption.html', context)


@login_required
def edit_exeption(request, exeption_id):
    """Edit an exeption"""
    exeption = Exeption.objects.get(id=exeption_id)
    if exeption.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request; prefill form with current entry.
        form = ExeptionForm(instance=exeption, user=request.user)
    else:
        # POST data submitted, process data
        form = ExeptionForm(instance=exeption,
                            data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('web_travel_data:exeptions')

    context = {'exeption': exeption, 'form': form}
    return render(request, 'web_travel_data/edit_exeption.html', context)


@login_required
def delete_exeption(request, exeption_id):
    """Delete an exeption"""
    exeption = Exeption.objects.get(id=exeption_id)
    if exeption.owner != request.user:
        raise Http404

    if request.method == 'POST':
        exeption.delete()
        messages.success(request, "Exeption has been successfully deleted.")
        return redirect('web_travel_data:exeptions')

    context = {'exeption': exeption}
    return render(request, 'web_travel_data/delete_exeption.html', context)


@login_required
def email_member_report(request, member_id):
    """Send email with member contribution data"""
    member = Member.objects.get(id=member_id)
    contributions = member.contribution_set.order_by('date_added')
    context = {'member': member, 'contributions': contributions, 'all_contributions': all_contributions(
        request.user), 'all_expences': all_expences(request.user), 'balance': balance(request.user)}
    if member.owner != request.user:
        raise Http404

    if request.method == 'POST':
        html_content = render_to_string(
            'web_travel_data/member_email.html', context)
        msg = EmailMultiAlternatives('TeaMWallet member info', create_member_report(
            member_id), 'cutterw7@gmail.com', [member.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        messages.success(request, "Email has been sent.")
        return redirect('web_travel_data:member', member.id)

    return render(request, 'web_travel_data/email_member_report.html', context)


@login_required
def delete_member(request, member_id):
    """ Delete member info"""
    member = Member.objects.get(id=member_id)
    if member.owner != request.user:
        raise Http404

    if request.method == 'POST':
        member.delete()
        messages.success(request, "Member has been successfully deleted.")
        return redirect('web_travel_data:index')

    context = {'member': member}
    return render(request, 'web_travel_data/delete_member.html', context)

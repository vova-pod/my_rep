from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from .models import Member, Contribution, Expence, Exeption, Team
from .forms import MemberForm, ContributionForm, ExpenceForm, ExeptionForm, TeamForm
from .balance_data import *


@login_required
def index(request):
    """ Page to manage user and teams"""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TeamForm()
    else:
        # POST data submitted, process data
        form = TeamForm(data=request.POST)
        if form.is_valid():
            new_team = form.save(commit=False)
            new_team.owner = request.user
            form.save()
            return redirect('web_travel_data:index')

    # Display a blank or invalid form.
    teams = Team.objects.filter(owner=request.user).order_by('date_added')
    context = {'form': form, 'teams': teams}
    return render(request, 'web_travel_data/index.html', context)


@login_required
def balance(request, team_id):
    """The home page for Web Travel Balance"""
    team = Team.objects.get(id=team_id)
    if team.owner != request.user:
        raise Http404
    team_contribution = all_contributions(team)
    team_expences = all_expences(team)
    team_balance = all_balance(team)
    contributions_per_member(team)
    expences_per_exeption(team)
    all_exeption_expences(team)
    base_expences_per_member(team)
    balance_per_member(team)
    return_to_close(team)
    members = Member.objects.filter(owner=team).order_by('date_added')
    context = {'members': members, 'team': team, 'team_balance': team_balance,
               'team_contribution': team_contribution, 'team_expences': team_expences}
    return render(request, 'web_travel_data/balance.html', context)


@login_required
def new_member(request, team_id):
    """Add new member."""
    team = Team.objects.get(id=team_id)
    if team.owner != request.user:
        raise Http404
    team_contribution = all_contributions(team)
    team_expences = all_expences(team)
    team_balance = all_balance(team)
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = MemberForm()
    else:
        # POST data submitted, process data
        form = MemberForm(data=request.POST)
        if form.is_valid():
            new_member = form.save(commit=False)
            new_member.owner = team
            form.save()
            return redirect('web_travel_data:balance', team_id)

    # Display a blank or invalid form.
    context = {'form': form, 'team': team, 'team_balance': team_balance,
               'team_contribution': team_contribution, 'team_expences': team_expences}
    return render(request, 'web_travel_data/new_member.html', context)


@login_required
def contributions(request, team_id):
    """ Add new contribution for particular member"""
    team = Team.objects.get(id=team_id)
    if team.owner != request.user:
        raise Http404
    team_contribution = all_contributions(team)
    team_expences = all_expences(team)
    team_balance = all_balance(team)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = ContributionForm(team=team)
    else:
        # POST data submitted, process data
        form = ContributionForm(data=request.POST, team=team)
        if form.is_valid():
            new_contribution = form.save(commit=False)
            new_contribution.owner = team
            form.save()
            return redirect('web_travel_data:contributions', team_id)

    # Display a blank or invalid form.
    contributions = Contribution.objects.filter(
        owner=team).order_by('-date_added')

    context = {'form': form, 'contributions': contributions, 'team': team,
               'team_balance': team_balance, 'team_contribution': team_contribution, 'team_expences': team_expences}
    return render(request, 'web_travel_data/contributions.html', context)


@login_required
def expences(request, team_id):
    """ Add new expence"""
    team = Team.objects.get(id=team_id)
    if team.owner != request.user:
        raise Http404
    team_contribution = all_contributions(team)
    team_expences = all_expences(team)
    team_balance = all_balance(team)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = ExpenceForm()
    else:
        # POST data submitted, process data
        form = ExpenceForm(data=request.POST)
        if form.is_valid():
            new_expence = form.save(commit=False)
            new_expence.owner = team
            form.save()
            return redirect('web_travel_data:expences', team_id)

    # Display a blank or invalid form.
    expences = Expence.objects.filter(
        owner=team).order_by('-date_added')

    context = {'form': form, 'expences': expences, 'team': team,
               'team_balance': team_balance, 'team_contribution': team_contribution, 'team_expences': team_expences}
    return render(request, 'web_travel_data/expences.html', context)


@login_required
def member(request, member_id, team_id):
    """ Show all member contributions"""
    team = Team.objects.get(id=team_id)
    if team.owner != request.user:
        raise Http404
    team_contribution = all_contributions(team)
    team_expences = all_expences(team)
    team_balance = all_balance(team)
    member = Member.objects.get(id=member_id)
    # Make sure the member belongs to the current user.
    if member.owner != team:
        raise Http404
    contributions = member.contribution_set.order_by('date_added')

    context = {'member': member, 'contributions': contributions, 'team': team,
               'team_balance': team_balance, 'team_contribution': team_contribution, 'team_expences': team_expences}
    return render(request, 'web_travel_data/member.html', context)


@login_required
def edit_member(request, member_id, team_id):
    """Edit an existing member """
    team = Team.objects.get(id=team_id)
    if team.owner != request.user:
        raise Http404
    team_contribution = all_contributions(team)
    team_expences = all_expences(team)
    team_balance = all_balance(team)

    member = Member.objects.get(id=member_id)
    if member.owner != team:
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
            return redirect('web_travel_data:member', team_id, member_id)

    context = {'member': member, 'form': form, 'team': team,
               'team_balance': team_balance, 'team_contribution': team_contribution, 'team_expences': team_expences}
    return render(request, 'web_travel_data/edit_member.html', context)


@login_required
def exeptions(request, team_id):
    """Show all exeptions"""
    team = Team.objects.get(id=team_id)
    if team.owner != request.user:
        raise Http404
    team_contribution = all_contributions(team)
    team_expences = all_expences(team)
    team_balance = all_balance(team)
    exeptions = Exeption.objects.filter(owner=team)
    expences_per_exeption(team)
    context = {'exeptions': exeptions, 'team': team, 'team_balance': team_balance,
               'team_contribution': team_contribution, 'team_expences': team_expences}
    return render(request, 'web_travel_data/exeptions.html', context)


@login_required
def new_exeption(request, team_id):
    """Add new exeption"""
    team = Team.objects.get(id=team_id)
    if team.owner != request.user:
        raise Http404
    team_contribution = all_contributions(team)
    team_expences = all_expences(team)
    team_balance = all_balance(team)
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = ExeptionForm(team=team, exeption_id=None)
    else:
        # POST data submitted, process data
        form = ExeptionForm(data=request.POST, team=team, exeption_id=None)
        if form.is_valid():
            new_exeption = form.save(commit=False)
            new_exeption.owner = team
            form.save()
            return redirect('web_travel_data:exeptions', team_id)

    # Display a blank or invalid form.
    context = {'form': form, 'team': team, 'team_balance': team_balance,
               'team_contribution': team_contribution, 'team_expences': team_expences}
    return render(request, 'web_travel_data/new_exeption.html', context)


@login_required
def edit_exeption(request, exeption_id, team_id):
    """Edit an exeption"""
    team = Team.objects.get(id=team_id)
    if team.owner != request.user:
        raise Http404
    team_contribution = all_contributions(team)
    team_expences = all_expences(team)
    team_balance = all_balance(team)
    exeption = Exeption.objects.get(id=exeption_id)
    if exeption.owner != team:
        raise Http404

    if request.method != 'POST':
        # Initial request; prefill form with current entry.
        form = ExeptionForm(instance=exeption, team=team,
                            exeption_id=exeption_id)
    else:
        # POST data submitted, process data
        form = ExeptionForm(instance=exeption,
                            data=request.POST, team=team, exeption_id=exeption_id)
        if form.is_valid():
            form.save()
            return redirect('web_travel_data:exeptions', team_id)

    context = {'exeption': exeption, 'form': form, 'team': team,
               'team_balance': team_balance, 'team_contribution': team_contribution, 'team_expences': team_expences}
    return render(request, 'web_travel_data/edit_exeption.html', context)


@login_required
def delete_exeption(request, exeption_id, team_id):
    """Delete an exeption"""
    team = Team.objects.get(id=team_id)
    if team.owner != request.user:
        raise Http404
    team_contribution = all_contributions(team)
    team_expences = all_expences(team)
    team_balance = all_balance(team)
    exeption = Exeption.objects.get(id=exeption_id)
    if exeption.owner != team:
        raise Http404

    if request.method == 'POST':
        exeption.delete()
        message = _("Exeption has been successfully deleted.")
        messages.success(request, message)
        return redirect('web_travel_data:exeptions', team_id)

    context = {'exeption': exeption, 'team': team, 'team_balance': team_balance,
               'team_contribution': team_contribution, 'team_expences': team_expences}
    return render(request, 'web_travel_data/delete_exeption.html', context)


@login_required
def email_member_report(request, member_id, team_id):
    """Send email with member contribution data"""
    team = Team.objects.get(id=team_id)
    if team.owner != request.user:
        raise Http404
    team_contribution = all_contributions(team)
    team_expences = all_expences(team)
    team_balance = all_balance(team)
    member = Member.objects.get(id=member_id)
    if member.owner != team:
        raise Http404
    contributions = member.contribution_set.order_by('date_added')
    context = {'member': member, 'contributions': contributions,
               'team_balance': team_balance,
               'team_contribution': team_contribution,
               'team_expences': team_expences,
               'team': team
               }

    if member.email is None:
        if request.method != 'POST':
            # Initial request; prefill form with current entry.
            form = MemberForm(instance=member)
        else:
            # POST data submitted, process data
            form = MemberForm(instance=member, data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Member info has been updated.")
                return redirect('web_travel_data:email_member_report', team_id, member_id)
        context = {'member': member, 'contributions': contributions,
                   'team_balance': team_balance,
                   'team_contribution': team_contribution,
                   'team_expences': team_expences,
                   'team': team, 'form': form
                   }

    else:
        if request.method == 'POST':
            html_content = render_to_string(
                'web_travel_data/member_email.html', context)
            subject = _('TeamWallet info for ' +
                        str(member.name) + ' from ' + str(team.name))
            msg = EmailMultiAlternatives(subject, create_member_report(
                member_id), 'cutterw7@gmail.com', [member.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            message = _("Email has been sent.")
            messages.success(request, message)
            return redirect('web_travel_data:member', team_id, member.id)

    return render(request, 'web_travel_data/email_member_report.html', context)


@login_required
def delete_member(request, member_id, team_id):
    """ Delete member info"""
    team = Team.objects.get(id=team_id)
    if team.owner != request.user:
        raise Http404
    team_contribution = all_contributions(team)
    team_expences = all_expences(team)
    team_balance = all_balance(team)
    member = Member.objects.get(id=member_id)
    if member.owner != team:
        raise Http404

    if request.method == 'POST':
        member.delete()
        message = _("Member has been successfully deleted.")
        messages.success(request, message)
        return redirect('web_travel_data:balance', team_id)

    context = {'member': member, 'team': team, 'team_balance': team_balance,
               'team_contribution': team_contribution, 'team_expences': team_expences}
    return render(request, 'web_travel_data/delete_member.html', context)


@login_required
def edit_contribution(request, contribution_id, team_id):
    """Edit an exeption"""
    team = Team.objects.get(id=team_id)
    if team.owner != request.user:
        raise Http404
    team_contribution = all_contributions(team)
    team_expences = all_expences(team)
    team_balance = all_balance(team)
    contribution = Contribution.objects.get(id=contribution_id)
    if contribution.owner != team:
        raise Http404

    if request.method != 'POST':
        # Initial request; prefill form with current entry.
        form = ContributionForm(instance=contribution, team=team)
    else:
        # POST data submitted, process data
        form = ContributionForm(instance=contribution,
                                data=request.POST, team=team)
        if form.is_valid():
            form.save()
            return redirect('web_travel_data:contributions', team_id)

    context = {'contribution': contribution, 'form': form, 'team': team,
               'team_balance': team_balance, 'team_contribution': team_contribution, 'team_expences': team_expences}
    return render(request, 'web_travel_data/edit_contribution.html', context)


@login_required
def edit_expence(request, expence_id, team_id):
    """Edit an exeption"""
    team = Team.objects.get(id=team_id)
    if team.owner != request.user:
        raise Http404
    team_contribution = all_contributions(team)
    team_expences = all_expences(team)
    team_balance = all_balance(team)
    expence = Expence.objects.get(id=expence_id)
    if expence.owner != team:
        raise Http404

    if request.method != 'POST':
        # Initial request; prefill form with current entry.
        form = ExpenceForm(instance=expence)
    else:
        # POST data submitted, process data
        form = ExpenceForm(instance=expence,
                           data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('web_travel_data:expences', team_id)

    context = {'expence': expence, 'form': form, 'team': team,
               'team_balance': team_balance, 'team_contribution': team_contribution, 'team_expences': team_expences}
    return render(request, 'web_travel_data/edit_expence.html', context)


@login_required
def delete_team(request, team_id):
    """ Delete member info"""
    team = Team.objects.get(id=team_id)
    if team.owner != request.user:
        raise Http404
    team_contribution = all_contributions(team)
    team_expences = all_expences(team)
    team_balance = all_balance(team)

    if request.method == 'POST':
        team.delete()
        message = _("Team has been successfully deleted.")
        messages.success(request, message)
        return redirect('web_travel_data:index')

    context = {'team': team, 'team_balance': team_balance,
               'team_contribution': team_contribution, 'team_expences': team_expences}
    return render(request, 'web_travel_data/delete_team.html', context)


@login_required
def delete_contribution(request, contribution_id, team_id):
    """Delete a contribution"""
    team = Team.objects.get(id=team_id)
    if team.owner != request.user:
        raise Http404
    team_contribution = all_contributions(team)
    team_expences = all_expences(team)
    team_balance = all_balance(team)
    contribution = Contribution.objects.get(id=contribution_id)
    if contribution.owner != team:
        raise Http404

    if request.method == 'POST':
        contribution.delete()
        message = _("Contribution has been successfully deleted.")
        messages.success(request, message)
        return redirect('web_travel_data:contributions', team_id)

    context = {'contribution': contribution, 'team': team, 'team_balance': team_balance,
               'team_contribution': team_contribution, 'team_expences': team_expences}
    return render(request, 'web_travel_data/delete_contribution.html', context)


@login_required
def delete_expence(request, expence_id, team_id):
    """Delete an expence"""
    team = Team.objects.get(id=team_id)
    if team.owner != request.user:
        raise Http404
    team_contribution = all_contributions(team)
    team_expences = all_expences(team)
    team_balance = all_balance(team)
    expence = Expence.objects.get(id=expence_id)
    if expence.owner != team:
        raise Http404

    if request.method == 'POST':
        expence.delete()
        message = _("Expence has been successfully deleted.")
        messages.success(request, message)
        return redirect('web_travel_data:expences', team_id)

    context = {'expence': expence, 'team': team, 'team_balance': team_balance,
               'team_contribution': team_contribution, 'team_expences': team_expences}
    return render(request, 'web_travel_data/delete_expence.html', context)
from django.shortcuts import render, redirect
from .models import Member, Contribution, Expence
from .forms import MemberForm, ContributionForm, ExpenceForm


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
    members = Member.objects.order_by('date_added')
    context = {'balance': balance(), 'contributed': all_contributions(), 'spent': all_expences(),
               'members': members, }
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
    """ Add new contribution for particular member"""

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

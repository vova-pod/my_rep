"""Defines URL patterns for web_travel_data"""

from django.urls import path

from . import views

app_name = 'web_travel_data'

urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Page for adding new member
    path('new_member/team_<int:team_id>/', views.new_member, name='new_member'),
    # Page for adding new contribution
    path('contributions/team_<int:team_id>/',
         views.contributions, name='contributions'),
    # Detail page for member's contributions
    path('member/team_<int:team_id>/member_<int:member_id>/',
         views.member, name='member'),
    # Page shows all spendings
    path('expences/team_<int:team_id>/', views.expences, name='expences'),
    # Page to show exeptions
    path('exeptions/team_<int:team_id>/', views.exeptions, name='exeptions'),
    # Page for adding new exeptions
    path('new_exeption/team_<int:team_id>/',
         views.new_exeption, name='new_exeption'),
    # Page to edit exeption
    path('edit_exeption/team_<int:team_id>/edit_exeption_<int:exeption_id>',
         views.edit_exeption, name='edit_exeption'),
    # page to delete exeption
    path('delete_exeption/team_<int:team_id>/delete_exeption_<int:exeption_id>',
         views.delete_exeption, name='delete_exeption'),
    path('email_member_report/team_<int:team_id>/<int:member_id>',
         views.email_member_report, name='email_member_report'),
    # page to delete member
    path('delete_member/team_<int:team_id>/delete_member_<int:member_id>',
         views.delete_member, name='delete_member'),
    # Page to edit member
    path('edit_member/team_<int:team_id>/edit_member_<int:member_id>',
         views.edit_member, name='edit_member'),
    # Page to manage user and teams
    path('balance/team_<int:team_id>/', views.balance, name='balance'),
    # Page to edit contribution
    path('edit_contribution/team_<int:team_id>/contribution_<int:contribution_id>/',
         views.edit_contribution, name='edit_contribution'),
    # Page to edit spending
    path('edit_expence/team_<int:team_id>/expence_<int:expence_id>/',
         views.edit_expence, name='edit_expence'),
    # Page to delete team
    path('delete_team/team_<int:team_id>',
         views.delete_team, name='delete_team'),
    # Page to delete contribution
    path('delete_contribution/team_<int:team_id>/delete_contribution_<int:contribution_id>',
         views.delete_contribution, name='delete_contribution'),
    # Page to delete spending
    path('delete_expence/team_<int:team_id>/delete_expence_<int:expence_id>',
         views.delete_expence, name='delete_expence'),
    # Page for offline view
    path('base', views.base, name='base'),


]

"""Defines URL patterns for web_travel_data"""

from django.urls import path

from . import views

app_name = 'web_travel_data'

urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Page that shows all mambers
    path('members/', views.members, name='members'),
    # Page for adding new member
    path('new_member/', views.new_member, name='new_member'),
    # Page for adding new contribution
    path('new_contribution/', views.new_contribution, name='new_contribution'),
    # Page for adding new spending
    path('new_expence/', views.new_expence, name='new_expence'),
    # Detail page for member's contributions
    path('members/member_<int:member_id>_contribution/',
         views.member_contribution, name='member_contribution'),
    # Page shows all spendings
    path('expences/', views.expences, name='expences'),
    # Page shows all contributions
    path('contributions/', views.contributions, name='contributions'),
    # Page to edit member info
    path('edit_member/edit_member_<int:member_id>/',
         views.edit_member, name='edit_member'),
    # Page to show exeptions
    path('exeptions/', views.exeptions, name='exeptions'),
    # Page for adding new exeptions
    path('new_exeption/', views.new_exeption, name='new_exeption'),
    # Page to edit exeption
    path('edit_exeption/edit_exeption_<int:exeption_id>',
         views.edit_exeption, name='edit_exeption'),
    path('delete_exeption/delete_exeption_<int:exeption_id>',
         views.delete_exeption, name='delete_exeption'),
    path('email_member_report/<int:member_id>',
         views.email_member_report, name='email_member_report'),

]

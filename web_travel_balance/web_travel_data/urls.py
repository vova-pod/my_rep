"""Defines URL patterns for web_travel_data"""

from django.urls import path

from . import views

app_name = 'web_travel_data'

urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Page for adding new member
    path('new_member/', views.new_member, name='new_member'),
    # Page for adding new contribution
    path('contributions/', views.contributions, name='contributions'),
    # Detail page for member's contributions
    path('members/member_<int:member_id>/',
         views.member, name='member'),
    # Page shows all spendings
    path('expences/', views.expences, name='expences'),
    # Page to show exeptions
    path('exeptions/', views.exeptions, name='exeptions'),
    # Page for adding new exeptions
    path('new_exeption/', views.new_exeption, name='new_exeption'),
    # Page to edit exeption
    path('edit_exeption/edit_exeption_<int:exeption_id>',
         views.edit_exeption, name='edit_exeption'),
    # page to delete exeption
    path('delete_exeption/delete_exeption_<int:exeption_id>',
         views.delete_exeption, name='delete_exeption'),
    path('email_member_report/<int:member_id>',
         views.email_member_report, name='email_member_report'),
    # page to delete member
    path('delete_member/delete_member_<int:member_id>',
         views.delete_member, name='delete_member')

]

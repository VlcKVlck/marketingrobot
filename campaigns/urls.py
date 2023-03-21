from django.urls import path

from . import views

urlpatterns = [
    path('', views.main_campaigns, name='main_campaigns'),
    path('newtemplate/', views.new_template, name='newtemplate'),
    path('newcampaign/', views.send_campaign_emails, name='newcampaign'),
    path('success/', views.success, name='success'),
]
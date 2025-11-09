"""
URL configuration for the Voting System application.

This module defines all URL patterns for the votes_app, including:
- Home page (voting form)
- Vote processing
- Results display
- Analytics dashboard
- Chart generation
- CSV export
"""

from django.urls import path
from . import views

# Application namespace
app_name = 'votes_app'

urlpatterns = [
    # Home page with voting form
    path('', views.home, name='home'),
    
    # Vote processing endpoint
    path('vote/', views.vote, name='vote'),
    
    # Results page
    path('results/', views.results, name='results'),
    
    # Analytics page with statistics and chart
    path('analytics/', views.analytics, name='analytics'),
    
    # Chart generation endpoints (returns JSON with base64 image)
    path('chart/', views.generate_chart, name='generate_chart'),
    path('chart/pie/', views.generate_pie_chart, name='generate_pie_chart'),
    path('chart/horizontal/', views.generate_horizontal_bar_chart, name='generate_horizontal_chart'),
    path('chart/party/', views.generate_party_chart, name='generate_party_chart'),
    path('chart/line/', views.generate_line_chart, name='generate_line_chart'),
    
    # CSV export endpoint
    path('export/', views.export_results, name='export_results'),
]


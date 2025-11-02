"""
Admin configuration for the Voting System models.

This module registers all models (Candidate, Voter, Vote) with the Django admin
interface, allowing CRUD operations through the admin panel.
"""

from django.contrib import admin
from .models import Candidate, Voter, Vote


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Candidate model.
    
    Features:
    - Display name, party, and creation date in list view
    - Filter by party
    - Search by name and party
    """
    list_display = ['name', 'party', 'created_at']
    list_filter = ['party', 'created_at']
    search_fields = ['name', 'party']
    ordering = ['name']


@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Voter model.
    
    Features:
    - Display name, UID, and registration date in list view
    - Filter by registration date
    - Search by name and UID
    """
    list_display = ['name', 'uid', 'registered_on']
    list_filter = ['registered_on']
    search_fields = ['name', 'uid']
    ordering = ['-registered_on']


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Vote model.
    
    Features:
    - Display voter, candidate, and timestamp in list view
    - Filter by candidate and timestamp
    - Search by voter and candidate names
    - Read-only fields for timestamp
    """
    list_display = ['voter', 'candidate', 'timestamp']
    list_filter = ['candidate', 'timestamp']
    search_fields = ['voter__name', 'candidate__name']
    ordering = ['-timestamp']
    readonly_fields = ['timestamp']  # Timestamp is auto-generated

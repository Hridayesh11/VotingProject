"""
Models for the Voting System application.

This module defines three main models:
- Candidate: Represents a political candidate with name and party
- Voter: Represents a registered voter with unique ID and registration date
- Vote: Represents a vote cast by a voter for a specific candidate
"""

from django.db import models
from django.core.exceptions import ValidationError


class Candidate(models.Model):
    """
    Model representing a political candidate.
    
    Attributes:
        name (str): Full name of the candidate
        party (str): Political party affiliation
        created_at (datetime): Timestamp when candidate was added
    """
    name = models.CharField(max_length=200, help_text="Full name of the candidate")
    party = models.CharField(max_length=100, help_text="Political party affiliation")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # Order candidates by name for consistency
        ordering = ['name']
    
    def __str__(self):
        """String representation of the candidate."""
        return f"{self.name} ({self.party})"


class Voter(models.Model):
    """
    Model representing a registered voter.
    
    Attributes:
        uid (str): Unique identifier for the voter (e.g., national ID)
        name (str): Full name of the voter
        registered_on (datetime): When the voter registered
    """
    uid = models.CharField(max_length=50, unique=True, help_text="Unique voter identifier")
    name = models.CharField(max_length=200, help_text="Full name of the voter")
    registered_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # Order voters by registration date
        ordering = ['-registered_on']
    
    def __str__(self):
        """String representation of the voter."""
        return f"{self.name} (UID: {self.uid})"


class Vote(models.Model):
    """
    Model representing a vote cast by a voter for a candidate.
    
    Attributes:
        voter (Voter): Foreign key to the voter who cast the vote
        candidate (Candidate): Foreign key to the candidate being voted for
        timestamp (datetime): When the vote was cast
    
    Constraints:
        - One voter can only vote once (enforced at database level)
    """
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE, related_name='votes')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='votes')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # Enforce one vote per voter at database level
        unique_together = [['voter']]
        # Order votes by timestamp
        ordering = ['-timestamp']
    
    def __str__(self):
        """String representation of the vote."""
        return f"{self.voter.name} voted for {self.candidate.name}"
    
    def clean(self):
        """
        Validate that a voter hasn't already voted.
        This provides an additional layer of validation beyond the database constraint.
        """
        if self.pk is None and Vote.objects.filter(voter=self.voter).exists():
            raise ValidationError("This voter has already cast a vote.")
    
    def save(self, *args, **kwargs):
        """Override save to run clean validation."""
        self.full_clean()
        super().save(*args, **kwargs)

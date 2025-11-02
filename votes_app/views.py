"""
Views for the Voting System application.

This module contains all view functions:
- home: Display voting form
- vote: Process vote submission
- results: Display voting results
- analytics: Display statistics and charts
- export_results: Export votes to CSV
- generate_chart: Generate matplotlib chart dynamically
"""

import io
import base64

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Q

from .models import Candidate, Voter, Vote


def home(request):
    """
    Home page view displaying the voting form.
    
    GET: Display form with voter UID input and candidate selection
    """
    # Get all candidates for the dropdown
    candidates = Candidate.objects.all().order_by('name')
    
    # Get voter name if UID is provided
    voter_name = None
    voter_uid = request.GET.get('uid', '')
    
    if voter_uid:
        try:
            voter = Voter.objects.get(uid=voter_uid)
            voter_name = voter.name
        except Voter.DoesNotExist:
            messages.error(request, "Voter UID not found. Please check your UID or register first.")
    
    context = {
        'candidates': candidates,
        'voter_name': voter_name,
        'voter_uid': voter_uid,
    }
    return render(request, 'votes_app/index.html', context)


def vote(request):
    """
    Process vote submission.
    
    POST: Save vote if valid, prevent duplicates
    GET: Redirect to home page
    """
    if request.method == 'POST':
        voter_uid = request.POST.get('voter_uid')
        candidate_id = request.POST.get('candidate_id')
        voter_name = request.POST.get('voter_name')
        
        # Validate that required fields are present
        if not all([voter_uid, candidate_id]):
            messages.error(request, "Please provide all required information.")
            return redirect('home')
        
        try:
            # Get or create voter
            voter, created = Voter.objects.get_or_create(
                uid=voter_uid,
                defaults={'name': voter_name or f"Voter {voter_uid}"}
            )
            
            # Check if voter has already voted
            if Vote.objects.filter(voter=voter).exists():
                messages.warning(request, f"Voter {voter.name} has already cast their vote!")
                return redirect('results')
            
            # Get candidate
            candidate = get_object_or_404(Candidate, id=candidate_id)
            
            # Create vote
            Vote.objects.create(voter=voter, candidate=candidate)
            
            messages.success(request, f"Vote cast successfully for {candidate.name}!")
            return redirect('results')
            
        except Exception as e:
            messages.error(request, f"Error processing vote: {str(e)}")
            return redirect('home')
    
    # GET request - redirect to home
    return redirect('home')


def results(request):
    """
    Display voting results page.
    
    Shows:
    - Total number of votes
    - Votes per candidate
    - Percentage breakdown
    """
    # Get total votes
    total_votes = Vote.objects.count()
    
    # Get votes per candidate with counts
    candidate_votes = (
        Candidate.objects
        .annotate(vote_count=Count('votes'))
        .order_by('-vote_count', 'name')
    )
    
    # Calculate percentages
    for candidate in candidate_votes:
        if total_votes > 0:
            candidate.percentage = round((candidate.vote_count / total_votes) * 100, 2)
        else:
            candidate.percentage = 0
    
    context = {
        'total_votes': total_votes,
        'candidate_votes': candidate_votes,
    }
    return render(request, 'votes_app/results.html', context)


def analytics(request):
    """
    Display analytics page with statistics and chart.
    
    Computes:
    - Mean votes per candidate
    - Median votes per candidate
    - Displays matplotlib chart
    """
    # Get vote counts per candidate
    candidate_votes = (
        Candidate.objects
        .annotate(vote_count=Count('votes'))
        .order_by('-vote_count', 'name')
    )
    
    # Extract vote counts as numpy array for statistical analysis
    vote_counts = np.array([cv.vote_count for cv in candidate_votes])
    
    # Calculate statistics
    mean_votes = np.mean(vote_counts) if len(vote_counts) > 0 else 0
    median_votes = np.median(vote_counts) if len(vote_counts) > 0 else 0
    
    context = {
        'candidate_votes': candidate_votes,
        'mean_votes': round(mean_votes, 2),
        'median_votes': round(median_votes, 2),
        'total_candidates': len(candidate_votes),
    }
    return render(request, 'votes_app/analytics.html', context)


def export_results(request):
    """
    Export voting results to CSV file.
    
    Uses pandas to create a DataFrame and export to CSV format.
    """
    # Get all votes with related data
    votes = Vote.objects.select_related('voter', 'candidate').order_by('-timestamp')
    
    # Convert to pandas DataFrame
    data = {
        'Voter UID': [vote.voter.uid for vote in votes],
        'Voter Name': [vote.voter.name for vote in votes],
        'Candidate': [vote.candidate.name for vote in votes],
        'Party': [vote.candidate.party for vote in votes],
        'Timestamp': [vote.timestamp.strftime('%Y-%m-%d %H:%M:%S') for vote in votes],
    }
    
    df = pd.DataFrame(data)
    
    # Create HTTP response with CSV content
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="voting_results.csv"'
    
    # Write DataFrame to CSV
    df.to_csv(response, index=False)
    
    return response


def generate_chart(request):
    """
    Generate a matplotlib bar chart dynamically and return as image.
    
    Creates a bar chart showing votes per candidate and returns it
    as a base64-encoded image that can be displayed in HTML.
    """
    # Get vote counts per candidate
    candidate_votes = (
        Candidate.objects
        .annotate(vote_count=Count('votes'))
        .order_by('-vote_count', 'name')
    )
    
    # Prepare data for plotting
    candidates = [cv.name for cv in candidate_votes]
    votes = [cv.vote_count for cv in candidate_votes]
    
    # Create matplotlib figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create bar chart
    bars = ax.bar(candidates, votes, color='skyblue', edgecolor='navy', alpha=0.7)
    
    # Customize chart
    ax.set_xlabel('Candidates', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Votes', fontsize=12, fontweight='bold')
    ax.set_title('Voting Results by Candidate', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height,
                f'{int(height)}', ha='center', va='bottom')
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save plot to BytesIO buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    buffer.seek(0)
    
    # Encode image to base64
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    
    # Close plot to free memory
    plt.close(fig)
    
    # Return JSON response with base64 image
    return JsonResponse({'image': f'data:image/png;base64,{image_base64}'})

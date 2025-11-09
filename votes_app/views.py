"""
Views for the Voting System application.

This module contains all view functions:
- home: Display voting form
- vote: Process vote submission
- results: Display voting results
- analytics: Display statistics and charts
- export_results: Export votes to CSV
- generate_chart: Generate matplotlib bar chart dynamically
- generate_pie_chart: Generate pie chart showing vote distribution
- generate_horizontal_bar_chart: Generate horizontal bar chart
- generate_party_chart: Generate bar chart grouped by political party
- generate_line_chart: Generate line chart showing voting trends over time
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
            return redirect('votes_app:home')
        
        try:
            # Get or create voter
            voter, created = Voter.objects.get_or_create(
                uid=voter_uid,
                defaults={'name': voter_name or f"Voter {voter_uid}"}
            )
            
            # Check if voter has already voted
            if Vote.objects.filter(voter=voter).exists():
                messages.warning(request, f"Voter {voter.name} has already cast their vote!")
                return redirect('votes_app:results')
            
            # Get candidate
            candidate = get_object_or_404(Candidate, id=candidate_id)
            
            # Create vote
            Vote.objects.create(voter=voter, candidate=candidate)
            
            messages.success(request, f"Vote cast successfully for {candidate.name}!")
            return redirect('votes_app:results')
            
        except Exception as e:
            messages.error(request, f"Error processing vote: {str(e)}")
            return redirect('votes_app:home')
    
    # GET request - redirect to home
    return redirect('votes_app:home')


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


def generate_pie_chart(request):
    """
    Generate a matplotlib pie chart showing vote distribution.
    
    Creates a pie chart showing percentage of votes per candidate.
    """
    # Get vote counts per candidate
    candidate_votes = (
        Candidate.objects
        .annotate(vote_count=Count('votes'))
        .filter(vote_count__gt=0)  # Only show candidates with votes
        .order_by('-vote_count')
    )
    
    if not candidate_votes:
        # Return empty chart if no votes
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.text(0.5, 0.5, 'No votes yet', ha='center', va='center', fontsize=16)
        ax.axis('off')
    else:
        # Prepare data for plotting
        candidates = [cv.name for cv in candidate_votes]
        votes = [cv.vote_count for cv in candidate_votes]
        
        # Create pie chart
        fig, ax = plt.subplots(figsize=(10, 8))
        colors = plt.cm.Set3(range(len(candidates)))
        
        wedges, texts, autotexts = ax.pie(
            votes, 
            labels=candidates, 
            autopct='%1.1f%%',
            colors=colors,
            startangle=90,
            textprops={'fontsize': 10, 'fontweight': 'bold'}
        )
        
        # Customize title
        ax.set_title('Vote Distribution by Candidate', fontsize=14, fontweight='bold', pad=20)
        
        # Make percentage text more visible
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
    
    plt.tight_layout()
    
    # Save plot to BytesIO buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    buffer.seek(0)
    
    # Encode image to base64
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close(fig)
    
    return JsonResponse({'image': f'data:image/png;base64,{image_base64}'})


def generate_horizontal_bar_chart(request):
    """
    Generate a horizontal bar chart showing votes per candidate.
    
    Creates a horizontal bar chart for better readability with many candidates.
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
    fig, ax = plt.subplots(figsize=(10, max(6, len(candidates) * 0.5)))
    
    # Create horizontal bar chart
    bars = ax.barh(candidates, votes, color='lightcoral', edgecolor='darkred', alpha=0.7)
    
    # Customize chart
    ax.set_xlabel('Number of Votes', fontsize=12, fontweight='bold')
    ax.set_ylabel('Candidates', fontsize=12, fontweight='bold')
    ax.set_title('Voting Results - Horizontal Bar Chart', fontsize=14, fontweight='bold')
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height() / 2.,
                f' {int(width)}', ha='left', va='center', fontweight='bold')
    
    plt.tight_layout()
    
    # Save plot to BytesIO buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    buffer.seek(0)
    
    # Encode image to base64
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close(fig)
    
    return JsonResponse({'image': f'data:image/png;base64,{image_base64}'})


def generate_party_chart(request):
    """
    Generate a bar chart showing votes grouped by political party.
    
    Creates a chart showing total votes per party.
    """
    # Get vote counts grouped by party
    from django.db.models import Sum
    party_votes = (
        Candidate.objects
        .annotate(vote_count=Count('votes'))
        .values('party')
        .annotate(total_votes=Sum('vote_count'))
        .order_by('-total_votes')
    )
    
    if not party_votes:
        # Return empty chart if no votes
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, 'No votes yet', ha='center', va='center', fontsize=16)
        ax.axis('off')
    else:
        # Prepare data for plotting
        parties = [pv['party'] for pv in party_votes]
        votes = [pv['total_votes'] for pv in party_votes]
        
        # Create matplotlib figure and axis
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create bar chart with different colors for each party
        colors = plt.cm.Pastel1(range(len(parties)))
        bars = ax.bar(parties, votes, color=colors, edgecolor='black', alpha=0.8)
        
        # Customize chart
        ax.set_xlabel('Political Party', fontsize=12, fontweight='bold')
        ax.set_ylabel('Total Votes', fontsize=12, fontweight='bold')
        ax.set_title('Voting Results by Political Party', fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height,
                    f'{int(height)}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    
    # Save plot to BytesIO buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    buffer.seek(0)
    
    # Encode image to base64
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close(fig)
    
    return JsonResponse({'image': f'data:image/png;base64,{image_base64}'})


def generate_line_chart(request):
    """
    Generate a line chart showing voting trends over time.
    
    Creates a line chart showing votes cast over time or vote distribution by candidate.
    """
    # Get all votes ordered by timestamp
    votes = Vote.objects.select_related('candidate').order_by('timestamp')
    
    if votes.exists():
        # Create time series data - group by date
        from django.db.models import Count
        from django.db.models.functions import TruncDate
        
        try:
            # Try to group by date for time series
            votes_by_date = (
                votes
                .annotate(date=TruncDate('timestamp'))
                .values('date')
                .annotate(vote_count=Count('id'))
                .order_by('date')
            )
            
            if votes_by_date.count() > 1:
                # Plot time-based data
                dates = [str(vb['date']) for vb in votes_by_date]
                vote_counts = [vb['vote_count'] for vb in votes_by_date]
                
                fig, ax = plt.subplots(figsize=(12, 6))
                ax.plot(dates, vote_counts, marker='o', linewidth=2, markersize=8, color='green')
                ax.fill_between(dates, vote_counts, alpha=0.3, color='green')
                ax.set_xlabel('Date', fontsize=12, fontweight='bold')
                ax.set_ylabel('Votes Cast', fontsize=12, fontweight='bold')
                ax.set_title('Voting Trends Over Time', fontsize=14, fontweight='bold')
                ax.grid(True, alpha=0.3, linestyle='--')
                plt.xticks(rotation=45, ha='right')
            else:
                # Fallback to candidate distribution
                candidate_votes = (
                    Candidate.objects
                    .annotate(vote_count=Count('votes'))
                    .filter(vote_count__gt=0)
                    .order_by('-vote_count', 'name')
                )
                
                if candidate_votes:
                    candidates = [cv.name for cv in candidate_votes]
                    vote_counts = [cv.vote_count for cv in candidate_votes]
                    
                    fig, ax = plt.subplots(figsize=(12, 6))
                    x_pos = range(len(candidates))
                    ax.plot(x_pos, vote_counts, marker='o', linewidth=2, markersize=8, color='steelblue')
                    ax.fill_between(x_pos, vote_counts, alpha=0.3, color='steelblue')
                    ax.set_xticks(x_pos)
                    ax.set_xticklabels(candidates, rotation=45, ha='right')
                    ax.set_xlabel('Candidates', fontsize=12, fontweight='bold')
                    ax.set_ylabel('Number of Votes', fontsize=12, fontweight='bold')
                    ax.set_title('Vote Distribution - Line Chart', fontsize=14, fontweight='bold')
                    ax.grid(True, alpha=0.3, linestyle='--')
                    
                    # Add value labels
                    for i, vote in enumerate(vote_counts):
                        ax.text(i, vote, f' {int(vote)}', ha='left', va='bottom', fontweight='bold')
                else:
                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.text(0.5, 0.5, 'No votes yet', ha='center', va='center', fontsize=16)
                    ax.axis('off')
        except Exception:
            # Fallback to candidate distribution if time grouping fails
            candidate_votes = (
                Candidate.objects
                .annotate(vote_count=Count('votes'))
                .filter(vote_count__gt=0)
                .order_by('-vote_count', 'name')
            )
            
            if candidate_votes:
                candidates = [cv.name for cv in candidate_votes]
                vote_counts = [cv.vote_count for cv in candidate_votes]
                
                fig, ax = plt.subplots(figsize=(12, 6))
                x_pos = range(len(candidates))
                ax.plot(x_pos, vote_counts, marker='o', linewidth=2, markersize=8, color='steelblue')
                ax.fill_between(x_pos, vote_counts, alpha=0.3, color='steelblue')
                ax.set_xticks(x_pos)
                ax.set_xticklabels(candidates, rotation=45, ha='right')
                ax.set_xlabel('Candidates', fontsize=12, fontweight='bold')
                ax.set_ylabel('Number of Votes', fontsize=12, fontweight='bold')
                ax.set_title('Vote Distribution - Line Chart', fontsize=14, fontweight='bold')
                ax.grid(True, alpha=0.3, linestyle='--')
                
                # Add value labels
                for i, vote in enumerate(vote_counts):
                    ax.text(i, vote, f' {int(vote)}', ha='left', va='bottom', fontweight='bold')
            else:
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.text(0.5, 0.5, 'No votes yet', ha='center', va='center', fontsize=16)
                ax.axis('off')
    else:
        # No votes at all
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, 'No votes yet', ha='center', va='center', fontsize=16)
        ax.axis('off')
    
    plt.tight_layout()
    
    # Save plot to BytesIO buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    buffer.seek(0)
    
    # Encode image to base64
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close(fig)
    
    return JsonResponse({'image': f'data:image/png;base64,{image_base64}'})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
import json
from django.contrib.auth.decorators import login_required
from .models import Vote, HealthCard
import json
from django.db.models import Avg

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('engineerdashboard')
        else:
            return render(request, 'my_app/home.html', {'error': 'invalid password or username'})
        
    return render(request, 'my_app/home.html')

def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            if User.objects.filter(username=username).exists():
                return render(request, 'my_app/home.html', {'error': 'username already exists'})
            
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
            login(request, user)
            
            return redirect('home')
        else:
            return render(request, 'my_app/home.html', {'error': 'Enter credentials in all fields'})
    return redirect('home')

#Mikayel Stuff

COLOR_MAPPING = {
    'red': 1,
    'amber': 2,
    'green': 3
}

REVERSE_COLOR_MAPPING = {
    1: 'red',
    2: 'amber',
    3: 'green'
}

@login_required
def voting_view(request):
    # First, check if the user already has a health card
    if HealthCard.objects.filter(user=request.user).exists():
        # If they do, redirect them to their health card
        return redirect('healthcard')
    
    context = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'username': request.user.username,
    }

    if request.method == 'POST':
        # Create or get the user's health card
        health_card, created = HealthCard.objects.get_or_create(user=request.user)
        
        # Process each category from the form
        for key, value in request.POST.items():
            if key not in ['csrfmiddlewaretoken']:
                try:
                    vote_data = json.loads(value)
                    color_name = vote_data['color']
                    feedback = vote_data['feedback']
                    
                    color_value = COLOR_MAPPING.get(color_name)

                    if color_value:
                        Vote.objects.update_or_create(
                            health_card=health_card,
                            category=key,
                            defaults={
                                'user': request.user,
                                'color': color_value,
                                'feedback': feedback
                            }
                        )
                except json.JSONDecodeError:
                    continue

        return redirect('healthcard')

    return render(request, 'my_app/voting.html', context)

#Healthcard
@login_required
def healthcard(request):
    try:
        # Get the user's health card and associated votes
        health_card = HealthCard.objects.get(user=request.user)
        votes = Vote.objects.filter(health_card=health_card)
        
        # Define all categories
        all_categories = [
            'Teamwork', 'Pawns or Players', 'Mission', 'Health of Codebase',
            'Suitable Process', 'Delivering Value', 'Learning', 'Speed',
            'Easy to Release', 'Fun'
        ]

        # Create a dictionary to store votes by category
        votes_dict = {vote.category: vote for vote in votes}
        
        # Prepare health items for template
        health_items = []
        for category in all_categories:
            if category in votes_dict:
                vote = votes_dict[category]
                # Convert numerical color value back to string
                color_name = {1: 'red', 2: 'amber', 3: 'green'}.get(vote.color, 'waiting')
                health_items.append({
                    'category': category,
                    'response': color_name,
                    'feedback': vote.feedback
                })
            else:
                health_items.append({
                    'category': category,
                    'response': 'waiting',
                    'feedback': ''
                })

        context = {
            'user': request.user,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'health_items': health_items,
            'last_updated': health_card.created_at
        }

        return render(request, 'my_app/healthcard.html', context)

    except HealthCard.DoesNotExist:
        # If no health card exists, redirect to voting page
        return redirect('voting')


#Summarypage
@login_required
def summary(request):
    # Get all health cards and votes
    health_cards = HealthCard.objects.all()
    all_votes = Vote.objects.all()
    
    # Define categories
    categories = [
        'Teamwork', 'Pawns or Players', 'Mission', 'Health of Codebase',
        'Suitable Process', 'Delivering Value', 'Learning', 'Speed',
        'Easy to Release', 'Fun'
    ]
    
    # Calculate summary for each category
    category_summary = {}
    for category in categories:
        category_votes = all_votes.filter(category=category)
        if category_votes.exists():
            avg_score = category_votes.aggregate(Avg('color'))['color__avg']
            if avg_score < 1.68:
                color = 'red'
            elif avg_score < 2.34:
                color = 'amber'
            else:
                color = 'green'
            
            category_summary[category] = {
                'score': round(avg_score, 1),
                'color': color
            }
        else:
            category_summary[category] = {
                'score': 'N/A',
                'color': 'waiting'
            }
    
    # Calculate overall score
    valid_scores = [summary['score'] for summary in category_summary.values() if summary['score'] != 'N/A']
    overall_score = round(sum(valid_scores) / len(valid_scores), 2) if valid_scores else 0
    
    # Get team member status
    team_members = User.objects.filter(is_staff=False)
    total_members = team_members.count()
    
    # Check completion status and count completed users
    member_status = []
    completed_count = 0
    
    for member in team_members:
        # A user is considered complete if they have a health card with all categories voted
        has_health_card = HealthCard.objects.filter(user=member).exists()
        
        if has_health_card:
            # Get this user's health card
            health_card = HealthCard.objects.get(user=member)
            
            # Count votes for this health card
            vote_count = Vote.objects.filter(health_card=health_card).count()
            
            # Check if all categories are voted
            has_completed = (vote_count == len(categories))
            
            if has_completed:
                completed_count += 1
        else:
            has_completed = False
        
        member_status.append({
            'name': f"{member.first_name} {member.last_name}",
            'initials': (member.first_name[0:1] + member.last_name[0:1]).upper() if member.first_name and member.last_name else member.username[0:2].upper(),
            'status': 'completed' if has_completed else 'pending'
        })
    
    # Calculate completion percentage
    completion_percentage = int((completed_count / total_members * 100) if total_members > 0 else 0)
    
    context = {
        'category_summary': category_summary,
        'overall_score': overall_score,
        'overall_color': 'red' if overall_score < 1.68 else 'amber' if overall_score < 2.34 else 'green',
        'team_members': member_status,
        'team_stats': {
            'total': total_members,
            'completed': completed_count,
            'percentage': completion_percentage
        }
    }
    
    return render(request, 'my_app/summary.html', context)

#End of Mikayel Stuff


def home(request):
    return render(request, "my_app/home.html")

def about(request):
    return render(request, "my_app/aboutus.html")

def contact(request):
    return render(request, "my_app/contactus.html")

@login_required
def profile(request):
    return render(request, "my_app/profile.html")

def engineerdashboard(request):
    return render(request, "my_app/engineerdashboard.html")

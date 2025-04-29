from django.contrib import admin
from .models import HealthCard, Vote

# Register your models here.

class VoteInline(admin.TabularInline):
    model = Vote
    extra = 0  # Don't show extra empty forms

#Gives the admin the ability to change/edit/delete health cards
@admin.register(HealthCard)
class HealthCardAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'get_vote_count')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    list_filter = ('created_at',)
    inlines = [VoteInline]
    
    #Function to get the counts of votes.
    def get_vote_count(self, obj):
        return obj.votes.count()
    get_vote_count.short_description = 'Votes'


#Function to get the votes for admin, allows admin to check for certain color, check for username on a specific category yada yada
@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('category', 'get_color_display', 'health_card', 'user', 'created_at')
    list_filter = ('category', 'color', 'created_at')
    search_fields = ('user__username', 'health_card__user__username', 'feedback')
    
    def get_color_display(self, obj):
        colors = {1: 'Red', 2: 'Amber', 3: 'Green'}
        return colors.get(obj.color, 'Unknown')
    get_color_display.short_description = 'Color'

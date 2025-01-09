from django.contrib import admin
from .models import Activity, Goal

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'duration', 'distance', 'calories_burned', 'date')
    list_filter = ('activity_type', 'date', 'user')
    search_fields = ('user__username', 'notes')
    date_hierarchy = 'date'

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'target_value', 'target_type', 'start_date', 'end_date', 'completed')
    list_filter = ('activity_type', 'target_type', 'completed')
    search_fields = ('user__username',)

from rest_framework import serializers
from .models import Activity, Goal

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

class GoalSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at', 'completed')

    def get_progress(self, obj):
        if obj.target_type == 'DISTANCE':
            activities = Activity.objects.filter(
                user=obj.user,
                activity_type=obj.activity_type,
                date__range=[obj.start_date, obj.end_date]
            )
            total = sum(a.distance or 0 for a in activities)
        elif obj.target_type == 'DURATION':
            activities = Activity.objects.filter(
                user=obj.user,
                activity_type=obj.activity_type,
                date__range=[obj.start_date, obj.end_date]
            )
            total = sum(a.duration for a in activities)
        else:  # CALORIES
            activities = Activity.objects.filter(
                user=obj.user,
                activity_type=obj.activity_type,
                date__range=[obj.start_date, obj.end_date]
            )
            total = sum(a.calories_burned for a in activities)
        
        return {
            'current': float(total),
            'target': float(obj.target_value),
            'percentage': min(100, (float(total) / float(obj.target_value)) * 100)
        } 
from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Avg
from apps.activities.models import Activity, Goal
from apps.activities.serializers import ActivitySerializer, GoalSerializer

class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Activity.objects.filter(user=self.request.user)
        activity_type = self.request.query_params.get('activity_type', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        if activity_type:
            queryset = queryset.filter(activity_type=activity_type)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        queryset = self.get_queryset()
        stats = {
            'total_activities': queryset.count(),
            'total_duration': queryset.aggregate(Sum('duration'))['duration__sum'] or 0,
            'total_calories': queryset.aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0,
            'avg_duration': queryset.aggregate(Avg('duration'))['duration__avg'] or 0,
        }
        return Response(stats)

class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

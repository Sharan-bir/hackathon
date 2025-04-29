from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegistrationView, CrimeReportViewSet, PoliceStationViewSet,
    PoliceTeamViewSet, ReportAssignmentView, UpdateReportStatusView,
    RecentCrimeReportsView, CrimeStatsView, DashboardView, ManagePolicemanView,
    CustomTokenObtainPairView
)

router = DefaultRouter()
router.register(r'crime-reports', CrimeReportViewSet, basename='crime-report')
router.register(r'police-stations', PoliceStationViewSet, basename='police-station')
router.register(r'police-teams', PoliceTeamViewSet, basename='police-team')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('recent-reports/', RecentCrimeReportsView.as_view(), name='recent-reports'),
    path('assign-report/', ReportAssignmentView.as_view(), name='assign-report'),
    path('crime-reports/<int:pk>/update-status/', UpdateReportStatusView.as_view(), name='update-status'),
    path('crime-stats/', CrimeStatsView.as_view(), name='crime-stats'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('manage-policemen/', ManagePolicemanView.as_view(), name='manage-policemen'),
    path('manage-policemen/<str:username>/', ManagePolicemanView.as_view(), name='manage-policeman-detail'),
]
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, PoliceStation, CrimeReport, PoliceTeam, ReportAssignment
from .serializers import (
    UserRegistrationSerializer, CrimeReportSerializer, PoliceStationSerializer,
    PoliceTeamSerializer, ReportAssignmentSerializer, CrimeReportUpdateSerializer,
    PolicemanSerializer, CustomTokenObtainPairSerializer
)
from .permissions import (
    IsUser, IsPolice, IsDepartment, IsPoliceOrDepartment,
    IsReportOwner, IsStationHead
)
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Count, Q
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

class CrimeReportViewSet(viewsets.ModelViewSet):
    queryset = CrimeReport.objects.all()
    serializer_class = CrimeReportSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'crime_type', 'police_station']

    def get_permissions(self):
        if self.action in ['create', 'list', 'retrieve']:
            if self.request.user.user_type in [2, 3]:  # Police or Department
                permission_classes = [IsAuthenticated, IsPoliceOrDepartment]
            else:
                permission_classes = [IsAuthenticated, IsUser]
        elif self.action in ['update', 'partial_update', 'destroy']:
            if self.request.user.user_type in [2, 3]:  # Police or Department
                permission_classes = [IsAuthenticated, IsPoliceOrDepartment]
            else:
                permission_classes = [IsAuthenticated, IsReportOwner]
        else:
            permission_classes = [IsAuthenticated, IsPoliceOrDepartment]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        if user.user_type == 1:  # User
            return queryset.filter(user=user)
        elif user.user_type == 2:  # Police
            station = PoliceStation.objects.filter(head=user).first()
            if station:
                return queryset.filter(police_station=station)
            return queryset.none()
        elif user.user_type == 3:  # Department
            return queryset
        return queryset.none()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

class RecentCrimeReportsView(generics.ListAPIView):
    serializer_class = CrimeReportSerializer
    permission_classes = [IsAuthenticated, IsPoliceOrDepartment]

    def get_queryset(self):
        user = self.request.user
        queryset = CrimeReport.objects.all().order_by('-created_at')
        
        if user.user_type == 2:  # Police or Department
            station = PoliceStation.objects.filter(head=user).first()
            if station:
                queryset = queryset.filter(police_station=station)
            else:
                return CrimeReport.objects.none()
        
        return queryset[:5]

class PoliceStationViewSet(viewsets.ModelViewSet):
    queryset = PoliceStation.objects.all()
    serializer_class = PoliceStationSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsDepartment]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        # Check if the selected head is already a station head
        head_id = request.data.get('head')
        if head_id:
            existing_station = PoliceStation.objects.filter(head_id=head_id).first()
            if existing_station:
                return Response(
                    {'error': f'This police officer is already the head of {existing_station.name}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # Check if the selected head is already a station head of a different station
        head_id = request.data.get('head')
        if head_id:
            existing_station = PoliceStation.objects.filter(head_id=head_id).exclude(id=kwargs.get('pk')).first()
            if existing_station:
                return Response(
                    {'error': f'This police officer is already the head of {existing_station.name}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return super().update(request, *args, **kwargs)

class PoliceTeamViewSet(viewsets.ModelViewSet):
    queryset = PoliceTeam.objects.all()
    serializer_class = PoliceTeamSerializer
    permission_classes = [IsAuthenticated, IsStationHead]

    def perform_create(self, serializer):
        station = PoliceStation.objects.get(head=self.request.user)
        serializer.save(station=station)

class ReportAssignmentView(generics.CreateAPIView):
    queryset = ReportAssignment.objects.all()
    serializer_class = ReportAssignmentSerializer
    permission_classes = [IsAuthenticated, IsStationHead]

    def create(self, request, *args, **kwargs):
        report_id = request.data.get('report')
        team_id = request.data.get('team')
        
        report = get_object_or_404(CrimeReport, id=report_id)
        team = get_object_or_404(PoliceTeam, id=team_id, station__head=request.user)
        
        # Update report status
        report.status = 'under_progress'
        report.police_station = team.station
        report.save()
        
        # Create assignment
        assignment = ReportAssignment.objects.create(
            report=report,
            team=team,
            assigned_by=request.user
        )
        
        serializer = self.get_serializer(assignment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UpdateReportStatusView(generics.UpdateAPIView):
    queryset = CrimeReport.objects.all()
    serializer_class = CrimeReportUpdateSerializer
    permission_classes = [IsAuthenticated, IsPoliceOrDepartment]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)

class CrimeStatsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsDepartment]
    
    def get(self, request):
        # Most common crime types
        crime_types = CrimeReport.objects.values('crime_type').annotate(
            count=Count('crime_type')
        ).order_by('-count')
        
        # Most common locations
        locations = CrimeReport.objects.values('address').annotate(
            count=Count('address')
        ).order_by('-count')[:5]
        
        # Status distribution
        status_dist = CrimeReport.objects.values('status').annotate(
            count=Count('status')
        )
        
        return Response({
            'crime_types': crime_types,
            'hotspots': locations,
            'status_distribution': status_dist
        })

class DashboardView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        response_data = {}
        
        if user.user_type == 2:  # Police
            # Get police station
            station = PoliceStation.objects.filter(head=user).first()
            if station:
                # Get assigned reports
                assigned_reports = CrimeReport.objects.filter(
                    police_station=station,
                    status__in=['under_progress', 'assigned']
                ).order_by('-created_at')[:5]
                
                # Get station-specific crime stats
                crime_types = CrimeReport.objects.filter(
                    police_station=station
                ).values('crime_type').annotate(
                    count=Count('crime_type')
                ).order_by('-count')
                
                # Get status distribution for station
                status_dist = CrimeReport.objects.filter(
                    police_station=station
                ).values('status').annotate(
                    count=Count('status')
                )
                
                response_data = {
                    'assigned_reports': CrimeReportSerializer(assigned_reports, many=True).data,
                    'crime_types': crime_types,
                    'status_distribution': status_dist,
                    'total_reports': CrimeReport.objects.filter(police_station=station).count(),
                    'active_reports': CrimeReport.objects.filter(
                        police_station=station,
                        status__in=['under_progress', 'assigned']
                    ).count()
                }
        
        elif user.user_type == 3:  # Department
            # Get all crime stats
            crime_types = CrimeReport.objects.values('crime_type').annotate(
                count=Count('crime_type')
            ).order_by('-count')
            
            # Get status distribution
            status_dist = CrimeReport.objects.values('status').annotate(
                count=Count('status')
            )
            
            # Get reports by station
            station_reports = PoliceStation.objects.annotate(
                total_reports=Count('crimereport'),
                active_reports=Count('crimereport', filter=Q(crimereport__status__in=['under_progress', 'assigned']))
            ).values('name', 'total_reports', 'active_reports')
            
            # Get recent reports
            recent_reports = CrimeReport.objects.all().order_by('-created_at')[:5]
            
            response_data = {
                'crime_types': crime_types,
                'status_distribution': status_dist,
                'station_reports': station_reports,
                'recent_reports': CrimeReportSerializer(recent_reports, many=True).data,
                'total_reports': CrimeReport.objects.count(),
                'active_reports': CrimeReport.objects.filter(
                    status__in=['under_progress', 'assigned']
                ).count()
            }
        
        return Response(response_data)

class ManagePolicemanView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsStationHead]
    serializer_class = PolicemanSerializer

    def post(self, request):
        """Add a policeman to the station"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Get the police station of the requesting user (station head)
            station = request.user.headed_station
            if not station:
                return Response(
                    {'error': 'You are not assigned as head of any police station'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create or update the policeman
            username = serializer.validated_data['username']
            user = User.objects.filter(username=username).first()
            
            if user:
                # Update existing user
                if user.user_type != 2:  # Not a police officer
                    return Response(
                        {'error': 'User exists but is not a police officer'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                # Create new user
                user = User.objects.create_user(
                    username=username,
                    password=serializer.validated_data['password'],
                    email=serializer.validated_data.get('email', ''),
                    user_type=2,
                    police_id=serializer.validated_data.get('police_id', '')
                )

            # Assign to police station
            user.managed_station = station
            user.save()

            return Response(
                {'message': f'Police officer {username} has been added to {station.name}'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username):
        """Remove a policeman from the station"""
        station = request.user.headed_station
        if not station:
            return Response(
                {'error': 'You are not assigned as head of any police station'},
                status=status.HTTP_400_BAD_REQUEST
            )

        policeman = get_object_or_404(User, username=username, managed_station=station)
        policeman.managed_station = None
        policeman.save()

        return Response(
            {'message': f'Police officer {username} has been removed from {station.name}'},
            status=status.HTTP_200_OK
        )

    def get(self, request):
        """List all policemen in the station"""
        station = request.user.headed_station
        if not station:
            return Response(
                {'error': 'You are not assigned as head of any police station'},
                status=status.HTTP_400_BAD_REQUEST
            )

        policemen = User.objects.filter(managed_station=station)
        serializer = self.get_serializer(policemen, many=True)
        return Response(serializer.data)

class PoliceUsersListView(generics.ListAPIView):
    serializer_class = PolicemanSerializer
    permission_classes = [IsAuthenticated, IsPoliceOrDepartment]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 2:  # Police station head
            station = PoliceStation.objects.filter(head=user).first()
            if station:
                return User.objects.filter(user_type=2, managed_station=station)
            return User.objects.none()
        return User.objects.filter(user_type=2)  # Department can see all police users
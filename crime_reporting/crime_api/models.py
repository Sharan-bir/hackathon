from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'User'),
        (2, 'Police'),
        (3, 'Department')
    )
    
    user_type = models.IntegerField(choices=USER_TYPE_CHOICES, default=1)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    police_id = models.CharField(max_length=50, blank=True, null=True)
    is_station_head = models.BooleanField(default=False)
    managed_station = models.ForeignKey('PoliceStation', on_delete=models.SET_NULL, null=True, blank=True, related_name='policemen')
    
    def __str__(self):
        return self.username

class PoliceStation(models.Model):
    name = models.CharField(max_length=100)
    location = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    head = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name='headed_station')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class CrimeReport(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('under_progress', 'Under Progress'),
        ('concluded', 'Concluded'),
    )
    
    CRIME_TYPE_CHOICES = (
        ('theft', 'Theft'),
        ('murder', 'Murder'),
        ('burglary', 'Burglary'),
        ('assault', 'Assault'),
        ('vandalism', 'Vandalism'),
        ('fraud', 'Fraud'),
        ('other', 'Other'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    description = models.TextField()
    crime_type = models.CharField(max_length=20, choices=CRIME_TYPE_CHOICES)
    image = models.ImageField(upload_to='crime_images/', blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    police_station = models.ForeignKey(PoliceStation, on_delete=models.SET_NULL, null=True, blank=True)
    output = models.TextField(blank=True, null=True)
    conclusion_date = models.DateTimeField(blank=True, null=True)
    police_notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Report #{self.id} - {self.crime_type}"

class PoliceTeam(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name='teams')
    station = models.ForeignKey(PoliceStation, on_delete=models.CASCADE, related_name='teams')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class ReportAssignment(models.Model):
    report = models.ForeignKey(CrimeReport, on_delete=models.CASCADE, related_name='assignments')
    team = models.ForeignKey(PoliceTeam, on_delete=models.CASCADE, related_name='assignments')
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_reports')
    assigned_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Assignment for Report #{self.report.id}"
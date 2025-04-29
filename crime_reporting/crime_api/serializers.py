from datetime import timezone
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import PoliceStation, CrimeReport, PoliceTeam, ReportAssignment
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'phone', 'address', 'user_type', 'police_id']
        extra_kwargs = {
            'police_id': {'required': False},
            'phone': {'required': False},
            'address': {'required': False},
        }
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data.get('phone', ''),
            address=validated_data.get('address', ''),
            user_type=validated_data.get('user_type', 1),
            police_id=validated_data.get('police_id', '')
        )
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_type'] = self.user.user_type
        data['username'] = self.user.username
        return data

class PoliceStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoliceStation
        fields = '__all__'

class CrimeReportSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    police_station = PoliceStationSerializer(read_only=True)
    image = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = CrimeReport
        fields = '__all__'
        read_only_fields = ['status', 'created_at', 'updated_at', 'conclusion_date']

class PoliceTeamSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(user_type=2), many=True)
    
    class Meta:
        model = PoliceTeam
        fields = '__all__'

class ReportAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportAssignment
        fields = '__all__'

class CrimeReportUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrimeReport
        fields = ['status', 'output', 'police_notes', 'conclusion_date']
    
    def update(self, instance, validated_data):
        if validated_data.get('status') == 'concluded' and not instance.conclusion_date:
            validated_data['conclusion_date'] = timezone.now()
        return super().update(instance, validated_data)

class PolicemanSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=False)
    police_id = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'police_id', 'phone', 'address')
        extra_kwargs = {
            'phone': {'required': False},
            'address': {'required': False}
        }

    def validate(self, attrs):
        if self.instance:
            # For existing users, password is not required
            attrs.pop('password', None)
        return attrs
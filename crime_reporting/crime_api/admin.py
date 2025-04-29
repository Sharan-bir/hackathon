from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, PoliceStation, CrimeReport, PoliceTeam, ReportAssignment

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'phone')
    ordering = ('username',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'phone', 'address', 'police_id')}),
        ('Permissions', {'fields': ('user_type', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type', 'phone', 'address', 'police_id'),
        }),
    )

    class Meta:
        app_label = 'crime_api'

@admin.register(PoliceStation)
class PoliceStationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'head', 'latitude', 'longitude')
    list_filter = ('head',)
    search_fields = ('name', 'location')
    raw_id_fields = ('head',)

    class Meta:
        app_label = 'crime_api'

@admin.register(CrimeReport)
class CrimeReportAdmin(admin.ModelAdmin):
    list_display = ('get_report_id', 'crime_type', 'status', 'user', 'police_station', 'created_at')
    list_filter = ('crime_type', 'status', 'police_station', 'created_at')
    search_fields = ('description', 'address', 'crime_type')
    raw_id_fields = ('user', 'police_station')
    readonly_fields = ('created_at', 'updated_at', 'conclusion_date')
    
    def get_report_id(self, obj):
        return f"Report #{obj.id}"
    get_report_id.short_description = 'Report'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('description', 'crime_type', 'address', 'latitude', 'longitude', 'image')
        }),
        ('Status Information', {
            'fields': ('status', 'output', 'police_notes', 'conclusion_date')
        }),
        ('Related Information', {
            'fields': ('user', 'police_station')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    class Meta:
        app_label = 'crime_api'

@admin.register(PoliceTeam)
class PoliceTeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'station', 'get_members_count')
    list_filter = ('station',)
    search_fields = ('name',)
    filter_horizontal = ('members',)
    
    def get_members_count(self, obj):
        return obj.members.count()
    get_members_count.short_description = 'Members Count'

    class Meta:
        app_label = 'crime_api'

@admin.register(ReportAssignment)
class ReportAssignmentAdmin(admin.ModelAdmin):
    list_display = ('report', 'team', 'assigned_by', 'assigned_at')
    list_filter = ('assigned_at', 'team')
    search_fields = ('report__id', 'team__name')
    raw_id_fields = ('report', 'team', 'assigned_by')
    readonly_fields = ('assigned_at',)

    class Meta:
        app_label = 'crime_api'

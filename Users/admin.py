from django.contrib import admin
from .models import (
    SeekerProfile, Skill, SeekerSkill,
    Certification, ToolProficiency,
    Specialization, WorkExperience,
    Review, DmFromResume
)

# --- Inline Models ---
class SeekerSkillInline(admin.TabularInline):
    model = SeekerSkill
    extra = 1
    autocomplete_fields = ['skill']


class CertificationInline(admin.TabularInline):
    model = Certification
    extra = 1


class ToolProficiencyInline(admin.TabularInline):
    model = ToolProficiency
    extra = 1


class SpecializationInline(admin.TabularInline):
    model = Specialization
    extra = 1


class WorkExperienceInline(admin.TabularInline):
    model = WorkExperience
    extra = 1


# --- SeekerProfile Admin ---
@admin.register(SeekerProfile)
class SeekerProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'primary_trade', 'years_experience',
        'location', 'hourly_rate', 'availability', 'profile_completion'
    )
    list_filter = ('primary_trade', 'years_experience', 'availability')
    search_fields = ('user__username', 'user__email', 'location', 'primary_trade')
    ordering = ('-created_at',)
    inlines = [SeekerSkillInline, CertificationInline, ToolProficiencyInline, SpecializationInline, WorkExperienceInline]
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Review)
class RegisterReview(admin.ModelAdmin):
    list_display = ['profile', 'ratings', 'teamwork', 'time_management', 'critical_thinking', 'leadership', 'Communication']
    search_fields = ('profile', 'ratings')
    list_filter = ('ratings',)

# --- Skill Admin ---
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name', 'category')
    ordering = ('name',)


# --- SeekerSkill Admin ---
@admin.register(SeekerSkill)
class SeekerSkillAdmin(admin.ModelAdmin):
    list_display = ('profile', 'skill', 'proficiency', 'years_experience')
    list_filter = ('proficiency',)
    search_fields = ('profile__user__username', 'skill__name')
    autocomplete_fields = ['profile', 'skill']


# --- Certification Admin ---
@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'issuing_organization', 'profile', 'status', 'issue_date')
    list_filter = ('status', 'issuing_organization')
    search_fields = ('name', 'profile__user__username', 'issuing_organization')
    readonly_fields = ('created_at',)
    autocomplete_fields = ['profile']


# --- Tool Proficiency Admin ---
@admin.register(ToolProficiency)
class ToolProficiencyAdmin(admin.ModelAdmin):
    list_display = ('profile', 'tool_name', 'proficiency_level')
    search_fields = ('profile__user__username', 'tool_name')
    list_filter = ('proficiency_level',)


# --- Specialization Admin ---
@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('profile', 'name')
    search_fields = ('profile__user__username', 'name')


# --- Work Experience Admin ---
@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('profile', 'company', 'position', 'start_date', 'end_date', 'current')
    search_fields = ('company', 'position', 'profile__user__username')
    list_filter = ('current', 'start_date')
    date_hierarchy = 'start_date'

from .models import DmFromResume

@admin.register(DmFromResume)
class DmFromResumeAdmin(admin.ModelAdmin):
    list_display = ('company', 'talent', 'subject', 'project_type', 'hourly_rate')
    search_fields = ('company__name', 'talent__user__username', 'subject')
    list_filter = ('project_type',)
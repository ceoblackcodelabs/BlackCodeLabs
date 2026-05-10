from django.urls import path
from .views import (BuildProfile, DeleteCertificationView,
                    MyResume, ResumeBuilder, TalentDetailView,
                    AddSkillView, RemoveSkillView,RemoveProfilePictureView,
                    UserProfileView, CompanyProfileView, BuildCompanyProfile,
                    auth_view, activate,
                    AddCompanySpecialization, RemoveCompanySpecialization
                    )

urlpatterns = [
    path('authenticate/', auth_view, name='authenticate'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),

    path('myProfile/', UserProfileView.as_view(), name='my_profile'),
    path('find-talent/Resume/<int:pk>/',TalentDetailView.as_view(), name="profile"),
    path('build-profile/', BuildProfile.as_view(), name='build_profile'),
    path('remove-profile-picture/', RemoveProfilePictureView.as_view(), name='remove_profile_picture'),
    path('add-skill/', AddSkillView.as_view(), name='add_skill'),
    path('remove-skill/<int:skill_id>/', RemoveSkillView.as_view(), name='remove_skill'),
    path('delete-certification/<int:cert_id>/', DeleteCertificationView.as_view(), name='delete_certification'),

    path('my-resume/', MyResume.as_view(), name='my_resume'),
    path('resume-builder/', ResumeBuilder.as_view(), name='resume_builder'),

    # company profile
    path('company/profile/build/', BuildCompanyProfile.as_view(), name='build_company_profile'),
    path('company/profile/<int:pk>/', CompanyProfileView.as_view(), name='company_profile_detail'),
    # AJAX URLs for specializations
    path('company/specialization/add/', AddCompanySpecialization.as_view(), name='add_company_specialization'),
    path('company/specialization/remove/<int:spec_id>/', RemoveCompanySpecialization.as_view(), name='remove_company_specialization'),
]

